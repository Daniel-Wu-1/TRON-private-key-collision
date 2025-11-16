# 🔐 TRON 私钥碰撞工具

- 一个集成了核心引擎、Web监控界面和自动化部署的TRON区块链私钥碰撞研究工具
- 通过随机生成私钥并检查对应地址的资产余额来探索区块链密码学原理
- 反正占用不大，没事可以挂着玩玩

**🌐 语言**: **中文** | [English](README_EN.md)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey.svg)

## ⚠️ 免责声明

**本工具仅供学习和研究用途，不建议用于任何非法或恶意活动。**

- 私钥碰撞的成功概率极低（约为 2^-256）
- 即使使用全世界所有的超级计算机，在宇宙毁灭之前也几乎不可能成功碰撞出有效私钥
- 本工具主要用于教育目的和区块链密码学研究
- 请遵守当地法律法规，不要将此工具用于非法用途

**祝你好运！但请理性对待！**

## 🏗️ 项目架构

```
Mnemonic_collision/
├── 📦 src/                           # 核心引擎
│   ├── tron.py                    # 主碰撞程序（异步高性能版本）
│   ├── test_api.py                   # TronGrid API测试工具
│   ├── requirements.txt              # Python依赖包
│   ├── logs.txt                      # 运行日志（自动生成）
│   └── non_zero_addresses.txt        # 发现的有资产地址（碰撞成功时生成）
├── 🌐 web-monitor/                   # Web监控界面
│   ├── web_monitor.py                # Flask监控服务（含WebSocket）
│   ├── templates/                    # HTML模板
│   │   └── index.html                # 响应式监控界面
│   ├── static/                       # 静态资源（CSS/JS）
│   ├── install-web-monitor.sh        # Web监控一键安装脚本
│   ├── web-requirements.txt          # Web服务依赖
│   ├── fix-sudo-permissions.sh       # 权限修复脚本
│   └── WEB_MONITOR_GUIDE.md          # Web监控使用指南
├── 🚀 deployment/                    # 自动化部署
│   ├── install-rocky-minimal.sh      # Rocky Linux极简安装脚本
│   └── ROCKY_LINUX_QUICK_START.md    # 部署快速指南
├── 💼 TRON私钥碰撞/                   # Windows独立版本（可选）
│   ├── tron.py                    # 独立程序副本
│   ├── tron.spec                  # PyInstaller打包配置
│   └── dist/                         # 编译后的可执行文件
│       └── tron.exe               # Windows可执行程序
├── README.md                         # 项目文档（中文）
└── README_EN.md                      # 项目文档（英文）
```

## 🚀 功能特性

### 核心引擎功能
- **🔐 私钥生成**: 使用安全的随机数生成器 (`os.urandom(32)`) 
- **📍 地址计算**: 完整的TRON地址生成链路（secp256k1 → Keccak-256 → Base58Check）
- **💰 多资产支持**: 检测TRX、TRC10和TRC20代币（包括USDT等）
- **⚡ 异步查询**: 基于aiohttp的高性能异步API请求
- **📊 智能日志**: 滚动日志系统，自动保留最新2000条记录
- **🎯 自动保存**: 发现有资产地址时自动保存完整信息
- **⏱️ 速率控制**: 遵守TronGrid API限制，每秒最多10次查询

### Web监控界面
- **📈 实时监控**: 服务状态、系统资源、运行统计
- **🎮 远程控制**: 启动、停止、重启碰撞服务
- **📝 实时日志**: WebSocket实时日志流
- **🔒 安全模式**: 私钥信息不在网络传输，仅保存在服务器
- **📊 性能监控**: CPU、内存、磁盘使用情况
- **🏆 发现展示**: 有资产地址发现时的醒目提醒

### 部署自动化
- **🐧 Rocky Linux优化**: 专为Rocky Linux 9.0优化的安装脚本
- **⚡ 极简安装**: 最小化依赖，仅安装必要组件
- **🇨🇳 国内优化**: 支持清华大学镜像源，显著提升下载速度
- **🔧 服务管理**: systemd服务集成，支持自动重启
- **📦 一键部署**: 从环境配置到服务启动的全自动化流程

## 📋 系统要求

### 最低要求
- **操作系统**: Linux (推荐Rocky Linux 9.0) / Windows 10+
- **Python**: 3.7或更高版本
- **内存**: 512MB可用内存
- **网络**: 稳定的互联网连接（访问TronGrid API）
- **磁盘**: 1GB可用空间

### 推荐配置
- **CPU**: 多核处理器（支持多实例并行）
- **内存**: 2GB以上
- **网络**: 高速稳定连接
- **系统**: 专用Linux服务器

## 🔧 安装部署

### 方法一：Rocky Linux一键部署（推荐）

适用于Rocky Linux 9.0服务器，提供完整的自动化部署：

```bash
# 1. 克隆项目
git clone <repository-url>
cd Mnemonic_collision

# 2. 运行部署脚本
chmod +x deployment/install-rocky-minimal.sh
./deployment/install-rocky-minimal.sh

# 3. 启动服务
sudo systemctl start tron-collision

# 4. 可选：安装Web监控
cd web-monitor
chmod +x install-web-monitor.sh
./install-web-monitor.sh
sudo systemctl start tron-web-monitor
```

