def fcfs(requests, head):
    """First Come First Serve Disk Scheduling."""
    order = requests.copy()
    movement = 0
    current = head
    path = [head]

    for request in order:
        movement += abs(current - request)
        current = request
        path.append(current)

    return order, movement, path


def sstf(requests, head):
    """Shortest Seek Time First."""
    pending = requests.copy()
    order = []
    movement = 0
    current = head
    path = [head]

    while pending:
        nearest = min(pending, key=lambda r: abs(current - r))
        movement += abs(current - nearest)
        current = nearest

        order.append(nearest)
        path.append(current)
        pending.remove(nearest)

    return order, movement, path


def scan(requests, head, disk_size=200, direction="left"):
    """SCAN / Elevator Disk Scheduling."""
    _validate_input(requests, head, disk_size, direction)

    pending = sorted(requests)
    left = [r for r in pending if r < head]
    right = [r for r in pending if r >= head]

    order = []
    path = [head]
    movement = 0
    current = head
    last_cylinder = disk_size - 1

    if direction == "left":
        for request in reversed(left):
            order.append(request)
            movement += abs(current - request)
            current = request
            path.append(current)

        if right:
            if current != 0:
                movement += current
                current = 0
                path.append(current)

            for request in right:
                order.append(request)
                movement += abs(current - request)
                current = request
                path.append(current)

    else:
        for request in right:
            order.append(request)
            movement += abs(current - request)
            current = request
            path.append(current)

        if left:
            if current != last_cylinder:
                movement += abs(current - last_cylinder)
                current = last_cylinder
                path.append(current)

            for request in reversed(left):
                order.append(request)
                movement += abs(current - request)
                current = request
                path.append(current)

    return order, movement, path


def c_scan(requests, head, disk_size=200, direction="right"):
    """Circular SCAN Disk Scheduling."""
    _validate_input(requests, head, disk_size, direction)

    pending = sorted(requests)
    left = [r for r in pending if r < head]
    right = [r for r in pending if r >= head]

    order = []
    path = [head]
    movement = 0
    current = head
    last_cylinder = disk_size - 1

    if direction == "right":
        for request in right:
            order.append(request)
            movement += abs(current - request)
            current = request
            path.append(current)

        if left:
            if current != last_cylinder:
                movement += abs(current - last_cylinder)
                current = last_cylinder
                path.append(current)

            if current != 0:
                movement += last_cylinder
                current = 0
                path.append(current)

            for request in left:
                order.append(request)
                movement += abs(current - request)
                current = request
                path.append(current)

    else:
        for request in reversed(left):
            order.append(request)
            movement += abs(current - request)
            current = request
            path.append(current)

        if right:
            if current != 0:
                movement += current
                current = 0
                path.append(current)

            if current != last_cylinder:
                movement += last_cylinder
                current = last_cylinder
                path.append(current)

            for request in reversed(right):
                order.append(request)
                movement += abs(current - request)
                current = request
                path.append(current)

    return order, movement, path


def _validate_input(requests, head, disk_size, direction):
    if disk_size <= 0:
        raise ValueError("Disk size must be positive.")

    if not isinstance(head, int) or not 0 <= head < disk_size:
        raise ValueError("Head must be within the disk range.")

    if direction not in ("left", "right"):
        raise ValueError("Direction must be 'left' or 'right'.")

    for request in requests:
        if not isinstance(request, int) or not 0 <= request < disk_size:
            raise ValueError("Requests must be valid disk cylinder numbers.")


def display_result(name, result):
    """Display disk scheduling results."""
    order, movement, path = result

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)
    print("Request service order:", " -> ".join(map(str, order)))
    print("Head movement path:", " -> ".join(map(str, path)))
    print("Total head movement:", movement, "cylinders")