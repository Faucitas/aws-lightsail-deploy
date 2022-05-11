import pulumi
import pulumi_aws as aws

# Create a new Lightsail Key Pair
lg_key_pair = aws.lightsail.KeyPair("lgKeyPair")

# Create a new Wordopress Lightsail Instance
wordpress_test = aws.lightsail.Instance("aws-lightsail-deployment",
    availability_zone="us-east-1b",
    blueprint_id="wordpress",
    bundle_id="nano_2_0",
    key_pair_name=lg_key_pair.id,
    tags={
        "Project": "Wordpress Deploy",
    })