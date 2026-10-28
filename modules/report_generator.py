
from datetime import datetime
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO

from modules.cpu_scheduling import fcfs, sjf, round_robin
from modules.memory_management import first_fit, best_fit, worst_fit
from modules.deadlock import is_safe_state
from modules.disk_scheduling import (
    fcfs as disk_fcfs,
    sstf,
    scan
)
from modules.logger import log_info, log_exception


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"


def add_cpu_report(lines, name, result):
    results, gantt = result

    if not results:
        lines.append(f"\n{name}: No process results available.")
        return

    avg_waiting = sum(p["waiting"] for p in results) / len(results)
    avg_turnaround = sum(p["turnaround"] for p in results) / len(results)

    lines.append(f"\n{name}")
    lines.append("-" * 45)
    lines.append(
        f"{'PID':<8}{'AT':<8}{'BT':<8}{'CT':<8}{'WT':<8}{'TAT':<8}"
    )

    for process in sorted(results, key=lambda p: p["pid"]):
        lines.append(
            f"{process['pid']:<8}"
            f"{process['arrival']:<8}"
            f"{process['burst']:<8}"
            f"{process['completion']:<8}"
            f"{process['waiting']:<8}"
            f"{process['turnaround']:<8}"
        )

    lines.append(f"Average Waiting Time: {avg_waiting:.2f}")
    lines.append(f"Average Turnaround Time: {avg_turnaround:.2f}")
    lines.append(
        "Gantt Chart: "
        + " | ".join(
            f"{pid} ({start}-{end})"
            for pid, start, end in gantt
        )
    )


def add_memory_report(lines, name, function, blocks, processes):
    lines.append(f"\n{name}")
    lines.append("-" * 45)

    captured_output = StringIO()

    # Capture the existing memory function's printed results.
    with redirect_stdout(captured_output):
        function(blocks.copy(), processes.copy())

    lines.append(captured_output.getvalue().strip())


def add_disk_report(lines, name, result):
    order, movement, path = result

    lines.append(f"\n{name}")
    lines.append("-" * 45)
    lines.append("Request service order: " + " -> ".join(map(str, order)))
    lines.append("Head movement path: " + " -> ".join(map(str, path)))
    lines.append(f"Total head movement: {movement} cylinders")


def generate_report():
    """Run all algorithms and save their results to a text report."""
    try:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now()
        report_name = timestamp.strftime("simulation_report_%Y%m%d_%H%M%S.txt")
        report_path = REPORT_DIR / report_name

        lines = [
            "OS RESOURCE MANAGEMENT SIMULATOR",
            "=" * 55,
            f"Report generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "This report contains results from the configured sample inputs.",
            "",
            "=" * 55,
            "1. CPU SCHEDULING",
            "=" * 55
        ]

        processes = [
            {"pid": "P1", "arrival": 0, "burst": 5},
            {"pid": "P2", "arrival": 1, "burst": 3},
            {"pid": "P3", "arrival": 2, "burst": 1},
            {"pid": "P4", "arrival": 3, "burst": 2}
        ]

        add_cpu_report(lines, "FCFS", fcfs(processes.copy()))
        add_cpu_report(lines, "SJF (Non-preemptive)", sjf(processes.copy()))
        add_cpu_report(
            lines,
            "Round Robin (Quantum = 2)",
            round_robin(processes.copy(), 2)
        )

        lines.extend([
            "",
            "=" * 55,
            "2. MEMORY MANAGEMENT",
            "=" * 55
        ])

        blocks = [100, 500, 200, 300, 600]
        memory_processes = [212, 417, 112, 426]

        add_memory_report(
            lines, "First Fit", first_fit, blocks, memory_processes
        )
        add_memory_report(
            lines, "Best Fit", best_fit, blocks, memory_processes
        )
        add_memory_report(
            lines, "Worst Fit", worst_fit, blocks, memory_processes
        )

        lines.extend([
            "",
            "=" * 55,
            "3. DEADLOCK AVOIDANCE - BANKER'S ALGORITHM",
            "=" * 55
        ])

        available = [3, 3, 2]

        allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]

        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ]

        safe, sequence, need = is_safe_state(
            available, allocation, maximum
        )

        lines.append(f"Available resources: {available}")
        lines.append("\nNeed Matrix (Maximum - Allocation):")
        lines.append(f"{'Process':<12}{'A':<8}{'B':<8}{'C':<8}")

        for i, row in enumerate(need):
            lines.append(
                f"{'P' + str(i):<12}{row[0]:<8}{row[1]:<8}{row[2]:<8}"
            )

        if safe:
            lines.append("\nSystem status: SAFE")
            lines.append("Safe sequence: " + " -> ".join(sequence))
        else:
            lines.append("\nSystem status: UNSAFE")
            lines.append("Partial sequence: " + " -> ".join(sequence))

        lines.extend([
            "",
            "=" * 55,
            "4. DISK SCHEDULING",
            "=" * 55
        ])

        requests = [98, 183, 37, 122, 14, 124, 65, 67]
        initial_head = 53

        add_disk_report(
            lines, "FCFS", disk_fcfs(requests, initial_head)
        )
        add_disk_report(
            lines, "SSTF", sstf(requests, initial_head)
        )
        add_disk_report(
            lines,
            "SCAN (Direction: left)",
            scan(requests, initial_head, direction="left")
        )

        lines.extend([
            "",
            "=" * 55,
            "END OF REPORT",
            "=" * 55
        ])

        report_path.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8"
        )

        log_info(f"Simulation report generated: {report_path.name}")
        print("\nReport generated successfully!")
        print(f"Saved at: {report_path}")

        return report_path

    except Exception:
        log_exception("Failed to generate simulation report")
        print("Report generation failed. Check logs/simulator.log")
        return None


if __name__ == "__main__":
    generate_report()
