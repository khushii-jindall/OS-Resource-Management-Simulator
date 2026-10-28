
def first_fit(blocks, processes):
    memory = blocks.copy()
    return allocate_memory(memory, processes, "First Fit", "first")


def best_fit(blocks, processes):
    memory = blocks.copy()
    return allocate_memory(memory, processes, "Best Fit", "best")


def worst_fit(blocks, processes):
    memory = blocks.copy()
    return allocate_memory(memory, processes, "Worst Fit", "worst")


def allocate_memory(blocks, processes, algorithm, strategy):
    allocations = [-1] * len(processes)

    for i, process_size in enumerate(processes):
        suitable = [
            j for j, block_size in enumerate(blocks)
            if block_size >= process_size
        ]

        if not suitable:
            continue

        if strategy == "first":
            chosen = suitable[0]
        elif strategy == "best":
            chosen = min(suitable, key=lambda j: blocks[j])
        else:
            chosen = max(suitable, key=lambda j: blocks[j])

        allocations[i] = chosen
        blocks[chosen] -= process_size

    print(f"\n{'=' * 45}")
    print(f"{algorithm} Memory Allocation")
    print("=" * 45)
    print(f"{'Process':<12}{'Size':<12}{'Block':<12}{'Status'}")

    for i, size in enumerate(processes):
        if allocations[i] == -1:
            print(f"{'P' + str(i + 1):<12}{size:<12}{'-':<12}Not Allocated")
        else:
            block_number = allocations[i] + 1
            print(
                f"{'P' + str(i + 1):<12}{size:<12}"
                f"{'B' + str(block_number):<12}Allocated"
            )

    print("\nRemaining memory in each block:")
    for i, remaining in enumerate(blocks):
        print(f"Block B{i + 1}: {remaining} units")

    allocated_count = sum(block != -1 for block in allocations)
    print(f"\nProcesses allocated: {allocated_count}/{len(processes)}")


def main():
    # Memory blocks and process sizes are measured in units.
    blocks = [100, 500, 200, 300, 600]
    processes = [212, 417, 112, 426]

    print("OS Resource Management Simulator - Memory Management")
    print("Memory blocks:", blocks)
    print("Process sizes:", processes)
    print("\n1. First Fit")
    print("2. Best Fit")
    print("3. Worst Fit")
    print("4. Compare all algorithms")

    choice = input("Select option (1-4): ").strip()

    if choice == "1":
        first_fit(blocks, processes)
    elif choice == "2":
        best_fit(blocks, processes)
    elif choice == "3":
        worst_fit(blocks, processes)
    elif choice == "4":
        first_fit(blocks, processes)
        best_fit(blocks, processes)
        worst_fit(blocks, processes)
    else:
        print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
