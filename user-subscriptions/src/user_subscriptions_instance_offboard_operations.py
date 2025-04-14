import boto3
import pprint

default_region = 'us-east-1'

def list_user_associations(IdentityProvider, InstanceId, MaxResults, NextToken):
    license-manager-user-subscriptions-client = get_user_subscriptions_client(default_region)
    response = license-manager-user-subscriptions-client.list_user_associations(
        IdentityProvider=IdentityProvider,
        InstanceId=InstanceId,
        MaxResults=MaxResults,
        NextToken=NextToken
    )
    print('AWS List User Associations response:')
    pprint.pprint(response)
    return response 

def list_instances(MaxResults, NextToken):
    license-manager-user-subscriptions-client = get_user_subscriptions_client(default_region)
    response = license-manager-user-subscriptions-client.list_instances(MaxResults, NextToken)
    print('AWS List Instances response:')
    pprint.pprint(response)
    return response  

def disassociate_user(Domain, IdentityProvider, InstanceId, Username):
    license-manager-user-subscriptions-client = get_user_subscriptions_client(default_region)
    response = license-manager-user-subscriptions-client.disassociate_user(
        Domain=Domain,
        IdentityProvider=IdentityProvider,
        InstanceId=InstanceId,
        Username=Username
    )
    print('AWS Disassociate User response:')
    pprint.pprint(response)
    return response  

def get_user_subscriptions_client(Region):
    return boto3.client('license-manager-user-subscriptions', Region)  

def main(command_line=None):
    print("Start of the AWS License Manager User Subscriptions instance offboard operations samples")
    
    # List instances
    list_instances(10, null)
    
    # Disassociate User to Instance
    disassociate_user('onpremises.local', {
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-9267ba49a1'
        }
    }, 'i-0c5c62d895b392d01', 'username')
    
    # List User Associations
    list_user_associations({
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-9267ba49a1'
        }
    }, 'i-0c5c62d895b392d01', 10, null)
    
if __name__ == '__main__':
    # Run main() in list_product_subscruser_subscriptions_onboard_identity_provider_operations.py followed by 
    main()