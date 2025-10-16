#!/usr/bin/env python3
"""
更新requirements.txt以包含SSL证书生成依赖
"""

import os

def update_requirements():
    """更新requirements.txt文件"""
    
    requirements_content = """websockets>=11.0
pyautogui>=0.9.54
cryptography>=41.0.0"""
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    
    print("requirements.txt已更新，包含cryptography库")
    print("运行以下命令安装依赖：")
    print("pip install -r requirements.txt")

if __name__ == "__main__":
    update_requirements()