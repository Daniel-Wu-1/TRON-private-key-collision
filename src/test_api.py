import requests
import json

# 测试 TRON API
url = "https://api.trongrid.io/wallet/getaccount"

# 测试1: 使用十六进制地址
hex_address = "41928c9af0651632157ef27a2cf17ca72c575a4d21"
payload1 = {"address": hex_address, "visible": False}

print("=" * 50)
print("测试1: 十六进制地址 + visible=False")
print(f"请求: {json.dumps(payload1, indent=2)}")
response1 = requests.post(url, json=payload1)
print(f"状态码: {response1.status_code}")
print(f"响应: {json.dumps(response1.json(), indent=2, ensure_ascii=False)}")

print("\n" + "=" * 50)
print("测试2: Base58地址 + visible=True")
base58_address = "TMuA6YqfCeX8EhbfYEg5y7S4DqzSJireY9"
payload2 = {"address": base58_address, "visible": True}
print(f"请求: {json.dumps(payload2, indent=2)}")
response2 = requests.post(url, json=payload2)
print(f"状态码: {response2.status_code}")
print(f"响应: {json.dumps(response2.json(), indent=2, ensure_ascii=False)}")

print("\n" + "=" * 50)
print("测试3: 空地址（不存在的地址）")
empty_hex = "4100000000000000000000000000000000000000"
payload3 = {"address": empty_hex, "visible": False}
print(f"请求: {json.dumps(payload3, indent=2)}")
response3 = requests.post(url, json=payload3)
print(f"状态码: {response3.status_code}")
print(f"响应: {response3.text}")
