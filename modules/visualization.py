
import csv
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from modules.cpu_scheduling import fcfs, sjf, round_robin
from modules.disk_scheduling import (
    fcfs as disk_fcfs,
    sstf,
    scan
)
from modules.logger import log_info, log_exception


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"


def get_sample_processes():
    """Return the sample CPU processes used by the simulator."""
    return [
        {"pid": "P1", "arrival": 0, "burst": 5},
        {"pid": "P2", "arrival": 1, "burst": 3},
        {"pid": "P3", "arrival": 2, "burst": 1},
        {"pid": "P4", "arrival": 3, "burst": 2}
    ]


def get_cpu_comparison():
    """Run all CPU algorithms and collect comparison metrics."""
    processes = get_sample_processes()

    algorithms = {
        "FCFS": fcfs(processes.copy()),
        "SJF": sjf(processes.copy()),
        "Round Robin (Q=2)": round_robin(processes.copy(), 2)
    }

    comparison = {}

    for name, (results, gantt) in algorithms.items():
        if not results:
            continue

        comparison[name] = {
            "results": results,
            "gantt": gantt,
            "avg_waiting": (
                sum(p["waiting"] for p in results) / len(results)
            ),
            "avg_turnaround": (
                sum(p["turnaround"] for p in results) / len(results)
            )
        }

    return comparison


def get_disk_comparison():
    """Run disk algorithms and collect total head movements."""
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    initial_head = 53

    return {
        "FCFS": disk_fcfs(requests.copy(), initial_head),
        "SSTF": sstf(requests.copy(), initial_head),
        "SCAN (left)": scan(
            requests.copy(),
            initial_head,
            direction="left"
        )
    }


def export_csv_reports():
    """Export CPU and disk scheduling results to separate CSV files."""
    try:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cpu_path = REPORT_DIR / f"cpu_results_{timestamp}.csv"
        disk_path = REPORT_DIR / f"disk_results_{timestamp}.csv"

        # Export CPU scheduling results.
        cpu_comparison = get_cpu_comparison()

        with cpu_path.open(
            "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.writer(file)

            writer.writerow([
                "Algorithm", "PID", "Arrival Time", "Burst Time",
                "Completion Time", "Waiting Time", "Turnaround Time",
                "Average Waiting Time", "Average Turnaround Time"
            ])

            for algorithm, data in cpu_comparison.items():
                for process in data["results"]:
                    writer.writerow([
                        algorithm,
                        process["pid"],
                        process["arrival"],
                        process["burst"],
                        process["completion"],
                        process["waiting"],
                        process["turnaround"],
                        round(data["avg_waiting"], 2),
                        round(data["avg_turnaround"], 2)
                    ])

        # Export disk scheduling results.
        requests = [98, 183, 37, 122, 14, 124, 65, 67]
        initial_head = 53
        disk_comparison = get_disk_comparison()

        with disk_path.open(
            "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.writer(file)

            writer.writerow([
                "Algorithm", "Initial Head", "Requests",
                "Service Order", "Total Head Movement",
                "Head Movement Path"
            ])

            for algorithm, (order, movement, path) in (
                disk_comparison.items()
            ):
                writer.writerow([
                    algorithm,
                    initial_head,
                    " -> ".join(map(str, requests)),
                    " -> ".join(map(str, order)),
                    movement,
                    " -> ".join(map(str, path))
                ])

        log_info("CPU and disk CSV reports generated successfully")
        print("\nCSV reports generated successfully!")
        print(f"CPU CSV:  {cpu_path}")
        print(f"Disk CSV: {disk_path}")

        return cpu_path, disk_path

    except Exception:
        log_exception("CSV report generation failed")
        print("CSV export failed. Check logs/simulator.log")
        return None


def generate_cpu_chart():
    """Save a comparison chart for CPU scheduling algorithms."""
    try:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

        comparison = get_cpu_comparison()
        names = list(comparison.keys())
        waiting = [
            comparison[name]["avg_waiting"] for name in names
        ]
        turnaround = [
            comparison[name]["avg_turnaround"] for name in names
        ]

        positions = list(range(len(names)))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(
            [p - width / 2 for p in positions],
            waiting,
            width,
            label="Average Waiting Time"
        )
        ax.bar(
            [p + width / 2 for p in positions],
            turnaround,
            width,
            label="Average Turnaround Time"
        )

        ax.set_title("CPU Scheduling Algorithm Comparison")
        ax.set_xlabel("Scheduling Algorithm")
        ax.set_ylabel("Time Units")
        ax.set_xticks(positions)
        ax.set_xticklabels(names)
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        fig.tight_layout()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_path = REPORT_DIR / f"cpu_comparison_{timestamp}.png"

        fig.savefig(chart_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        log_info(f"CPU comparison chart saved: {chart_path.name}")
        print(f"\nCPU comparison chart saved:\n{chart_path}")

        return chart_path

    except Exception:
        log_exception("CPU chart generation failed")
        print("CPU chart generation failed. Check logs/simulator.log")
        return None


def generate_disk_chart():
    """Save a chart comparing total disk head movement."""
    try:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

        comparison = get_disk_comparison()
        names = list(comparison.keys())
        movements = [
            comparison[name][1] for name in names
        ]

        fig, ax = plt.subplots(figsize=(9, 6))
        bars = ax.bar(names, movements)

        ax.set_title("Disk Scheduling: Total Head Movement")
        ax.set_xlabel("Scheduling Algorithm")
        ax.set_ylabel("Head Movement (Cylinders)")
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        ax.bar_label(bars, padding=3)
        fig.tight_layout()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_path = REPORT_DIR / f"disk_comparison_{timestamp}.png"

        fig.savefig(chart_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        log_info(f"Disk comparison chart saved: {chart_path.name}")
        print(f"\nDisk comparison chart saved:\n{chart_path}")

        return chart_path

    except Exception:
        log_exception("Disk chart generation failed")
        print("Disk chart generation failed. Check logs/simulator.log")
        return None


def generate_all_charts():
    """Generate both CPU and disk comparison charts."""
    cpu_path = generate_cpu_chart()
    disk_path = generate_disk_chart()

    if cpu_path and disk_path:
        print("\nBoth comparison charts generated successfully.")
        return cpu_path, disk_path

    print("\nOne or more charts could not be generated.")
    return None
