import boto3
import pprint
from boto3.session import Session

"""
This script allows you to set up an AWS License Manager license configuration to track your licenses across an AWS Organizational Unit (OU).

The following pre-requisites must be completed before running this script:
1. Use credentials for any administrator account of an AWS Organization (i.e. management account or delegated admin).
2. Fill in the ARN of the OU below.
3. Create an S3 bucket and fill in the ARN below. This is necessary to set up License Manager cross account discovery.
4. Fill in the EC2 AMI ARN that represents the software/licenses you are tracking.

This script performs the following steps:
1. Onboard to License Manager.
2. Create a RAM resource share and associate it with the provided OU.
3. Create a license configuration with pre-configured automated discovery rules.
4. Associate the license configuration with the resource share.
5. Associate the license configuration with the AMI to enforce the license hard limit for instances launched from the AMI.

Each helper method below is annotated with additional comments.
"""

# Customer inputs
ou_arn = ''
s3_bucket_arn = ''
ami_arn = ''

default_region = 'us-east-1'
resource_share_name = 'license-manager-resource-share-for-ou'
license_configuration_name = 'license-configuration-for-ou'

# Helper method to complete License Manager onboarding
def enable_organization_integration_and_cross_account_discovery():
    # Get initial service settings
    lm_client = get_lm_client(default_region)
    get_service_settings_response = lm_client.get_service_settings()
    print('AWS License Manager - GetServiceSettings API response:')
    pprint.pprint(get_service_settings_response)

    # If any of the settings are not complete, begin onboarding.
    if get_service_settings_response['OrganizationConfiguration']['EnableIntegration'] is False or get_service_settings_response['EnableCrossAccountsDiscovery'] is False:
        print('AWS License Manager cross account onboarding not completed, enabling it now.')

        if s3_bucket_arn == '':
            raise Exception('S3 bucket must be provided to complete License Manager cross account onboarding!')

        update_service_settings_response = lm_client.update_service_settings(
            S3BucketArn = s3_bucket_arn,
            OrganizationConfiguration = {
                'EnableIntegration': True
            },
            EnableCrossAccountsDiscovery = True
        )
        print('AWS License Manager - UpdateServiceSettings API response:')
        pprint.pprint(update_service_settings_response)

    else:
        print('AWS License Manager cross account onboarding is already completed.')


# Helper method to create a new resource share
def create_and_return_resource_share():
    ram_client = get_ram_client(default_region)
    get_resource_shares_response = ram_client.get_resource_shares(
        resourceShareStatus='ACTIVE',
        resourceOwner='SELF',
        name=resource_share_name
    )
    print('AWS Resource Access Manager - GetResourceShares API response:')
    pprint.pprint(get_resource_shares_response)

    # If resource share does not exist, create it.
    if len(get_resource_shares_response['resourceShares']) == 0:
        print('Resource share does not exist, creating it now.')

        create_resource_share_response = ram_client.create_resource_share(
            name=resource_share_name
        )
        print('AWS Resource Access Manager - CreateResourceShare API response:')
        pprint.pprint(create_resource_share_response)
        return create_resource_share_response['resourceShare']['resourceShareArn']
    else:
        print('Resource share already exists.')
        return get_resource_shares_response['resourceShares'][0]['resourceShareArn']


# Helper method to associate the resource share with the specified OU
def associate_resource_share_with_ou(resource_share_arn):
    ram_client = get_ram_client(default_region)
    list_principals_response = ram_client.list_principals(
        resourceOwner='SELF',
        resourceShareArns=[resource_share_arn]
    )
    print('AWS Resource Access Manager - ListPrincipals API response:')
    pprint.pprint(list_principals_response)
    contains_principal = False
    for principal in list_principals_response['principals']:
        if principal['id'] == ou_arn:
            contains_principal = True
            break

    if not contains_principal:
        print('OU is not associated with resource share, associating it now.')
        associate_resource_share_response = ram_client.associate_resource_share(
            resourceShareArn=resource_share_arn,
            principals=[ou_arn]
        )
        print('AWS Resource Access Manager - AssociateResourceShare API response:')
        pprint.pprint(associate_resource_share_response)

    else:
        print('OU is already associated with resource share.')


