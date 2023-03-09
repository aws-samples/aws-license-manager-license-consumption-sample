import boto3
import base64
import datetime
import pprint
import uuid

default_region = 'us-east-1'

def create_license_configuration(Name, LicenseCountingType):
    lm_client = get_client(default_region)
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
    lm_client = get_client(default_region)
    response = lm_client.get_license_configuration(
        LicenseConfigurationArn = LicenseConfigurationArn,
    )
    print('AWS License Manager - GetLicenseConfiguration API response:')
    pprint.pprint(response)
    return response


# sample function to update license specifications for all resources
def update_license_specifications_for_all_resources(LicenseConfigurationArn):
    lm_client = get_client(default_region)
    response = lm_client.list_resource_inventory(
            MaxResults=20,
        )
    while True:
        print('AWS License Manager - ListResourceInventory API response:')
        pprint.pprint(response)
        if "ResourceInventoryList" in response:
            for resource in response['ResourceInventoryList']:
                lm_client.update_license_specifications_for_resource(
                    ResourceArn=resource['ResourceArn'],
                    AddLicenseSpecifications=[
                        {
                            'LicenseConfigurationArn': LicenseConfigurationArn
                        },
                    ],
                )
                list_response = lm_client.list_license_specifications_for_resource(
                    ResourceArn=resource['ResourceArn'],
                )
                pprint.pprint(list_response)
        if "NextToken" in response:
            next_token = response['NextToken']
            response = lm_client.list_resource_inventory(
                NextToken=next_token,
            )
        else: 
            break
    return response


def get_client(Region):
    return boto3.client('license-manager', Region)

def main(command_line=None):
    print("Start of the self-managed license sample - UpdateLicenseSpecifications")
    model_1_license_configuration_name = "TestLicenseConfiguration_1"
    model_1_license_counting_type = "Instance"

    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]

    # Creating a sample license configuration for tracking instances
    license_configuration = create_license_configuration(model_1_license_configuration_name, model_1_license_counting_type)

    # Get the sample license configuration details.
    get_license_configuration(license_configuration['LicenseConfigurationArn'])

    # Updates license specifications for all resources using the sample license configuration
    update_license_specifications_for_all_resources(license_configuration['LicenseConfigurationArn'])
    

if __name__ == '__main__':
    main()
