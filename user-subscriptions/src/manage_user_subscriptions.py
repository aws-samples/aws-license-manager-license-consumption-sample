#!/usr/bin/env python3
"""
AWS License Manager User Subscriptions - User Management Sample

This script demonstrates how to manage user subscriptions in AWS License Manager
User Subscriptions, including starting/stopping subscriptions and associating/
disassociating users with identity providers.

Author: AWS License Manager Team

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


def start_product_subscription(username: str, identity_provider: Dict[str, Any], product: str, domain: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Start a product subscription for a user.
    
    Args:
        username: The user name from the identity provider
        identity_provider: Identity provider configuration dict
        product: Product to subscribe to. Valid values:
                - 'VISUAL_STUDIO_ENTERPRISE'
                - 'VISUAL_STUDIO_PROFESSIONAL' 
                - 'OFFICE_PROFESSIONAL_PLUS'
                - 'REMOTE_DESKTOP_SERVICES'
        domain: Optional domain name (required for some identity providers)
        
    Returns:
        Dict containing subscription response or None if error
    """
    client = get_client()
    
    try:
        # Build the request parameters
        request_params = {
            'IdentityProvider': identity_provider,
            'Product': product,
            'Username': username
        }
        
        # Add domain if provided
        if domain:
            request_params['Domain'] = domain
        
        response = client.start_product_subscription(**request_params)
        
        print(f'AWS License Manager User Subscriptions - StartProductSubscription API response:')
        print(f'User: {username}')
        print(f'Product: {product}')
        if domain:
            print(f'Domain: {domain}')
        pprint.pprint(response)
        return response
        
    except Exception as e:
        print(f"Error starting product subscription for user {username}: {e}")
        print(f"Error details: {str(e)}")
        return None


