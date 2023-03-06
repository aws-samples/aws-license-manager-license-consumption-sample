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

# Lists resources managed using Systems Manager inventory.
def list_resource_inventory():
    lm_client = get_client(default_region)
    response = lm_client.list_resource_inventory()
    print('AWS License Manager - ListResourceInventory API response:')
    pprint.pprint(response)
    return response

# Modifies the attributes of an existing license configuration.
def update_license_configuration(LicenseConfigurationArn):
    lm_client = get_client(default_region)
    response = lm_client.update_license_configuration(
        LicenseConfigurationArn = LicenseConfigurationArn,
        ProductInformationList=[
        {
            'ResourceType': 'SSM_MANAGED',
            'ProductInformationFilterList': [
                {
                    'ProductInformationFilterName': 'Application Name',
                    'ProductInformationFilterValue': [
                        'Amazon EC2Launch',
                    ],
                    'ProductInformationFilterComparator': 'EQUALS'
                },
            ]
        },
    ],
    )
    print('AWS License Manager - UpdateLicenseConfiguration API response:')
    pprint.pprint(response)
    return response

def delete_license_configuration(LicenseConfigurationArn):
    lm_client = get_client(default_region)
    response = lm_client.delete_license_configuration(
        LicenseConfigurationArn = LicenseConfigurationArn
    )
    print('AWS License Manager - DeleteLicenseConfiguration API response:')
    pprint.pprint(response)


def get_client(Region):
    return boto3.client('license-manager', Region)

def main(command_line=None):
    print("Start of the self-managed license sample model 1")
    model_1_license_configuration_name = "TestLicenseConfiguration_1"
    model_1_license_counting_type = "Instance"

    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]

    # Creating a sample license configuration for tracking instances
    license_configuration = create_license_configuration(model_1_license_configuration_name, model_1_license_counting_type)

    # Get the sample license configuration details.
    get_license_configuration(license_configuration['LicenseConfigurationArn'])

    # Lists the resources managed using Systems Manager inventory.
    list_resource_inventory()
    
    # Updating the sample license configuration with Product information
    update_license_configuration(license_configuration['LicenseConfigurationArn'])
    
    # Delete the sample license configuration.
    delete_license_configuration(license_configuration['LicenseConfigurationArn'])

if __name__ == '__main__':
    main()
