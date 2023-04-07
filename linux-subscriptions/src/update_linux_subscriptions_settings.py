import boto3
import base64
import datetime
import pprint
import uuid
from boto3.session import Session

default_region = 'us-east-1'

# Helper method to update license manager linux subscription settings
def update_linux_subscriptions_settings(OrganizationIntegration, SourceRegions):
    lm_linux_subscriptions_client = get_lm_client(default_region)
    response = lm_linux_subscriptions_client.update_service_settings(
                    LinuxSubscriptionsDiscovery='Enabled',
                    LinuxSubscriptionsDiscoverySettings={
                        'OrganizationIntegration': OrganizationIntegration,
                        'SourceRegions': SourceRegions
                    }
                )
    print('AWS License Manager Linux Subscriptions - UpdateServiceSettings API response:')
    pprint.pprint(response)
    return response

# Helper method to get license manager linux subscription settings
def get_linux_subscriptions_settings():
    lm_linux_subscriptions_client = get_lm_client(default_region)
    response = lm_linux_subscriptions_client.get_service_settings()
    print('AWS License Manager Linux Subscriptions - GetServiceSettings API response:')
    pprint.pprint(response)
    return response

# Helper method to enabled the integration of Linux Subscriptions with AWS Organizations.
def enable_linux_subscriptions_orgs_service_access():
    orgs_client = get_orgs_client(default_region)
    response = orgs_client.enable_aws_service_access(
                    ServicePrincipal = 'license-manager-linux-subscriptions.amazonaws.com'
                )
    print('AWS Organizations EnableAWSServiceAccess API response:')
    pprint.pprint(response)
    return response
    
# Helper method to crate Linux Subscriptions SLR.
def create_linux_subscriptions_slr():
    iam_client = get_iam_client(default_region)
    response = iam_client.create_service_linked_role(
                    AWSServiceName='license-manager-linux-subscriptions.amazonaws.com'
                )
    print('AWS IAM CreateServiceLinkedRole API response:')
    pprint.pprint(response)
    return response


def get_lm_client(Region):
    return boto3.client('license-manager-linux-subscriptions', Region)

def get_orgs_client(Region):
    return boto3.client('organizations', Region)
    
def get_iam_client(Region):
    return boto3.client('iam', Region)

def main(command_line=None):
    print("Start of the AWS License Manager Linux Subscriptions samples")
    
    # License Manager requires a service-linked role for managing AWS resources that will provide Linux subscriptions.
    # Fore more details please visit: https://docs.aws.amazon.com/license-manager/latest/userguide/linux-subscriptions-role.html
    create_linux_subscriptions_slr()
    
    # Enable the integration of Linux Subscriptions with Organizations
    # https://docs.aws.amazon.com/organizations/latest/APIReference/API_EnableAWSServiceAccess.html 
    enable_linux_subscriptions_orgs_service_access()

    # sample source regions - collects linux subscriptions resources from these regions
    source_regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ap-south-1']

    # Onboard to Linux Subscriptions with Cross Account (if not enabled - Single Account Mode), Cross Region features enabled
    update_linux_subscriptions_settings('Enabled', source_regions)

    # Get current linux subscriptions settings 
    get_linux_subscriptions_settings()
    
    # For more details: https://docs.aws.amazon.com/license-manager/latest/userguide/linux-subscriptions.html 

if __name__ == '__main__':
    main()
