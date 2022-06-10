import pulumi
import pulumi_aws as aws
from config import config

domain_name = config.get('domain_name')

# Create a new Lightsail Key Pair
wp_key_pair = aws.lightsail.KeyPair("wpKeyPair")

# Create a static IP address
static_ip = aws.lightsail.StaticIp("StaticIp")

# Create a new WordPress Lightsail Instance
server = aws.lightsail.Instance(
    "lightsail-wordpress-deployment",
    blueprint_id="wordpress",
    availability_zone="us-east-1b",
    bundle_id="nano_2_0",
    key_pair_name=wp_key_pair.id,
    tags={
        "Project": "Wordpress Deploy",
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

# Add DNS record entries to point to the newly created Lightsail Instance
www_dns_record = aws.route53.Record(
    "www_dns_record",
    zone_id=hosted_zone.zone_id,
    name=f"www.{hosted_zone.name}",
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
