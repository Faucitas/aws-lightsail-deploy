import pulumi
import pulumi_aws as aws

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

static_ip_attachment = aws.lightsail.StaticIpAttachment(
    "StaticIpAttachment",
    static_ip_name=static_ip.id,
    instance_name=new_instance.id)
