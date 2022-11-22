import pulumi
import pulumi_aws as aws
from config import config

domain_name = config.get('domain_name')
blueprint = "wordpress"
key_pair_name = "wpKeyPair"
static_ip_name = "wpStaticIp"
instance_name = "lightsail-wordpress-deployment"
instance_size = "nano_2_0"
region = "us-east-1b"
tags = {
    "Project": "Wordpress Deploy",
}

# Create a new Lightsail Key Pair
wp_key_pair = aws.lightsail.KeyPair(key_pair_name)

# Create a static IP address
static_ip = aws.lightsail.StaticIp(static_ip_name)

# Create a new WordPress Lightsail Instance
server = aws.lightsail.Instance(
    instance_name,
    blueprint_id=blueprint,
    availability_zone=region,
    bundle_id=instance_size,
    key_pair_name=wp_key_pair.id,
    tags={
        tags
    })

# Attached Static IP address to new instance
static_ip_attachment = aws.lightsail.StaticIpAttachment(
    "StaticIpAttachment",
    static_ip_name=static_ip.id,
    instance_name=server.id)

# locate Hosted Zone for Site
hosted_zone = aws.route53.get_zone(
    name=domain_name,
    private_zone=False)

# Add DNS record entries to point to the Lightsail instance
www_dns_record = aws.route53.Record(
    "www_dns_record",
    zone_id=hosted_zone.zone_id,
    name=f"wp.{hosted_zone.name}",
    type="A",
    ttl=300,
    records=[static_ip.ip_address])

base_dns_record = aws.route53.Record(
    "base_dns_record",
    zone_id=hosted_zone.zone_id,
    name=hosted_zone.name,
    type="A",
    ttl=300,
    records=[static_ip.ip_address])
