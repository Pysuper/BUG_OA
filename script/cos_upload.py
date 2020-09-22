# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author   : Zheng Xingtao
# File     : cos_upload.py
# Datetime : 2020/9/22 下午3:15
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = 'AKIDmIXrvU52dyNDhvIa2E9onYmkQq2xay6g'  # 替换为用户的 secretId
secret_key = 'TfbFdjX5NO9algJlxmKaaLp1vYv3ziBi'  # 替换为用户的 secretKey
region = 'ap-shanghai'  # 替换为用户的 Region
key_id = '-1302804547'  # API_KEY_ID

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)

client = CosS3Client(config)

"""高级上传接口（推荐）"""
# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
response = client.upload_file(
    Bucket='mr-zheng' + key_id,
    LocalFilePath='cos_test.ico',  # 本地文件的路径
    Key='test.ico',  # 上传到桶之后的文件名
)
print(response['ETag'])
