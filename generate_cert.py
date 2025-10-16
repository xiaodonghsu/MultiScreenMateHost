#!/usr/bin/env python3
"""
生成自签名SSL证书的脚本
用于WSS（安全WebSocket）连接
"""

import ssl
import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

def generate_self_signed_cert():
    """生成自签名SSL证书"""
    
    # 生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # 创建证书主题
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Beijing"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Beijing"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "WebSocket Server"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    # 创建证书
    certificate = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.DNSName("127.0.0.1"),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    return private_key, certificate

def save_certificates(private_key, certificate):
    """保存证书和私钥到文件"""
    
    # 保存私钥
    with open("server.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    
    # 保存证书
    with open("server.crt", "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))
    
    print("SSL证书生成成功！")
    print("已创建文件: server.key (私钥)")
    print("已创建文件: server.crt (证书)")

if __name__ == "__main__":
    try:
        print("正在生成自签名SSL证书...")
        private_key, certificate = generate_self_signed_cert()
        save_certificates(private_key, certificate)
        print("\n证书信息:")
        print("- 有效期: 1年")
        print("- 主题: WebSocket Server")
        print("- 支持的域名: localhost, 127.0.0.1")
        print("\n现在可以使用WSS协议连接服务器了！")
        
    except ImportError:
        print("错误: 需要安装cryptography库")
        print("请运行: pip install cryptography")
    except Exception as e:
        print(f"生成证书时发生错误: {e}")