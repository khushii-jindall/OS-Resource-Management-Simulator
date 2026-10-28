def fcfs(processes):
    """First Come First Serve CPU Scheduling."""
    processes = sorted(processes, key=lambda p: (p["arrival"], p["pid"]))
    time = 0
    results = []
    gantt = []

    for p in processes:
        start = max(time, p["arrival"])
        completion = start + p["burst"]
        waiting = start - p["arrival"]
        turnaround = completion - p["arrival"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

        gantt.append((p["pid"], start, completion))
        time = completion

    return results, gantt


def sjf(processes):
    """Non-preemptive Shortest Job First Scheduling."""
    processes = [p.copy() for p in processes]
    time = 0
    completed = set()
    results = []
    gantt = []

    while len(completed) < len(processes):
        available = [
            p for p in processes
            if p["pid"] not in completed and p["arrival"] <= time
        ]

        if not available:
            time = min(
                p["arrival"] for p in processes
                if p["pid"] not in completed
            )
            continue

        p = min(
            available,
            key=lambda p: (p["burst"], p["arrival"], p["pid"])
        )

        start = time
        completion = start + p["burst"]
        turnaround = completion - p["arrival"]
        waiting = turnaround - p["burst"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

        gantt.append((p["pid"], start, completion))
        completed.add(p["pid"])
        time = completion

    return results, gantt


def round_robin(processes, quantum):
    """Round Robin CPU Scheduling."""
    if quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")

    processes = sorted(processes, key=lambda p: (p["arrival"], p["pid"]))

    if not processes:
        return [], []

    remaining = {p["pid"]: p["burst"] for p in processes}
    completion_times = {}
    queue = []
    gantt = []
    time = 0
    index = 0

    while index < len(processes) or queue:
        if not queue:
            time = max(time, processes[index]["arrival"])

            while (
                index < len(processes)
                and processes[index]["arrival"] <= time
            ):
                queue.append(processes[index])
                index += 1

        p = queue.pop(0)
        pid = p["pid"]

        start = time
        run_time = min(quantum, remaining[pid])
        time += run_time
        remaining[pid] -= run_time

        gantt.append((pid, start, time))

        while (
            index < len(processes)
            and processes[index]["arrival"] <= time
        ):
            queue.append(processes[index])
            index += 1

        if remaining[pid] > 0:
            queue.append(p)
        else:
            completion_times[pid] = time

    results = []

    for p in processes:
        turnaround = completion_times[p["pid"]] - p["arrival"]
        waiting = turnaround - p["burst"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "completion": completion_times[p["pid"]],
            "waiting": waiting,
            "turnaround": turnaround
        })

    return results, gantt


def srtf(processes):
    """Preemptive Shortest Remaining Time First Scheduling."""
    if not processes:
        return [], []

    processes = [p.copy() for p in processes]
    remaining = {p["pid"]: p["burst"] for p in processes}
    completion_times = {}
    time = 0
    gantt = []

    while len(completion_times) < len(processes):
        available = [
            p for p in processes
            if p["arrival"] <= time and remaining[p["pid"]] > 0
        ]

        if not available:
            time += 1
            continue

        current = min(
            available,
            key=lambda p: (
                remaining[p["pid"]],
                p["arrival"],
                p["pid"]
            )
        )

        pid = current["pid"]
        start = time
        time += 1
        remaining[pid] -= 1

        if gantt and gantt[-1][0] == pid and gantt[-1][2] == start:
            gantt[-1] = (pid, gantt[-1][1], time)
        else:
            gantt.append((pid, start, time))

        if remaining[pid] == 0:
            completion_times[pid] = time

    results = []

    for p in processes:
        completion = completion_times[p["pid"]]
        turnaround = completion - p["arrival"]
        waiting = turnaround - p["burst"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

    return results, gantt


def preemptive_priority(processes):
    """Smaller priority number means higher priority."""
    if not processes:
        return [], []

    processes = [p.copy() for p in processes]
    remaining = {p["pid"]: p["burst"] for p in processes}
    completion_times = {}
    time = 0
    gantt = []

    while len(completion_times) < len(processes):
        available = [
            p for p in processes
            if p["arrival"] <= time and remaining[p["pid"]] > 0
        ]

        if not available:
            time += 1
            continue

        current = min(
            available,
            key=lambda p: (
                p.get("priority", 0),
                p["arrival"],
                p["pid"]
            )
        )

        pid = current["pid"]
        start = time
        time += 1
        remaining[pid] -= 1

        if gantt and gantt[-1][0] == pid and gantt[-1][2] == start:
            gantt[-1] = (pid, gantt[-1][1], time)
        else:
            gantt.append((pid, start, time))

        if remaining[pid] == 0:
            completion_times[pid] = time

    results = []

    for p in processes:
        completion = completion_times[p["pid"]]
        turnaround = completion - p["arrival"]
        waiting = turnaround - p["burst"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

    return results, gantt


def display_results(title, results, gantt):
    """Display CPU scheduling metrics and Gantt chart."""
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    if not results:
        print("No processes to schedule.")
        return

    print(
        f"{'PID':<8}{'AT':<8}{'BT':<8}"
        f"{'CT':<8}{'WT':<8}{'TAT':<8}"
    )

    for p in sorted(results, key=lambda p: p["pid"]):
        print(
            f"{p['pid']:<8}{p['arrival']:<8}{p['burst']:<8}"
            f"{p['completion']:<8}{p['waiting']:<8}"
            f"{p['turnaround']:<8}"
        )

    avg_waiting = sum(p["waiting"] for p in results) / len(results)
    avg_turnaround = sum(p["turnaround"] for p in results) / len(results)

    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")

    print("\nGantt Chart:")
    for pid, start, end in gantt:
        print(f"| {pid} ({start}-{end}) ", end="")
    print("|")