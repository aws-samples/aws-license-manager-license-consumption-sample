import boto3
import base64
import datetime
import pprint
import uuid

default_region = 'us-east-1'
default_account = '062544142987' #sample

def create_license_configuration(Name, LicenseCountingType):
    lm_client = get_lm_client(default_region)
    response = lm_client.create_license_configuration(
        Name = Name,
        Description = "My Sample License Configuration",
        LicenseCountingType = LicenseCountingType,
        LicenseCount = 123,
        LicenseCountHardLimit= True
    )
    print('AWS License Manager - CreateLicenseConfiguration API response:')
    pprint.pprint(response)
    return response

def get_license_configuration(LicenseConfigurationArn):
    lm_client = get_lm_client(default_region)
    response = lm_client.get_license_configuration(
        LicenseConfigurationArn = LicenseConfigurationArn,
    )
    print('AWS License Manager - GetLicenseConfiguration API response:')
    pprint.pprint(response)
    return response


# sample function to update license specifications for all ec2 instances based on tags
def update_license_specifications_for_all_ec2_tagged_instances(LicenseConfigurationArn):
    lm_client = get_lm_client(default_region)
    ec2_client = get_ec2_client(default_region)
    
    response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:testsample',
                    'Values': [
                            'samplekey',
                        ]
                },
            ]
        )
    while True:
        print('EC2 DescribeInstances API response:')
        pprint.pprint(response)
        if "Reservations" in response:
            reservations = response['Reservations']
            instances = reservations[0]['Instances']
            for resource in instances:
                resource_arn = "arn:aws:ec2:{}:{}:instance/{}".format(default_region, default_account, resource['InstanceId'])
                lm_client.update_license_specifications_for_resource(
                    ResourceArn = resource_arn,
                    AddLicenseSpecifications=[
                        {
                            'LicenseConfigurationArn': LicenseConfigurationArn
                        },
                    ],
                )
                list_response = lm_client.list_license_specifications_for_resource(
                    ResourceArn=resource_arn,
                )
                pprint.pprint(list_response)
        if "NextToken" in response:
            next_token = response['NextToken']
            response = ec2_client.describe_instances(
                Filters = [
                    {
                        'Name': 'tag:samplekey',
                        'Values': [
                            'samplekey',
                        ]
                    },
                ],
                NextToken = next_token
            )
        else: 
            break
    return response


def get_lm_client(Region):
    return boto3.client('license-manager', Region)

def get_ec2_client(Region):
    return boto3.client('ec2', Region)

def main(command_line=None):
    print("Start of the self-managed license sample - UpdateLicenseSpecifications tag based")
    model_1_license_configuration_name = "TestLicenseConfiguration_1"
    model_1_license_counting_type = "Instance"

    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]

    # Creating a sample license configuration for tracking instances
    license_configuration = create_license_configuration(model_1_license_configuration_name, model_1_license_counting_type)

    # Get the sample license configuration details.
    get_license_configuration(license_configuration['LicenseConfigurationArn'])

    # Updates license specifications for tagged ec2 instances using the sample license configuration and tags
    update_license_specifications_for_all_ec2_tagged_instances(['LicenseConfigurationArn'])
    

if __name__ == '__main__':
    main()
