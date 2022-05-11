import pulumi
import pulumi_aws as aws

site_domain_name="illumifi.xyz"

# Create a new Lightsail Key Pair
lg_key_pair = aws.lightsail.KeyPair("lgKeyPair")

# Create a static IP address
static_ip = aws.lightsail.StaticIp("StaticIp")

# Create a new WordPress Lightsail Instance
new_instance = aws.lightsail.Instance(
    "aws-lightsail-deployment",
    blueprint_id="wordpress",
    availability_zone="us-east-1b",
    bundle_id="nano_2_0",
    key_pair_name=lg_key_pair.id,
    tags={
        "Project": "Wordpress Deploy",
    })

# Attached Static IP address to new instance
static_ip_attachment = aws.lightsail.StaticIpAttachment(
    "StaticIpAttachment",
    static_ip_name=static_ip.id,
    instance_name=new_instance.id)

# locate Hosted Zone for Site
hosted_zone = aws.route53.get_zone(
    name=site_domain_name,
    private_zone=False)

# Add Record entries to point to the newly created Lightsail Instance
www = aws.route53.Record("www",
    zone_id=hosted_zone.zone_id,
    name=f"www.{hosted_zone.name}",
    type="A",
    ttl=300,
    records=[static_ip.ip_address])

base_domain = aws.route53.Record("base",
    zone_id=hosted_zone.zone_id,
    name=f"{hosted_zone.name}",
    type="A",
    ttl=300,
    records=[static_ip.ip_address])
