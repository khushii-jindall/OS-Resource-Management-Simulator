# OS Resource Management Simulator

A Python-based, menu-driven **Operating System Resource Management Simulator** that demonstrates core OS algorithms for CPU scheduling, memory allocation, deadlock handling, and disk scheduling. The project also includes automated unit testing, logging, report generation, CSV exports, and performance comparison charts.

## 1. Project Overview

The OS Resource Management Simulator provides a practical way to understand how an operating system allocates resources and schedules processes. Users can execute multiple algorithms, view their results, compare performance, and generate reports through a command-line interface.

The project is developed in Python and runs in Ubuntu on Windows Subsystem for Linux (WSL).

## 2. Objectives

- Understand and compare CPU scheduling algorithms.
- Simulate memory allocation strategies.
- Analyze deadlock avoidance and detection.
- Calculate disk-head movement using disk scheduling algorithms.
- Generate reports, CSV files, and comparison charts.
- Maintain application logs for monitoring execution.
- Verify core functionality using automated unit tests.

## 3. Technologies Used

- **Programming Language:** Python 3
- **Operating Environment:** Ubuntu on WSL
- **Code Editor:** Visual Studio Code
- **Testing Framework:** Python `unittest`
- **Logging:** Python `logging` module
- **Version Control:** Git and GitHub
- **Data Export:** CSV
- **Visualization:** Matplotlib (if configured in the project environment)

## 4. Features and Implemented Algorithms

### 4.1 CPU Scheduling

The simulator implements the following CPU scheduling algorithms:

- First Come First Serve (FCFS)
- Shortest Job First (SJF), non-preemptive
- Round Robin (RR)
- Shortest Remaining Time First (SRTF)
- Preemptive Priority Scheduling

**Features:**
- Process scheduling and execution order
- Waiting time and turnaround time calculation
- Average waiting time and average turnaround time
- Gantt chart representation
- Comparison of scheduling performance

### 4.2 Memory Management

The simulator demonstrates three memory allocation strategies:

- First Fit
- Best Fit
- Worst Fit

These algorithms allocate processes to suitable memory blocks according to their respective allocation strategies.

### 4.3 Deadlock Management

The project includes deadlock avoidance and detection.

**Banker's Algorithm — Deadlock Avoidance**
- Available resource vector
- Need matrix calculation
- Safe-state verification
- Safe-sequence generation

**Deadlock Detection**
- Analyzes the configured resource allocation and request data
- Identifies processes involved in the detected deadlock scenario

### 4.4 Disk Scheduling

The simulator implements:

- First Come First Serve (FCFS)
- Shortest Seek Time First (SSTF)
- SCAN
- C-SCAN

**Features:**
- Disk request processing order
- Total disk-head movement calculation
- Comparison of disk scheduling algorithms
- Sorted comparison results and charts

### 4.5 Additional Features

- Menu-driven command-line interface
- Application logging in `logs/simulator.log`
- Automated unit testing
- Timestamped text reports
- CSV exports for CPU and disk scheduling results
- CPU scheduling comparison charts
- Disk scheduling comparison charts

## 5. Project Structure

```text
OS-Resource-Management-Simulator/
├── main.py
├── modules/
│   ├── cpu_scheduling.py
│   ├── memory_management.py
│   ├── deadlock.py
│   ├── disk_scheduling.py
│   ├── logger.py
│   ├── report_generator.py
│   └── visualization.py
├── tests/
│   └── test_simulator.py
├── reports/
│   ├── simulation_report_*.txt
│   ├── cpu_results_*.csv
│   ├── disk_results_*.csv
│   ├── cpu_comparison_*.png
│   └── disk_comparison_*.png
├── logs/
│   └── simulator.log
├── data/
├── screenshots/
├── scripts/
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: The structure above represents the expected project layout. Actual files in each folder may vary.*

## 6. Prerequisites

Before running the project, ensure you have:

- Python 3 installed
- Ubuntu on WSL or a compatible Linux environment
- Git (optional, for version control)
- Required Python packages installed from `requirements.txt`

## 7. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/OS-Resource-Management-Simulator.git
cd OS-Resource-Management-Simulator
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

If the project uses only Python's standard library for a particular feature, additional packages may not be required for that feature.

### Step 4: Run the simulator

```bash
python3 main.py
```

Select an option from the displayed menu to execute an algorithm, compare results, or generate reports.

## 8. Running Unit Tests

Execute the following command from the project root directory:

```bash
python3 -m unittest discover -s tests -v
```

### Test Results

The current test suite contains **10 tests**, all of which passed in the latest recorded execution.

| Module | Tests Passed |
|---|---:|
| CPU Scheduling | 3 |
| Memory Management | 3 |
| Deadlock Avoidance | 1 |
| Disk Scheduling | 3 |
| **Total** | **10/10** |

The tests verify selected CPU scheduling algorithms, memory allocation strategies, Banker's Algorithm, and disk scheduling algorithms.

## 9. Sample Simulation Results

The following values were observed during a sample execution using the project's configured inputs.

### CPU Scheduling

| Algorithm | Average Waiting Time | Average Turnaround Time |
|---|---:|---:|
| FCFS | 4.00 | 6.75 |
| SJF (Non-preemptive) | 3.25 | 6.00 |
| Round Robin (Q = 2) | 4.50 | 7.25 |
| SRTF | 2.25 | 5.00 |
| Preemptive Priority | 4.00 | 6.75 |

*These values depend on the configured sample processes and Round Robin time quantum.*

### Disk Scheduling

Sample total disk-head movement:

| Algorithm | Head Movement |
|---|---:|
| FCFS | 640 |
| SSTF | 236 |
| SCAN (Left) | 236 |
| SCAN (Right) | 331 |
| C-SCAN (Left) | 386 |
| C-SCAN (Right) | 382 |

*These results are based on the configured sample disk requests, initial head position, disk direction, and disk-size assumptions.*

## 10. Reports, Exports, and Logs

The simulator supports generating and saving execution outputs.

- **Text Reports:** Timestamped reports are saved in `reports/`.
- **CSV Exports:** CPU and disk scheduling comparison data can be exported to CSV files.
- **Charts:** CPU and disk scheduling comparison charts are generated as PNG files when the corresponding visualization options are executed.
- **Logs:** Application events are recorded in `logs/simulator.log`.

Generated files can be opened using compatible text editors, spreadsheet software, or image viewers.

## 11. Future Enhancements

Potential future improvements include:

- Interactive input for processes, memory blocks, and disk requests
- Additional CPU and disk scheduling algorithms
- More detailed memory fragmentation analysis
- Enhanced Gantt charts and disk-head movement visualizations
- PDF report export
- A graphical user interface
- Configurable simulation datasets
- Expanded automated test coverage

## 12. Learning Outcomes

This project provides practical experience with:

- Operating system resource management concepts
- CPU scheduling and process execution
- Memory allocation strategies
- Deadlock avoidance and detection
- Disk scheduling and seek-time analysis
- Python modular programming
- Unit testing and application logging
- Data export, visualization, and Git-based version control

## 13. Conclusion

The OS Resource Management Simulator brings together several fundamental operating system algorithms in a single Python application. Its menu-driven interface, automated tests, logging, report generation, and visual comparisons make it a useful learning tool for understanding resource management and analyzing algorithm performance.

The latest recorded test execution completed successfully, with **all 10 unit tests passing**.

---
