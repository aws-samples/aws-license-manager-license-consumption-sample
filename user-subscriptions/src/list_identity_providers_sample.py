#!/usr/bin/env python3
"""
AWS License Manager User Subscriptions - Identity Providers Sample

This script demonstrates how to interact with AWS License Manager User Subscriptions
to list and manage identity providers, instances, product subscriptions, and user associations.

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


def list_identity_providers() -> Optional[Dict[str, Any]]:
    """
    List all identity providers.
    
    Returns:
        Dict containing identity providers response or None if error
    """
    client = get_client()
    try:
        response = client.list_identity_providers()
        print('AWS License Manager User Subscriptions - ListIdentityProviders API response:')
        pprint.pprint(response)
        return response
    except Exception as e:
        print(f"Error listing identity providers: {e}")
        return None


def list_identity_providers_paginated() -> None:
    """
    List identity providers with pagination support.
    """
    client = get_client()
    try:
        response = client.list_identity_providers()
        page_count = 1
        
        while True:
            print(f'\n=== Page {page_count} - AWS License Manager User Subscriptions - ListIdentityProviders API response ===')
            pprint.pprint(response)
            
            if 'IdentityProviderSummaries' in response:
                print(f"\nFound {len(response['IdentityProviderSummaries'])} identity providers on this page:")
                for idx, provider_summary in enumerate(response['IdentityProviderSummaries']):
                    print(f"\n--- Identity Provider {idx + 1} (Page {page_count}) ---")
                    display_identity_provider_details(provider_summary)
            
            if "NextToken" in response:
                next_token = response['NextToken']
                response = client.list_identity_providers(NextToken=next_token)
                page_count += 1
            else:
                break
        
        print(f"\nCompleted pagination. Total pages processed: {page_count}")
    except Exception as e:
        print(f"Error in paginated listing: {e}")


def list_user_associations(identity_provider: Dict[str, Any], instance_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    List user associations for a given identity provider and instance.
    
    Args:
        identity_provider: Identity provider configuration
        instance_id: EC2 instance ID (optional, will fetch if not provided)
        
    Returns:
        Dict containing user associations response or None if error
    """
    client = get_client()
    
    if not instance_id:
        print("No InstanceId provided. Fetching instances first to get a valid InstanceId...")
        try:
            instances_response = client.list_instances()
            
            if 'InstanceSummaries' in instances_response and instances_response['InstanceSummaries']:
                instance_id = instances_response['InstanceSummaries'][0]['InstanceId']
                print(f"Using InstanceId: {instance_id}")
            else:
                print("No instances found. Cannot list user associations.")
                return None
        except Exception as e:
            print(f"Error fetching instances: {e}")
            return None
    
    try:
        params = {
            'IdentityProvider': identity_provider,
            'InstanceId': instance_id
        }
        
        response = client.list_user_associations(**params)
        
        while True:
            print('AWS License Manager User Subscriptions - ListUserAssociations API response:')
            pprint.pprint(response)
            
            if "NextToken" in response:
                next_token = response['NextToken']
                params['NextToken'] = next_token
                response = client.list_user_associations(**params)
            else:
                break
                
        return response
    except Exception as e:
        print(f"Error listing user associations: {e}")
        return None