# Helper method to create a new license configuration
def create_and_return_license_configuration():
    lm_client = get_lm_client(default_region)
    license_configuration_arn = None
    next_token = ''
    while True:
        list_license_configurations_response = lm_client.list_license_configurations(
            NextToken=next_token
        )
        for license_configuration in list_license_configurations_response['LicenseConfigurations']:
            if license_configuration['Name'] == license_configuration_name:
                license_configuration_arn = license_configuration['LicenseConfigurationArn']
                break

        next_token = list_license_configurations_response['NextToken'] if 'NextToken' in list_license_configurations_response else None

        if license_configuration_arn is not None or next_token is None:
            break

    if license_configuration_arn is None:
        print('License configuration does not exist, creating it now.')
        create_license_configuration_response = lm_client.create_license_configuration(
            Name=license_configuration_name,
            LicenseCountingType='Instance',
            # The LicenseCount and LicenseCountHardLimit fields tell License Manager to block instance launches once the specified limit has been reached.
            LicenseCount=10,
            LicenseCountHardLimit=True,
            # The ProductInformationList field tells License Manager which instances to track across the Organization (i.e. the software specified in the rules).
            ProductInformationList=[
                {
                    'ResourceType': 'SSM_MANAGED',
                    'ProductInformationFilterList': [
                        {
                            'ProductInformationFilterName': 'Platform Name',
                            'ProductInformationFilterValue': [
                                'Microsoft Windows Server 2022 Datacenter',
                            ],
                            'ProductInformationFilterComparator': 'EQUALS'
                        },
                    ]
                }
            ]
        )
        print('AWS License Manager - CreateLicenseConfiguration API response:')
        pprint.pprint(create_license_configuration_response)
        return create_license_configuration_response['LicenseConfigurationArn']

    else:
        print('License configuration already exists.')
        return license_configuration_arn


# Helper method to associate the resource share with the specified license configuration
def associate_resource_share_with_license_configuration(resource_share_arn, license_configuration_arn):
    ram_client = get_ram_client(default_region)
    contains_resource = False
    next_token = None
    while True:
        params = {
            'resourceOwner': 'SELF',
            'resourceShareArns': [resource_share_arn]
        }
        if next_token is not None:
            params['nextToken'] = next_token
        list_resources_response = ram_client.list_resources(**params)
        for resource in list_resources_response['resources']:
            if resource['arn'] == license_configuration_arn:
                contains_resource = True
                break

        next_token = list_resources_response['nextToken'] if 'nextToken' in list_resources_response else None
        if contains_resource or next_token is None:
            break


    if not contains_resource:
        print('License configuration is not associated with resource share, associating it now.')
        # This action allows each account in the OU to view the specified license configuration.
        associate_resource_share_response = ram_client.associate_resource_share(
            resourceShareArn=resource_share_arn,
            resourceArns=[license_configuration_arn]
        )
        print('AWS Resource Access Manager - AssociateResourceShare API response:')
        pprint.pprint(associate_resource_share_response)

    else:
        print('License configuration is already associated with resource share.')


# Helper method to associate the specified AMI with the license configuration
def associate_ami_with_license_configuration(license_configuration_arn):
    lm_client = get_lm_client(default_region)
    contains_resource = False
    next_token = None
    while True:
        params = {
            'LicenseConfigurationArn': license_configuration_arn
        }
        if next_token is not None:
            params['NextToken'] = next_token
        list_associations_for_license_configuration_response = lm_client.list_associations_for_license_configuration(**params)
        for association in list_associations_for_license_configuration_response['LicenseConfigurationAssociations']:
            if ami_arn == association['ResourceArn']:
                contains_resource = True
                break

        next_token = list_associations_for_license_configuration_response['NextToken'] if 'NextToken' in list_associations_for_license_configuration_response else None
        if contains_resource or next_token is None:
            break

    if not contains_resource:
        print('License configuration is not associated with AMI, associating it now.')
        update_license_specifications_for_resource_response = lm_client.update_license_specifications_for_resource(
            ResourceArn=ami_arn,
            AddLicenseSpecifications=[
                {
                    'LicenseConfigurationArn': license_configuration_arn,
                    # Note that this field must be set to 'cross-account', which tells License Manager that instance launches should be blocked if the caller account does not have this license configuration shared with them.
                    'AmiAssociationScope': 'cross-account',
                }
            ]
        )
        print('AWS License Manager - UpdateLicenseSpecificationsForResource API response:')
        pprint.pprint(update_license_specifications_for_resource_response)

    else:
        print('License configuration is already associated with AMI.')


def get_ram_client(Region):
    return boto3.client('ram', Region)


def get_lm_client(Region):
    return boto3.client('license-manager', Region)


def main(command_line=None):
    print("Start of the script to create a license configuration that tracks instances from accounts in a specific OU.")

    # Enable AWS Organization integration and cross-account discovery in AWS License Manager
    # For more information on this setting, visit https://docs.aws.amazon.com/license-manager/latest/userguide/settings-managed-licenses.html
    enable_organization_integration_and_cross_account_discovery()

    # Create a resource share
    resource_share_arn = create_and_return_resource_share()

    # Associate the resource share with the specified OU
    associate_resource_share_with_ou(resource_share_arn)

    # Create a license configuration
    license_configuration_arn = create_and_return_license_configuration()

    # Associate the resource share with the license configuration
    associate_resource_share_with_license_configuration(resource_share_arn, license_configuration_arn)

    # Associate an AMI with the license configuration for cross-account use
    associate_ami_with_license_configuration(license_configuration_arn)
    
if __name__ == '__main__':
    main()