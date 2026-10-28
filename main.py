from modules.cpu_scheduling import (
    fcfs,
    sjf,
    round_robin,
    srtf,
    preemptive_priority,
    display_results,
)

from modules.memory_management import first_fit, best_fit, worst_fit

from modules.deadlock import is_safe_state, detect_deadlock

from modules.disk_scheduling import (
    fcfs as disk_fcfs,
    sstf,
    scan,
    c_scan,
    display_result,
)

from modules.report_generator import generate_report

from modules.logger import log_info, log_warning, log_exception

from modules.visualization import (
    export_csv_reports,
    generate_cpu_chart,
    generate_disk_chart,
    generate_all_charts,
)


# ==================================================
# CPU SCHEDULING
# ==================================================

def cpu_menu():
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 5},
        {"pid": "P2", "arrival": 1, "burst": 3},
        {"pid": "P3", "arrival": 2, "burst": 1},
        {"pid": "P4", "arrival": 3, "burst": 2},
    ]

    while True:
        print("\n========== CPU SCHEDULING ==========")
        print("Processes:", processes)
        print("1. FCFS")
        print("2. SJF (Non-preemptive)")
        print("3. Round Robin")
        print("4. SRTF")
        print("5. Preemptive Priority")
        print("6. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                results, gantt = fcfs([p.copy() for p in processes])
                display_results("FCFS Scheduling", results, gantt)

            elif choice == "2":
                results, gantt = sjf([p.copy() for p in processes])
                display_results("SJF Scheduling", results, gantt)

            elif choice == "3":
                raw = input("Enter time quantum (default 2): ").strip()
                quantum = int(raw) if raw else 2

                if quantum <= 0:
                    print("Quantum must be greater than zero.")
                    continue

                results, gantt = round_robin(
                    [p.copy() for p in processes], quantum
                )
                display_results(
                    f"Round Robin (Q={quantum})", results, gantt
                )

            elif choice == "4":
                results, gantt = srtf([p.copy() for p in processes])
                display_results("SRTF Scheduling", results, gantt)

            elif choice == "5":
                priorities = [2, 1, 4, 3]
                priority_processes = [
                    {**p, "priority": priority}
                    for p, priority in zip(processes, priorities)
                ]

                print("\nSmaller priority number = Higher priority")
                for p in priority_processes:
                    print(f"{p['pid']}: Priority {p['priority']}")

                results, gantt = preemptive_priority(priority_processes)
                display_results(
                    "Preemptive Priority Scheduling", results, gantt
                )

            elif choice == "6":
                return

            else:
                print("Invalid choice. Enter 1-6.")

        except ValueError as error:
            log_warning(f"Invalid CPU scheduling input: {error}")
            print("Invalid input:", error)

        except Exception:
            log_exception("CPU scheduling failed")
            print("CPU scheduling failed. Check logs/simulator.log")


# ==================================================
# MEMORY MANAGEMENT
# ==================================================

def memory_menu():
    blocks = [100, 500, 200, 300, 600]
    processes = [212, 417, 112, 426]

    while True:
        print("\n========== MEMORY MANAGEMENT ==========")
        print("Memory Blocks:", blocks)
        print("Processes:", processes)
        print("1. First Fit")
        print("2. Best Fit")
        print("3. Worst Fit")
        print("4. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                first_fit(blocks.copy(), processes.copy())
            elif choice == "2":
                best_fit(blocks.copy(), processes.copy())
            elif choice == "3":
                worst_fit(blocks.copy(), processes.copy())
            elif choice == "4":
                return
            else:
                print("Invalid choice. Enter 1-4.")

        except Exception:
            log_exception("Memory management failed")
            print("Memory management failed. Check logs/simulator.log")


# ==================================================
# DEADLOCK AVOIDANCE
# ==================================================

def deadlock_menu():
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2],
    ]

    maximum = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3],
    ]

    available = [3, 3, 2]

    print("\n========== DEADLOCK AVOIDANCE ==========")

    try:
        safe, sequence, need = is_safe_state(
            available, allocation, maximum
        )

        print("Available Resources:", available)
        print("Need Matrix:")
        print(need)

        if safe:
            print("\nSystem is in a SAFE state.")
            print("Safe Sequence:", " -> ".join(map(str, sequence)))
        else:
            print("\nSystem is in an UNSAFE state.")

    except Exception:
        log_exception("Deadlock avoidance failed")
        print("Deadlock check failed. Check logs/simulator.log")


# ==================================================
# DEADLOCK DETECTION
# ==================================================

def deadlock_detection_menu():
    available = [0, 0, 0]

    allocation = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]

    request = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ]

    print("\n========== DEADLOCK DETECTION ==========")

    try:
        result = detect_deadlock(available, allocation, request)

        if isinstance(result, (list, tuple, set)):
            if result:
                print("Deadlock detected!")
                print("Processes involved:", ", ".join(map(str, result)))
            else:
                print("No deadlock detected.")
        elif result:
            print("Deadlock detected!")
        else:
            print("No deadlock detected.")

    except Exception:
        log_exception("Deadlock detection failed")
        print("Deadlock detection failed. Check logs/simulator.log")