def list_product_subscriptions(identity_provider: Dict[str, Any], product: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    List product subscriptions for a given identity provider.
    
    Args:
        identity_provider: Identity provider configuration
        product: Product name to filter by (optional)
        
    Returns:
        Dict containing product subscriptions response or None if error
    """
    client = get_client()
    
    params = {'IdentityProvider': identity_provider}
    
    if product:
        params['Product'] = product
        print(f"Filtering results for Product: {product}")
    
    try:
        response = client.list_product_subscriptions(**params)
        
        while True:
            print('AWS License Manager User Subscriptions - ListProductSubscriptions API response:')
            pprint.pprint(response)
            
            if "NextToken" in response:
                next_token = response['NextToken']
                params['NextToken'] = next_token
                response = client.list_product_subscriptions(**params)
            else:
                break
                
        return response
    except Exception as e:
        print(f"Error listing product subscriptions: {e}")
        return None


def list_instances(product: Optional[str] = None, status: Optional[str] = None, instance_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    List EC2 instances providing user-based subscriptions.
    
    Args:
        product: Product name to filter by (client-side filtering)
        status: Instance status to filter by
        instance_id: Specific instance ID to filter by
        
    Returns:
        Dict containing instances response or None if error
    """
    client = get_client()
    
    params = {}
    filters = []
    
    if status:
        filters.append({
            'Attribute': 'Status',
            'Operation': 'Equals',
            'Value': status
        })
        print(f"Filtering by Status: {status}")
    
    if instance_id:
        filters.append({
            'Attribute': 'InstanceId',
            'Operation': 'Equals',
            'Value': instance_id
        })
        print(f"Filtering by InstanceId: {instance_id}")
    
    if filters:
        params['Filters'] = filters
    
    if product:
        print(f"Note: Product filtering for '{product}' will be done client-side after receiving results.")
    
    try:
        response = client.list_instances(**params)
        
        while True:
            print('AWS License Manager User Subscriptions - ListInstances API response:')
            
            if product and 'InstanceSummaries' in response:
                filtered_summaries = []
                for summary in response['InstanceSummaries']:
                    if 'Products' in summary and product in summary['Products']:
                        filtered_summaries.append(summary)
                
                filtered_response = response.copy()
                filtered_response['InstanceSummaries'] = filtered_summaries
                print(f"Filtered results for Product '{product}':")
                pprint.pprint(filtered_response)
            else:
                pprint.pprint(response)
            
            if "NextToken" in response:
                next_token = response['NextToken']
                params['NextToken'] = next_token
                response = client.list_instances(**params)
            else:
                break
        
        return response
    except Exception as e:
        print(f"Error listing instances: {e}")
        return None


def display_identity_provider_details(provider_summary: Dict[str, Any]) -> None:
    """
    Display detailed information about an identity provider in a readable format.
    
    Args:
        provider_summary: Identity provider summary from API response
    """
    print(f"ARN: {provider_summary['IdentityProviderArn']}")
    print(f"Product: {provider_summary['Product']}")
    print(f"Status: {provider_summary['Status']}")
    
    identity_provider = provider_summary['IdentityProvider']
    
    if 'ActiveDirectoryIdentityProvider' in identity_provider:
        ad_provider = identity_provider['ActiveDirectoryIdentityProvider']
        print(f"Directory ID: {ad_provider['DirectoryId']}")
        
        if 'ActiveDirectorySettings' in ad_provider:
            ad_settings = ad_provider['ActiveDirectorySettings']
            if 'DomainName' in ad_settings:
                print(f"Domain Name: {ad_settings['DomainName']}")
            if 'DomainIpv4List' in ad_settings:
                print(f"Domain IPv4 List: {ad_settings['DomainIpv4List']}")
            
            if 'DomainNetworkSettings' in ad_settings:
                subnets = ad_settings['DomainNetworkSettings'].get('Subnets', [])
                print(f"Domain Network Subnets: {subnets}")
        
        if 'ActiveDirectoryType' in ad_provider:
            print(f"Active Directory Type: {ad_provider['ActiveDirectoryType']}")
    
    if provider_summary.get('Settings'):
        settings = provider_summary['Settings']
        if 'SecurityGroupId' in settings:
            print(f"Security Group ID: {settings['SecurityGroupId']}")
        if 'Subnets' in settings:
            print(f"Settings Subnets: {settings['Subnets']}")
    
    print("-" * 50)


def list_instances_by_status(status: str) -> Optional[Dict[str, Any]]:
    """
    List instances filtered by status.
    
    Args:
        status: Instance status to filter by
        
    Returns:
        Dict containing filtered instances response or None if error
    """
    return list_instances(status=status)


def list_instances_by_instance_id(instance_id: str) -> Optional[Dict[str, Any]]:
    """
    List instances filtered by instance ID.
    
    Args:
        instance_id: Instance ID to filter by
        
    Returns:
        Dict containing filtered instances response or None if error
    """
    return list_instances(instance_id=instance_id)


def list_product_subscriptions_by_username(identity_provider: Dict[str, Any], username: str) -> Optional[Dict[str, Any]]:
    """
    List product subscriptions filtered by username.
    
    Args:
        identity_provider: Identity provider configuration
        username: Username to filter by
        
    Returns:
        Dict containing filtered product subscriptions response or None if error
    """
    client = get_client()
    
    params = {
        'IdentityProvider': identity_provider,
        'Filters': [
            {
                'Attribute': 'Username',
                'Operation': 'Equals',
                'Value': username
            }
        ]
    }
    
    try:
        response = client.list_product_subscriptions(**params)
        print(f'AWS License Manager User Subscriptions - ListProductSubscriptions filtered by Username={username}:')
        pprint.pprint(response)
        return response
    except Exception as e:
        print(f"Error listing product subscriptions by username: {e}")
        return None


def main() -> None:
    """
    Main function demonstrating AWS License Manager User Subscriptions operations.
    """
    print("Start of the AWS License Manager User Subscriptions samples")
    
    # List all identity providers
    identity_providers_response = list_identity_providers()
    
    if 'IdentityProviderSummaries' in identity_providers_response and identity_providers_response['IdentityProviderSummaries']:
        print("\n==========> Identity Providers Found <==========")
        
        # Display information about each identity provider
        for idx, provider_summary in enumerate(identity_providers_response['IdentityProviderSummaries']):
            print(f"\n--- Identity Provider {idx + 1} ---")
            display_identity_provider_details(provider_summary)
        
        # Get the first identity provider for demonstration
        first_provider_summary = identity_providers_response['IdentityProviderSummaries'][0]
        first_identity_provider = first_provider_summary['IdentityProvider']
        
        print(f"\n=== Using first identity provider for demonstration ===")
        print(f"Provider ARN: {first_provider_summary['IdentityProviderArn']}")
        
        # List all instances
        print(f"\n--- Listing all instances ---")
        instances_response = list_instances()
        
        # List product subscriptions for the first identity provider
        print(f"\n--- Listing product subscriptions ---")
        list_product_subscriptions(first_identity_provider)
        
        # List user associations for the first identity provider
        print(f"\n--- Listing user associations ---")
        if instances_response and 'InstanceSummaries' in instances_response and instances_response['InstanceSummaries']:
            first_instance_id = instances_response['InstanceSummaries'][0]['InstanceId']
            print(f"Using InstanceId: {first_instance_id}")
            list_user_associations(first_identity_provider, first_instance_id)
        else:
            print("No instances found. Cannot list user associations without a valid InstanceId.")
            list_user_associations(first_identity_provider)
        
        # Demonstrate product-specific filtering
        available_products = list(set([summary['Product'] for summary in identity_providers_response['IdentityProviderSummaries']]))
        print(f"\n--- Available products: {available_products} ---")
        
        if available_products:
            sample_product = available_products[0]
            print(f"\n--- Listing product subscriptions filtered by {sample_product} ---")
            list_product_subscriptions(first_identity_provider, sample_product)
            
            print(f"\n--- Listing instances with client-side filtering by {sample_product} ---")
            list_instances(product=sample_product)
        
        # Demonstrate server-side filtering
        print(f"\n--- Demonstrating server-side filtering ---")
        print(f"\n--- Listing instances filtered by Status='ACTIVATED' ---")
        list_instances_by_status('ACTIVATED')
        
    else:
        print("No identity providers found. Please ensure you have configured identity providers in License Manager User Subscriptions.")
    
    print("\nEnd of the AWS License Manager User Subscriptions samples")
    print("\n=== API PARAMETER REFERENCE ===")
    print("list_instances API parameters:")
    print("  - Filters (optional): Status, InstanceId")
    print("  - Filter Operations: Equals, geq, leq")
    print("  - MaxResults (optional)")
    print("  - NextToken (optional)")
    print("  - Note: IdentityProvider is not a valid parameter for list_instances")
    print("\nlist_product_subscriptions API parameters:")
    print("  - IdentityProvider (required)")
    print("  - Product (optional)")
    print("  - Filters (optional): Status, Username, Domain")
    print("  - Filter Operations: Equals, geq, leq")
    print("\nlist_user_associations API parameters:")
    print("  - IdentityProvider (required)")
    print("  - InstanceId (required)")
    print("  - Filters (optional)")
    print("  - Filter Operations: Equals, geq, leq")
    print("\nFor more details, check:")
    print("https://docs.aws.amazon.com/license-manager/latest/userguide/user-subscriptions.html")


if __name__ == '__main__':
    main()
