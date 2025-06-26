#!/usr/bin/env python3
"""
AWS License Manager User Subscriptions - License Server Endpoints Management

This script demonstrates how to manage license server endpoints in AWS License Manager
User Subscriptions, including creating, listing, and deleting license server endpoints.

Author: AWS License Manager Team
License: MIT-0
"""

import boto3
import datetime
import pprint
from typing import Dict, List, Optional, Any

# Default AWS region
DEFAULT_REGION = 'us-east-1'


def get_client(region: str = DEFAULT_REGION) -> boto3.client:
    """
    Create and return AWS License Manager User Subscriptions client.
    
    Args:
        region: AWS region name
        
    Returns:
        boto3.client: License Manager User Subscriptions client
    """
    return boto3.client('license-manager-user-subscriptions', region)


def create_license_server_endpoint(
    identity_provider_arn: str,
    license_server_settings: Dict[str, Any],
    tags: Optional[Dict[str, str]] = None
) -> Optional[Dict[str, Any]]:
    """
    Create a new license server endpoint.
    
    Args:
        identity_provider_arn: ARN of the identity provider (not the full object)
        license_server_settings: License server configuration settings
        tags: Optional tags to apply to the endpoint (as dict, not list)
        
    Returns:
        Dict containing creation response or None if error
    """
    client = get_client()
    
    try:
        params = {
            'IdentityProviderArn': identity_provider_arn,
            'LicenseServerSettings': license_server_settings
        }
        
        if tags:
            params['Tags'] = tags
        
        response = client.create_license_server_endpoint(**params)
        print('AWS License Manager User Subscriptions - CreateLicenseServerEndpoint API response:')
        pprint.pprint(response)
        return response
    except Exception as e:
        print(f"Error creating license server endpoint: {e}")
        return None


def delete_license_server_endpoint(
    license_server_endpoint_arn: str,
    server_type: str = 'RDS_SAL'
) -> Optional[Dict[str, Any]]:
    """
    Delete an existing license server endpoint.
    
    Args:
        license_server_endpoint_arn: ARN of the license server endpoint to delete
        server_type: Type of license server (default: 'RDS_SAL')
        
    Returns:
        Dict containing deletion response or None if error
    """
    client = get_client()
    
    try:
        response = client.delete_license_server_endpoint(
            LicenseServerEndpointArn=license_server_endpoint_arn,
            ServerType=server_type
        )
        print('AWS License Manager User Subscriptions - DeleteLicenseServerEndpoint API response:')
        pprint.pprint(response)
        return response
    except Exception as e:
        print(f"Error deleting license server endpoint: {e}")
        
        # Provide helpful error messages for common scenarios
        if 'ValidationException' in str(e):
            if 'failed provisioning' in str(e):
                print("💡 This endpoint is in PROVISIONING_FAILED state and cannot be deleted via API.")
                print("   Contact AWS Support to remove failed endpoints.")
            elif 'not found' in str(e).lower():
                print("💡 The specified endpoint ARN was not found. Please verify the ARN is correct.")
        elif 'UnauthorizedException' in str(e):
            print("💡 Check that:")
            print("   - You have the correct IAM permissions")
            print("   - The endpoint ARN belongs to your AWS account")
            print("   - The endpoint exists and is in a deletable state")
        
        return None


