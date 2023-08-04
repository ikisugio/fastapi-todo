import pulumi
from pulumi_aws import ec2
from configs import (
    aws_envs,
    ec2_entry_script,
    ingress_dicts,
)

sg_dict = {
    'name': aws_envs['sg_name'],
    'description': aws_envs['sg_desc'],
    'ingress': [
        ec2.SecurityGroupIngressArgs(**ingress_dicts),
    ],
}

# SGの作成または取得
try:
    # 既存のセキュリティグループを参照
    sg = ec2.get_security_group(
        name=aws_envs['sg_name'],
        opts=pulumi.ResourceOptions(id=aws_envs['sg_name']),
    )
except Exception:
    # セキュリティグループが存在しない場合は新規作成
    sg = ec2.SecurityGroup(aws_envs['sg_name'], **sg_dict)

# EC2インスタンスの作成または更新
instance = ec2.Instance(
    aws_envs['instance_name'],
    instance_type=aws_envs['instance_type'],
    ami=aws_envs['ubuntu_ami_id'],
    vpc_security_group_ids=[sg.id],
    user_data=ec2_entry_script,
    tags={
        "Name": aws_envs['instance_tag_name'],
    },
    opts=pulumi.ResourceOptions(id=aws_envs['instance_name'],
                                ignore_changes=["ami",
                                                "instance_type",
                                                "user_data"]
                               ),
)

# インスタンスIDをファイルに保存
with open('.pulumi/instance_id.txt', 'w') as f:
    f.write(instance.id)

pulumi.export('instance_id', instance.id)
pulumi.export('public_ip', instance.public_ip)
pulumi.export('public_dns', instance.public_dns)
