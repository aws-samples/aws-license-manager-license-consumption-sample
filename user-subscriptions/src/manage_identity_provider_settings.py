#!/usr/bin/env python3
"""
AWS License Manager User Subscriptions - Identity Provider Management Sample

This script demonstrates how to manage identity providers in AWS License Manager
User Subscriptions, including registration, deregistration, and settings updates.

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


def register_identity_provider(product: str, identity_provider: Dict[str, Any], settings: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Register the identity provider with License Manager User Subscriptions for a specific product.
    
    Args:
        product: Product to associate. Valid values:
                - 'VISUAL_STUDIO_ENTERPRISE'
                - 'VISUAL_STUDIO_PROFESSIONAL' 
                - 'OFFICE_PROFESSIONAL_PLUS'
        identity_provider: Identity provider configuration dict (required). 
                          The caller must create this using create_identity_provider() or similar.
        settings: Optional provider settings dict. 
                 NOTE: Settings are not required for VISUAL_STUDIO_PROFESSIONAL.
                 Only provide if specifically needed for your use case.
        
    Returns:
        Dict containing registration response or None if error
    """
    client = get_client()
    
    try:
        # Settings are not required for VISUAL_STUDIO_PROFESSIONAL
        # Only include Settings if explicitly provided and not None
        if settings is not None:
            response = client.register_identity_provider(
                IdentityProvider=identity_provider,
                Product=product,
                Settings=settings
            )
        else:
            response = client.register_identity_provider(
                IdentityProvider=identity_provider,
                Product=product
            )
        print(f'AWS License Manager User Subscriptions - RegisterIdentityProvider API response for {product}:')
        pprint.pprint(response)
        return response
    except Exception as e:
        print(f"Error registering identity provider with {product}: {e}")
        print(f"Error details: {str(e)}")
        return None


def deregister_identity_provider(identity_provider: Dict[str, Any], product: str) -> Optional[Dict[str, Any]]:
    """
    Deregister an identity provider from License Manager User Subscriptions.
    
    Args:
        identity_provider: Identity provider configuration dict
        product: Product to disassociate
        
    Returns:
        Dict containing deregistration response or None if error
    """
    client = get_client()
    
    try:
        response = client.deregister_identity_provider(
            IdentityProvider=identity_provider,
            Product=product
        )
        print('AWS License Manager User Subscriptions - DeregisterIdentityProvider API response:')
        pprint.pprint(response)
        return response
    except Exception as e:
        print(f"Error deregistering identity provider: {e}")
        return None


