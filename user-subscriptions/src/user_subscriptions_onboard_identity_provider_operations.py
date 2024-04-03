import boto3
import pprint

default_region = 'us-east-1'

def get_iam_client(Region):
    return boto3.client('iam', Region)

def create_user_subscriptions_slr():
    iam_client = get_iam_client(default_region)
    response = iam_client.create_service_linked_role(
                    AWSServiceName='license-manager-user-subscriptions.amazonaws.com'
                )
    print('AWS IAM CreateServiceLinkedRole API response:')
    pprint.pprint(response)
    return response   

def list_product_subscriptions(IdentityProvider, MaxResults, NextToken, Product):
    license-manager-user-subscriptions-client = get_user_subscriptions_client(default_region)
    response = license-manager-user-subscriptions-client.list_product_subscriptions(
        IdentityProvider=IdentityProvider,
        MaxResults=MaxResults,
        NextToken=NextToken,
        Product=Product
    ) 
    print('AWS List Product Subscriptions response:')
    pprint.pprint(response)
    return response   

def start_product_subscription(Domain, IdentityProvider, Product, Username):
    license-manager-user-subscriptions-client = get_user_subscriptions_client(default_region)
    response = license-manager-user-subscriptions-client.start_product_subscription(
        Domain=Domain,
        IdentityProvider=IdentityProvider,
        Product=Product,
        Username=Username
    )
    print('AWS Start Product Subscription response:')
    pprint.pprint(response)
    return response



def list_identity_providers(MaxResults, NextToken):
    license-manager-user-subscriptions-client = get_user_subscriptions_client(default_region)
    response = license-manager-user-subscriptions-client.list_identity_providers(
        MaxResults=MaxResults,
        NextToken=NextToken
    )
    print('AWS List Identity Providers response:')
    pprint.pprint(response)
    return response


def register_identity_provider(IdentityProvider, Product):
    license-manager-user-subscriptions-client = get_user_subscriptions_client(default_region)
    response = license-manager-user-subscriptions-client.register_identity_provider(
        IdentityProvider=IdentityProvider,
        Product=Product
    )
    print('AWS Register Identity Provider response:')
    pprint.pprint(response)
    return response



def get_user_subscriptions_client(Region):
    return boto3.client('license-manager-user-subscriptions', Region)


def onboard():
    # Follow steps in https://docs.aws.amazon.com/license-manager/latest/userguide/user-based-subscriptions-getting-started.html#user-based-subscriptions-subscribe-products
    # to subscribe to Visual Studio Professional from AWS Marketplace
    
    # Register Identity Provider
    register_identity_provider({
            'ActiveDirectoryIdentityProvider': {
                'DirectoryId': 'd-9267ba49a1'
            }
        }, 'VISUAL_STUDIO_PROFESSIONAL')

    # List Identity Provider. Wait until IdentityProvider is registered.
    while True:
        response = list_identity_providers(10, null)
        if response['IdentityProviderSummaries'][0]['Status'] == 'REGISTERED':
            break
    
    # Start Product Subscription for Identity Provider user
    start_product_subscription('onpremises.local', {
            'ActiveDirectoryIdentityProvider': {
                'DirectoryId': 'd-9267ba49a1'
            }
        }, 'VISUAL_STUDIO_PROFESSIONAL', 'username')

    # List Product Subscriptions
    list_product_subscriptions({
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-9267ba49a1'
        }
    }, 100, null, 'VISUAL_STUDIO_PROFESSIONAL')


def main(command_line=None):
    print("Start of the AWS License Manager User Subscriptions onboard Identity Provider samples")

    # License Manager requires a service-linked role for managing AWS resources that will provide User subscriptions.
    # Fore more details please visit: https://docs.aws.amazon.com/license-manager/latest/userguide/user-based-subscription-role.html
    create_user_subscriptions_slr()
    onboard()
    
if __name__ == '__main__':
    main()