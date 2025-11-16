import os
import asyncio
import aiohttp
import time
from coincurve import PublicKey
from Crypto.Hash import keccak
from hashlib import sha256
import base58
from datetime import datetime
from collections import deque

# TRON API 端点
TRON_API_URL = "https://api.trongrid.io/wallet/getaccount"
API_CALL_LIMIT = 10  # 每秒最大 API 调用次数（默认限制）
LOG_LIMIT = 2000  # 日志文件保留的最大条目数

# 日志文件路径
LOG_FILE = os.path.join(os.getcwd(), "logs.txt")
NON_ZERO_LOG_FILE = os.path.join(os.getcwd(), "non_zero_addresses.txt")

# 全局日志队列（保留最新的日志）
log_queue = deque(maxlen=LOG_LIMIT)

# 随机生成私钥
def generate_private_key():
    return os.urandom(32)

# 从私钥生成 TRON 地址（Base58Check 格式）
def private_key_to_tron_address(private_key):
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)
    public_key_without_prefix = public_key[1:]  # 去掉前缀

    # 对公钥的后 64 字节进行 Keccak-256 哈希
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_without_prefix)
    address_hash = keccak_hash.digest()

    # 添加前缀 0x41（TRON 主网地址）
    tron_address_hex = b'\x41' + address_hash[-20:]

    # 生成 Base58Check 编码
    checksum = sha256(sha256(tron_address_hex).digest()).digest()[:4]
    base58_address = base58.b58encode(tron_address_hex + checksum)
    return base58_address.decode(), tron_address_hex.hex()

# 将 Base58 地址转换为十六进制地址
def base58_to_hex_address(base58_address):
    decoded = base58.b58decode(base58_address)
    return decoded[:-4].hex()  # 去掉最后 4 字节的校验和

# 查询地址资产（异步）
async def query_tron_address_balance(session, hex_address):
    payload = {"address": hex_address, "visible": False}
    headers = {"Content-Type": "application/json"}
    try:
        async with session.post(TRON_API_URL, json=payload, headers=headers, timeout=10) as response:
            if response.status == 200:
                data = await response.json()
                balance = data.get("balance", 0) / 1e6  # TRX 余额
                tokens = data.get("assetV2", [])  # TRC10 代币
                trc20_tokens = data.get("trc20", {})  # TRC20 代币
                return balance, tokens, trc20_tokens
            elif response.status == 403:
                raise Exception("Rate limit exceeded")
            else:
                return 0, [], {}
    except Exception as e:
        return 0, [], {}

# 写入日志
def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    log_queue.append(log_message)
    with open(LOG_FILE, "w") as file:
        file.write("\n".join(log_queue))
    print(log_message)

# 保存非零资产地址及私钥信息
def save_non_zero_address(private_key, address, trx_balance, tokens, trc20_tokens):
    with open(NON_ZERO_LOG_FILE, "a") as file:
        file.write(f"Private Key: {private_key.hex()}\n")
        file.write(f"Address: {address}\n")
        file.write(f"TRX Balance: {trx_balance} TRX\n")
        if tokens:
            file.write(f"TRC10 Tokens: {tokens}\n")
        if trc20_tokens:
            file.write(f"TRC20 Tokens: {trc20_tokens}\n")
        file.write("\n")

# 主任务：生成私钥、地址并查询
async def process_key(index, session):
    private_key = generate_private_key()
    tron_address, hex_address = private_key_to_tron_address(private_key)
    trx_balance, tokens, trc20_tokens = await query_tron_address_balance(session, hex_address)

    # 实时显示查询信息
    write_log(f"[{index}] Address: {tron_address}, Private Key: {private_key.hex()}, TRX: {trx_balance}")

    # 保存非零资产信息
    if trx_balance > 0 or tokens or trc20_tokens:
        write_log(f"[{index}] Non-zero address found: {tron_address}")
        save_non_zero_address(private_key, tron_address, trx_balance, tokens, trc20_tokens)

# 主函数
async def main():
    global API_CALL_LIMIT
    tasks = []
    index = 0
    async with aiohttp.ClientSession() as session:
        while True:
            start_time = time.time()
            for _ in range(API_CALL_LIMIT):
                tasks.append(process_key(index, session))
                index += 1
            await asyncio.gather(*tasks)
            tasks.clear()
            elapsed_time = time.time() - start_time
            if elapsed_time < 1:  # 每秒执行一轮
                await asyncio.sleep(1 - elapsed_time)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已停止。")