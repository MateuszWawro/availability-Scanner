# Availability Scanner

A Python-based tool to monitor the availability of popular online services.

## Features

- Monitors the status of multiple online services including:
  - AWS
  - Claude (Anthropic)
  - Cloudflare
  - Google DNS
  - Microsoft Teams
  - Microsoft 365
  - OpenAI
  - GitHub Copilot
  - Docker Hub
  - Pingdom
  - GitHub (Bonus)

- Displays results in a clear, tabular format
- Shows online/offline status with visual indicators (✅/❌)
- Provides detailed status information for each service
- Calculates availability statistics

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MateuszWawro/availability-Scanner.git
cd availability-Scanner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scanner:
```bash
python availability_scanner.py
```

Or make it executable and run directly:
```bash
chmod +x availability_scanner.py
./availability_scanner.py
```

## Sample Output

```
======================================================================
Availability Scanner - Service Status Monitor
Scan Time: 2026-02-16 22:10:00
======================================================================

Checking AWS... ✅ Online
Checking Claude (Anthropic)... ✅ Online
Checking Cloudflare... ✅ Online
Checking Google DNS... ✅ Online
Checking Microsoft Teams... ✅ Online
Checking Microsoft 365... ✅ Online
Checking OpenAI... ✅ Online
Checking GitHub Copilot... ✅ Online
Checking Docker Hub... ✅ Online
Checking Pingdom... ✅ Online
Checking GitHub (Bonus)... ✅ Online

======================================================================
Summary Report
======================================================================

+--------------------+-----------+--------------------+
| Service            | Status    | Details            |
+====================+===========+====================+
| AWS                | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+
| Claude (Anthropic) | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+
| Cloudflare         | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+
| Google DNS         | ✅ Online | Port 53 accessible |
+--------------------+-----------+--------------------+
| Microsoft Teams    | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+
| Microsoft 365      | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+
| OpenAI             | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+
| GitHub Copilot     | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+
| Docker Hub         | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+
| Pingdom            | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+
| GitHub (Bonus)     | ✅ Online | HTTP 200           |
+--------------------+-----------+--------------------+

Total Services Checked: 11
Online: 11 (100.0%)
Offline: 0 (0.0%)
```

## How It Works

The scanner uses HTTP/HTTPS requests to check the availability of web services and APIs. For each service:
- It sends a test request to the service endpoint
- Records the response status
- Displays the result with status codes or error messages
- Aggregates all results in a summary table

## Configuration

The scanner uses a default timeout of 10 seconds for each check. You can modify the timeout and other parameters by editing the `availability_scanner.py` file.

## License

MIT License