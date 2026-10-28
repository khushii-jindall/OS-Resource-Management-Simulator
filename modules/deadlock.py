
# ==================================================
# DEADLOCK AVOIDANCE - BANKER'S ALGORITHM
# ==================================================

def is_safe_state(available, allocation, maximum):
    processes = len(allocation)
    resources = len(available)

    # Need = Maximum - Allocation
    need = [
        [
            maximum[i][j] - allocation[i][j]
            for j in range(resources)
        ]
        for i in range(processes)
    ]

    work = available.copy()
    finish = [False] * processes
    safe_sequence = []

    while len(safe_sequence) < processes:
        found = False

        for i in range(processes):
            if finish[i]:
                continue

            # Check whether the process's needs can be satisfied
            if all(
                need[i][j] <= work[j]
                for j in range(resources)
            ):
                # Process completes and releases allocated resources
                for j in range(resources):
                    work[j] += allocation[i][j]

                safe_sequence.append(f"P{i}")
                finish[i] = True
                found = True

        if not found:
            return False, safe_sequence, need

    return True, safe_sequence, need


# ==================================================
# DEADLOCK DETECTION ALGORITHM
# ==================================================

def detect_deadlock(available, allocation, request):
    """
    Detects deadlocked processes.

    available: Available instances of each resource
    allocation: Resources currently allocated to each process
    request: Additional resources each process currently requests

    Returns:
        List of deadlocked process names, e.g. ["P0", "P1"].
        An empty list means no deadlock was detected.
    """

    process_count = len(allocation)
    resource_count = len(available)

    # Validate matrix dimensions
    if len(request) != process_count:
        raise ValueError(
            "Allocation and request must have the same process count."
        )

    if any(
        len(row) != resource_count
        for row in allocation + request
    ):
        raise ValueError(
            "Resource matrix dimensions do not match available resources."
        )

    if any(value < 0 for value in available):
        raise ValueError("Available resources cannot be negative.")

    if any(
        value < 0
        for matrix in (allocation, request)
        for row in matrix
        for value in row
    ):
        raise ValueError(
            "Allocation and request values cannot be negative."
        )

    # Work represents currently available resources
    work = available.copy()

    # A process holding no resources can be considered finished
    finish = [
        all(value == 0 for value in allocation[i])
        for i in range(process_count)
    ]

    # Try to find processes whose requests can be satisfied
    while True:
        found = False

        for i in range(process_count):
            if finish[i]:
                continue

            # Can this process receive its requested resources?
            if all(
                request[i][j] <= work[j]
                for j in range(resource_count)
            ):
                # Assume process finishes and releases its resources
                for j in range(resource_count):
                    work[j] += allocation[i][j]

                finish[i] = True
                found = True

        # Stop when no additional process can finish
        if not found:
            break

    # Unfinished processes are reported as deadlocked
    deadlocked = [
        f"P{i}"
        for i in range(process_count)
        if not finish[i]
    ]

    return deadlocked


# ==================================================
# TEST / STANDALONE EXECUTION
# ==================================================

def main():
    print("OS Resource Management Simulator")
    print("Banker's Algorithm - Deadlock Avoidance")

    available = [3, 3, 2]

    allocation = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2]   # P4
    ]

    maximum = [
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3]   # P4
    ]

    safe, sequence, need = is_safe_state(
        available, allocation, maximum
    )

    print("\nAvailable resources:", available)
    print("\nNeed Matrix (Maximum - Allocation):")
    print(f"{'Process':<12}{'A':<8}{'B':<8}{'C':<8}")

    for i, row in enumerate(need):
        print(
            f"{'P' + str(i):<12}"
            f"{row[0]:<8}"
            f"{row[1]:<8}"
            f"{row[2]:<8}"
        )

    if safe:
        print("\nSystem is in a SAFE STATE.")
        print("Safe sequence:", " -> ".join(sequence))
    else:
        print("\nSystem is in an UNSAFE STATE.")
        print("No complete safe sequence exists.")

        if sequence:
            print("Partial sequence:", " -> ".join(sequence))


if __name__ == "__main__":
    main()
