#!/usr/bin/env python3
"""
Availability Scanner with Discord Notifications
Monitors service availability and sends alerts to Discord webhook
"""

import os
import sys
import time
import json
import requests
from datetime import datetime, timezone
from typing import Dict, List, Tuple

# Import all functionality from the original scanner
from availability_scanner import ServiceChecker, format_status


def send_discord_notification(webhook_url: str, results: List[Tuple[str, bool, str]], scan_time: str) -> bool:
    """
    Send notification to Discord webhook
    
    Args:
        webhook_url: Discord webhook URL
        results: List of tuples (service_name, is_available, details)
        scan_time: Timestamp of the scan
        
    Returns:
        bool: True if notification was sent successfully
    """
    if not webhook_url:
        print("❌ No Discord webhook URL configured")
        return False
    
    # Check if any service is offline
    has_offline = any(not is_available for _, is_available, _ in results)
    
    if not has_offline:
        print("✅ All services online - no notification needed")
        return True
    
    # Calculate statistics
    total = len(results)
    online = sum(1 for _, is_available, _ in results if is_available)
    offline = total - online
    online_pct = (online / total * 100) if total > 0 else 0
    offline_pct = (offline / total * 100) if total > 0 else 0
    
    # Determine embed color (green if all OK, red if any offline)
    embed_color = 0x00ff00 if not has_offline else 0xff0000
    
    # Create fields for each service
    fields = []
    for service_name, is_available, details in results:
        emoji = "✅" if is_available else "❌"
        status = "Online" if is_available else "Offline"
        fields.append({
            "name": f"{emoji} {service_name}",
            "value": f"**{status}** - {details}",
            "inline": True
        })
    
    # Create embed
    embed = {
        "title": "🔍 Availability Scanner Report",
        "description": f"Scan completed at {scan_time}",
        "color": embed_color,
        "fields": fields,
        "footer": {
            "text": f"Total: {total} | Online: {online} ({online_pct:.1f}%) | Offline: {offline} ({offline_pct:.1f}%)"
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Create payload
    payload = {
        "embeds": [embed]
    }
    
    # Send to Discord
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 204:
            print("✅ Discord notification sent successfully")
            return True
        else:
            print(f"⚠️ Discord webhook returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Discord notification: {e}")
        return False


def run_checks() -> Tuple[List[Tuple[str, bool, str]], str]:
    """
    Run all service checks
    
    Returns:
        Tuple of (results list, scan time string)
    """
    scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("=" * 70)
    print("Availability Scanner - Service Status Monitor")
    print(f"Scan Time: {scan_time}")
    print("=" * 70)
    print()
    
    with ServiceChecker(timeout=10) as checker:
        # Define services to check
        services = [
            ("AWS", checker.check_aws),
            ("Claude (Anthropic)", checker.check_claude),
            ("Cloudflare", checker.check_cloudflare),
            ("Google DNS", checker.check_google_dns),
            ("Microsoft Teams", checker.check_teams),
            ("Microsoft 365", checker.check_microsoft_365),
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
            results.append((service_name, is_available, details))
            print(status)
    
    print()
    
    # Calculate and display statistics
    total = len(results)
    online = sum(1 for _, is_available, _ in results if is_available)
    offline = total - online
    
    print(f"📊 Summary: {online}/{total} online ({online/total*100:.1f}%), {offline} offline ({offline/total*100:.1f}%)")
    print()
    
    return results, scan_time


def main():
    """
    Main function with monitoring loop
    """
    # Get configuration from environment variables
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "")
    check_interval = int(os.environ.get("CHECK_INTERVAL", "1800"))
    
    print("🚀 Starting Availability Scanner with Discord Notifications")
    print(f"📡 Check Interval: {check_interval} seconds ({check_interval/60:.1f} minutes)")
    print(f"🔔 Discord Webhook: {'Configured' if webhook_url else 'Not configured'}")
    print()
    
    if not webhook_url:
        print("⚠️ WARNING: DISCORD_WEBHOOK_URL not set. Notifications will not be sent.")
        print("   Set the environment variable to enable Discord notifications.")
        print()
    
    iteration = 0
    
    try:
        while True:
            iteration += 1
            print(f"🔄 Starting check iteration #{iteration}")
            print()
            
            try:
                # Run checks
                results, scan_time = run_checks()
                
                # Send Discord notification if configured
                if webhook_url:
                    send_discord_notification(webhook_url, results, scan_time)
                
            except Exception as e:
                print(f"❌ Error during check iteration: {e}")
                print("   Will retry on next iteration...")
                print()
            
            # Wait for next check
            print(f"⏳ Waiting {check_interval} seconds until next check...")
            print("=" * 70)
            print()
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print()
        print("🛑 Received stop signal. Shutting down gracefully...")
        print("👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
