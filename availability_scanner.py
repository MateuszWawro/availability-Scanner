#!/usr/bin/env python3
"""
Availability Scanner - Monitor the status of popular online services
"""

import requests
import socket
from datetime import datetime
from typing import Dict, Tuple
from tabulate import tabulate


class ServiceChecker:
    """Base class for checking service availability"""
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AvailabilityScanner/1.0'
        })
    
    def check_http(self, url: str, expected_status: int = 200) -> Tuple[bool, str]:
        """Check HTTP endpoint availability"""
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            if response.status_code == expected_status or response.status_code < 400:
                return True, f"HTTP {response.status_code}"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.ConnectionError:
            return False, "Connection failed"
        except requests.exceptions.RequestException as e:
            return False, f"Error: {str(e)[:30]}"
    
    def check_dns(self, hostname: str, expected_ip: str = None) -> Tuple[bool, str]:
        """Check DNS resolution"""
        try:
            ip = socket.gethostbyname(hostname)
            if expected_ip and ip != expected_ip:
                return False, f"Wrong IP: {ip}"
            return True, f"Resolved to {ip}"
        except socket.gaierror:
            return False, "DNS resolution failed"
        except Exception as e:
            return False, f"Error: {str(e)[:30]}"
    
    def check_google_dns(self) -> Tuple[bool, str]:
        """Check Google DNS (8.8.8.8)"""
        try:
            # Try to resolve a known domain using Google DNS
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            sock.connect(("8.8.8.8", 53))
            sock.close()
            return True, "Port 53 accessible"
        except Exception:
            return False, "Port 53 not accessible"
    
    def check_aws(self) -> Tuple[bool, str]:
        """Check AWS availability"""
        # Check AWS status page
        return self.check_http("https://status.aws.amazon.com")
    
    def check_claude(self) -> Tuple[bool, str]:
        """Check Claude (Anthropic) availability"""
        # Check Anthropic website
        return self.check_http("https://www.anthropic.com")
    
    def check_cloudflare(self) -> Tuple[bool, str]:
        """Check Cloudflare availability"""
        # Check Cloudflare's 1.1.1.1 DNS
        return self.check_http("https://1.1.1.1")
    
    def check_teams(self) -> Tuple[bool, str]:
        """Check Microsoft Teams availability"""
        # Check Teams web app
        return self.check_http("https://teams.microsoft.com")
    
    def check_microsoft_365(self) -> Tuple[bool, str]:
        """Check Microsoft 365 availability"""
        # Check Microsoft 365 status page
        return self.check_http("https://www.microsoft.com/en-us/microsoft-365")
    
    def check_openai(self) -> Tuple[bool, str]:
        """Check OpenAI availability"""
        # Check OpenAI website
        return self.check_http("https://www.openai.com")
    
    def check_copilot(self) -> Tuple[bool, str]:
        """Check GitHub Copilot availability"""
        # Check GitHub Copilot page
        return self.check_http("https://github.com/features/copilot")
    
    def check_docker_hub(self) -> Tuple[bool, str]:
        """Check Docker Hub availability"""
        # Check Docker Hub
        return self.check_http("https://hub.docker.com")
    
    def check_pingdom(self) -> Tuple[bool, str]:
        """Check Pingdom availability"""
        # Check Pingdom website
        return self.check_http("https://www.pingdom.com")
    
    def check_github(self) -> Tuple[bool, str]:
        """Check GitHub availability (bonus)"""
        # Check GitHub API
        return self.check_http("https://api.github.com")


def format_status(is_available: bool) -> str:
    """Format status as Online/Offline with emoji"""
    if is_available:
        return "✅ Online"
    else:
        return "❌ Offline"


def main():
    """Main function to check all services and display results"""
    print("=" * 70)
    print("Availability Scanner - Service Status Monitor")
    print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    checker = ServiceChecker(timeout=10)
    
    # Define services to check
    services = [
        ("AWS", checker.check_aws),
        ("Claude (Anthropic)", checker.check_claude),
        ("Cloudflare", checker.check_cloudflare),
        ("Google DNS", checker.check_google_dns),
        ("Microsoft Teams", checker.check_teams),
        ("Microsoft 365", checker.check_microsoft_365),
        ("OpenAI", checker.check_openai),
        ("GitHub Copilot", checker.check_copilot),
        ("Docker Hub", checker.check_docker_hub),
        ("Pingdom", checker.check_pingdom),
        ("GitHub (Bonus)", checker.check_github),
    ]
    
    # Check all services
    results = []
    for service_name, check_func in services:
        print(f"Checking {service_name}...", end=" ", flush=True)
        is_available, details = check_func()
        status = format_status(is_available)
        results.append([service_name, status, details])
        print(status)
    
    print()
    print("=" * 70)
    print("Summary Report")
    print("=" * 70)
    print()
    
    # Display results in a table
    headers = ["Service", "Status", "Details"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
    
    # Calculate statistics
    total = len(results)
    online = sum(1 for r in results if "✅" in r[1])
    offline = total - online
    
    print()
    print(f"Total Services Checked: {total}")
    print(f"Online: {online} ({online/total*100:.1f}%)")
    print(f"Offline: {offline} ({offline/total*100:.1f}%)")
    print()


if __name__ == "__main__":
    main()
