#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TRON 私钥碰撞工具 - Web监控界面
"""

import os
import json
import time
import psutil
import subprocess
from datetime import datetime
from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tron_collision_monitor_2024'
app.config['JSON_AS_ASCII'] = False  # 支持中文JSON
socketio = SocketIO(app, cors_allowed_origins="*")

# 配置
TRON_PROJECT_PATH = "/opt/tron-collision"
LOG_FILE = os.path.join(TRON_PROJECT_PATH, "logs.txt")
NON_ZERO_FILE = os.path.join(TRON_PROJECT_PATH, "non_zero_addresses.txt")
SERVICE_NAME = "tron-collision"

class TronMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.total_checked = 0
        self.last_log_size = 0
        
    def get_service_status(self):
        """获取服务状态"""
        try:
            result = subprocess.run(['systemctl', 'is-active', SERVICE_NAME], 
                                  capture_output=True, text=True)
            is_active = result.stdout.strip() == 'active'
            
            result = subprocess.run(['systemctl', 'is-enabled', SERVICE_NAME], 
                                  capture_output=True, text=True)
            is_enabled = result.stdout.strip() == 'enabled'
            
            return {
                'status': 'running' if is_active else 'stopped',
                'enabled': is_enabled,
                'active': is_active
            }
        except Exception as e:
            return {
                'status': 'unknown',
                'enabled': False,
                'active': False,
                'error': str(e)
            }
    
    def get_system_info(self):
        """获取系统信息"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            
            # 磁盘使用率
            disk = psutil.disk_usage(TRON_PROJECT_PATH)
            
            # 网络统计
            network = psutil.net_io_counters()
            
            return {
                'cpu_percent': cpu_percent,
                'memory': {
                    'total': memory.total,
                    'used': memory.used,
                    'percent': memory.percent
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'percent': (disk.used / disk.total) * 100
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_process_info(self):
        """获取进程信息"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_info', 'cpu_percent']):
                if 'tron.py' in str(proc.info['cmdline']):
                    return {
                        'pid': proc.info['pid'],
                        'memory_mb': proc.info['memory_info'].rss / 1024 / 1024,
                        'cpu_percent': proc.info['cpu_percent'],
                        'running': True
                    }
            return {'running': False}
        except Exception as e:
            return {'running': False, 'error': str(e)}
    
    def get_logs(self, lines=50):
        """获取日志"""
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    logs = f.readlines()
                    return logs[-lines:] if len(logs) > lines else logs
            return []
        except Exception as e:
            return [f"读取日志错误: {str(e)}"]
    
    def get_statistics(self):
        """获取统计信息"""
        try:
            # 从日志文件计算总检查数
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    logs = f.readlines()
                    self.total_checked = len([line for line in logs if 'Address:' in line])
            
            # 检查是否有发现（安全模式：不传输私钥）
            found_addresses = []
            if os.path.exists(NON_ZERO_FILE):
                with open(NON_ZERO_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 简单解析发现的地址数量
                    addresses = content.split('Private Key:')[1:] if content else []
                    for i, addr_block in enumerate(addresses):
                        lines = addr_block.strip().split('\n')
                        if len(lines) >= 3:
                            found_addresses.append({
                                # 安全：不传输私钥！私钥只保存在服务器文件中
                                'id': i + 1,  # 发现序号
                                'address': lines[1].replace('Address:', '').strip(),
                                'balance': lines[2].replace('TRX Balance:', '').strip(),
                                'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'private_key_saved': True  # 标记私钥已安全保存
                            })
            
            # 运行时间
            runtime = time.time() - self.start_time
            
            # 计算速度
            speed = self.total_checked / runtime if runtime > 0 else 0
            
            return {
                'total_checked': self.total_checked,
                'found_count': len(found_addresses),
                'found_addresses': found_addresses,
                'runtime_seconds': runtime,
                'speed_per_second': speed,
                'probability': 0.0000000000000000000000000000000000000000000000000000000000000000000376
            }
        except Exception as e:
            return {
                'total_checked': self.total_checked,
                'found_count': 0,
                'found_addresses': [],
                'runtime_seconds': 0,
                'speed_per_second': 0,
                'error': str(e)
            }

monitor = TronMonitor()

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': 'API端点不存在', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({'error': '服务器内部错误', 'message': str(error)}), 500

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/test')
def api_test():
    """API连接测试"""
    return jsonify({
        'status': 'success',
        'message': 'Web监控API工作正常',
        'timestamp': datetime.now().isoformat(),
        'port': 5168
    })

@app.route('/api/status')
def api_status():
    """获取所有状态信息"""
    try:
        return jsonify({
            'service': monitor.get_service_status(),
            'system': monitor.get_system_info(),
            'process': monitor.get_process_info(),
            'statistics': monitor.get_statistics(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': '获取状态信息失败',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/logs')
def api_logs():
    """获取日志"""
    try:
        lines = int(request.args.get('lines', 50))
        return jsonify({
            'logs': monitor.get_logs(lines),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': '获取日志失败',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/control/<action>')
def api_control(action):
    """服务控制"""
    try:
        if action == 'start':
            result = subprocess.run(['/usr/bin/sudo', 'systemctl', 'start', SERVICE_NAME], 
                                  capture_output=True, text=True)
        elif action == 'stop':
            result = subprocess.run(['/usr/bin/sudo', 'systemctl', 'stop', SERVICE_NAME], 
                                  capture_output=True, text=True)
        elif action == 'restart':
            result = subprocess.run(['/usr/bin/sudo', 'systemctl', 'restart', SERVICE_NAME], 
                                  capture_output=True, text=True)
        else:
            return jsonify({'success': False, 'message': '无效的操作'})
        
        success = result.returncode == 0
        return jsonify({
            'success': success,
            'message': result.stdout if success else result.stderr
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@socketio.on('connect')
def handle_connect():
    """WebSocket连接"""
    print('Client connected')
    emit('status', monitor.get_service_status())

@socketio.on('request_update')
def handle_request_update():
    """客户端请求更新"""
    emit('status_update', {
        'service': monitor.get_service_status(),
        'system': monitor.get_system_info(),
        'process': monitor.get_process_info(),
        'statistics': monitor.get_statistics(),
        'timestamp': datetime.now().isoformat()
    })

def background_task():
    """后台任务：定时推送更新"""
    while True:
        time.sleep(5)  # 每5秒更新一次
        socketio.emit('status_update', {
            'service': monitor.get_service_status(),
            'system': monitor.get_system_info(),
            'process': monitor.get_process_info(),
            'statistics': monitor.get_statistics(),
            'timestamp': datetime.now().isoformat()
        })

if __name__ == '__main__':
    # 启动后台任务
    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()
    
    # 启动Web服务器
    print("🚀 TRON碰撞监控服务启动中...")
    print("📊 访问地址: http://your-server-ip:5168")
    print("🔧 确保防火墙已开放5168端口")
    
    socketio.run(app, host='0.0.0.0', port=5168, debug=False, allow_unsafe_werkzeug=True)
