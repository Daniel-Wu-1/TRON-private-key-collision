# 🔐 TRON Private Key Collision Tool

- An integrated TRON blockchain private key collision research tool with core engine, web monitoring interface, and automated deployment
- Explore blockchain cryptography principles by randomly generating private keys and checking asset balances of corresponding addresses
- Lightweight resource usage, perfect for casual background running

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey.svg)

**🌐 Language**: [中文](README.md) | **English**

## ⚠️ Disclaimer

**This tool is for educational and research purposes only. Not recommended for any illegal or malicious activities.**

- The probability of successful private key collision is extremely low (approximately 2^-256)
- Even using all the world's supercomputers, it would be nearly impossible to successfully collide a valid private key before the universe ends
- This tool is primarily for educational purposes and blockchain cryptography research
- Please comply with local laws and regulations, do not use this tool for illegal purposes

**Good luck! But please be realistic!**

## 🏗️ Project Architecture

```
Mnemonic_collision/
├── 📦 src/                           # Core Engine
│   ├── jiutong.py                    # Main collision program (async high-performance)
│   ├── test_api.py                   # TronGrid API testing tool
│   ├── requirements.txt              # Python dependencies
│   ├── logs.txt                      # Runtime logs (auto-generated)
│   └── non_zero_addresses.txt        # Found addresses with assets (generated on success)
├── 🌐 web-monitor/                   # Web Monitoring Interface
│   ├── web_monitor.py                # Flask monitoring service (with WebSocket)
│   ├── templates/                    # HTML templates
│   │   └── index.html                # Responsive monitoring dashboard
│   ├── static/                       # Static assets (CSS/JS)
│   ├── install-web-monitor.sh        # Web monitor installation script
│   ├── web-requirements.txt          # Web service dependencies
│   ├── fix-sudo-permissions.sh       # Permission fix script
│   └── WEB_MONITOR_GUIDE.md          # Web monitoring guide
├── 🚀 deployment/                    # Automated Deployment
│   ├── install-rocky-minimal.sh      # Rocky Linux minimal installation script
│   └── ROCKY_LINUX_QUICK_START.md    # Quick deployment guide
├── 💼 TRON私钥碰撞/                   # Windows Standalone Version (Optional)
│   ├── jiutong.py                    # Standalone program copy
│   ├── jiutong.spec                  # PyInstaller packaging config
│   └── dist/                         # Compiled executables
│       └── jiutong.exe               # Windows executable
├── README.md                         # Project documentation (Chinese)
└── README_EN.md                      # Project documentation (English)
```

## 🚀 Features

### Core Engine Features
- **🔐 Private Key Generation**: Uses secure random number generator (`os.urandom(32)`)
- **📍 Address Calculation**: Complete TRON address generation pipeline (secp256k1 → Keccak-256 → Base58Check)
- **💰 Multi-Asset Support**: Detects TRX, TRC10, and TRC20 tokens (including USDT, etc.)
- **⚡ Async Queries**: High-performance async API requests based on aiohttp
- **📊 Smart Logging**: Rolling log system, automatically retains latest 2000 records
- **🎯 Auto Save**: Automatically saves complete information when addresses with assets are found
- **⏱️ Rate Control**: Respects TronGrid API limits, maximum 10 queries per second

### Web Monitoring Interface
- **📈 Real-time Monitoring**: Service status, system resources, runtime statistics
- **🎮 Remote Control**: Start, stop, restart collision services
- **📝 Real-time Logs**: WebSocket real-time log streaming
- **🔒 Security Mode**: Private key information not transmitted over network, only saved on server
- **📊 Performance Monitoring**: CPU, memory, disk usage
- **🏆 Discovery Display**: Prominent alerts when addresses with assets are found

