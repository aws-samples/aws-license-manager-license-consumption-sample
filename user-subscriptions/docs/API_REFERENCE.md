# AWS License Manager User Subscriptions - API Reference

This document provides detailed information about the AWS License Manager User Subscriptions API operations used in the sample scripts.

## Core Operations

### list_identity_providers

Lists all registered identity providers in your AWS account.

**Parameters:**
- `MaxResults` (optional): Maximum number of results to return
- `NextToken` (optional): Token for pagination

**Response:**
- `IdentityProviderSummaries`: List of identity provider summaries
- `NextToken`: Token for next page (if applicable)

**Example:**
```python
response = client.list_identity_providers()
```

### list_instances

Lists EC2 instances that provide user-based subscriptions.

**Parameters:**
- `Filters` (optional): List of filters to apply
  - Valid attributes: `Status`, `InstanceId`
  - Valid operations: `Equals`, `geq`, `leq`
- `MaxResults` (optional): Maximum number of results to return
- `NextToken` (optional): Token for pagination

**Response:**
- `InstanceSummaries`: List of instance summaries
- `NextToken`: Token for next page (if applicable)

**Example:**
```python
response = client.list_instances(
    Filters=[
        {
            'Attribute': 'Status',
            'Operation': 'Equals',
            'Value': 'ACTIVATED'
        }
    ]
)
```

### list_product_subscriptions

Lists product subscriptions for a specific identity provider.

**Parameters:**
- `IdentityProvider` (required): Identity provider configuration
- `Product` (optional): Specific product to filter by
- `Filters` (optional): List of filters to apply
  - Valid attributes: `Status`, `Username`, `Domain`
  - Valid operations: `Equals`, `geq`, `leq`
- `MaxResults` (optional): Maximum number of results to return
- `NextToken` (optional): Token for pagination

**Response:**
- `ProductUserSummaries`: List of product subscription summaries
- `NextToken`: Token for next page (if applicable)

**Example:**
```python
response = client.list_product_subscriptions(
    IdentityProvider={
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-1234567890'
        }
    },
    Product='VISUAL_STUDIO_PROFESSIONAL'
)
```

### list_user_associations

Lists user associations for a specific identity provider and instance.

**Parameters:**
- `IdentityProvider` (required): Identity provider configuration
- `InstanceId` (required): EC2 instance ID
- `Filters` (optional): List of filters to apply
  - Valid attributes: `Username`, `Status`
  - Valid operations: `Equals`, `geq`, `leq`
- `MaxResults` (optional): Maximum number of results to return
- `NextToken` (optional): Token for pagination

**Response:**
- `InstanceUserSummaries`: List of user association summaries
- `NextToken`: Token for next page (if applicable)

**Example:**
```python
response = client.list_user_associations(
    IdentityProvider={
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-1234567890'
        }
    },
    InstanceId='i-1234567890abcdef0'
)
```

## Management Operations

### register_identity_provider

Registers a new identity provider with License Manager User Subscriptions.

**Parameters:**
- `IdentityProvider` (required): Identity provider configuration
- `Product` (required): Product to associate
- `Settings` (optional): Additional settings

**Response:**
- `IdentityProviderSummary`: Details of the registered identity provider

### deregister_identity_provider

Deregisters an identity provider from License Manager User Subscriptions.

**Parameters:**
- `IdentityProvider` (required): Identity provider configuration
- `Product` (required): Product to disassociate

**Response:**
- `IdentityProviderSummary`: Details of the deregistered identity provider

### update_identity_provider_settings

Updates settings for an existing identity provider.

**Parameters:**
- `IdentityProvider` (required): Identity provider configuration
- `Product` (required): Associated product
- `Settings` (required): New settings to apply

**Response:**
- `IdentityProviderSummary`: Updated identity provider details

## License Server Endpoint Operations

### create_license_server_endpoint

Creates a new license server endpoint for user subscriptions.

**Parameters:**
- `IdentityProvider` (required): Identity provider configuration
- `LicenseServerSettings` (required): License server configuration
- `Tags` (optional): Tags to apply to the endpoint

**Response:**
- `LicenseServerEndpointId`: ID of the created endpoint
- `LicenseServerEndpointArn`: ARN of the created endpoint
- `Status`: Current status of the endpoint