def register_self_managed_ad_identity_provider(
    product: str,
    domain_name: str,
    domain_ipv4_list: List[str],
    subnets: List[str],
    secrets_manager_secret_id: str,
    directory_id: Optional[str] = None,
    security_group_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Register a self-managed Active Directory identity provider with License Manager User Subscriptions.
    This function is specifically designed for products that require self-managed AD and settings.
    
    Args:
        product: Product to associate. Valid values are:
                - 'VISUAL_STUDIO_ENTERPRISE'
                - 'VISUAL_STUDIO_PROFESSIONAL' 
                - 'OFFICE_PROFESSIONAL_PLUS'
                - 'REMOTE_DESKTOP_SERVICES'
        domain_name: The domain name for the Active Directory (e.g., 'example.com')
        domain_ipv4_list: List of domain IPv4 addresses for the Active Directory
        subnets: List of subnet IDs for the domain network settings
        secrets_manager_secret_id: The ID of the Secrets Manager secret containing AD credentials
        directory_id: Optional Directory Service directory ID (auto-generated if not provided)
        security_group_id: Optional security group ID for VPC endpoint communication
                          (only used for OFFICE_PROFESSIONAL_PLUS)
        
    Returns:
        Dict containing registration response or None if error
        
    Note:
        - Settings parameter is only required for OFFICE_PROFESSIONAL_PLUS
        - REMOTE_DESKTOP_SERVICES and VISUAL_STUDIO_* products don't use Settings
    """
    client = get_client()
    
    # Create self-managed Active Directory settings
    ad_settings = {
        'DomainCredentialsProvider': {
            'SecretsManagerCredentialsProvider': {
                'SecretId': secrets_manager_secret_id
            }
        },
        'DomainIpv4List': domain_ipv4_list,
        'DomainName': domain_name,
        'DomainNetworkSettings': {
            'Subnets': subnets
        }
    }
    
    # Create identity provider for self-managed AD
    identity_provider = {
        'ActiveDirectoryIdentityProvider': {
            'ActiveDirectoryType': 'SELF_MANAGED',
            'ActiveDirectorySettings': ad_settings
        }
    }
    
    # Add DirectoryId only if provided
    if directory_id:
        identity_provider['ActiveDirectoryIdentityProvider']['DirectoryId'] = directory_id
    
    # Create provider settings only for OFFICE_PROFESSIONAL_PLUS
    provider_settings = None
    if product == 'OFFICE_PROFESSIONAL_PLUS' and security_group_id:
        provider_settings = {
            'SecurityGroupId': security_group_id,
            'Subnets': subnets
        }
    
    try:
        print(f"\n\n----Registering self-managed AD identity provider for {product}...")
        if directory_id:
            print(f"Directory ID: {directory_id}")
        else:
            print("Directory ID: Auto-generated by service")
        print(f"Domain: {domain_name}")
        print(f"Domain IPs: {domain_ipv4_list}")
        print(f"Subnets: {subnets}")
        print(f"Secret ID: {secrets_manager_secret_id}")
        if security_group_id:
            print(f"Security Group: {security_group_id}")
        
        # Settings are only required for OFFICE_PROFESSIONAL_PLUS
        if product == 'OFFICE_PROFESSIONAL_PLUS' and provider_settings:
            print(f"Registering {product} with Settings parameter...")
            response = client.register_identity_provider(
                IdentityProvider=identity_provider,
                Product=product,
                Settings=provider_settings
            )
        else:
            # For REMOTE_DESKTOP_SERVICES, VISUAL_STUDIO_*, no Settings parameter needed
            print(f"Registering {product} without Settings parameter...")
            response = client.register_identity_provider(
                IdentityProvider=identity_provider,
                Product=product
            )
            
        print(f'AWS License Manager User Subscriptions - RegisterIdentityProvider API response for {product}:')
        pprint.pprint(response)
        return response
        
    except Exception as e:
        print(f"Error registering self-managed AD identity provider for {product}: {e}")
        print(f"Error details: {str(e)}")
        return None


def create_self_managed_ad_example():
    """
    Example function showing how to register a self-managed Active Directory identity provider.
    This demonstrates the complete setup required for products that need self-managed AD.
    """
    print("\n=== Self-Managed Active Directory Registration Example ===")
    
    # Example configuration - replace with your actual values
    example_config = {
        'product': 'REMOTE_DESKTOP_SERVICES',  # Valid product that supports self-managed AD
        'domain_name': 'corp.example.com',
        'domain_ipv4_list': ['10.0.1.10', '10.0.1.11'],  # Your domain controller IPs
        'subnets': ['subnet-12345678', 'subnet-87654321'],  # Your VPC subnets
        'secrets_manager_secret_id': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:license-manager-user-subscription-mad-admin-AbCdEf',  # Your secret in Secrets Manager
        'directory_id': None,  # Optional: Auto-generated by service if not provided
        'security_group_id': 'sg-12345678'  # Optional: Security group for VPC endpoints
    }
    
    print("Example configuration for self-managed AD:")
    pprint.pprint(example_config)
    
    print("\nTo use this function, call:")
    print("register_self_managed_ad_identity_provider(")
    print(f"    product='{example_config['product']}',")
    print(f"    domain_name='{example_config['domain_name']}',")
    print(f"    domain_ipv4_list={example_config['domain_ipv4_list']},")
    print(f"    subnets={example_config['subnets']},")
    print(f"    secrets_manager_secret_id='{example_config['secrets_manager_secret_id']}',")
    print(f"    directory_id={example_config['directory_id']},  # Optional")
    print(f"    security_group_id='{example_config['security_group_id']}'")
    print(")")
    
    print("\nNote: Make sure to:")
    print("1. Create a Secrets Manager secret with your AD admin credentials")
    print("2. Ensure your subnets have connectivity to your domain controllers")
    print("3. Configure security groups to allow necessary AD traffic")
    print("4. Replace example values with your actual infrastructure details")
    print("5. DirectoryId is optional - the service can auto-generate it")
    print("6. SecurityGroupId is only used for OFFICE_PROFESSIONAL_PLUS product")
    print("7. REMOTE_DESKTOP_SERVICES and VISUAL_STUDIO_* don't require Settings parameter")
    
    # Uncomment the following line to actually register (ensure you have valid values)
    result = register_self_managed_ad_identity_provider(**example_config)
    return result


def register_rds_sal_identity_provider(
    directory_id: str,
    domain_name: str,
    domain_ipv4_list: List[str],
    subnets: List[str],
    secrets_manager_secret_id: str,
    security_group_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Convenience function specifically for registering Remote Desktop Services SAL (RDSSAL).
    This is a wrapper around register_self_managed_ad_identity_provider for RDS SAL.
    
    Args:
        directory_id: The Directory Service directory ID for self-managed AD
        domain_name: The domain name for the Active Directory
        domain_ipv4_list: List of domain IPv4 addresses for the Active Directory
        subnets: List of subnet IDs for the domain network settings
        secrets_manager_secret_id: The ID of the Secrets Manager secret containing AD credentials
        security_group_id: Optional security group ID for VPC endpoint communication
        
    Returns:
        Dict containing registration response or None if error
    """
    print("\\n=== Registering Remote Desktop Services SAL ===")
    
    # Try different possible product names for RDS SAL
    possible_product_names = [
        'REMOTE_DESKTOP_SERVICES'
    ]
    
    for product_name in possible_product_names:
        print(f"\\nTrying product name: {product_name}")
        result = register_self_managed_ad_identity_provider(
            product=product_name,
            directory_id=directory_id,
            domain_name=domain_name,
            domain_ipv4_list=domain_ipv4_list,
            subnets=subnets,
            secrets_manager_secret_id=secrets_manager_secret_id,
            security_group_id=security_group_id
        )
        
        if result:
            print(f"Successfully registered with product name: {product_name}")
            return result
        else:
            print(f"Failed to register with product name: {product_name}")
    
    print("\\nFailed to register with any of the attempted product names.")
    print("Please check the AWS documentation for the correct product name for RDS SAL.")
    return None
    """
    Update settings for an existing identity provider.
    
    Args:
        identity_provider: Identity provider configuration
        product: Product associated with the identity provider
        settings: New settings to apply
        
    Returns:
        Dict containing update response or None if error
    """
    client = get_client()
    
    try:
        response = client.update_identity_provider_settings(
            IdentityProvider=identity_provider,
            Product=product,
            Settings=settings
        )
        print('AWS License Manager User Subscriptions - UpdateIdentityProviderSettings API response:')
        pprint.pprint(response)
        return response
    except Exception as e:
        print(f"Error updating identity provider settings: {e}")
        return None

# Helper methods
def create_active_directory_settings(domain_name: str, domain_ipv4_list: List[str], subnets: List[str]) -> Dict[str, Any]:
    """
    Create Active Directory settings configuration.
    
    Args:
        domain_name: Active Directory domain name
        domain_ipv4_list: List of domain controller IP addresses
        subnets: List of subnet IDs for domain network settings
        
    Returns:
        Dict containing Active Directory settings
    """
    return {
        'DomainName': domain_name,
        'DomainIpv4List': domain_ipv4_list,
        'DomainNetworkSettings': {
            'Subnets': subnets
        },
        'DomainCredentialsProvider': {
            'SecretsManagerCredentialsProvider': {}
        }
    }


def create_identity_provider_settings(security_group_id: Optional[str] = None, subnets: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Create identity provider settings configuration.
    
    Args:
        security_group_id: Security group ID (optional)
        subnets: List of subnet IDs (optional)
        
    Returns:
        Dict containing identity provider settings
    """
    settings = {}
    
    if security_group_id:
        settings['SecurityGroupId'] = security_group_id
    
    if subnets:
        settings['Subnets'] = subnets
    
    return settings


def create_identity_provider(directory_id: str, directory_type: str = 'AWS_MANAGED', ad_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create an identity provider configuration.
    
    Args:
        directory_id: The Directory Service directory ID
        directory_type: Type of Active Directory ('AWS_MANAGED' or 'SELF_MANAGED')
        ad_settings: Optional Active Directory settings (required for SELF_MANAGED)
        
    Returns:
        Dict containing identity provider configuration
    """
    identity_provider = {
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': directory_id,
            'ActiveDirectoryType': directory_type
        }
    }
    
    # Add ActiveDirectorySettings if provided (typically for SELF_MANAGED)
    if ad_settings:
        identity_provider['ActiveDirectoryIdentityProvider']['ActiveDirectorySettings'] = ad_settings
    
    return identity_provider
    """
    Create identity provider settings configuration.
    
    Args:
        security_group_id: Security group ID (optional)
        subnets: List of subnet IDs (optional)
        
    Returns:
        Dict containing identity provider settings
    """
    settings = {}
    
    if security_group_id:
        settings['SecurityGroupId'] = security_group_id
    
    if subnets:
        settings['Subnets'] = subnets
    
    return settings

# Sample Demonstrations
def demonstrate_active_directory_registration() -> None:
    """
    Register the actual Active Directory identity provider with multiple products.
    """
    print("\n=== Active Directory Identity Provider Registration ===")
    
    # Create the identity provider configuration
    identity_provider = create_identity_provider(
        directory_id='d-1234567890',
        directory_type='AWS_MANAGED'
    )
    
    # Try registering with different products
    products_to_try = [
        'VISUAL_STUDIO_ENTERPRISE',
        'VISUAL_STUDIO_PROFESSIONAL',
        'OFFICE_PROFESSIONAL_PLUS'
    ]
    
    successful_registrations = []
    
    for product in products_to_try:
        print(f"\n--- Trying to register with {product} ---")
        result = register_identity_provider(product, identity_provider)
        
        if result:
            print(f" Successfully registered with {product}!")
            successful_registrations.append(product)
        else:
            print(f" Failed to register with {product}")
    
    if successful_registrations:
        print(f"\n Successfully registered with products: {', '.join(successful_registrations)}")
        return True
    else:
        print("\n Failed to register with any products")
        return False


def demonstrate_settings_update() -> None:
    """
    Demonstrate updating identity provider settings.
    """
    print("\n=== Identity Provider Settings Update Example ===")
    
    # Example identity provider (you would get this from list_identity_providers)
    identity_provider = {
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-1234567890'
        }
    }
    
    # New settings to apply
    new_settings = create_identity_provider_settings(
        security_group_id='sg-new12345',
        subnets=['subnet-new12345', 'subnet-new67890']
    )
    
    print("Example configuration for settings update:")
    print("Identity Provider:")
    pprint.pprint(identity_provider)
    print("\nNew Settings:")
    pprint.pprint(new_settings)
    
    # Note: Uncomment the following line to actually update (ensure you have valid values)
    # update_identity_provider_settings(identity_provider, 'VISUAL_STUDIO_PROFESSIONAL', new_settings)


