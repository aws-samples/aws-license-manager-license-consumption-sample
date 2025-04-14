import boto3
import pprint

default_region = 'us-east-1'

def stop_product_subscription(Domain, IdentityProvider, Product, Username):
    license-manager-user-subscriptions-client = get_user_subscriptions_client(default_region)
    response = license-manager-user-subscriptions-client.stop_product_subscription(
        Domain=Domain,
        IdentityProvider=IdentityProvider,
        Product=Product,
        Username=Username
    )
    print('AWS Stop Product Subscription response:')
    pprint.pprint(response)
    return response      

def deregister_identity_provider(IdentityProvider, Product):
    license-manager-user-subscriptions-client = get_user_subscriptions_client(default_region)
    response = license-manager-user-subscriptions-client.deregister_identity_provider(
        IdentityProvider=IdentityProvider,
        Product=Product
    )
    print('AWS Deregister Identity Provider response:')
    pprint.pprint(response)
    return response

def get_user_subscriptions_client(Region):
    return boto3.client('license-manager-user-subscriptions', Region)    


def main(command_line=None):
    print("Start of the AWS License Manager User Subscriptions offboard Identity Provider samples")
    # Run main() in list_product_subscruser_subscriptions_onboard_identity_provider_operations.py 
    # followed by user_subscriptions_instance_onboard_operations.py
    # followed by user_subscriptions_instance_offboard_operations.py

    # Stop Product subscription for Identity Provider user
    stop_product_subscription('onpremises.local', {
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-9267ba49a1'
        }
    }, 'VISUAL_STUDIO_PROFESSIONAL', 'username')

    # De-register Identity Provider
    deregister_identity_provider({
            'ActiveDirectoryIdentityProvider': {
                'DirectoryId': 'd-9267ba49a1'
            }
        }, 'VISUAL_STUDIO_PROFESSIONAL')
