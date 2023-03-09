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

# Update an existing license configuration with tag based exclusion rules.
def update_license_configuration_with_exclusion_rules(LicenseConfigurationArn):
    lm_client = get_client(default_region)
    response = lm_client.update_license_configuration(
        LicenseConfigurationArn = LicenseConfigurationArn,
        ProductInformationList=[
        {
            'ResourceType': 'SSM_MANAGED',
            'ProductInformationFilterList': [
                {
                    'ProductInformationFilterName': 'Tag:samplekey',
                    'ProductInformationFilterValue': [
                        'samplevalue', #optional 
                    ],
                    'ProductInformationFilterComparator': 'NOT_EQUALS'
                },
                {
                    'ProductInformationFilterName': 'Application Name',
                    'ProductInformationFilterValue': [
                        'windows',
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
    
    # Updating the sample license configuration with Tags based exclusion rules
    update_license_configuration_with_exclusion_rules(license_configuration['LicenseConfigurationArn'])
    
    # Delete the sample license configuration.
    delete_license_configuration(license_configuration['LicenseConfigurationArn'])

if __name__ == '__main__':
    main()