def list_current_identity_providers() -> Optional[List[Dict[str, Any]]]:
    """
    List currently registered identity providers.
    
    Returns:
        List of identity provider summaries or None if error
    """
    client = get_client()
    
    try:
        response = client.list_identity_providers()
        
        if 'IdentityProviderSummaries' in response:
            print("\n=== Current Identity Providers ===")
            for idx, provider in enumerate(response['IdentityProviderSummaries']):
                print(f"\n--- Identity Provider {idx + 1} ---")
                print(f"ARN: {provider['IdentityProviderArn']}")
                print(f"Product: {provider['Product']}")
                print(f"Status: {provider['Status']}")
                
                if 'Settings' in provider and provider['Settings']:
                    print("Settings:")
                    pprint.pprint(provider['Settings'])
            
            return response['IdentityProviderSummaries']
        else:
            print("No identity providers found.")
            return []
            
    except Exception as e:
        print(f"Error listing identity providers: {e}")
        return None


def check_permissions() -> bool:
    """
    Check if we have the necessary permissions to use License Manager User Subscriptions.
    
    Returns:
        bool: True if permissions are available, False otherwise
    """
    client = get_client()
    
    try:
        # Try to list identity providers as a permission check
        response = client.list_identity_providers()
        print(" License Manager User Subscriptions permissions verified")
        return True
    except Exception as e:
        print(f" Permission check failed: {e}")
        print("Make sure you have the following IAM permissions:")
        print("- license-manager-user-subscriptions:ListIdentityProviders")
        print("- license-manager-user-subscriptions:RegisterIdentityProvider")
        print("- license-manager-user-subscriptions:DeregisterIdentityProvider")
        print("- license-manager-user-subscriptions:UpdateIdentityProviderSettings")
        return False


