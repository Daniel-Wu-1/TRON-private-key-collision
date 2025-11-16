#!/bin/bash

# TRON 私钥碰撞工具 - Rocky Linux 9.0 极简版安装脚本

set -e

echo "🚀 开始极简安装 TRON 私钥碰撞工具..."

# 检查操作系统
if ! grep -q "Rocky Linux" /etc/os-release 2>/dev/null; then
    echo "⚠️  警告：此脚本专为 Rocky Linux 设计"
    read -p "是否继续？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查是否为root用户
if [[ $EUID -eq 0 ]]; then
   echo "❌ 请不要使用root用户运行此脚本"
   exit 1
fi

# 询问是否使用清华源
echo "🌐 选择下载源："
echo "  1) 使用清华源（推荐：国内服务器）"
echo "  2) 使用默认源（海外服务器）"
echo "  3) 强制使用清华源（跳过连接测试）"
read -p "请选择 [1/2/3，默认1]: " -n 1 -r
echo
USE_TSINGHUA_MIRROR=${REPLY:-1}

if [[ $USE_TSINGHUA_MIRROR == "1" || $USE_TSINGHUA_MIRROR == "3" ]]; then
    # 配置清华源（国内服务器加速）
    if [[ $USE_TSINGHUA_MIRROR == "3" ]]; then
        echo "🚀 强制配置清华源（跳过连接测试）..."
    else
        echo "🇨🇳 配置清华源，加速下载..."
    fi
    
    # 备份原有的repo文件（如果还没备份过）
    if [ ! -d "/etc/yum.repos.d.backup.$(date +%Y%m%d)" ]; then
        sudo cp -r /etc/yum.repos.d /etc/yum.repos.d.backup.$(date +%Y%m%d) 2>/dev/null || true
        echo "📦 已备份原有仓库配置"
    fi

    # 清理可能存在的重复配置
    echo "🧹 清理旧的仓库配置..."
    sudo rm -f /etc/yum.repos.d/Rocky-BaseOS.repo
    sudo rm -f /etc/yum.repos.d/Rocky-AppStream.repo  
    sudo rm -f /etc/yum.repos.d/Rocky-Extras.repo

    # 获取系统版本
    ROCKY_VERSION=$(grep -oP 'VERSION_ID="\K[^"]+' /etc/os-release)
    echo "📋 检测到 Rocky Linux 版本: $ROCKY_VERSION"

    # 配置Rocky Linux清华源 - 使用多个备选URL
    echo "📝 配置清华源仓库文件..."
    sudo tee /etc/yum.repos.d/Rocky-Tsinghua.repo > /dev/null <<EOF
[baseos-tsinghua]
name=Rocky Linux \$releasever - BaseOS (Tsinghua Mirror)
baseurl=https://mirrors.tuna.tsinghua.edu.cn/rocky/\$releasever/BaseOS/\$basearch/os/
        http://mirrors.tuna.tsinghua.edu.cn/rocky/\$releasever/BaseOS/\$basearch/os/
        https://mirror.nju.edu.cn/rocky/\$releasever/BaseOS/\$basearch/os/
gpgcheck=1
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rockyofficial
priority=1
skip_if_unavailable=1

[appstream-tsinghua]
name=Rocky Linux \$releasever - AppStream (Tsinghua Mirror)
baseurl=https://mirrors.tuna.tsinghua.edu.cn/rocky/\$releasever/AppStream/\$basearch/os/
        http://mirrors.tuna.tsinghua.edu.cn/rocky/\$releasever/AppStream/\$basearch/os/
        https://mirror.nju.edu.cn/rocky/\$releasever/AppStream/\$basearch/os/
gpgcheck=1
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rockyofficial
priority=1
skip_if_unavailable=1

[extras-tsinghua]
name=Rocky Linux \$releasever - Extras (Tsinghua Mirror)
baseurl=https://mirrors.tuna.tsinghua.edu.cn/rocky/\$releasever/extras/\$basearch/os/
        http://mirrors.tuna.tsinghua.edu.cn/rocky/\$releasever/extras/\$basearch/os/
        https://mirror.nju.edu.cn/rocky/\$releasever/extras/\$basearch/os/
