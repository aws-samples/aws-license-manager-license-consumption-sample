import boto3
import base64
import datetime
import pprint
import uuid
from boto3.session import Session

default_region = 'us-east-1'

# Helper method to list linux subscriptions
def list_linux_subscriptions():
    lm_linux_subscriptions_client = get_client(default_region)
    response = lm_linux_subscriptions_client.list_linux_subscriptions()
    print('AWS License Manager Linux Subscriptions - ListLinuxSubscriptions API response:')
    pprint.pprint(response)
    return

# Helper method to list linux subscription instances
def list_linux_subscription_instances(FilterName, Condition, FilterValues):
    lm_linux_subscriptions_client = get_client(default_region)
    response = lm_linux_subscriptions_client.list_linux_subscription_instances(
                    Filters=[
                        {
                            'Name': FilterName,
                            'Operator': Condition, # 'Equal'|'NotEqual'|'Contains'
                            'Values': FilterValues 
                        }
                    ]
    )
    while True:
        print('AWS License Manager Linux Subscriptions - ListLinuxSubscriptions API response:')
        pprint.pprint(response)
        if "NextToken" in response:
            next_token = response['NextToken']
            response = lm_linux_subscriptions_client.list_linux_subscription_instances(
                    Filters=[
                        {
                            'Name': FilterName,
                            'Operator': Condition,
                            'Values': FilterValues 
                        }
                    ]
            )
        else:
            break
    return

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
    
    # Get current linux subscriptions settings 
    get_linux_subscriptions_settings()
    
    # Lists Linux Subscriptions
    list_linux_subscriptions()
    
    # List all Linux Subscription Instances in some particular geographical area
    list_linux_subscription_instances('Region', 'Contains', ['us'])
    
    # List all Linux Subscription Instances with SUSE Billing Code
    list_linux_subscription_instances('UsageOperation', 'Equal', ['RunInstances:000g'])
    
    #For more details on filters please check: https://docs.aws.amazon.com/license-manager/latest/userguide/linux-subscriptions-instances-view.html
    
    
if __name__ == '__main__':
    main()
