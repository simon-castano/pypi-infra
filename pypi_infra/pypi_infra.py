"""Contain main stack definition."""
from typing import Optional

from aws_cdk.aws_ec2 import Peer, Port, Protocol, SecurityGroup, Vpc
from aws_cdk.aws_ecs import (
    AwsLogDriver,
    CloudMapNamespaceOptions,
    CloudMapOptions,
    Cluster,
    ContainerImage,
    EfsVolumeConfiguration,
    FargatePlatformVersion,
    FargateService,
    FargateTaskDefinition,
    Host,
    Volume,
)
from aws_cdk.aws_efs import FileSystem
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.core import Construct, RemovalPolicy, Stack


class PypiserverInfra(Stack):
    """Pypiserver Resources."""

    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        vpc: Optional[Vpc] = None,
        namespace: str = "vf-integrations-development",
        cpu: int = 256,
        memory_limit_mib: int = 512,
        version: str = "1.3.2",
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        if vpc is None:
            vpc = Vpc(self, "vpc", max_azs=1)

        security_group = SecurityGroup(self, "security-group", vpc=vpc)
        security_group.add_ingress_rule(
            peer=Peer.any_ipv4(),
            connection=Port(protocol=Protocol.TCP, string_representation="pypi", from_port=8080, to_port=8080),
        )
        security_group.add_ingress_rule(
            peer=Peer.any_ipv6(),
            connection=Port(protocol=Protocol.TCP, string_representation="pypi", from_port=8080, to_port=8080),
        )

        efs = FileSystem(self, "efs", vpc=vpc, encrypted=True, removal_policy=RemovalPolicy.DESTROY)
        efs.connections.allow_from(
            other=security_group,
            port_range=Port(protocol=Protocol.TCP, string_representation="NFS", from_port=2049, to_port=2049),
        )

        task_definition = FargateTaskDefinition(
            self,
            "task-def",
            cpu=cpu,
            memory_limit_mib=memory_limit_mib,
            volumes=[
                Volume(
                    name="packages",
                    efs_volume_configuration=EfsVolumeConfiguration(
                        file_system_id=efs.file_system_id, transit_encryption="ENABLED"
                    ),
                )
            ],
        )
        task_definition.add_container(
            "container",
            image=ContainerImage.from_registry(f"pypiserver/pypiserver:v{version}"),
            logging=AwsLogDriver(stream_prefix=self.node.id, log_retention=RetentionDays.ONE_DAY),
        )
        FargateService(
            self,
            "service",
            task_definition=task_definition,
            assign_public_ip=True,
            platform_version=FargatePlatformVersion.VERSION1_4,
            security_group=security_group,
            cluster=Cluster(
                self, "cluster", default_cloud_map_namespace=CloudMapNamespaceOptions(name=namespace), vpc=vpc
            ),
            cloud_map_options=CloudMapOptions(),
            desired_count=1,
            max_healthy_percent=100,
            min_healthy_percent=0,
            service_name="pypiserver",
        )
