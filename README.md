![图片描述](Snipaste_2025-12-01_01-31-43.png)

运行主程序jiutong.exe，软件会自动开始运行

当发现任何余额不为0的钱包出现则会自动把钱包信息保存在本地

日志会生成在同文件夹中的logs.txt中（运行过软件后日志才会生成，仅保留最后2000条），如果遇到有资产的地址你会在这个文件夹内看到一个non_zero_addresses.txt的文件，打开就能看到详细信息，如果non_zero_addresses.txt还没生成那就代表还没碰撞出来，默认使用TronGrid API动态查询地址，如果遇到403报错可以更换ip

此版本每秒效率15次，仅做演示功能，此版本不包含CUDA加速和多GPU兼容（因为不需要）
正式软件每秒效率亿为单位（包含CUDA加速和多GPU兼容，根据当前设备算力，例如3060显卡每秒可达500亿次）
当前软件为TRON链，另有BTC链和ETH链碰撞，别的链可定制

联系：飞机telegram [@jiutong9999](https://t.me/jiutong9999)

Run the main program jiutong.exe, and the software will start automatically.
When any wallet with a non-zero balance is detected, the wallet information will be automatically saved locally.
Logs will be generated in logs.txt in the same folder (logs are only generated after the software is run, and only the last 2000 entries are retained). If an address with assets is encountered, you will see a file named non_zero_addresses.txt in this folder. Opening it will show detailed information. If non_zero_addresses.txt has not yet been generated, it means that no collision has occurred. By default, the TronGrid API is used to dynamically query addresses. If you encounter a 403 error, try changing the IP address.
This version has an efficiency of 15 operations per second and is for demonstration purposes only. This version does not include CUDA acceleration and multi-GPU compatibility (because it is not needed). The official software has an efficiency in the hundreds of millions per second (including CUDA acceleration and multi-GPU compatibility; depending on the current device's computing power, for example, a 3060 graphics card can reach 50 billion operations per second).
The current software is for the TRON chain. Collision on the BTC and ETH chains is also available. Customization is available for other chains.