### Deployment Automation
- **🐧 Rocky Linux Optimization**: Installation script optimized for Rocky Linux 9.0
- **⚡ Minimal Installation**: Minimal dependencies, only installs necessary components
- **🇨🇳 China Optimization**: Supports Tsinghua University mirror sources, significantly improves download speed
- **🔧 Service Management**: systemd service integration, supports automatic restart
- **📦 One-click Deployment**: Fully automated process from environment configuration to service startup

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Linux (recommended Rocky Linux 9.0) / Windows 10+
- **Python**: 3.7 or higher
- **Memory**: 512MB available memory
- **Network**: Stable internet connection (access to TronGrid API)
- **Disk**: 1GB available space

### Recommended Configuration
- **CPU**: Multi-core processor (supports multi-instance parallel)
- **Memory**: 2GB or more
- **Network**: High-speed stable connection
- **System**: Dedicated Linux server

## 🔧 Installation & Deployment

### Method 1: Rocky Linux One-click Deployment (Recommended)

Suitable for Rocky Linux 9.0 servers, provides complete automated deployment:

```bash
# 1. Clone project
git clone <repository-url>
cd Mnemonic_collision

# 2. Run deployment script
chmod +x deployment/install-rocky-minimal.sh
./deployment/install-rocky-minimal.sh

# 3. Start service
sudo systemctl start tron-collision

# 4. Optional: Install web monitoring
cd web-monitor
chmod +x install-web-monitor.sh
./install-web-monitor.sh
sudo systemctl start tron-web-monitor
```

**Deployment Script Features**:
- 🇨🇳 **Smart Source Selection**: Automatically detects and configures Tsinghua University mirror sources
- ⚡ **Minimal Installation**: Only installs necessary 6 system packages
- 🔒 **Security Configuration**: Creates dedicated user, configures appropriate permissions
- 🔄 **Auto Restart**: System-level service management, supports automatic failure recovery

### Method 2: Manual Installation

#### Windows Users

**Method 1: Python Execution (Recommended)**
```powershell
# 1. Install Python dependencies
pip install -r src/requirements.txt

# 2. Run program
cd src
python jiutong.py
```

**Method 2: Use Compiled Version (if available)**
```powershell
# Run compiled executable directly
cd TRON私钥碰撞\dist
jiutong.exe
```

> 💡 **Tip**: To compile your own exe, refer to `TRON私钥碰撞/jiutong.spec` and use PyInstaller

#### Linux Users

```bash
# 1. Install system dependencies
sudo apt update && sudo apt install -y python3 python3-pip python3-venv

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install Python dependencies
pip install -r src/requirements.txt

# 4. Run program
cd src
python jiutong.py
```

### Method 3: Docker Deployment (Coming Soon)

```bash
# Build image
docker build -t tron-collision .

# Run container
docker run -d --name tron-collision \
  -v ./logs:/app/logs \
  -v ./data:/app/data \
  tron-collision
```

## 🎯 Usage Guide

### Basic Usage

1. **Test API Connection (Recommended before first run)**
   ```bash
   # Test if TronGrid API is accessible
   cd src
   python test_api.py
   ```

2. **Start Program**
   ```bash
   # Direct run
   python src/jiutong.py
   
   # Or use system service (Linux)
   sudo systemctl start tron-collision
   ```

3. **View Logs**
   ```bash
   # View runtime logs
   tail -f src/logs.txt
   
   # View system service logs (Linux)
   sudo journalctl -u tron-collision -f
   ```

4. **Check Results**
   ```bash
   # View found addresses with assets
   cat src/non_zero_addresses.txt
   ```

### Web Monitoring Usage

Access `http://your-server-ip:5168` to use web interface:

- **📊 Dashboard**: View real-time running status and statistics
- **🎮 Control Panel**: Remotely start, stop, restart services
- **📝 Log Viewer**: Real-time program output logs
- **⚙️ System Monitoring**: CPU, memory, disk usage

### Advanced Configuration

#### Performance Tuning

Configurable parameters in `src/jiutong.py`:

