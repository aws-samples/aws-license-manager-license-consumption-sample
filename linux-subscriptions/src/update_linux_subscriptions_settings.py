import boto3
import base64
import datetime
import pprint
import uuid
from boto3.session import Session

default_region = 'us-east-1'

# Helper method to update license manager linux subscription settings
def update_linux_subscriptions_settings(OrganizationIntegration, SourceRegions):
    lm_linux_subscriptions_client = get_client(default_region)
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
    lm_linux_subscriptions_client = get_client(default_region)
    response = lm_linux_subscriptions_client.get_service_settings()
    print('AWS License Manager Linux Subscriptions - GetServiceSettings API response:')
    pprint.pprint(response)
    return response


def get_client(Region):
    return boto3.client('license-manager-linux-subscriptions', Region)

def main(command_line=None):
    print("Start of the AWS License Manager Linux Subscriptions samples")
    
    # sample source regions - collects linux subscriptions resources from these regions
    source_regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ap-south-1']
    
    # Onboard to Linux Subscriptions with Cross Account, Cross Region feature enabled
    update_linux_subscriptions_settings('Enabled', source_regions)
    
    # Get current linux subscriptions settings 
    get_linux_subscriptions_settings()
    
if __name__ == '__main__':
    main()
