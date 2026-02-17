# 🐳 Docker Deployment Guide

This guide explains how to deploy the Availability Scanner as a Docker container with automatic Discord webhook notifications.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Docker Compose Deployment](#docker-compose-deployment)
- [Docker CLI Deployment](#docker-cli-deployment)
- [Container Management](#container-management)
- [Discord Notifications](#discord-notifications)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/MateuszWawro/availability-Scanner.git
cd availability-Scanner

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f
```

The scanner will now run continuously, checking service availability every 5 minutes and sending Discord notifications when services go offline.

## 📦 Prerequisites

- Docker Engine 20.10+ or Docker Desktop
- Docker Compose 2.0+ (included with Docker Desktop)
- Internet connection for pulling images and checking services
- Discord webhook URL (configured in `docker-compose.yml` or via environment variable)

## ⚙️ Configuration

The scanner is configured using environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DISCORD_WEBHOOK_URL` | Discord webhook URL for notifications | - | Yes |
| `CHECK_INTERVAL` | Time between checks (in seconds) | 300 (5 min) | No |

### Getting a Discord Webhook URL

1. Open Discord and go to your server
2. Go to Server Settings → Integrations → Webhooks
3. Click "New Webhook" or select an existing one
4. Copy the Webhook URL
5. Use it in your configuration

## 🐋 Docker Compose Deployment

### Step 1: Edit Configuration

Edit `docker-compose.yml` and update the `DISCORD_WEBHOOK_URL`:

```yaml
environment:
  - DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
  - CHECK_INTERVAL=300  # Optional: adjust check interval
```

### Step 2: Start the Container

```bash
docker-compose up -d
```

This will:
- Build the Docker image
- Create and start the container
- Configure automatic restart on failure
- Run checks every 5 minutes (or your configured interval)

### Step 3: Verify It's Running

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f availability-scanner
```

## 🖥️ Docker CLI Deployment

If you prefer not to use Docker Compose:

### Build the Image

```bash
docker build -t availability-scanner .
```

### Run the Container

```bash
docker run -d \
  --name availability-scanner \
  --restart unless-stopped \
  -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN" \
  -e CHECK_INTERVAL=300 \
  availability-scanner
```

### View Logs

```bash
docker logs -f availability-scanner
```

## 🎛️ Container Management

### Stop the Container

```bash
# Using Docker Compose
docker-compose stop

# Using Docker CLI
docker stop availability-scanner
```

### Start the Container

```bash
# Using Docker Compose
docker-compose start

# Using Docker CLI
docker start availability-scanner
```

### Restart the Container

```bash
# Using Docker Compose
docker-compose restart

# Using Docker CLI
docker restart availability-scanner
```

### View Logs

```bash
# Using Docker Compose - follow logs in real-time
docker-compose logs -f

# Using Docker Compose - last 100 lines
docker-compose logs --tail=100

# Using Docker CLI
docker logs -f availability-scanner
docker logs --tail=100 availability-scanner
```

### Stop and Remove Container

```bash
# Using Docker Compose
docker-compose down

# Using Docker CLI
docker stop availability-scanner
docker rm availability-scanner
```

### Rebuild After Code Changes

```bash
# Using Docker Compose
docker-compose build --no-cache
docker-compose up -d

# Using Docker CLI
docker build --no-cache -t availability-scanner .
docker stop availability-scanner
docker rm availability-scanner
docker run -d --name availability-scanner --restart unless-stopped \
  -e DISCORD_WEBHOOK_URL="YOUR_WEBHOOK_URL" \
  availability-scanner
```

## 🔔 Discord Notifications

### Notification Behavior

- **Trigger**: Notifications are sent **only when one or more services are offline**
- **Frequency**: Each time a check runs (every `CHECK_INTERVAL` seconds)
- **Content**: The notification includes:
  - Title: "🔍 Availability Scanner Report"
  - Timestamp of the scan
  - Status of each service with emoji (✅ online, ❌ offline)
  - Footer with statistics (online/offline counts and percentages)
  - Color: 🟢 Green if all OK, 🔴 Red if any service is offline

### Example Notification

When services are offline, Discord will receive an embed like:

```
🔍 Availability Scanner Report
Scan completed at 2026-02-17 08:30:00

✅ AWS - Online - HTTP 200
❌ Claude (Anthropic) - Offline - Timeout
✅ Cloudflare - Online - HTTP 200
...

Total: 11 | Online: 10 (90.9%) | Offline: 1 (9.1%)
```

### Silence Notifications

If you want to temporarily disable notifications without stopping the scanner:

1. Set `DISCORD_WEBHOOK_URL` to empty string
2. Restart the container

The scanner will continue running but won't send notifications.

## 🌐 Production Deployment

### Ubuntu/Debian Server

#### 1. Install Docker

```bash
# Update package list
sudo apt update

# Install dependencies
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker
sudo systemctl enable docker
sudo systemctl start docker

# Add your user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
```

#### 2. Deploy the Scanner

```bash
# Clone repository
git clone https://github.com/MateuszWawro/availability-Scanner.git
cd availability-Scanner

# Edit configuration
nano docker-compose.yml  # Update DISCORD_WEBHOOK_URL

# Start the service
docker-compose up -d

# Enable auto-start on reboot (already configured with restart: unless-stopped)
```

#### 3. Set Up as a System Service (Optional)

For even more control, you can create a systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/availability-scanner.service
```

Add the following content:

```ini
[Unit]
Description=Availability Scanner
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/availability-Scanner
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable availability-scanner
sudo systemctl start availability-scanner
sudo systemctl status availability-scanner
```

### Environment-Specific Configuration

For different environments (dev, staging, production), create separate `.env` files:

```bash
# .env.production
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/prod/token
CHECK_INTERVAL=300

# .env.staging
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/staging/token
CHECK_INTERVAL=600
```

Then use:

```bash
docker-compose --env-file .env.production up -d
```

## 🔧 Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs
```

**Common issues:**
- Missing `DISCORD_WEBHOOK_URL`: Check environment variables
- Port conflicts: The scanner doesn't expose ports, so this shouldn't occur
- Build errors: Try rebuilding with `--no-cache`

### No Discord Notifications

**Verify webhook URL:**
```bash
# Check environment variable is set
docker exec availability-scanner env | grep DISCORD_WEBHOOK_URL
```

**Test webhook manually:**
```bash
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content": "Test message"}'
```

**Check logs for errors:**
```bash
docker-compose logs -f | grep Discord
```

### Services Showing as Offline

**Check network connectivity:**
```bash
# Enter the container
docker exec -it availability-scanner bash

# Test connectivity
ping -c 3 8.8.8.8
curl -I https://www.google.com
```

**Check timeout settings:**
- Default timeout is 10 seconds
- Increase if needed by modifying `availability_scanner_discord.py`

### High Memory Usage

The scanner is lightweight and should use minimal resources:
- Expected memory: ~50-100 MB
- Expected CPU: <1% when idle

**Check resource usage:**
```bash
docker stats availability-scanner
```

### Container Keeps Restarting

**Check exit code and logs:**
```bash
docker ps -a | grep availability-scanner
docker logs availability-scanner
```

**Common causes:**
- Python errors: Check logs for stack traces
- Missing dependencies: Rebuild image
- Invalid environment variables: Verify configuration

### Update to Latest Version

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Reset Everything

If all else fails, start fresh:

```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker rmi availability-scanner

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Discord Webhooks Guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
- [Main README](README.md)

## 🆘 Getting Help

If you encounter issues not covered in this guide:

1. Check the [Issues](https://github.com/MateuszWawro/availability-Scanner/issues) page
2. Create a new issue with:
   - Your Docker version (`docker --version`)
   - Error messages and logs
   - Steps to reproduce
   - Your configuration (without sensitive data)

---

**Happy Monitoring! 🎉**
