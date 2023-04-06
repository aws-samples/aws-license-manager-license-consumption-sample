import boto3
import base64
import datetime
import pprint
import uuid
from boto3.session import Session

default_region = 'us-east-1'
default_role = 'LicenseConversionRole'

# Management Account(MA)/Delegated Admin(DA)  assumes default role (LicenseConversionRole) in each resoure owner account id
# with below permissions to start/get license conversion Tasks. 
# https://docs.aws.amazon.com/license-manager/latest/userguide/conversion-prerequisites.html 

# To create default role and set trust relationship with MA/DA: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html 

# Helper method to create license conversion task
def create_license_conversion_task(AccountId, ResourceArn, SourceContext, DestinationContext):
    assume_role_client = get_client_using_assume_role(AccountId, default_region)
    response = assume_role_client.create_license_conversion_task_for_resource(
                    ResourceArn = ResourceArn,
                    SourceLicenseContext={
                        'UsageOperation': SourceContext 
                    },
                    DestinationLicenseContext={
                        'UsageOperation': DestinationContext
                    }
                )
    print('AWS License Manager - CreateLicenseConversionTask API response:')
    pprint.pprint(response)
    return response

# Helper method to track license conversion task status
def get_license_conversion_task_status(AccountId, LicenseConversionTaskId):
    assume_role_client = get_client_using_assume_role(AccountId, default_region)
    response = assume_role_client.get_license_conversion_task(
        LicenseConversionTaskId = LicenseConversionTaskId,
    )
    print('AWS License Manager - GetLicenseConfiguration API response:')
    pprint.pprint(response)
    # Status message in the response provides more details on the Staus
    if ((response['Status'] == 'SUCCEEDED') or (response['Status'] == 'FAILED')):
        return True
    else: 
        return False

# Sample function to convert Windows Server from BYOL to license included
# for all eligible conversion types please visit: https://docs.aws.amazon.com/license-manager/latest/userguide/conversion-types.html 
def convert_BYOL_to_license_included_for_all_resources():
    lm_client = get_client(default_region)
    
    # Pass filters to apply conversion on certain resources
    # https://docs.aws.amazon.com/license-manager/latest/APIReference/API_ListResourceInventory.html#licensemanager-ListResourceInventory-request-Filters 
    response = lm_client.list_resource_inventory(
            MaxResults=20,
        )
    
    pending_conversion_tasks = []
    while True:
        print('AWS License Manager - ListResourceInventory API response:')
        pprint.pprint(response)
        if "ResourceInventoryList" in response:
            for resource in response['ResourceInventoryList']:
                resource_arn = resource['ResourceArn']
                account_id = resource_arn.split(':')[4]
                converstion_task_response = create_license_conversion_task (account_id, resource_arn, 'RunInstances:0800', 'RunInstances:0002')
                pending_conversion_tasks.append((account_id, converstion_task_response['LicenseConversionTaskId']))
                pprint.pprint(converstion_task_response)
        if "NextToken" in response:
            next_token = response['NextToken']
            response = lm_client.list_resource_inventory(
                NextToken=next_token,
            )
        else:
            break
    while len(pending_conversion_tasks) != 0: 
        for task in pending_conversion_tasks:
            task_completed = get_license_conversion_task_status(task[0], task[1])
            if task_completed == True: 
                pending_conversion_tasks.remove(task)
    return
    
# Sample function to convert Windows Server from LI to BYOL
def convert_LI_to_BYOL_for_all_resources():
    lm_client = get_client(default_region)
    response = lm_client.list_resource_inventory(
            MaxResults=20,
        )
    pending_conversion_tasks = []
    while True:
        print('AWS License Manager - ListResourceInventory API response:')
        pprint.pprint(response)
        if "ResourceInventoryList" in response:
            for resource in response['ResourceInventoryList']:
                resource_arn = resource['ResourceArn']
                account_id = resource_arn.split(':')[4]
                converstion_task_response = create_license_conversion_task (account_id, resource_arn, 'RunInstances:0002', 'RunInstances:0800')
                pending_conversion_tasks.append((account_id, converstion_task_response['LicenseConversionTaskId']))
                pprint.pprint(converstion_task_response)
        if "NextToken" in response:
            next_token = response['NextToken']
            response = lm_client.list_resource_inventory(
                NextToken=next_token,
            )
        else: 
            break
    while len(pending_conversion_tasks) != 0: 
        for task in pending_conversion_tasks:
            task_completed = get_license_conversion_task_status(task[0], task[1])
            if task_completed == True: 
                pending_conversion_tasks.remove(task)
    return True

def get_client(Region):
    return boto3.client('license-manager', Region)

def get_client_using_assume_role(AccountId, Region):
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn="arn:aws:iam::{}:role/{}".format(AccountId, default_role),
        RoleSessionName="AssumeRoleSession1"
    )
    session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                      aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                      aws_session_token=response['Credentials']['SessionToken'])
    return session.client('license-manager', Region)

def main(command_line=None):
    print("Start of the License Conversion Tasks samples")
    
    # Convert BYOL to license included (LI) for all windows resources in the AWS Organization
    convert_BYOL_to_license_included_for_all_resources()
    
    # Convert LI to BYOL for all windows resources in the AWS Organization
    convert_LI_to_BYOL_for_all_resources()
    
    # For other type of suppoerted conversions please visit: https://docs.aws.amazon.com/license-manager/latest/userguide/conversion-types.html
    
if __name__ == '__main__':
    main()
