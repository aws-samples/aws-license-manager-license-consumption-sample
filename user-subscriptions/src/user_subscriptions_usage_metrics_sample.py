#!/usr/bin/env python3
"""
AWS License Manager User Subscriptions - Usage Metrics Sample

This script demonstrates how to generate comprehensive usage metrics and reports
for AWS License Manager User Subscriptions, including product subscription metrics,
instance usage statistics, and user association analysis.

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


def get_user_association_details(identity_provider: Dict[str, Any], username: str, instance_id: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed user association information for a specific user and instance.
    
    Args:
        identity_provider: Identity provider configuration
        username: Username to query
        instance_id: EC2 instance ID
        
    Returns:
        Dict containing user association details or None if error
    """
    client = get_client()
    
    try:
        response = client.list_user_associations(
            IdentityProvider=identity_provider,
            InstanceId=instance_id,
            Filters=[
                {
                    'Attribute': 'Username',
                    'Operation': 'Equals',
                    'Value': username
                }
            ]
        )
        print(f'User Association Details for {username} on {instance_id}:')
        pprint.pprint(response)
        return response
    except Exception as e:
        print(f"Error retrieving user association details: {e}")
        return None


def get_product_subscription_metrics(identity_provider: Dict[str, Any], product: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Calculate and display product subscription usage metrics.
    
    Args:
        identity_provider: Identity provider configuration
        product: Specific product to analyze (optional)
        
    Returns:
        Dict containing product metrics summary or None if error
    """
    client = get_client()
    
    params = {'IdentityProvider': identity_provider}
    
    if product:
        params['Product'] = product
        print(f"Filtering for Product: {product}")
    
    try:
        response = client.list_product_subscriptions(**params)
        
        # Initialize metrics counters
        total_subscriptions = 0
        active_subscriptions = 0
        products_summary = {}
        
        while True:
            if 'ProductUserSummaries' in response:
                for summary in response['ProductUserSummaries']:
                    product_name = summary.get('Product', 'Unknown')
                    status = summary.get('Status', 'Unknown')
                    
                    if product_name not in products_summary:
                        products_summary[product_name] = {'total': 0, 'active': 0}
                    
                    products_summary[product_name]['total'] += 1
                    total_subscriptions += 1
                    
                    if status == 'SUBSCRIBED':
                        products_summary[product_name]['active'] += 1
                        active_subscriptions += 1
            
            if "NextToken" in response:
                params['NextToken'] = response['NextToken']
                response = client.list_product_subscriptions(**params)
            else:
                break
        
        # Display metrics
        print(f'\n--- Product Subscription Usage Metrics ---')
        print(f'Total Subscriptions: {total_subscriptions}')
        print(f'Active Subscriptions: {active_subscriptions}')
        print(f'Inactive Subscriptions: {total_subscriptions - active_subscriptions}')
        print(f'\nBreakdown by Product:')
        
        for product_name, metrics in products_summary.items():
            print(f'  {product_name}:')
            print(f'    Total: {metrics["total"]}')
            print(f'    Active: {metrics["active"]}')
            print(f'    Inactive: {metrics["total"] - metrics["active"]}')
        
        return products_summary
        
    except Exception as e:
        print(f"Error retrieving product subscription metrics: {e}")
        return None


def get_instance_usage_metrics() -> Optional[Dict[str, Any]]:
    """
    Calculate and display instance usage metrics.
    
    Returns:
        Dict containing instance metrics summary or None if error
    """
    client = get_client()
    
    try:
        response = client.list_instances()
        
        # Initialize metrics counters
        total_instances = 0
        instances_by_product = {}
        instances_by_status = {}
        
        while True:
            if 'InstanceSummaries' in response:
                for instance in response['InstanceSummaries']:
                    instance_id = instance.get('InstanceId', 'Unknown')
                    products = instance.get('Products', [])
                    status = instance.get('Status', 'Unknown')
                    
                    total_instances += 1
                    
                    # Count by status
                    if status not in instances_by_status:
                        instances_by_status[status] = 0
                    instances_by_status[status] += 1
                    
                    # Count by product
                    for product in products:
                        if product not in instances_by_product:
                            instances_by_product[product] = 0
                        instances_by_product[product] += 1
            
            if "NextToken" in response:
                response = client.list_instances(NextToken=response['NextToken'])
            else:
                break
        
        # Display metrics
        print(f'\n--- Instance Usage Metrics ---')
        print(f'Total Instances: {total_instances}')
        print(f'\nInstances by Status:')
        for status, count in instances_by_status.items():
            print(f'  {status}: {count}')
        
        print(f'\nInstances by Product:')
        for product, count in instances_by_product.items():
            print(f'  {product}: {count}')
        
        return {
            'total_instances': total_instances,
            'by_status': instances_by_status,
            'by_product': instances_by_product
        }
        
    except Exception as e:
        print(f"Error retrieving instance usage metrics: {e}")
        return None


def generate_usage_summary_report(identity_provider: Dict[str, Any]) -> None:
    """
    Generate a comprehensive usage summary report.
    
    Args:
        identity_provider: Identity provider configuration
    """
    print(f'\n=== Usage Summary Report for Identity Provider ===')
    print(f'Identity Provider: {identity_provider}')
    
    # Get product subscription metrics
    product_metrics = get_product_subscription_metrics(identity_provider)
    
    # Get instance usage metrics
    instance_metrics = get_instance_usage_metrics()
    
    # Generate summary
    print(f'\n--- Summary ---')
    if product_metrics:
        total_products = len(product_metrics)
        print(f'Total Product Types: {total_products}')
    
    if instance_metrics:
        print(f'Total Instances with User Subscriptions: {instance_metrics["total_instances"]}')
    
    print(f'Report Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')


def main() -> None:
    """
    Main function demonstrating usage metrics generation.
    """
    print("Start of the AWS License Manager User Subscriptions Usage Metrics samples")
    
    # Get available identity providers
    client = get_client()
    try:
        identity_providers_response = client.list_identity_providers()
    except Exception as e:
        print(f"Error listing identity providers: {e}")
        return
    
    if 'IdentityProviderSummaries' in identity_providers_response and identity_providers_response['IdentityProviderSummaries']:
        # Use the first identity provider for demonstration
        first_identity_provider_summary = identity_providers_response['IdentityProviderSummaries'][0]
        first_identity_provider = first_identity_provider_summary['IdentityProvider']
        
        print(f"Using identity provider ARN: {first_identity_provider_summary['IdentityProviderArn']}")
        print(f"Product: {first_identity_provider_summary['Product']}")
        print(f"Status: {first_identity_provider_summary['Status']}")
        
        # Generate comprehensive usage metrics
        generate_usage_summary_report(first_identity_provider)
        
        # Get metrics for specific products found in the environment
        available_products = list(set([summary['Product'] for summary in identity_providers_response['IdentityProviderSummaries']]))
        print(f"\n--- Available Products: {available_products} ---")
        
        # Demonstrate metrics for each product (limit to first 2 for demo)
        for product in available_products[:2]:
            print(f"\n--- {product} Specific Metrics ---")
            get_product_subscription_metrics(first_identity_provider, product)
        
        # Example of user association details (if instances are available)
        print(f"\n--- User Association Example ---")
        try:
            instances_response = client.list_instances()
            if 'InstanceSummaries' in instances_response and instances_response['InstanceSummaries']:
                sample_instance_id = instances_response['InstanceSummaries'][0]['InstanceId']
                print(f"Checking user associations for instance: {sample_instance_id}")
                
                # Get user associations for this instance
                user_associations_response = client.list_user_associations(
                    IdentityProvider=first_identity_provider,
                    InstanceId=sample_instance_id
                )
                
                if 'InstanceUserSummaries' in user_associations_response and user_associations_response['InstanceUserSummaries']:
                    sample_username = user_associations_response['InstanceUserSummaries'][0]['Username']
                    get_user_association_details(first_identity_provider, sample_username, sample_instance_id)
                else:
                    print("No user associations found for this instance.")
            else:
                print("No instances available for user association demonstration.")
        except Exception as e:
            print(f"Error in user association example: {e}")
        
    else:
        print("No identity providers found. Please ensure you have configured identity providers in License Manager User Subscriptions.")
    
    print("\nEnd of the AWS License Manager User Subscriptions Usage Metrics samples")
    print("\n=== API INFORMATION ===")
    print("Key API Operations Used:")
    print("- list_instances: Lists EC2 instances with user subscriptions")
    print("- list_product_subscriptions: Lists product subscriptions by identity provider")
    print("- list_user_associations: Lists user associations for specific instances")
    print("- list_identity_providers: Lists configured identity providers")
    print("\nStatus Values:")
    print("- Product Subscriptions: SUBSCRIBED, UNSUBSCRIBED")
    print("- Instances: ACTIVATED, FAILED, TERMINATED")
    print("\nFor more details on user subscriptions, please check:")
    print("https://docs.aws.amazon.com/license-manager/latest/userguide/user-subscriptions.html")


if __name__ == '__main__':
    main()
