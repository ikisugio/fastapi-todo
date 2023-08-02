import pulumi
from pulumi_aws import ec2
from dotenv import load_dotenv
import os  # Add this line

# AWSの環境変数を読み込む
load_dotenv('../.env.pub/.env.dev')
aws_envs = {key.lower(): val for key, val in os.environ.items()}  # Use os module here

# DockerとFastAPIアプリケーションを起動するためのスクリプト
user_data = f"""
#!/bin/bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
docker run -d -p 80:80 {aws_envs['dockerhub_username']}/fastapi-todo  # Use aws_envs instead of envs
"""

# セキュリティグループのイングレスルール設定
ingress_args = {
    'protocol': 'tcp',
    'from_port': 80,
    'to_port': 80,
    'cidr_blocks': ['0.0.0.0/0'],
}

# セキュリティグループの設定
security_group_config = {
    'name': aws_envs['sg_name'],
    'description': aws_envs['sg_desc'],
    'ingress': [
        ec2.SecurityGroupIngressArgs(**ingress_args),
    ],
}

# セキュリティグループの作成
security_group = ec2.SecurityGroup(aws_envs['sg_name'], **security_group_config)

# EC2インスタンスの作成
instance = ec2.Instance(
    instance_type=aws_envs['instance_type'],  # Use aws_envs instead of envs
    ami=aws_envs['ubuntu_ami_id'],  # Use aws_envs instead of envs
    vpc_security_group_ids=[security_group.id], # セキュリティグループのIDを指定
    user_data=user_data, # DockerとFastAPIアプリケーションを起動するスクリプト
    tags={
        "Name": aws_envs['instance_tag_name'],  # Use aws_envs instead of envs
    },
    **aws_envs # アンパックして環境変数を渡します
)

pulumi.export('instance_id', instance.id)
pulumi.export('public_ip', instance.public_ip)
pulumi.export('public_dns', instance.public_dns)
