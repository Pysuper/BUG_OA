# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author   : Zheng Xingtao
# File     : cos.py
# Datetime : 2020/9/23 上午9:11


from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from setting.variable import TENCENT_COS_ID, TENCENT_COS_KEY


def create_bucket(region, bucket):
    """
    创建腾讯的数据存储桶
    :param region: 区域名
    :param bucket: 桶名称
    :return:
    """
    region = region  # 替换为用户的 Region
    config = CosConfig(Region=region, SecretId=TENCENT_COS_ID, SecretKey=TENCENT_COS_KEY)
    client = CosS3Client(config)

    """创建桶"""
    client.create_bucket(
        Bucket=bucket,
        ACL="public-read"
    )


def upload_image(region, bucket, image_obj, image_name):
    region = region  # 替换为用户的 Region
    config = CosConfig(Region=region, SecretId=TENCENT_COS_ID, SecretKey=TENCENT_COS_KEY)
    client = CosS3Client(config)

    """高级上传接口（推荐）"""
    # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
    # client.upload_file(
    #     Bucket=bucket,
    #     LocalFilePath='cos_test.ico',  # 本地文件的路径
    #     Key='test.ico',  # 上传到桶之后的文件名
    # )

    client.upload_file_from_buffer(
        Bucket=bucket,
        Body=image_obj,
        Key=image_name
    )

    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, image_name)