gpgcheck=1
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rockyofficial
priority=1
skip_if_unavailable=1
EOF

    # 禁用原有的Rocky仓库（避免冲突）
    echo "🔒 禁用原有仓库配置..."
    sudo dnf config-manager --disable baseos appstream extras 2>/dev/null || true
    
    # 清理缓存并重建
    echo "🔄 清理缓存并重建..."
    sudo dnf clean all
    
    # 根据选择决定是否测试连接
    if [[ $USE_TSINGHUA_MIRROR == "3" ]]; then
        # 强制模式：跳过连接测试
        echo "🚀 强制模式：跳过连接测试，直接使用清华源"
        echo "✅ 清华源配置完成（强制模式）"
    else
        # 普通模式：测试连接
        echo "🔍 测试清华源连接..."
        if sudo timeout 60 dnf makecache --refresh 2>/dev/null; then
            echo "✅ 清华源配置成功"
        else
            echo "⚠️  清华源连接失败，尝试诊断问题..."
            
            # 详细诊断
            echo "🔍 连接诊断："
            echo "   1. 测试基础网络连接..."
            if ping -c 2 mirrors.tuna.tsinghua.edu.cn &>/dev/null; then
                echo "   ✅ 网络连接正常"
            else
                echo "   ❌ 网络连接失败"
            fi
            
            echo "   2. 测试DNS解析..."
            if nslookup mirrors.tuna.tsinghua.edu.cn &>/dev/null; then
                echo "   ✅ DNS解析正常"
            else
                echo "   ❌ DNS解析失败"
            fi
            
            echo ""
            echo "💡 建议解决方案："
            echo "   1. 检查防火墙设置"
            echo "   2. 稍后重新尝试"
            echo "   3. 使用强制模式: 重新运行脚本选择选项 3"
            echo ""
            
            read -p "🤔 是否要回滚到默认源？(y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "⚠️  回滚到默认源..."
                # 回滚操作
                sudo rm -f /etc/yum.repos.d/Rocky-Tsinghua.repo
                sudo dnf config-manager --enable baseos appstream extras 2>/dev/null || true
                sudo dnf clean all
                sudo dnf makecache
                USE_TSINGHUA_MIRROR="2"  # 标记为使用默认源
                echo "🌐 已回滚到默认源"
            else
                echo "🚀 继续使用清华源（强制模式）"
                echo "✅ 清华源配置完成（用户选择继续）"
            fi
        fi
    fi
else
    echo "🌐 使用默认源"
    # 确保有基本的仓库配置
    sudo dnf clean all
    sudo dnf makecache
fi

# 只安装最必要的包（先尝试不编译）
echo "📦 安装 Python 基础环境..."
sudo dnf install python3 python3-pip -y

# 智能检测项目根目录和文件路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT=""
SRC_PATH=""

# 检查是否在deployment目录运行脚本
if [[ "$(basename "$SCRIPT_DIR")" == "deployment" ]]; then
    # 脚本在deployment目录，项目根目录在上一级
    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
    SRC_PATH="$PROJECT_ROOT/src"
    echo "📍 检测到从deployment目录运行脚本"
else
    # 脚本可能被复制到其他位置，尝试当前目录
    PROJECT_ROOT="$(pwd)"
    SRC_PATH="$PROJECT_ROOT/src"
    echo "📍 检测到从当前目录运行脚本"
fi

echo "📂 项目根目录: $PROJECT_ROOT"
echo "📂 源码目录: $SRC_PATH"