def register_additional_products() -> None:
    """
    Register the directory with additional products.
    """
    print("\n=== Registering Additional Products ===")
    
    # Real Active Directory configuration using provided directory information
    ad_settings = create_active_directory_settings(
        domain_name='example.com',
        domain_ipv4_list=['172.31.2.252', '172.31.63.122'],
        subnets=['subnet-66245500', 'subnet-7b46c34a']
    )
    
    identity_provider = {
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-1234567890',
            'ActiveDirectorySettings': ad_settings,
            'ActiveDirectoryType': 'AWS_MANAGED'
        }
    }
    
    provider_settings = create_identity_provider_settings(
        security_group_id='sg-05a0262ba60f56a95',
        subnets=['subnet-66245500', 'subnet-7b46c34a']
    )
    
    # Products to register (excluding REMOTE_DESKTOP_SERVICES which is already registered)
    products_to_register = [
        'VISUAL_STUDIO_PROFESSIONAL',
        'OFFICE_PROFESSIONAL_PLUS'
    ]
    
    successful_registrations = []
    
    for product in products_to_register:
        print(f"\n--- Registering with {product} ---")
        result = register_identity_provider(product, identity_provider, provider_settings)
        
        if result:
            print(f" Successfully registered with {product}!")
            successful_registrations.append(product)
        else:
            print(f" Failed to register with {product}")
    
    if successful_registrations:
        print(f"\n Successfully registered with additional products: {', '.join(successful_registrations)}")
        return True
    else:
        print("\n Failed to register with any additional products")
        return False