**Example:**
```python
response = client.create_license_server_endpoint(
    IdentityProvider={
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-1234567890'
        }
    },
    LicenseServerSettings={
        'ServerType': 'RDS_LICENSE_SERVER',
        'ServerSettings': {
            'RdsLicenseServerSettings': {
                'LicenseServerEndpointUrl': 'https://rds-license-server.example.com:443'
            }
        }
    },
    Tags=[
        {
            'Key': 'Environment',
            'Value': 'Production'
        }
    ]
)
```

### delete_license_server_endpoint

Deletes an existing license server endpoint.

**Parameters:**
- `IdentityProvider` (required): Identity provider configuration
- `LicenseServerEndpointId` (required): ID of the endpoint to delete

**Response:**
- `LicenseServerEndpointId`: ID of the deleted endpoint
- `LicenseServerEndpointArn`: ARN of the deleted endpoint
- `Status`: Final status of the endpoint

**Example:**
```python
response = client.delete_license_server_endpoint(
    IdentityProvider={
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-1234567890'
        }
    },
    LicenseServerEndpointId='lse-1234567890abcdef0'
)
```

### list_license_server_endpoints

Lists license server endpoints, optionally filtered by identity provider.

**Parameters:**
- `IdentityProvider` (optional): Filter by identity provider
- `MaxResults` (optional): Maximum number of results to return
- `NextToken` (optional): Token for pagination

**Response:**
- `LicenseServerEndpoints`: List of license server endpoint details
- `NextToken`: Token for next page (if applicable)

**Example:**
```python
response = client.list_license_server_endpoints(
    IdentityProvider={
        'ActiveDirectoryIdentityProvider': {
            'DirectoryId': 'd-1234567890'
        }
    }
)
```

## Data Structures

### Identity Provider

```python
{
    'ActiveDirectoryIdentityProvider': {
        'DirectoryId': 'string',
        'ActiveDirectorySettings': {
            'DomainName': 'string',
            'DomainIpv4List': ['string'],
            'DomainNetworkSettings': {
                'Subnets': ['string']
            },
            'DomainCredentialsProvider': {
                'SecretsManagerCredentialsProvider': {}
            }
        },
        'ActiveDirectoryType': 'AWS_MANAGED'|'SELF_MANAGED'
    }
}
```

### Filter

```python
{
    'Attribute': 'string',
    'Operation': 'Equals'|'geq'|'leq',
    'Value': 'string'
}
```

### Settings

```python
{
    'SecurityGroupId': 'string',
    'Subnets': ['string']
}
```

### License Server Settings

```python
{
    'ServerType': 'RDS_LICENSE_SERVER',
    'ServerSettings': {
        'RdsLicenseServerSettings': {
            'LicenseServerEndpointUrl': 'string'
        }
    }
}
```

### Tags

```python
[
    {
        'Key': 'string',
        'Value': 'string'
    }
]
```

## Supported Products

- `VISUAL_STUDIO_PROFESSIONAL`
- `OFFICE_PROFESSIONAL_PLUS`
- `REMOTE_DESKTOP_SERVICES`

## Status Values

### Instance Status
- `ACTIVATED`: Instance is active and ready for use
- `FAILED`: Instance activation failed
- `TERMINATED`: Instance has been terminated

### Product Subscription Status
- `SUBSCRIBED`: User has an active subscription
- `UNSUBSCRIBED`: User subscription has ended

### Identity Provider Status
- `REGISTERED`: Identity provider is registered and active
- `DEREGISTERED`: Identity provider has been deregistered

### License Server Endpoint Status
- `CREATING`: Endpoint is being created
- `AVAILABLE`: Endpoint is ready for use
- `FAILED`: Endpoint creation or operation failed
- `DELETING`: Endpoint is being deleted

## Error Handling

Common error types and their meanings:

- `ValidationException`: Invalid parameters provided
- `ResourceNotFoundException`: Requested resource not found
- `AccessDeniedException`: Insufficient permissions
- `ThrottlingException`: Request rate exceeded
- `InternalServerException`: AWS service error

## Best Practices

1. **Pagination**: Always handle pagination for list operations
2. **Error Handling**: Implement proper exception handling
3. **Filtering**: Use server-side filtering when available
4. **Rate Limiting**: Implement backoff strategies for throttling
5. **Resource Management**: Clean up resources when no longer needed

## Examples

See the sample scripts in the `src/` directory for complete working examples of these API operations.