**部署脚本特性**：
- 🇨🇳 **智能源选择**: 自动检测并配置清华大学镜像源
- ⚡ **极简安装**: 仅安装必要的6个系统包
- 🔒 **安全配置**: 创建专用用户，配置适当权限
- 🔄 **自动重启**: 系统级服务管理，支持故障自动恢复

### 方法二：手动安装

#### Windows 用户

**方式1：Python运行（推荐）**
```powershell
# 1. 安装Python依赖
pip install -r src/requirements.txt

# 2. 运行程序
cd src
python tron.py
```

**方式2：使用编译版本（如果已有）**
```powershell
# 直接运行编译好的可执行文件
cd TRON私钥碰撞\dist
tron.exe
```

> 💡 **提示**: 如需自己编译exe，参考 `TRON私钥碰撞/tron.spec` 使用PyInstaller打包

#### Linux 用户

```bash
# 1. 安装系统依赖
sudo apt update && sudo apt install -y python3 python3-pip python3-venv

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装Python依赖
pip install -r src/requirements.txt

# 4. 运行程序
cd src
python tron.py
```

### 方法三：Docker部署（即将支持）

```bash
# 构建镜像
docker build -t tron-collision .

# 运行容器
docker run -d --name tron-collision \
  -v ./logs:/app/logs \
  -v ./data:/app/data \
  tron-collision
```

## 🎯 使用指南

### 基础使用

1. **测试API连接（首次运行前推荐）**
   ```bash
   # 测试TronGrid API是否可访问
   cd src
   python test_api.py
   ```

2. **启动程序**
   ```bash
   # 直接运行
   python src/tron.py
   
   # 或使用系统服务（Linux）
   sudo systemctl start tron-collision
   ```

3. **查看日志**
   ```bash
   # 查看运行日志
   tail -f src/logs.txt
   
   # 查看系统服务日志（Linux）
   sudo journalctl -u tron-collision -f
   ```

4. **检查结果**
   ```bash
   # 查看发现的有资产地址
   cat src/non_zero_addresses.txt
   ```

### Web监控使用

访问 `http://your-server-ip:5168` 使用Web界面：

- **📊 仪表板**: 查看实时运行状态和统计信息
- **🎮 控制面板**: 远程启动、停止、重启服务
- **📝 日志查看**: 实时查看程序输出日志
- **⚙️ 系统监控**: CPU、内存、磁盘使用情况

### 高级配置

#### 性能调优

在 `src/tron.py` 中可调整的配置项：

```python
# API配置
TRON_API_URL = "https://api.trongrid.io/wallet/getaccount"  # TronGrid API端点
API_CALL_LIMIT = 10      # 每秒最大API调用次数（默认10，遵守API限制）

# 日志配置
LOG_LIMIT = 2000         # 日志队列保留的最大条目数
LOG_FILE = "logs.txt"    # 日志文件路径
NON_ZERO_LOG_FILE = "non_zero_addresses.txt"  # 发现地址保存文件
```

> ⚠️ **警告**: 
> - `API_CALL_LIMIT` 不建议超过10，否则可能触发TronGrid API限流（403错误）
> - 增大 `LOG_LIMIT` 会占用更多内存

#### 多实例运行

```bash
# 创建多个运行实例（提高效率）
for i in {2..4}; do
    sudo cp -r /opt/tron-collision /opt/tron-collision-$i
    sudo systemctl enable tron-collision-$i
    sudo systemctl start tron-collision-$i
done
```

#### 安全加固

```bash
# 配置防火墙
sudo firewall-cmd --permanent --add-port=5168/tcp
sudo firewall-cmd --reload

# 限制访问IP
sudo firewall-cmd --permanent --add-rich-rule="rule family='ipv4' source address='YOUR_IP' port port=5168 protocol=tcp accept"
```

## 📊 技术原理

### 密码学流程

1. **私钥生成**
   ```python
   private_key = os.urandom(32)  # 256位随机数
   ```

2. **公钥推导**
   ```python
   public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)
   ```

3. **地址计算**
   ```python
   # Keccak-256哈希
   keccak_hash = keccak.new(digest_bits=256)
   keccak_hash.update(public_key[1:])  # 去掉0x04前缀
   
   # 添加TRON前缀0x41
   tron_address = b'\x41' + keccak_hash.digest()[-20:]
   
   # Base58Check编码
   checksum = sha256(sha256(tron_address).digest()).digest()[:4]
   final_address = base58.b58encode(tron_address + checksum)
   ```

### 性能优化

- **异步IO**: 使用aiohttp进行并发API请求
- **内存管理**: 滚动日志队列，避免内存泄漏
- **速率限制**: 智能请求频率控制
- **错误处理**: 完善的异常处理和重试机制

### 概率分析

- **总私钥空间**: 2^256 ≈ 1.16 × 10^77
- **TRON地址空间**: 2^160 ≈ 1.46 × 10^48  
- **碰撞概率**: 约 2^-256 ≈ 8.6 × 10^-78
- **理论计算时间**: 即使每秒10^12次尝试，也需要约10^58年