# ==================================================
# DISK SCHEDULING
# ==================================================

def disk_menu():
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    initial_head = 53
    disk_size = 200

    algorithms = {
        "1": (
            "FCFS",
            lambda: disk_fcfs(requests.copy(), initial_head),
        ),
        "2": (
            "SSTF",
            lambda: sstf(requests.copy(), initial_head),
        ),
        "3": (
            "SCAN (Left)",
            lambda: scan(
                requests.copy(), initial_head, disk_size, "left"
            ),
        ),
        "4": (
            "SCAN (Right)",
            lambda: scan(
                requests.copy(), initial_head, disk_size, "right"
            ),
        ),
        "5": (
            "C-SCAN (Left)",
            lambda: c_scan(
                requests.copy(), initial_head, disk_size, "left"
            ),
        ),
        "6": (
            "C-SCAN (Right)",
            lambda: c_scan(
                requests.copy(), initial_head, disk_size, "right"
            ),
        ),
    }

    while True:
        print("\n========== DISK SCHEDULING ==========")
        print("Initial Head:", initial_head)
        print("Disk Size:", disk_size)
        print("Requests:", requests)
        print("1. FCFS")
        print("2. SSTF")
        print("3. SCAN (Left)")
        print("4. SCAN (Right)")
        print("5. C-SCAN (Left)")
        print("6. C-SCAN (Right)")
        print("7. Compare All Algorithms")
        print("8. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "8":
                return

            elif choice in algorithms:
                name, function = algorithms[choice]
                result = function()
                display_result(name, result)

            elif choice == "7":
                comparison = []

                print("\n========== DISK MOVEMENT COMPARISON ==========")
                print(f"{'Algorithm':<20}{'Head Movement':>18}")
                print("-" * 38)

                for name, function in algorithms.values():
                    result = function()
                    movement = result[1]
                    comparison.append((name, movement))
                    print(f"{name:<20}{movement:>18} cylinders")

                print("\nSorted from lowest to highest movement:")
                for name, movement in sorted(
                    comparison, key=lambda item: item[1]
                ):
                    print(f"{name:<20}{movement} cylinders")

            else:
                print("Invalid choice. Enter 1-8.")

        except ValueError as error:
            log_warning(f"Invalid disk scheduling input: {error}")
            print("Invalid input:", error)

        except Exception:
            log_exception("Disk scheduling failed")
            print("Disk scheduling failed. Check logs/simulator.log")


# ==================================================
# REPORTS AND CHARTS
# ==================================================

def report_menu():
    print("\n========== GENERATE TEXT REPORT ==========")

    try:
        result = generate_report()
        print("Report generation completed.")
        if result is not None:
            print(result)
        print("Check the reports/ directory.")

    except Exception:
        log_exception("Text report generation failed")
        print("Report generation failed. Check logs/simulator.log")


def run_action(label, function):
    try:
        print(f"\n{label}...")
        result = function()

        if result is not None:
            print(result)

        print(f"{label} completed. Check the reports/ directory.")
        log_info(f"{label} completed")

    except Exception:
        log_exception(f"{label} failed")
        print(f"{label} failed. Check logs/simulator.log")


# ==================================================
# MAIN MENU
# ==================================================

def main():
    log_info("OS Resource Management Simulator started")

    try:
        while True:
            print("\n" + "=" * 55)
            print("       OS RESOURCE MANAGEMENT SIMULATOR")
            print("=" * 55)
            print("1.  CPU Scheduling")
            print("2.  Memory Management")
            print("3.  Deadlock Avoidance (Banker's Algorithm)")
            print("4.  Deadlock Detection")
            print("5.  Disk Scheduling")
            print("6.  Generate Text Report")
            print("7.  Export CSV Reports")
            print("8.  Generate CPU Comparison Chart")
            print("9.  Generate Disk Comparison Chart")
            print("10. Generate All Comparison Charts")
            print("11. Exit")
            print("=" * 55)

            choice = input("Enter your choice (1-11): ").strip()

            if choice == "1":
                cpu_menu()
            elif choice == "2":
                memory_menu()
            elif choice == "3":
                deadlock_menu()
            elif choice == "4":
                deadlock_detection_menu()
            elif choice == "5":
                disk_menu()
            elif choice == "6":
                report_menu()
            elif choice == "7":
                run_action("CSV report export", export_csv_reports)
            elif choice == "8":
                run_action("CPU chart generation", generate_cpu_chart)
            elif choice == "9":
                run_action("Disk chart generation", generate_disk_chart)
            elif choice == "10":
                run_action("All charts generation", generate_all_charts)
            elif choice == "11":
                print("\nThank you for using the simulator!")
                log_info("OS Resource Management Simulator stopped")
                break
            else:
                print("Invalid choice. Enter 1-11.")
                log_warning(f"Invalid main menu choice: {choice}")

    except (KeyboardInterrupt, EOFError):
        print("\nSimulator stopped.")
        log_info("Simulator stopped by keyboard interrupt or EOF")


if __name__ == "__main__":
    main()