```python
# API Configuration
TRON_API_URL = "https://api.trongrid.io/wallet/getaccount"  # TronGrid API endpoint
API_CALL_LIMIT = 10      # Maximum API calls per second (default 10, respects API limits)

# Logging Configuration
LOG_LIMIT = 2000         # Maximum entries retained in log queue
LOG_FILE = "logs.txt"    # Log file path
NON_ZERO_LOG_FILE = "non_zero_addresses.txt"  # Found addresses save file
```

> ⚠️ **Warning**: 
> - `API_CALL_LIMIT` should not exceed 10, or you may trigger TronGrid API rate limiting (403 error)
> - Increasing `LOG_LIMIT` will consume more memory

#### Multi-instance Running

```bash
# Create multiple running instances (improve efficiency)
for i in {2..4}; do
    sudo cp -r /opt/tron-collision /opt/tron-collision-$i
    sudo systemctl enable tron-collision-$i
    sudo systemctl start tron-collision-$i
done
```

#### Security Hardening

```bash
# Configure firewall
sudo firewall-cmd --permanent --add-port=5168/tcp
sudo firewall-cmd --reload

# Restrict access IP
sudo firewall-cmd --permanent --add-rich-rule="rule family='ipv4' source address='YOUR_IP' port port=5168 protocol=tcp accept"
```

## 📊 Technical Principles

### Cryptographic Process

1. **Private Key Generation**
   ```python
   private_key = os.urandom(32)  # 256-bit random number
   ```

2. **Public Key Derivation**
   ```python
   public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)
   ```

3. **Address Calculation**
   ```python
   # Keccak-256 hash
   keccak_hash = keccak.new(digest_bits=256)
   keccak_hash.update(public_key[1:])  # Remove 0x04 prefix
   
   # Add TRON prefix 0x41
   tron_address = b'\x41' + keccak_hash.digest()[-20:]
   
   # Base58Check encoding
   checksum = sha256(sha256(tron_address).digest()).digest()[:4]
   final_address = base58.b58encode(tron_address + checksum)
   ```

### Performance Optimization

- **Async IO**: Use aiohttp for concurrent API requests
- **Memory Management**: Rolling log queue, avoid memory leaks
- **Rate Limiting**: Smart request frequency control
- **Error Handling**: Comprehensive exception handling and retry mechanisms

### Probability Analysis

- **Total Private Key Space**: 2^256 ≈ 1.16 × 10^77
- **TRON Address Space**: 2^160 ≈ 1.46 × 10^48
- **Collision Probability**: Approximately 2^-256 ≈ 8.6 × 10^-78
- **Theoretical Computation Time**: Even at 10^12 attempts per second, would require about 10^58 years

## 🛠️ Troubleshooting

### Common Issues

#### 1. API 403 Error
```bash
# Solutions:
# 1. Change IP address (VPN/proxy)
# 2. Wait a few minutes and retry
# 3. Check network connection stability
```

#### 2. Service Won't Start
```bash
# Check service status
sudo systemctl status tron-collision

# View detailed errors
sudo journalctl -u tron-collision --no-pager

# Manual test program
sudo -u tron python3 /opt/tron-collision/jiutong.py
```

#### 3. Web Interface Inaccessible
```bash
# Check web service
sudo systemctl status tron-web-monitor

# Check port open
sudo ss -tlnp | grep 5168

# Check firewall
sudo firewall-cmd --list-ports
```

#### 4. Dependency Installation Failed
```bash
# Rocky Linux
sudo dnf install gcc python3-devel openssl-devel libffi-devel -y

# Ubuntu/Debian
sudo apt install build-essential python3-dev libssl-dev libffi-dev -y

# Force reinstallation
pip install --force-reinstall --no-cache-dir -r requirements.txt
```

### Log Analysis

```bash
# View program running status
grep "Address:" logs.txt | tail -10

# Check error information
grep "Error\|Exception" logs.txt

# Count queries
grep -c "Address:" logs.txt

# View API response time
grep "timeout\|slow" logs.txt
```

## 🔒 Security Recommendations

### Private Key Security