## 🛠️ 故障排除

### 常见问题

#### 1. API 403错误
```bash
# 解决方案：
# 1. 更换IP地址（VPN/代理）
# 2. 等待几分钟后重试
# 3. 检查网络连接稳定性
```

#### 2. 服务无法启动
```bash
# 检查服务状态
sudo systemctl status tron-collision

# 查看详细错误
sudo journalctl -u tron-collision --no-pager

# 手动测试程序
sudo -u tron python3 /opt/tron-collision/tron.py
```

#### 3. Web界面无法访问
```bash
# 检查Web服务
sudo systemctl status tron-web-monitor

# 检查端口开放
sudo ss -tlnp | grep 5168

# 检查防火墙
sudo firewall-cmd --list-ports
```

#### 4. 依赖安装失败
```bash
# Rocky Linux
sudo dnf install gcc python3-devel openssl-devel libffi-devel -y

# Ubuntu/Debian  
sudo apt install build-essential python3-dev libssl-dev libffi-dev -y

# 强制重新安装
pip install --force-reinstall --no-cache-dir -r requirements.txt
```

### 日志分析

```bash
# 查看程序运行状态
grep "Address:" logs.txt | tail -10

# 检查错误信息
grep "Error\|Exception" logs.txt

# 统计查询次数
grep -c "Address:" logs.txt

# 查看API响应时间
grep "timeout\|slow" logs.txt
```

## 🔒 安全建议

### 私钥安全

⚠️ **重要**: 如果发现有资产的地址，请立即采取安全措施：

1. **立即备份**: 安全备份 `non_zero_addresses.txt` 文件
2. **多重备份**: 使用加密存储设备进行多重备份
3. **快速转移**: 尽快将资产转移到安全的钱包
4. **访问控制**: 严格限制服务器访问权限

### 系统安全

```bash
# 定期更新系统
sudo dnf update -y

# 配置防火墙
sudo firewall-cmd --set-default-zone=drop
sudo firewall-cmd --permanent --zone=trusted --add-interface=lo

# 监控异常访问
sudo journalctl -u tron-collision | grep -i "suspicious\|error"
```

### 网络安全

- 使用VPN或专用网络访问Web界面
- 配置IP白名单限制访问
- 定期更改访问端口
- 启用HTTPS（推荐使用Let's Encrypt）

## 📈 性能监控

### 系统监控

```bash
# CPU使用率
top -p $(pgrep -f tron.py)

# 内存使用
ps aux | grep tron.py

# 网络连接
ss -tlnp | grep python

# 磁盘IO
iotop -p $(pgrep -f tron.py)
```

### 业务监控

```bash
# 查询速度统计
echo "Total queries: $(grep -c 'Address:' logs.txt)"
echo "Runtime: $(systemctl show tron-collision -p ActiveEnterTimestamp)"

# 成功率监控
echo "API errors: $(grep -c '403\|timeout' logs.txt)"

# 发现统计  
echo "Found addresses: $([ -f non_zero_addresses.txt ] && grep -c 'Private Key:' non_zero_addresses.txt || echo 0)"
```

## 🤝 贡献指南

欢迎贡献代码和提出改进建议！

### 开发环境

```bash
# 1. Fork项目并克隆
git clone <your-fork>
cd Mnemonic_collision

# 2. 创建开发环境
python3 -m venv dev-env
source dev-env/bin/activate
pip install -r src/requirements.txt
pip install -r web-monitor/web-requirements.txt

# 3. 安装开发工具
pip install black flake8 pytest
```

### 代码规范

- 使用Black进行代码格式化
- 遵循PEP 8编码规范
- 添加必要的注释和文档字符串
- 编写单元测试

### 提交流程

```bash
# 1. 创建功能分支
git checkout -b feature/your-feature

# 2. 代码格式化
black src/ web-monitor/

# 3. 运行测试
pytest tests/

# 4. 提交更改
git commit -m "feat: add your feature"

# 5. 创建Pull Request
```

## 📞 支持与反馈

### 获取帮助

- **📧 邮箱**: monika18dol@gmail.com
- **📖 文档**: 查看项目Wiki和Issues
- **🐛 Bug报告**: 使用GitHub Issues
- **💡 功能建议**: 欢迎提交Enhancement请求

### 常用链接

- [Rocky Linux部署指南](deployment/ROCKY_LINUX_QUICK_START.md)
- [Web监控使用指南](web-monitor/WEB_MONITOR_GUIDE.md)
- [TronGrid API文档](https://developers.tron.network/reference)

## 💰 支持项目

如果这个项目对您有帮助，欢迎打赏支持：

**TRON打赏地址**: `TVYt4chs2VdxDRbPUVG2TRm6f7bG51ytWW`

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

**免责声明**: 本项目仅供学习和研究使用，请确保遵守当地法律法规。

---


**再次提醒**: 此工具仅供教育和研究目的，成功碰撞的概率极低，请理性对待！

**祝你好运！🍀**

*最后更新: 2024年11月16日，已针对最新的项目结构和功能进行全面优化*