def list_license_server_endpoints(
    identity_provider_arn: Optional[str] = None,
    max_results: Optional[int] = None,
    next_token: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    List license server endpoints.
    
    Args:
        identity_provider_arn: Identity provider ARN to filter by (optional)
        max_results: Maximum number of results to return (optional)
        next_token: Token for pagination (optional)
        
    Returns:
        Dict containing list response or None if error
    """
    client = get_client()
    
    try:
        params = {}
        
        if identity_provider_arn:
            params['IdentityProviderArn'] = identity_provider_arn
        
        if max_results:
            params['MaxResults'] = max_results
            
        if next_token:
            params['NextToken'] = next_token
        
        response = client.list_license_server_endpoints(**params)
        print('AWS License Manager User Subscriptions - ListLicenseServerEndpoints API response:')
        pprint.pprint(response)
        return response
    except Exception as e:
        print(f"Error listing license server endpoints: {e}")
        return None


def list_license_server_endpoints_paginated(
    identity_provider_arn: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List all license server endpoints with pagination support.
    
    Args:
        identity_provider_arn: Identity provider ARN to filter by (optional)
        
    Returns:
        List of all license server endpoint summaries
    """
    client = get_client()
    all_endpoints = []
    next_token = None
    page_count = 1
    
    try:
        while True:
            params = {}
            
            if identity_provider_arn:
                params['IdentityProviderArn'] = identity_provider_arn
                
            if next_token:
                params['NextToken'] = next_token
            
            response = client.list_license_server_endpoints(**params)
            
            print(f'\n=== Page {page_count} - License Server Endpoints ===')
            
            if 'LicenseServerEndpoints' in response:
                endpoints = response['LicenseServerEndpoints']
                all_endpoints.extend(endpoints)
                
                print(f"Found {len(endpoints)} license server endpoints on this page:")
                for idx, endpoint in enumerate(endpoints):
                    print(f"\n--- License Server Endpoint {idx + 1} (Page {page_count}) ---")
                    display_license_server_endpoint_details(endpoint)
            
            if 'NextToken' in response:
                next_token = response['NextToken']
                page_count += 1
            else:
                break
        
        print(f"\nCompleted pagination. Total pages processed: {page_count}")
        print(f"Total license server endpoints found: {len(all_endpoints)}")
        
        return all_endpoints
        
    except Exception as e:
        print(f"Error in paginated listing: {e}")
        return []


def display_license_server_endpoint_details(endpoint: Dict[str, Any]) -> None:
    """
    Display detailed information about a license server endpoint.
    
    Args:
        endpoint: License server endpoint details from API response
    """
    print(f"Endpoint ID: {endpoint.get('LicenseServerEndpointId', 'N/A')}")
    print(f"ARN: {endpoint.get('LicenseServerEndpointArn', 'N/A')}")
    print(f"Status: {endpoint.get('Status', 'N/A')}")
    print(f"Status Message: {endpoint.get('StatusMessage', 'N/A')}")
    
    if 'CreationTime' in endpoint:
        print(f"Creation Time: {endpoint['CreationTime']}")
    
    if 'IdentityProvider' in endpoint:
        identity_provider = endpoint['IdentityProvider']
        if 'ActiveDirectoryIdentityProvider' in identity_provider:
            ad_provider = identity_provider['ActiveDirectoryIdentityProvider']
            print(f"Directory ID: {ad_provider.get('DirectoryId', 'N/A')}")
    
    if 'LicenseServerSettings' in endpoint:
        settings = endpoint['LicenseServerSettings']
        if 'ServerType' in settings:
            print(f"Server Type: {settings['ServerType']}")
        if 'ServerSettings' in settings:
            server_settings = settings['ServerSettings']
            if 'RdsSalSettings' in server_settings:
                rds_settings = server_settings['RdsSalSettings']
                if 'RdsSalCredentialsProvider' in rds_settings:
                    creds_provider = rds_settings['RdsSalCredentialsProvider']
                    if 'SecretsManagerCredentialsProvider' in creds_provider:
                        sm_provider = creds_provider['SecretsManagerCredentialsProvider']
                        print(f"Secrets Manager Secret ID: {sm_provider.get('SecretId', 'N/A')}")
    
    print("-" * 50)


def create_rds_license_server_settings(
    secret_id: str
) -> Dict[str, Any]:
    """
    Create RDS license server settings configuration.
    
    Args:
        secret_id: The ID of the Secrets Manager secret that contains credentials
                  for RDS license server user administration
        
    Returns:
        Dict containing RDS license server settings
    """
    return {
        'ServerType': 'RDS_SAL',
        'ServerSettings': {
            'RdsSalSettings': {
                'RdsSalCredentialsProvider': {
                    'SecretsManagerCredentialsProvider': {
                        'SecretId': secret_id
                    }
                }
            }
        }
    }


def get_identity_provider_arn_for_rds() -> Optional[str]:
    """
    Helper function to get the Identity Provider ARN for RDS product.
    This looks for a registered REMOTE_DESKTOP_SERVICES identity provider.
    
    Returns:
        Identity Provider ARN string or None if not found
    """
    try:
        client = get_client()
        response = client.list_identity_providers()
        
        if 'IdentityProviderSummaries' in response:
            for provider in response['IdentityProviderSummaries']:
                if (provider.get('Product') == 'REMOTE_DESKTOP_SERVICES' and 
                    provider.get('Status') == 'REGISTERED'):
                    arn = provider.get('IdentityProviderArn')
                    print(f"Found RDS Identity Provider ARN: {arn}")
                    return arn
        
        print("No registered REMOTE_DESKTOP_SERVICES identity provider found")
        print("Please register an identity provider for RDS first using manage_identity_provider_settings.py")
        return None
        
    except Exception as e:
        print(f"Error getting identity provider ARN: {e}")
        return None


def demonstrate_endpoint_deletion_example() -> None:
    """
    Demonstrate how to delete a license server endpoint with a specific ID.
    This is a separate function to show the deletion process clearly.
    """
    print("\n=== License Server Endpoint Deletion Example ===")
    
    # Get the identity provider ARN for RDS
    identity_provider_arn = get_identity_provider_arn_for_rds()
    
    if not identity_provider_arn:
        print("❌ Cannot proceed without a registered RDS identity provider")
        return
    
    # Example endpoint ARN - replace with actual ARN from your environment
    example_endpoint_arn = "arn:aws:license-manager-user-subscriptions:us-east-1:123456789012:license-server-endpoint/lse-12345678-1234-1234-1234-123456789012"
    
    print(f"To delete a license server endpoint:")
    print(f"1. Get the endpoint ARN from the list command")
    print(f"2. Use the delete function with the license server endpoint ARN")
    print(f"\nExample (commented out for safety):")
    print(f"# delete_license_server_endpoint(")
    print(f"#     license_server_endpoint_arn='{example_endpoint_arn}',")
    print(f"#     server_type='RDS_SAL'")
    print(f"# )")
    
    print(f"\n⚠️  WARNING: Deletion is permanent and cannot be undone!")
    print(f"Make sure you have the correct endpoint ID before uncommenting the deletion call.")


    """
    Create example tags for license server endpoints.
    
    Returns:
        Dict of tags (not list)
    """
    return {
        'Environment': 'Production',
        'Team': 'Infrastructure',
        'Purpose': 'LicenseManagement'
    }


def create_example_tags() -> Dict[str, str]:
    """
    Create example tags for license server endpoints.
    
    Returns:
        Dict of tags (not list)
    """
    return {
        'Environment': 'Production',
        'Team': 'Infrastructure',
        'Purpose': 'LicenseManagement'
    }


def demonstrate_license_server_endpoint_lifecycle() -> None:
    """
    Demonstrate the complete lifecycle of license server endpoint management.
    """
    print("\n=== License Server Endpoint Lifecycle Demonstration ===")
    
    # Get the identity provider ARN for RDS
    print("--- Getting Identity Provider ARN for RDS ---")
    identity_provider_arn = get_identity_provider_arn_for_rds()
    
    if not identity_provider_arn:
        print("❌ Cannot proceed without a registered RDS identity provider")
        print("Please run manage_identity_provider_settings.py first to register RDS")
        return
    
    # Example RDS license server settings
    license_server_settings = create_rds_license_server_settings(
        'arn:aws:secretsmanager:us-east-1:123456789012:secret:license-manager-user-subscription-mad-admin-AbCdEf'
    )
    
    # Example tags
    tags = create_example_tags()
    
    print("Configuration for license server endpoint creation:")
    print(f"\nIdentity Provider ARN: {identity_provider_arn}")
    print("\nLicense Server Settings:")
    pprint.pprint(license_server_settings)
    print("\nTags:")
    pprint.pprint(tags)
    
    print("\n--- Step 1: Create License Server Endpoint ---")
    print("Note: Uncomment the following line to actually create (ensure you have valid secret ID)")
    #create_response = create_license_server_endpoint(identity_provider_arn, license_server_settings, tags)
    #create_response = None  # Initialize to None since creation is commented out
    
    print("\n--- Step 2: List License Server Endpoints ---")
    print("This will list all existing endpoints:")
    list_license_server_endpoints()
    
    print("\n--- Step 3: Delete License Server Endpoint ---")
    print("Note: To delete an endpoint, you need to:")
    print("1. Uncomment the creation line above to get a valid endpoint ID")
    print("2. Or manually specify an existing endpoint ID")
    print("3. Then uncomment the deletion lines below")
    
    # Example of how to delete if you have a valid endpoint ARN
    # Replace 'your-endpoint-arn-here' with an actual endpoint ARN
    example_endpoint_arn = 'arn:aws:license-manager-user-subscriptions:us-east-1:123456789012:license-server-endpoint/lse-12345678-1234-1234-1234-123456789012'
    print(f"\nExample deletion (commented out):")
    print(f"# delete_license_server_endpoint('{example_endpoint_arn}', 'RDS_SAL')")
    delete_license_server_endpoint(example_endpoint_arn, 'RDS_SAL')
    
    # Uncomment the following lines if you want to delete after creation
    # if create_response and 'LicenseServerEndpointArn' in create_response:
    #     endpoint_arn = create_response['LicenseServerEndpointArn']
    #     delete_license_server_endpoint(endpoint_arn, 'RDS_SAL')
    
    print("\n=== Important Notes ===")
    print("1. Replace the example secret ARN with your actual Secrets Manager secret ARN")
    print("2. The secret must contain credentials for RDS license server user administration")
    print("3. The license server endpoint will be used for RDS CAL (Client Access License) management")
    print("4. Make sure the secret is accessible from the AWS License Manager service")
    print("5. Ensure your Active Directory is properly configured and accessible")


def generate_license_server_endpoints_report() -> None:
    """
    Generate a comprehensive report of all license server endpoints.
    """
    print("\n=== License Server Endpoints Report ===")
    
    try:
        # Get all endpoints
        all_endpoints = list_license_server_endpoints_paginated()
        
        if not all_endpoints:
            print("No license server endpoints found.")
            return
        
        # Generate summary statistics
        total_endpoints = len(all_endpoints)
        status_counts = {}
        server_type_counts = {}
        
        for endpoint in all_endpoints:
            # Count by status
            status = endpoint.get('Status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Count by server type
            server_type = endpoint.get('ServerType', 'Unknown')
            server_type_counts[server_type] = server_type_counts.get(server_type, 0) + 1
        
        # Display summary
        print(f"\n--- Summary Statistics ---")
        print(f"Total License Server Endpoints: {total_endpoints}")
        
        print(f"\nEndpoints by Status:")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")
        
        print(f"\nEndpoints by Server Type:")
        for server_type, count in server_type_counts.items():
            server_type_display = server_type
            if server_type == 'RDS_SAL':
                server_type_display = 'RDS_SAL (Remote Desktop Services SAL)'
            print(f"  {server_type_display}: {count}")
        
        print(f"\nReport Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"Error generating report: {e}")


def test_delete_license_server_endpoint_with_real_arn() -> None:
    """
    Test function to demonstrate correct deletion with a real endpoint ARN.
    This function shows the proper way to call the delete function.
    """
    print("\n=== Test Delete License Server Endpoint ===")
    
    # Use the correct ARN from the current account
    endpoint_arn = "arn:aws:license-manager-user-subscriptions:us-east-1:123456789012:license-server-endpoint/lse-12345678-1234-1234-1234-123456789012"
    server_type = "RDS_SAL"
    
    print(f"Attempting to delete license server endpoint:")
    print(f"  ARN: {endpoint_arn}")
    print(f"  Server Type: {server_type}")
    print()
    
    # Call the corrected delete function
    result = delete_license_server_endpoint(endpoint_arn, server_type)
    
    if result:
        print("✅ License server endpoint deleted successfully!")
    else:
        print("❌ Failed to delete license server endpoint.")


def main() -> None:
    """
    Main function demonstrating license server endpoint management operations.
    """
    print("Start of the AWS License Manager User Subscriptions License Server Endpoints Management samples")
    
    # List current license server endpoints
    print("\n=== Current License Server Endpoints ===")
    list_license_server_endpoints()
    
    # Generate comprehensive report
    generate_license_server_endpoints_report()
    
    # Demonstrate lifecycle management
    demonstrate_license_server_endpoint_lifecycle()
    
    # Demonstrate deletion example
    #demonstrate_endpoint_deletion_example()
    
    # Test deletion with real ARN (commented out for safety)
    print("\n=== Test Deletion (Commented Out) ===")
    print("To test deletion with a real endpoint ARN, uncomment the following line:")
    print("# test_delete_license_server_endpoint_with_real_arn()")
    # test_delete_license_server_endpoint_with_real_arn()
    
    print("\n=== Important Notes ===")
    print("1. Before creating a license server endpoint, ensure you have:")
    print("   - Valid identity provider configured")
    print("   - Accessible license server URL")
    print("   - Appropriate network connectivity")
    print("   - Necessary IAM permissions")
    
    print("\n2. Supported server types:")
    print("   - RDS_SAL: Remote Desktop Services SAL License Server")
    
    print("\n3. License server endpoint statuses:")
    print("   - CREATING: Endpoint is being created")
    print("   - AVAILABLE: Endpoint is ready for use")
    print("   - FAILED: Endpoint creation or operation failed")
    print("   - DELETING: Endpoint is being deleted")
    
    print("\n4. Best practices:")
    print("   - Use descriptive tags for resource management")
    print("   - Monitor endpoint status regularly")
    print("   - Store RDS license server credentials securely in Secrets Manager")
    print("   - Implement proper error handling")
    print("   - Ensure proper IAM permissions for Secrets Manager access")
    print("   - Test Active Directory connectivity before creating endpoint")
    print("   - Only attempt to delete endpoints in AVAILABLE status")
    print("   - Contact AWS Support for endpoints in PROVISIONING_FAILED status")
    
    print("\nEnd of the AWS License Manager User Subscriptions License Server Endpoints Management samples")
    print("\n=== API OPERATIONS REFERENCE ===")
    print("create_license_server_endpoint:")
    print("  - Required: IdentityProviderArn, LicenseServerSettings")
    print("  - Optional: Tags (as dict, not list)")
    print("\ndelete_license_server_endpoint:")
    print("  - Required: LicenseServerEndpointArn, ServerType")
    print("\nlist_license_server_endpoints:")
    print("  - Optional: IdentityProviderArn, MaxResults, NextToken")
    print("\n=== PARAMETER CORRECTIONS ===")
    print("1. Use IdentityProviderArn (string) instead of IdentityProvider (object)")
    print("2. Use RdsSalSettings with RdsSalCredentialsProvider structure")
    print("3. Use RDS_SAL as ServerType (not RDS_SAL_LICENSE_SERVER)")
    print("4. Tags should be dict format: {'key': 'value'} not list format")
    print("5. RdsSalSettings requires SecretsManagerCredentialsProvider with SecretId")
    print("6. The secret must contain credentials for Active Directory user administration")
    print("7. DELETE operation requires LicenseServerEndpointArn and ServerType (not IdentityProviderArn and LicenseServerEndpointId)")
    print("\nFor more details on license server endpoint management, please check:")
    print("https://docs.aws.amazon.com/license-manager/latest/userguide/user-subscriptions.html")


if __name__ == '__main__':
    main()