⚠️ **Important**: If addresses with assets are found, take security measures immediately:

1. **Immediate Backup**: Securely backup `non_zero_addresses.txt` file
2. **Multiple Backups**: Use encrypted storage devices for multiple backups
3. **Quick Transfer**: Transfer assets to secure wallets as soon as possible
4. **Access Control**: Strictly limit server access permissions

### System Security

```bash
# Regular system updates
sudo dnf update -y

# Configure firewall
sudo firewall-cmd --set-default-zone=drop
sudo firewall-cmd --permanent --zone=trusted --add-interface=lo

# Monitor suspicious access
sudo journalctl -u tron-collision | grep -i "suspicious\|error"
```

### Network Security

- Use VPN or dedicated network to access web interface
- Configure IP whitelist to restrict access
- Regularly change access ports
- Enable HTTPS (recommend using Let's Encrypt)

## 📈 Performance Monitoring

### System Monitoring

```bash
# CPU usage
top -p $(pgrep -f jiutong.py)

# Memory usage
ps aux | grep jiutong.py

# Network connections
ss -tlnp | grep python

# Disk IO
iotop -p $(pgrep -f jiutong.py)
```

### Business Monitoring

```bash
# Query speed statistics
echo "Total queries: $(grep -c 'Address:' logs.txt)"
echo "Runtime: $(systemctl show tron-collision -p ActiveEnterTimestamp)"

# Success rate monitoring
echo "API errors: $(grep -c '403\|timeout' logs.txt)"

# Discovery statistics
echo "Found addresses: $([ -f non_zero_addresses.txt ] && grep -c 'Private Key:' non_zero_addresses.txt || echo 0)"
```

## 🤝 Contributing Guide

Welcome to contribute code and improvement suggestions!

### Development Environment

```bash
# 1. Fork project and clone
git clone <your-fork>
cd Mnemonic_collision

# 2. Create development environment
python3 -m venv dev-env
source dev-env/bin/activate
pip install -r src/requirements.txt
pip install -r web-monitor/web-requirements.txt

# 3. Install development tools
pip install black flake8 pytest
```

### Code Standards

- Use Black for code formatting
- Follow PEP 8 coding standards
- Add necessary comments and docstrings
- Write unit tests

### Submission Process

```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Code formatting
black src/ web-monitor/

# 3. Run tests
pytest tests/

# 4. Commit changes
git commit -m "feat: add your feature"

# 5. Create Pull Request
```

## 📞 Support & Feedback

### Getting Help

- **📧 Email**: monika18dol@gmail.com
- **📖 Documentation**: Check project Wiki and Issues
- **🐛 Bug Report**: Use GitHub Issues
- **💡 Feature Requests**: Welcome to submit Enhancement requests

### Useful Links

- [Rocky Linux Deployment Guide](deployment/ROCKY_LINUX_QUICK_START.md)
- [Web Monitoring Usage Guide](web-monitor/WEB_MONITOR_GUIDE.md)
- [TronGrid API Documentation](https://developers.tron.network/reference)

## 💰 Support the Project

If this project has been helpful for your learning, donations are welcome:

**TRON Donation Address**: `TVYt4chs2VdxDRbPUVG2TRm6f7bG51ytWW`

## 📄 License

This project is released under the MIT License - see the [LICENSE](LICENSE) file for details.

**Disclaimer**: This project is for educational and research use only, please ensure compliance with local laws and regulations.

---

### 🔮 Future Plans

- [ ] Support for more blockchain networks (ETH, BSC, Polygon, etc.)
- [ ] Graphical desktop client
- [ ] Docker containerized deployment
- [ ] Distributed computing support
- [ ] Machine learning optimization algorithms
- [ ] Mobile monitoring app

---

**Reminder**: This tool is for educational and research purposes only. The probability of successful collision is extremely low, please be realistic!

**Good luck! 🍀**

*Last Updated: November 16, 2024, fully optimized for the latest project structure and features*