def stop_product_subscription(username: str, identity_provider: Dict[str, Any], product: str, domain: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Stop a product subscription for a user.
    
    Args:
        username: The user name from the identity provider
        identity_provider: Identity provider configuration dict
        product: Product to unsubscribe from
        domain: Optional domain name (required for some identity providers)
        
    Returns:
        Dict containing unsubscription response or None if error
    """
    client = get_client()
    
    try:
        # Build the request parameters
        request_params = {
            'IdentityProvider': identity_provider,
            'Product': product,
            'Username': username
        }
        
        # Add domain if provided
        if domain:
            request_params['Domain'] = domain
        
        response = client.stop_product_subscription(**request_params)
        
        print(f'AWS License Manager User Subscriptions - StopProductSubscription API response:')
        print(f'User: {username}')
        print(f'Product: {product}')
        if domain:
            print(f'Domain: {domain}')
        pprint.pprint(response)
        return response
        
    except Exception as e:
        print(f"Error stopping product subscription for user {username}: {e}")
        print(f"Error details: {str(e)}")
        return None


def associate_user(username: str, identity_provider: Dict[str, Any], instance_id: str, domain: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Associate a user with an identity provider.
    
    Args:
        username: The user name from the identity provider
        identity_provider: Identity provider configuration dict
        instance_id: The ID of the EC2 instance
        domain: Optional domain name (required for some identity providers)
        
    Returns:
        Dict containing association response or None if error
    """
    client = get_client()
    
    try:
        # Build the request parameters
        request_params = {
            'IdentityProvider': identity_provider,
            'InstanceId': instance_id,
            'Username': username
        }
        
        # Add domain if provided
        if domain:
            request_params['Domain'] = domain
        
        response = client.associate_user(**request_params)
        
        print(f'AWS License Manager User Subscriptions - AssociateUser API response:')
        print(f'User: {username}')
        print(f'Instance ID: {instance_id}')
        if domain:
            print(f'Domain: {domain}')
        pprint.pprint(response)
        return response
        
    except Exception as e:
        print(f"Error associating user {username}: {e}")
        print(f"Error details: {str(e)}")
        return None


def disassociate_user(username: str, identity_provider: Dict[str, Any], instance_id: str, domain: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Disassociate a user from an identity provider.
    
    Args:
        username: The user name from the identity provider
        identity_provider: Identity provider configuration dict
        instance_id: The ID of the EC2 instance
        domain: Optional domain name (required for some identity providers)
        
    Returns:
        Dict containing disassociation response or None if error
    """
    client = get_client()
    
    try:
        # Build the request parameters
        request_params = {
            'IdentityProvider': identity_provider,
            'InstanceId': instance_id,
            'Username': username
        }
        
        # Add domain if provided
        if domain:
            request_params['Domain'] = domain
        
        response = client.disassociate_user(**request_params)
        
        print(f'AWS License Manager User Subscriptions - DisassociateUser API response:')
        print(f'User: {username}')
        print(f'Instance ID: {instance_id}')
        if domain:
            print(f'Domain: {domain}')
        pprint.pprint(response)
        return response
        
    except Exception as e:
        print(f"Error disassociating user {username}: {e}")
        print(f"Error details: {str(e)}")
        return None


def list_user_associations(identity_provider: Dict[str, Any], instance_id: str, max_results: int = 25, next_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    List user associations for an identity provider and instance.
    
    Args:
        identity_provider: Identity provider configuration dict
        instance_id: The ID of the EC2 instance
        max_results: Maximum number of results to return (1-25)
        next_token: Token for pagination
        
    Returns:
        Dict containing list of user associations or None if error
    """
    client = get_client()
    
    try:
        # Build the request parameters
        request_params = {
            'IdentityProvider': identity_provider,
            'InstanceId': instance_id,
            'MaxResults': max_results
        }
        
        # Add next token if provided
        if next_token:
            request_params['NextToken'] = next_token
        
        response = client.list_user_associations(**request_params)
        
        print(f'AWS License Manager User Subscriptions - ListUserAssociations API response:')
        print(f'Instance ID: {instance_id}')
        pprint.pprint(response)
        return response
        
    except Exception as e:
        print(f"Error listing user associations for instance {instance_id}: {e}")
        print(f"Error details: {str(e)}")
        return None


def list_product_subscriptions(identity_provider: Dict[str, Any], product: str, max_results: int = 25, next_token: Optional[str] = None, filters: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    """
    List product subscriptions for an identity provider and product.
    
    Args:
        identity_provider: Identity provider configuration dict
        product: Product to list subscriptions for
        max_results: Maximum number of results to return (1-25)
        next_token: Token for pagination
        filters: Optional list of filters to apply
        
    Returns:
        Dict containing list of product subscriptions or None if error
    """
    client = get_client()
    
    try:
        # Build the request parameters
        request_params = {
            'IdentityProvider': identity_provider,
            'Product': product,
            'MaxResults': max_results
        }
        
        # Add optional parameters
        if next_token:
            request_params['NextToken'] = next_token
        if filters:
            request_params['Filters'] = filters
        
        response = client.list_product_subscriptions(**request_params)
        
        print(f'AWS License Manager User Subscriptions - ListProductSubscriptions API response:')
        print(f'Product: {product}')
        pprint.pprint(response)
        return response
        
    except Exception as e:
        print(f"Error listing product subscriptions for {product}: {e}")
        print(f"Error details: {str(e)}")
        return None


def list_instances(identity_provider: Dict[str, Any], max_results: int = 25, next_token: Optional[str] = None, filters: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    """
    List instances associated with an identity provider.
    
    Args:
        identity_provider: Identity provider configuration dict
        max_results: Maximum number of results to return (1-25)
        next_token: Token for pagination
        filters: Optional list of filters to apply
        
    Returns:
        Dict containing list of instances or None if error
    """
    client = get_client()
    
    try:
        # Build the request parameters
        request_params = {
            'IdentityProvider': identity_provider,
            'MaxResults': max_results
        }
        
        # Add optional parameters
        if next_token:
            request_params['NextToken'] = next_token
        if filters:
            request_params['Filters'] = filters
        
        response = client.list_instances(**request_params)
        
        print(f'AWS License Manager User Subscriptions - ListInstances API response:')
        pprint.pprint(response)
        return response
        
    except Exception as e:
        print(f"Error listing instances: {e}")
        print(f"Error details: {str(e)}")
        return None


# Helper functions
def create_identity_provider(directory_id: str, directory_type: str = 'AWS_MANAGED') -> Dict[str, Any]:
    """
    Create an identity provider configuration.
    
    Args:
        directory_id: The Directory Service directory ID
        directory_type: Type of Active Directory ('AWS_MANAGED' or 'SELF_MANAGED')
        
    Returns:
        Dict containing identity provider configuration
    """
    return {
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': directory_id,
            'ActiveDirectoryType': directory_type
        }
    }


def create_filter(attribute: str, operation: str, value: str) -> Dict[str, Any]:
    """
    Create a filter for list operations.
    
    Args:
        attribute: The attribute to filter on
        operation: The operation to perform (e.g., 'Equals', 'Contains')
        value: The value to filter by
        
    Returns:
        Dict containing filter configuration
    """
    return {
        'Attribute': attribute,
        'Operation': operation,
        'Value': value
    }


# Sample demonstrations
def demonstrate_visual_studio_subscription():
    """
    Demonstrate starting a Visual Studio subscription (async operation).
    This should be run separately from association operations.
    """
    print("\n=== Visual Studio Subscription Demo ===")
    
    # Configuration
    directory_id = 'd-1234567890'
    username = 'testuser1'
    domain = 'example.com'
    product = 'VISUAL_STUDIO_PROFESSIONAL'
    
    # Create identity provider
    identity_provider = create_identity_provider(directory_id, 'AWS_MANAGED')
    
    print(f"Starting subscription for user: {username}")
    print(f"Product: {product}")
    print(f"Domain: {domain}")
    print("⚠️  Note: This is an async operation - subscription may take time to become active")
    
    # Start product subscription
    print("\n--- Starting Product Subscription ---")
    subscription_result = start_product_subscription(
        username=username,
        identity_provider=identity_provider,
        product=product,
        domain=domain
    )
    
    if subscription_result:
        print("✅ Subscription request submitted successfully")
        print("ℹ️  Status: PENDING - subscription is being processed")
        print("ℹ️  Wait for subscription to become ACTIVE before associating with instances")
    else:
        print("❌ Failed to start product subscription")
        return False
    
    # List subscriptions to show current status
    print("\n--- Checking Subscription Status ---")
    subscriptions = list_product_subscriptions(
        identity_provider=identity_provider,
        product=product
    )
    
    if subscriptions and 'ProductUserSummaries' in subscriptions:
        for user_summary in subscriptions['ProductUserSummaries']:
            if user_summary.get('Username') == username:
                status = user_summary.get('Status', 'UNKNOWN')
                print(f"Current subscription status: {status}")
                break
    
    print("\n=== Next Steps ===")
    print("1. Wait for subscription status to become 'ACTIVE'")
    print("2. Run demonstrate_visual_studio_association() to associate with instances")
    print("3. Monitor subscription status using list_product_subscriptions()")
    
    return True


def demonstrate_visual_studio_association():
    """
    Demonstrate associating a Visual Studio user with an instance.
    This should only be run AFTER the subscription is ACTIVE.
    """
    print("\n=== Visual Studio User Association Demo ===")
    
    # Configuration
    directory_id = 'd-1234567890'
    username = 'testuser1@example.com'
    domain = 'example.com'
    instance_id = 'i-1234567890abcdef0'  # Replace with actual instance ID
    
    # Create identity provider
    identity_provider = create_identity_provider(directory_id, 'AWS_MANAGED')
    
    print(f"Associating user: {username}")
    print(f"Instance: {instance_id}")
    print(f"Domain: {domain}")
    print("⚠️  Prerequisites: User must have an ACTIVE subscription first")
    
    # Check subscription status first
    print("\n--- Checking Prerequisites ---")
    subscriptions = list_product_subscriptions(
        identity_provider=identity_provider,
        product='VISUAL_STUDIO_PROFESSIONAL'
    )
    
    user_has_active_subscription = False
    if subscriptions and 'ProductUserSummaries' in subscriptions:
        for user_summary in subscriptions['ProductUserSummaries']:

            if (user_summary.get('Username') == username and 
                user_summary.get('Status') == 'SUBSCRIBED'):
                user_has_active_subscription = True
                print("✅ User has ACTIVE subscription")
                break
    
    if not user_has_active_subscription:
        print("❌ User does not have an ACTIVE subscription")
        print("ℹ️  Run demonstrate_visual_studio_subscription() first and wait for ACTIVE status")
        return False
    
    # Associate user with instance
    print("\n--- Associating User with Instance ---")
    association_result = associate_user(
        username=username,
        identity_provider=identity_provider,
        instance_id=instance_id,
        domain=domain
    )
    
    if association_result:
        print("✅ User association request submitted successfully")
        print("ℹ️  Status: Association is being processed (async operation)")
    else:
        print("❌ Failed to associate user with instance")
        return False
    
    # List user associations to show current status
    print("\n--- Checking Association Status ---")
    associations = list_user_associations(
        identity_provider=identity_provider,
        instance_id=instance_id
    )
    
    if associations and 'InstanceUserSummaries' in associations:
        for user_summary in associations['InstanceUserSummaries']:
            if user_summary.get('Username') == username:
                status = user_summary.get('Status', 'UNKNOWN')
                print(f"Current association status: {status}")
                break
    
    print("\n=== Association Complete ===")
    print("• User can now access Visual Studio on the associated instance")
    print("• Monitor association status using list_user_associations()")
    
    return True


def demonstrate_status_monitoring():
    """
    Demonstrate how to monitor subscription and association status.
    Use this to check the progress of async operations.
    """
    print("\n=== Status Monitoring Demo ===")
    
    # Configuration
    directory_id = 'd-1234567890'
    username = 'testuser1'
    domain = 'example.com'
    product = 'VISUAL_STUDIO_PROFESSIONAL'
    instance_id = 'i-1234567890abcdef0'
    
    # Create identity provider
    identity_provider = create_identity_provider(directory_id, 'AWS_MANAGED')
    
    print(f"Monitoring status for user: {username}")
    print(f"Product: {product}")
    print(f"Instance: {instance_id}")
    
    # Check subscription status
    print("\n--- Checking Subscription Status ---")
    subscriptions = list_product_subscriptions(
        identity_provider=identity_provider,
        product=product
    )
    
    subscription_status = "NOT_FOUND"
    if subscriptions and 'ProductUserSummaries' in subscriptions:
        for user_summary in subscriptions['ProductUserSummaries']:
            if user_summary.get('Username') == username:
                subscription_status = user_summary.get('Status', 'UNKNOWN')
                subscription_date = user_summary.get('SubscriptionStartDate', 'N/A')
                print(f"✅ Subscription Status: {subscription_status}")
                print(f"   Start Date: {subscription_date}")
                break
    
    if subscription_status == "NOT_FOUND":
        print("❌ No subscription found for this user")
        return False
    
    # Check association status (only if subscription is active)
    print("\n--- Checking Association Status ---")
    if subscription_status == "ACTIVE":
        associations = list_user_associations(
            identity_provider=identity_provider,
            instance_id=instance_id
        )
        
        association_found = False
        if associations and 'InstanceUserSummaries' in associations:
            for user_summary in associations['InstanceUserSummaries']:
                if user_summary.get('Username') == username:
                    association_status = user_summary.get('Status', 'UNKNOWN')
                    association_date = user_summary.get('AssociationDate', 'N/A')
                    print(f"✅ Association Status: {association_status}")
                    print(f"   Association Date: {association_date}")
                    association_found = True
                    break
        
        if not association_found:
            print("ℹ️  No association found - user may not be associated with this instance yet")
    else:
        print(f"ℹ️  Skipping association check - subscription status is {subscription_status}")
        print("   Association can only be checked when subscription is ACTIVE")
    
    # Provide status interpretation
    print("\n--- Status Interpretation ---")
    print("Subscription Status:")
    print("  • PENDING: Subscription is being processed")
    print("  • ACTIVE: Subscription is ready, user can be associated with instances")
    print("  • INACTIVE: Subscription has been stopped")
    print("  • FAILED: Subscription failed to activate")
    
    print("\nAssociation Status:")
    print("  • ASSOCIATING: Association is being processed")
    print("  • ASSOCIATED: User is successfully associated with the instance")
    print("  • DISASSOCIATING: Association is being removed")
    print("  • DISASSOCIATED: User is no longer associated with the instance")
    
    return True
    """
    Demonstrate user management workflow for Remote Desktop Services.
    
    Note: RDS only uses user subscriptions, NOT user associations with instances.
    RDS licensing is managed at the subscription level, not per-instance.
    """
    print("\n=== Remote Desktop Services User Management Demo ===")
    
    # Configuration for self-managed AD
    username = 'testuser2@corp.example.com'
    domain = 'corp.example.com'
    product = 'REMOTE_DESKTOP_SERVICES'
    
    # Create identity provider for self-managed AD
    identity_provider = {
        'ActiveDirectoryIdentityProvider': {
            'ActiveDirectoryType': 'SELF_MANAGED',
            'DirectoryId': 'sd-1234567890',  # This would be auto-generated from registration
            'ActiveDirectorySettings': {
                'DomainName': domain,
                'DomainIpv4List': ['10.0.0.18', '10.0.0.124'],
                'DomainNetworkSettings': {
                    'Subnets': ['subnet-12345678', 'subnet-87654321']
                },
                'DomainCredentialsProvider': {
                    'SecretsManagerCredentialsProvider': {
                        'SecretId': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:license-manager-user-subscription-mad-admin-AbCdEf'
                    }
                }
            }
        }
    }
    
    print(f"Managing RDS user: {username}")
    print(f"Product: {product}")
    print(f"Domain: {domain}")
    print("Note: RDS does not require instance associations")
    
    # Start RDS subscription (this is all that's needed for RDS)
    print("\n--- Starting RDS Product Subscription ---")
    subscription_result = start_product_subscription(
        username=username,
        identity_provider=identity_provider,
        product=product,
        domain=domain
    )
    
    if subscription_result:
        print("✅ RDS subscription started successfully")
        print("ℹ️  RDS licensing is now active for this user across all RDS resources")
    else:
        print("❌ Failed to start RDS subscription")
        return False
    
    # List RDS subscriptions to verify
    print("\n--- Listing RDS Product Subscriptions ---")
    subscriptions = list_product_subscriptions(
        identity_provider=identity_provider,
        product=product
    )
    
    if subscriptions:
        print("✅ Successfully retrieved RDS subscriptions")
    else:
        print("❌ Failed to retrieve RDS subscriptions")
    
    print("\n=== RDS User Management Notes ===")
    print("• RDS uses subscription-based licensing, not per-instance licensing")
    print("• Once a user has an RDS subscription, they can access RDS on any configured server")
    print("• No need to associate users with specific EC2 instances for RDS")
    print("• RDS licensing is managed through Active Directory group membership")
    print("• Users with RDS subscriptions can connect to any RDS-enabled server in the domain")
    
    return True


def demonstrate_bulk_user_start_subscription_operations():
    """
    Demonstrate bulk user operations for multiple users.
    """
    print("\n=== Bulk User Operations Demo ===")
    
    # Configuration
    directory_id = 'd-1234567890'
    domain = 'example.com'
    product = 'VISUAL_STUDIO_PROFESSIONAL'
    
    # List of users to manage
    users = [
        'testuser1',
        'testuser2',
        'maduser3'
    ]
    
    # Create identity provider
    identity_provider = create_identity_provider(directory_id, 'AWS_MANAGED')
    
    print(f"Managing {len(users)} users for {product}")
    
    successful_subscriptions = []
    failed_subscriptions = []
    
    # Start subscriptions for all users
    print("\n--- Starting Bulk Start Product Subscriptions ---")
    for username in users:
        print(f"\nProcessing user: {username}")
        result = start_product_subscription(
            username=username,
            identity_provider=identity_provider,
            product=product,
            domain=domain
        )
        
        if result:
            successful_subscriptions.append(username)
            print(f" Subscription started for {username}")
        else:
            failed_subscriptions.append(username)
            print(f" Failed to start subscription for {username}")
    
    # Summary
    print(f"\n=== Bulk Operations Summary ===")
    print(f"Successful subscriptions: {len(successful_subscriptions)}")
    print(f"Failed subscriptions: {len(failed_subscriptions)}")
    
    if successful_subscriptions:
        print("Successful users:")
        for user in successful_subscriptions:
            print(f"  - {user}")
    
    if failed_subscriptions:
        print("Failed users:")
        for user in failed_subscriptions:
            print(f"  - {user}")
    
    return len(successful_subscriptions) > 0

def demonstrate_bulk_stop_user_subscription_operations():
    """
    Demonstrate bulk user operations for multiple users.
    """
    print("\n=== Bulk User Operations Demo ===")

    # Configuration
    directory_id = 'd-1234567890'
    domain = 'example.com'
    product = 'VISUAL_STUDIO_PROFESSIONAL'

    # List of users to manage
    users = [
        'testuser1',
        'testuser2',
        'maduser3'
    ]

    # Create identity provider
    identity_provider = create_identity_provider(directory_id, 'AWS_MANAGED')

    print(f"Managing {len(users)} users for {product}")

    successful_subscriptions = []
    failed_subscriptions = []

    # Start subscriptions for all users
    print("\n--- Starting Bulk Stop Product Subscriptions ---")
    for username in users:
        print(f"\nProcessing user: {username}")
        result = stop_product_subscription(
            username=username,
            identity_provider=identity_provider,
            product=product,
            domain=domain
        )

        if result:
            successful_subscriptions.append(username)
            print(f" Subscription stopped for {username}")
        else:
            failed_subscriptions.append(username)
            print(f" Failed to stop subscription for {username}")

    # Summary
    print(f"\n=== Bulk Operations Summary ===")
    print(f"Successful subscriptions: {len(successful_subscriptions)}")
    print(f"Failed subscriptions: {len(failed_subscriptions)}")

    if successful_subscriptions:
        print("Successful users:")
        for user in successful_subscriptions:
            print(f"  - {user}")

    if failed_subscriptions:
        print("Failed users:")
        for user in failed_subscriptions:
            print(f"  - {user}")

    return len(successful_subscriptions) > 0


def demonstrate_visual_studio_disassociation():
    """
    Demonstrate disassociating a Visual Studio user from an instance (async operation).
    This should be run before stopping the subscription.
    """
    print("\n=== Visual Studio User Disassociation Demo ===")
    
    # Configuration
    directory_id = 'd-1234567890'
    username = 'testuser1@example.com'
    domain = 'example.com'
    instance_id = 'i-1234567890abcdef0'
    
    # Create identity provider
    identity_provider = create_identity_provider(directory_id, 'AWS_MANAGED')
    
    print(f"Disassociating user: {username}")
    print(f"Instance: {instance_id}")
    print(f"Domain: {domain}")
    print("⚠️  Prerequisites: User must be currently ASSOCIATED with the instance")
    
    # Check association status first
    print("\n--- Checking Prerequisites ---")
    associations = list_user_associations(
        identity_provider=identity_provider,
        instance_id=instance_id
    )
    
    user_is_associated = False
    if associations and 'InstanceUserSummaries' in associations:
        for user_summary in associations['InstanceUserSummaries']:
            if (user_summary.get('Username') == username and 
                user_summary.get('Status') == 'ASSOCIATED'):
                user_is_associated = True
                print("✅ User is currently ASSOCIATED with instance")
                break
    
    if not user_is_associated:
        print("❌ User is not currently ASSOCIATED with this instance")
        print("ℹ️  Check association status or skip disassociation step")
        return False
    
    # Disassociate user from instance
    print("\n--- Disassociating User from Instance ---")
    disassociation_result = disassociate_user(
        username=username,
        identity_provider=identity_provider,
        instance_id=instance_id,
        domain=domain
    )
    
    if disassociation_result:
        print("✅ Disassociation request submitted successfully")
        print("ℹ️  Status: DISASSOCIATING - operation is being processed (async)")
    else:
        print("❌ Failed to disassociate user from instance")
        return False
    
    # Check disassociation status
    print("\n--- Checking Disassociation Status ---")
    associations = list_user_associations(
        identity_provider=identity_provider,
        instance_id=instance_id
    )
    
    if associations and 'InstanceUserSummaries' in associations:
        for user_summary in associations['InstanceUserSummaries']:
            if user_summary.get('Username') == username:
                status = user_summary.get('Status', 'UNKNOWN')
                print(f"Current disassociation status: {status}")
                break
    
    print("\n=== Next Steps ===")
    print("1. Wait for disassociation status to become 'DISASSOCIATED'")
    print("2. Run demonstrate_subscription_stop() to stop the subscription")
    print("3. Monitor disassociation status using list_user_associations()")
    
    return True


def demonstrate_subscription_stop():
    """
    Demonstrate stopping a product subscription (async operation).
    This should only be run AFTER disassociation is complete (for Visual Studio/Office).
    """
    print("\n=== Product Subscription Stop Demo ===")
    
    # Configuration
    directory_id = 'd-1234567890'
    username = 'testuser1@example.com'
    domain = 'example.com'
    product = 'VISUAL_STUDIO_PROFESSIONAL'
    
    # Create identity provider
    identity_provider = create_identity_provider(directory_id, 'AWS_MANAGED')
    
    print(f"Stopping subscription for user: {username}")
    print(f"Product: {product}")
    print(f"Domain: {domain}")
    print("⚠️  Prerequisites: User should be disassociated from instances first (for VS/Office)")
    
    # Check subscription status first
    print("\n--- Checking Current Subscription Status ---")
    subscriptions = list_product_subscriptions(
        identity_provider=identity_provider,
        product=product
    )
    
    user_has_active_subscription = False
    if subscriptions and 'ProductUserSummaries' in subscriptions:
        for user_summary in subscriptions['ProductUserSummaries']:
            if (user_summary.get('Username') == username and 
                user_summary.get('Status') == 'SUBSCRIBED'):
                user_has_active_subscription = True
                print("✅ User has ACTIVE subscription")
                break
    
    if not user_has_active_subscription:
        print("❌ User does not have an ACTIVE subscription")
        print("ℹ️  Subscription may already be stopped or never existed")
        return False
    
    # Stop product subscription
    print("\n--- Stopping Product Subscription ---")
    stop_result = stop_product_subscription(
        username=username,
        identity_provider=identity_provider,
        product=product,
        domain=domain
    )
    
    if stop_result:
        print("✅ Subscription stop request submitted successfully")
        print("ℹ️  Status: Subscription is being stopped (async operation)")
    else:
        print("❌ Failed to stop product subscription")
        return False
    
    # Check subscription status after stop request
    print("\n--- Checking Subscription Status After Stop ---")
    subscriptions = list_product_subscriptions(
        identity_provider=identity_provider,
        product=product
    )
    
    if subscriptions and 'ProductUserSummaries' in subscriptions:
        for user_summary in subscriptions['ProductUserSummaries']:
            if user_summary.get('Username') == username:
                status = user_summary.get('Status', 'UNKNOWN')
                print(f"Current subscription status: {status}")
                break
    
    print("\n=== Subscription Stop Complete ===")
    print("• Monitor subscription status using list_product_subscriptions()")
    print("• Subscription should transition to INACTIVE status")
    print("• User will no longer have access to the product")
    
    return True
    
    print("\n=== Cleanup Demo Completed ===")
    return True


def demonstrate_rds_subscription_cleanup():
    """
    Demonstrate how to clean up RDS user subscriptions.
    Note: RDS only requires stopping the subscription, no instance disassociation needed.
    """
    print("\n=== RDS Subscription Cleanup Demo ===")
    
    # Configuration for self-managed AD
    username = 'testuser2@corp.example.com'
    domain = 'corp.example.com'
    product = 'REMOTE_DESKTOP_SERVICES'
    
    # Create identity provider for self-managed AD
    identity_provider = {
        'ActiveDirectoryIdentityProvider': {
            'ActiveDirectoryType': 'SELF_MANAGED',
            'DirectoryId': 'sd-1234567890',
            'ActiveDirectorySettings': {
                'DomainName': domain,
                'DomainIpv4List': ['10.0.0.18', '10.0.0.124'],
                'DomainNetworkSettings': {
                    'Subnets': ['subnet-12345678', 'subnet-87654321']
                },
                'DomainCredentialsProvider': {
                    'SecretsManagerCredentialsProvider': {
                        'SecretId': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:license-manager-user-subscription-mad-admin-AbCdEf'
                    }
                }
            }
        }
    }
    
    print(f"Cleaning up RDS subscription for user: {username}")
    print("Note: RDS only requires stopping the subscription - no instance disassociation")
    
    # Stop RDS product subscription (this is all that's needed for RDS)
    print("\n--- Stopping RDS Product Subscription ---")
    stop_result = stop_product_subscription(
        username=username,
        identity_provider=identity_provider,
        product=product,
        domain=domain
    )
    
    if stop_result:
        print("✅ RDS subscription stopped successfully")
        print("ℹ️  User no longer has RDS licensing across all RDS resources")
    else:
        print("❌ Failed to stop RDS subscription")
    
    print("\n=== RDS Cleanup Notes ===")
    print("• RDS cleanup only requires stopping the subscription")
    print("• No need to disassociate from specific instances")
    print("• User will lose RDS access across all servers in the domain")
    print("• Cleanup is simpler than Visual Studio/Office products")
    
    return True


def demonstrate_advanced_filtering():
    """
    Demonstrate advanced filtering capabilities for listing operations.
    """
    print("\n=== Advanced Filtering Demo ===")
    
    # Configuration
    directory_id = 'd-1234567890'
    product = 'VISUAL_STUDIO_PROFESSIONAL'
    
    # Create identity provider
    identity_provider = create_identity_provider(directory_id, 'AWS_MANAGED')
    
    # Example filters
    filters = [
        create_filter('Username', 'Contains', 'maduser'),
        create_filter('Status', 'Equals', 'UNSUBSCRIBED')
    ]
    
    print("Using filters:")
    for filter_item in filters:
        print(f"  - {filter_item['Attribute']} {filter_item['Operation']} '{filter_item['Value']}'")
    
    # List product subscriptions with filters
    print("\n--- Listing Product Subscriptions with Filters ---")
    filtered_subscriptions = list_product_subscriptions(
        identity_provider=identity_provider,
        product=product,
        filters=filters
    )
    
    if filtered_subscriptions:
        print(" Successfully retrieved filtered subscriptions")
    else:
        print(" Failed to retrieve filtered subscriptions")
    
    # List instances with filters
    print("\n--- Listing Instances with Filters ---")
    instance_filters = [
        create_filter('Status', 'Equals', 'ACTIVE')
    ]
    
    filtered_instances = list_instances(
        identity_provider=identity_provider,
        filters=instance_filters
    )
    
    if filtered_instances:
        print("✅ Successfully retrieved filtered instances")
    else:
        print("❌ Failed to retrieve filtered instances")
    
    return True


def check_permissions() -> bool:
    """
    Check if we have the necessary permissions for user management operations.
    
    Returns:
        bool: True if permissions are available, False otherwise
    """
    client = get_client()
    
    try:
        # Try to list identity providers as a permission check
        response = client.list_identity_providers()
        print("✅ License Manager User Subscriptions permissions verified")
        return True
    except Exception as e:
        print(f" Permission check failed: {e}")
        print("Make sure you have the following IAM permissions:")
        print("- license-manager-user-subscriptions:StartProductSubscription")
        print("- license-manager-user-subscriptions:StopProductSubscription")
        print("- license-manager-user-subscriptions:AssociateUser")
        print("- license-manager-user-subscriptions:DisassociateUser")
        print("- license-manager-user-subscriptions:ListUserAssociations")
        print("- license-manager-user-subscriptions:ListProductSubscriptions")
        print("- license-manager-user-subscriptions:ListInstances")
        print("- license-manager-user-subscriptions:ListIdentityProviders")
        return False


def main() -> None:
    """
    Main function demonstrating user management operations.
    """
    print("AWS License Manager User Subscriptions - User Management Sample")
    print("=" * 70)
    
    # Check permissions first
    print("\n=== Checking Permissions ===")
    if not check_permissions():
        print(" Insufficient permissions. Please check your IAM configuration.")
        return
    
    # List current identity providers
    print("\n=== Current Identity Providers ===")
    client = get_client()
    try:
        response = client.list_identity_providers()
        if response.get('IdentityProviderSummaries'):
            for provider in response['IdentityProviderSummaries']:
                print(f"Product: {provider['Product']}, Status: {provider['Status']}")
        else:
            print("No identity providers found. Please register identity providers first.")
            return
    except Exception as e:
        print(f"Error listing identity providers: {e}")
        return
    
    # Run demonstrations
    print("\n" + "=" * 70)
    print("RUNNING USER MANAGEMENT DEMONSTRATIONS")
    print("=" * 70)
    
    # Note: These are examples - uncomment to run actual operations
    print("\n  IMPORTANT: The following demonstrations are examples.")
    print("   Uncomment the function calls to run actual operations.")
    print("   Make sure to update usernames, instance IDs, and other parameters.")
    
    # Example 1: Visual Studio subscription management
    print("\n--- Example 1: Visual Studio Subscription Management ---")
    print("# demonstrate_visual_studio_subscription()  # Start subscription (async)")
    print("# demonstrate_status_monitoring()  # Check subscription status")
    print("# demonstrate_visual_studio_association()  # Associate with instance (after ACTIVE)")

    
    # Example 2: RDS user management  
    print("\n--- Example 2: Remote Desktop Services User Management ---")
    print("# demonstrate_rds_user_management()  # RDS only needs subscription")
    
    # Example 3: Bulk operations
    print("\n--- Example 3: Bulk User Operations ---")
    print("# demonstrate_bulk_start_user_subscription_operations()")
    print("# demonstrate_bulk_stop_user_subscription_operations()")
    #demonstrate_bulk_stop_user_subscription_operations()
    
    # Example 4: Cleanup operations (separate async steps)
    print("\n--- Example 4: Cleanup Operations ---")
    print("# demonstrate_visual_studio_disassociation()  # Step 1: Disassociate (async)")
    print("# demonstrate_status_monitoring()  # Check disassociation status")
    print("# demonstrate_subscription_stop()  # Step 2: Stop subscription (async)")
    print("# demonstrate_rds_subscription_cleanup()  # For RDS (subscription stop only)")
    #demonstrate_subscription_stop()
    #demonstrate_status_monitoring()

    # Example 5: Advanced filtering
    print("\n--- Example 5: Advanced Filtering ---")
    print("# demonstrate_advanced_filtering()")
    demonstrate_advanced_filtering()
    
    print("\n" + "=" * 70)
    print("USAGE EXAMPLES")
    print("=" * 70)
    
    print("\n1. Start a product subscription (async):")
    print("   identity_provider = create_identity_provider('d-1234567890')")
    print("   start_product_subscription(")
    print("       username='user@domain.com',")
    print("       identity_provider=identity_provider,")
    print("       product='VISUAL_STUDIO_PROFESSIONAL',")
    print("       domain='domain.com'")
    print("   )")
    print("   # Wait for subscription to become ACTIVE")
    
    print("\n2. Monitor subscription status:")
    print("   list_product_subscriptions(")
    print("       identity_provider=identity_provider,")
    print("       product='VISUAL_STUDIO_PROFESSIONAL'")
    print("   )")
    print("   # Check Status field in response")
    
    print("\n3. Associate user with instance (after subscription is ACTIVE):")
    print("   associate_user(")
    print("       username='user@domain.com',")
    print("       identity_provider=identity_provider,")
    print("       instance_id='i-1234567890abcdef0',")
    print("       domain='domain.com'")
    print("   )")
    
    print("\n4. Monitor association status:")
    print("   list_user_associations(")
    print("       identity_provider=identity_provider,")
    print("       instance_id='i-1234567890abcdef0'")
    print("   )")
    
    print("\n5. Cleanup operations (separate async steps):")
    print("   # For Visual Studio/Office - Step 1: Disassociate")
    print("   disassociate_user(...)  # Async operation")
    print("   # Wait for disassociation to complete (DISASSOCIATED status)")
    print("   # Step 2: Stop subscription")
    print("   stop_product_subscription(...)  # Async operation")
    print("   # For RDS - Single step:")
    print("   stop_product_subscription(...)  # Async operation (no disassociation needed)")
    
    print("\n" + "=" * 70)
    print("IMPORTANT NOTES")
    print("=" * 70)
    print("1. ⚠️  ALL OPERATIONS ARE ASYNCHRONOUS:")
    print("   - Subscriptions: PENDING → ACTIVE (may take several minutes)")
    print("   - Associations: ASSOCIATING → ASSOCIATED")
    print("   - Disassociations: DISASSOCIATING → DISASSOCIATED")
    print("   - Always check status before proceeding to next step")
    print("2. Ensure identity providers are registered before managing users")
    print("3. Replace example usernames, instance IDs, and domains with actual values")
    print("4. Users must exist in your Active Directory")
    print("5. Workflow order matters:")
    print("   - Start subscription → Wait for ACTIVE → Associate with instance")
    print("   - Disassociate from instance → Wait for completion → Stop subscription")
    print("6. Different products have different workflows:")
    print("   - Visual Studio/Office: Require instance associations + subscriptions")
    print("   - RDS: Only requires subscriptions (no instance associations)")
    print("7. Product-specific requirements:")
    print("   - Visual Studio: Windows instances with Visual Studio installed")
    print("   - Office: Windows instances with Office installed")
    print("   - RDS: RDS-enabled servers (subscription-based licensing)")
    print("8. RDS licensing differences:")
    print("   - RDS uses domain-wide subscription licensing")
    print("   - Users with RDS subscriptions can access any RDS server in the domain")
    print("   - No need to associate users with specific EC2 instances")
    print("9. Monitor costs - each subscription may incur charges")
    print("10. Use bulk operations for managing multiple users efficiently")
    print("11. Always clean up unused subscriptions to avoid unnecessary costs")
    print("12. Status monitoring is crucial:")
    print("    - Use list_product_subscriptions() to check subscription status")
    print("    - Use list_user_associations() to check association status")
    print("    - Wait for operations to complete before proceeding")
    print("13. Cleanup procedures are separate async operations:")
    print("    - Visual Studio/Office:")
    print("      1. Disassociate from instance (async) → Wait for DISASSOCIATED")
    print("      2. Stop subscription (async) → Wait for INACTIVE")
    print("    - RDS: Stop subscription only (async) → Wait for INACTIVE")
    print("14. Never run cleanup operations simultaneously:")
    print("    - Always wait for disassociation to complete before stopping subscription")
    print("    - Monitor each step independently")
    
    print("\nFor more details on user subscription management, please check:")
    print("https://docs.aws.amazon.com/license-manager/latest/userguide/user-subscriptions.html")


if __name__ == '__main__':
    main()