# 检查必要文件
if [ ! -f "$SRC_PATH/tron.py" ] || [ ! -f "$SRC_PATH/requirements.txt" ]; then
    echo "❌ 缺少必要文件，请检查以下位置："
    echo "   需要: $SRC_PATH/tron.py"
    echo "   需要: $SRC_PATH/requirements.txt"
    echo ""
    echo "💡 运行方式："
    echo "   方式1: cd /path/to/Mnemonic_collision && ./deployment/install-rocky-minimal.sh"
    echo "   方式2: cd /path/to/Mnemonic_collision/deployment && ./install-rocky-minimal.sh"
    exit 1
fi

echo "✅ 找到必要文件"

# 创建项目目录
echo "📁 创建项目目录..."
sudo mkdir -p /opt/tron-collision
sudo cp "$SRC_PATH/tron.py" "$SRC_PATH/requirements.txt" /opt/tron-collision/

# 创建虚拟环境
echo "🐍 创建虚拟环境..."
cd /opt/tron-collision
sudo python3 -m venv venv

# 配置pip源
if [[ $USE_TSINGHUA_MIRROR == "1" || $USE_TSINGHUA_MIRROR == "3" ]]; then
    echo "🐍 配置 pip 清华源..."
    # 为tron用户创建pip配置目录（稍后会用到）
    sudo mkdir -p /home/tron/.pip
    sudo tee /home/tron/.pip/pip.conf > /dev/null <<EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 120
EOF
    PIP_INDEX="-i https://pypi.tuna.tsinghua.edu.cn/simple"
    echo "✅ pip清华源配置完成"
else
    echo "🐍 使用 pip 默认源..."
    PIP_INDEX=""
fi

# 升级pip
sudo /opt/tron-collision/venv/bin/pip install --upgrade pip $PIP_INDEX

# 尝试安装依赖（如果失败再安装编译工具）
echo "📚 安装 Python 依赖..."
if ! sudo /opt/tron-collision/venv/bin/pip install -r requirements.txt --only-binary=all $PIP_INDEX 2>/dev/null; then
    echo "⚠️  预编译包不可用，安装编译工具..."
    sudo dnf install gcc python3-devel openssl-devel libffi-devel -y
    sudo /opt/tron-collision/venv/bin/pip install -r requirements.txt $PIP_INDEX
fi

# 创建系统用户和服务（保持原有逻辑）
echo "👤 创建系统用户..."
if ! id "tron" &>/dev/null; then
    sudo useradd -r -s /bin/false -d /opt/tron-collision tron
fi

sudo chown -R tron:tron /opt/tron-collision

# 设置pip配置文件权限（如果使用了清华源）
if [[ $USE_TSINGHUA_MIRROR == "1" || $USE_TSINGHUA_MIRROR == "3" ]]; then
    sudo chown -R tron:tron /home/tron/.pip 2>/dev/null || true
fi

# 创建简化的服务
echo "⚙️ 创建系统服务..."
sudo tee /etc/systemd/system/tron-collision.service > /dev/null <<EOF
[Unit]
Description=TRON Private Key Collision Detection
After=network.target

[Service]
Type=simple
User=tron
Group=tron
WorkingDirectory=/opt/tron-collision
ExecStart=/opt/tron-collision/venv/bin/python tron.py
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable tron-collision

echo ""
echo "🎉 极简安装完成！"
echo ""
if [[ $USE_TSINGHUA_MIRROR == "1" || $USE_TSINGHUA_MIRROR == "3" ]]; then
    if [[ $USE_TSINGHUA_MIRROR == "3" ]]; then
        echo "🚀 已强制配置清华源（跳过连接测试）"
    else
        echo "📦 已配置清华源（适合国内服务器）"
    fi
    echo "   - 系统包源：https://mirrors.tuna.tsinghua.edu.cn/rocky/"
    echo "   - Python包源：https://pypi.tuna.tsinghua.edu.cn/simple"
    echo "   - 备选镜像：南京大学镜像站 + HTTP备选"
    echo ""
fi
echo "🚀 服务管理："
echo "   启动服务: sudo systemctl start tron-collision"
echo "   查看状态: sudo systemctl status tron-collision"
echo "   查看日志: sudo journalctl -u tron-collision -f"