# Add this at the end of the file before if __name__ == '__main__':
def register_specific_product(product: str) -> bool:
    """
    Register the directory with a specific product.
    
    Args:
        product: The product to register (e.g., 'VISUAL_STUDIO_PROFESSIONAL')
        
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\n=== Registering with {product} ===")
    
    # Real Active Directory configuration using provided directory information
    ad_settings = create_active_directory_settings(
        domain_name='example.com',
        domain_ipv4_list=['172.31.2.252', '172.31.63.122'],
        subnets=['subnet-66245500', 'subnet-7b46c34a']
    )
    
    identity_provider = {
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-1234567890',
            'ActiveDirectorySettings': ad_settings,
            'ActiveDirectoryType': 'AWS_MANAGED'
        }
    }
    
    provider_settings = create_identity_provider_settings(
        security_group_id='sg-05a0262ba60f56a95',
        subnets=['subnet-66245500', 'subnet-7b46c34a']
    )
    
    result = register_identity_provider(product, identity_provider, provider_settings)
    
    if result:
        print(f" Successfully registered with {product}!")
        return True
    else:
        print(f" Failed to register with {product}")
        return False
    """
    Main function demonstrating identity provider management operations.
    """
    print("Start of the AWS License Manager User Subscriptions Identity Provider Management")
    
    # Check permissions first
    print("\n=== Checking Permissions ===")
    if not check_permissions():
        print(" Insufficient permissions. Please check your IAM configuration.")
        return
    
    # List current identity providers first
    print("\n=== Checking Current Identity Providers ===")
    current_providers = list_current_identity_providers()
    
    # Check if our directory is already registered and with which products
    directory_id = 'd-1234567890'
    registered_products = []
    
    if current_providers:
        for provider in current_providers:
            if 'IdentityProvider' in provider:
                ip = provider['IdentityProvider']
                if 'ActiveDirectoryIdentityProvider' in ip:
                    if ip['ActiveDirectoryIdentityProvider'].get('DirectoryId') == directory_id:
                        product = provider.get('Product', 'Unknown')
                        registered_products.append(product)
                        print(f"✅ Directory {directory_id} is registered with product: {product}")
    
    if registered_products:
        print(f"Directory {directory_id} is already registered with products: {', '.join(registered_products)}")
        
        # Ask if user wants to register with additional products
        all_products = ['VISUAL_STUDIO_PROFESSIONAL', 'OFFICE_PROFESSIONAL_PLUS', 'REMOTE_DESKTOP_SERVICES']
        unregistered_products = [p for p in all_products if p not in registered_products]
        
        if unregistered_products:
            print(f"Available products to register: {', '.join(unregistered_products)}")
            print("You can modify the script to register with additional products if needed.")
        else:
            print("Directory is registered with all available products.")
    else:
        print(f"Directory {directory_id} is not registered. Proceeding with registration...")
        # Register the Active Directory identity provider
        result = demonstrate_active_directory_registration()
        
        if result:
            print("\n Registration completed successfully!")
        else:
            print("\n Registration failed. Please check the error messages above.")
    
    # List identity providers again to show current state
    print("\n=== Final Identity Provider Status ===")
    list_current_identity_providers()
    
    print("\n=== Important Notes ===")
    print("1. Make sure you have the necessary IAM permissions for License Manager User Subscriptions")
    print("2. Ensure your Active Directory is properly configured and accessible")
    print("3. Verify that the security groups and subnets allow proper communication")
    print("4. Each product requires a separate registration with the same identity provider")
    
    print("\nFor more details on identity provider management, please check:")
    print("https://docs.aws.amazon.com/license-manager/latest/userguide/user-subscriptions.html")


def main() -> None:
    """
    Main function demonstrating identity provider management operations.
    """
    print("Start of the AWS License Manager User Subscriptions Identity Provider Management")
    
    # Check permissions first
    print("\n=== Checking Permissions ===")
    if not check_permissions():
        print(" Insufficient permissions. Please check your IAM configuration.")
        return
    
    # List current identity providers first
    print("\n=== Checking Current Identity Providers ===")
    current_providers = list_current_identity_providers()
    
    # Check if our directory is already registered and with which products
    directory_id = 'd-1234567890'
    registered_products = []
    
    if current_providers:
        for provider in current_providers:
            if 'IdentityProvider' in provider:
                ip = provider['IdentityProvider']
                if 'ActiveDirectoryIdentityProvider' in ip:
                    if ip['ActiveDirectoryIdentityProvider'].get('DirectoryId') == directory_id:
                        product = provider.get('Product', 'Unknown')
                        registered_products.append(product)
                        print(f" Directory {directory_id} is registered with product: {product}")
    
    if registered_products:
        print(f"Directory {directory_id} is already registered with products: {', '.join(registered_products)}")
        
        # Check for unregistered products
        all_products = ['VISUAL_STUDIO_ENTERPRISE', 'VISUAL_STUDIO_PROFESSIONAL', 'OFFICE_PROFESSIONAL_PLUS']
        unregistered_products = [p for p in all_products if p not in registered_products]
        
        if unregistered_products:
            print(f"Available products to register: {', '.join(unregistered_products)}")
            
            print("\nTo register additional products, you can call:")
            for product in unregistered_products:
                print(f"  # Usage with identity provider:")
                print(f"  identity_provider = create_identity_provider('d-1234567890')")
                print(f"  register_identity_provider('{product}', identity_provider)")
                print(f"  ")
                print(f"  # Or with custom identity provider:")
                print(f"  custom_provider = create_identity_provider('your-directory-id')")
                print(f"  register_identity_provider('{product}', custom_provider)")
                print(f"  ")
                
            # Example: Uncomment to register Visual Studio Professional
            # print(f"\n--- Registering {unregistered_products[0]} ---")
            # identity_provider = create_identity_provider('d-1234567890')
            # register_identity_provider(unregistered_products[0], identity_provider)
        else:
            print("Directory is registered with all available products.")
    else:
        print(f"Directory {directory_id} is not registered. Proceeding with registration...")
        # Register the Active Directory identity provider
        result = demonstrate_active_directory_registration()
        
        if result:
            print("\n Registration completed successfully!")
        else:
            print("\n Registration failed. Please check the error messages above.")
    


    # Register identity providers for a given product
    print("\n=== Register Identity Provider for Product ===")
    # Create identity provider configuration
    example_identity_provider = create_identity_provider(
        directory_id='d-1234567890',
        directory_type='AWS_MANAGED'
    )
    #register_identity_provider('VISUAL_STUDIO_PROFESSIONAL', example_identity_provider)

    # Show self-managed AD example
    print("\n=== Register Self managed AD ===")
    create_self_managed_ad_example()

    # Deregister identity providers for a given product
    print("\n=== Deregister Identity Provider for Product ===")
    #deregister_identity_provider(example_identity_provider, 'VISUAL_STUDIO_ENTERPRISE')

    # List identity providers again to show current state
    print("\n=== Final Identity Provider Status ===")
    list_current_identity_providers()

    # List identity providers again to show current state
    print("\n=== Final Identity Provider Status ===")
    list_current_identity_providers()
    
    print("\n=== Important Notes ===")
    print("1. Make sure you have the necessary IAM permissions for License Manager User Subscriptions")
    print("2. Ensure your Active Directory is properly configured and accessible")
    print("3. Verify that the security groups and subnets allow proper communication")
    print("4. Each product requires a separate registration with the same identity provider")
    print("5. Valid products: VISUAL_STUDIO_ENTERPRISE, VISUAL_STUDIO_PROFESSIONAL, OFFICE_PROFESSIONAL_PLUS")
    print("6. For self-managed AD products (like RDS SAL), use register_self_managed_ad_identity_provider()")
    print("7. Usage examples:")
    print("   # AWS Managed AD (simple):")
    print("   identity_provider = create_identity_provider('d-1234567890')")
    print("   register_identity_provider('VISUAL_STUDIO_PROFESSIONAL', identity_provider)")
    print("   ")
    print("   # Self-managed AD (with full settings):")
    print("   register_self_managed_ad_identity_provider(")
    print("       product='REMOTE_DESKTOP_SERVICES',")
    print("       directory_id='d-sm1234567890',")
    print("       domain_name='corp.example.com',")
    print("       domain_ipv4_list=['10.0.1.10', '10.0.1.11'],")
    print("       subnets=['subnet-12345678', 'subnet-87654321'],")
    print("       secrets_manager_secret_id='ad-admin-credentials',")
    print("       security_group_id='sg-12345678'")
    print("   )")
    print("   register_identity_provider('VISUAL_STUDIO_PROFESSIONAL', custom_provider)")
    
    print("\nFor more details on identity provider management, please check:")
    print("https://docs.aws.amazon.com/license-manager/latest/userguide/user-subscriptions.html")


if __name__ == '__main__':
    main()
