import pulumi
import pulumi_aws as aws
from config import config

name = config['tags']['Project']

# Create a static IP address
static_ip = aws.lightsail.StaticIp(f'{name}_static_ip')

# Create a new WordPress Lightsail Instance
server = aws.lightsail.Instance(
    f'{name}-server',
    blueprint_id=config['blueprint_id'],
    availability_zone=config['availability_zone'],
    bundle_id=config['bundle_id'],
    key_pair_name=config['key_pair'],
    tags=config['tags'])

# Attached Static IP address to new instance
static_ip_attachment = aws.lightsail.StaticIpAttachment(
    f'{name}-ip-attachment',
    static_ip_name=static_ip.id,
    instance_name=server.id)

# locate Hosted Zone for Site
hosted_zone = aws.route53.get_zone(
    name=config['domain_name'],
    private_zone=False)

# Add DNS record entries to point to the Lightsail instance

subdomain = config['subdomain']

dns_record = aws.route53.Record(
    f"{subdomain}-dns-record",
    zone_id=hosted_zone.zone_id,
    name=f"{subdomain}.{hosted_zone.name}",
    type="A",
    ttl=300,
    records=[static_ip.ip_address])

# base_dns_record = aws.route53.Record(
#     "base_dns_record",
#     zone_id=hosted_zone.zone_id,
#     name=hosted_zone.name,
#     type="A",
#     ttl=300,
#     records=[static_ip.ip_address])
