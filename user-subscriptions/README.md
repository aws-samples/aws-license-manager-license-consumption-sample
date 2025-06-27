# AWS License Manager User Subscriptions - Sample Scripts
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](https://opensource.org/licenses/MIT-0)

This repository contains production-ready sample scripts for AWS License Manager User Subscriptions service. These scripts demonstrate best practices for managing user-based software licenses in AWS environments using **dummy resource references** for safe public distribution.

## 📋 Overview

AWS License Manager User Subscriptions helps you manage user-based software licenses from software vendors like Microsoft. These sample scripts provide comprehensive examples of how to:

- List and manage identity providers
- Generate usage metrics and reports
- Manage product subscriptions and user associations
- Create and manage license server endpoints
- Monitor instance and user associations

## ⚠️ Important: Dummy Resource References

**These scripts use dummy/placeholder resource references for public distribution:**

- **AWS Account ID**: `123456789012` (replace with your actual account ID)
- **Directory IDs**: `d-1234567890` (replace with your AWS Managed AD directory ID)
- **Domain Names**: `example.com`, `corp.example.com` (replace with your actual domains)
- **Usernames**: `testuser1`, `testuser2` (replace with your actual usernames)
- **Network Resources**: `subnet-12345678`, `sg-12345678` (replace with your actual subnet/security group IDs)
- **Secrets Manager ARNs**: Use `-AbCdEf` suffix (replace with your actual secret ARNs)

**Before using these scripts, you MUST replace all dummy values with your actual AWS resource identifiers.**

## 🚀 Quick Start

### Prerequisites

1. **AWS Account** with License Manager User Subscriptions enabled
2. **Python 3.7+** installed
3. **AWS credentials** configured (AWS CLI, environment variables, or IAM roles)
4. **Required IAM permissions** (see [Permissions](#permissions) section)
5. **Active Directory** (AWS Managed AD or Self-Managed AD) configured
6. **AWS Secrets Manager** secret with AD admin credentials (for some operations)

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd aws-license-manager-license-consumption-sample/user-subscriptions
   ```

2. Install dependencies:
   ```bash
   pip install boto3
   ```

3. **Configure your resources**: Replace dummy values with your actual AWS resources:
   ```bash
   # Edit the scripts and replace:
   # - Account ID: 123456789012 → your-account-id
   # - Directory ID: d-1234567890 → your-directory-id  
   # - Domain: example.com → your-domain.com
   # - Usernames: testuser1 → your-actual-username
   # - Subnets: subnet-12345678 → your-subnet-id
   # - Secrets: secret-name-AbCdEf → your-secret-name
   ```

4. Configure AWS credentials:
   ```bash
   aws configure
   # OR set environment variables
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

### Usage

Run any of the sample scripts:

```bash
cd src
python3 list_identity_providers_sample.py
python3 user_subscriptions_usage_metrics_sample.py
python3 manage_identity_provider_settings.py
python3 manage_license_server_endpoints.py
python3 manage_user_subscriptions.py
```

**⚠️ Important**: Before running scripts, ensure you've replaced all dummy resource references with your actual AWS resources.

## 📁 Repository Structure

```
user-subscriptions/
├── README.md                                   # This file
├── src/                                       # Sample scripts
│   ├── list_identity_providers_sample.py      # Identity provider operations
│   ├── user_subscriptions_usage_metrics_sample.py  # Usage metrics and reporting
│   ├── manage_identity_provider_settings.py   # Identity provider management
│   ├── manage_license_server_endpoints.py     # License server endpoint management
│   ├── manage_user_subscriptions.py           # User subscription management
│   └── PRODUCTIONIZATION_SUMMARY.md           # Details on dummy resource replacements
├── docs/                                      # Documentation
│   ├── API_REFERENCE.md                       # Comprehensive API guide
│   └── CONTRIBUTING.md                        # Contribution guidelines
└── backup/                                   # Backup directory
    └── old-scripts/                          # Archived versions
```

## 🔧 Sample Scripts

### 1. Identity Providers Sample (`list_identity_providers_sample.py`)

**Purpose**: Comprehensive demonstration of identity provider operations

**Features**:
- List all identity providers with pagination
- Query instances with filtering capabilities
- Manage product subscriptions
- Handle user associations
- Demonstrate proper API parameter usage

**Example Output** (with dummy data):
```
==========> Identity Providers Found <==========

--- Identity Provider 1 ---
ARN: arn:aws:license-manager-user-subscriptions:us-east-1:123456789012:identity-provider/IdentityProvider-xxx
Product: REMOTE_DESKTOP_SERVICES
Status: REGISTERED
Directory ID: d-1234567890
Domain Name: example.com
```

### 2. Usage Metrics Sample (`user_subscriptions_usage_metrics_sample.py`)

**Purpose**: Generate comprehensive usage metrics and reports

**Features**:
- Calculate product subscription metrics
- Analyze instance usage patterns
- Generate detailed usage reports
- Breakdown statistics by product and status
- User association analysis

**Example Output**:
```
--- Product Subscription Usage Metrics ---
Total Subscriptions: 10
Active Subscriptions: 8
Inactive Subscriptions: 2

Breakdown by Product:
  VISUAL_STUDIO_PROFESSIONAL:
    Total: 4
    Active: 3
    Inactive: 1
```

### 3. Identity Provider Management (`manage_identity_provider_settings.py`)

**Purpose**: Manage identity provider lifecycle and settings

**Features**:
- Register new identity providers
- Update existing provider settings
- Deregister identity providers
- Configure Active Directory settings
- Manage network and security configurations

### 4. License Server Endpoints Management (`manage_license_server_endpoints.py`)

**Purpose**: Comprehensive user subscription lifecycle management

**Features**:
- Start and stop product subscriptions for users
- Associate and disassociate users with EC2 instances
- Support for both AWS Managed AD and Self-Managed AD
- Demonstrate Visual Studio and Remote Desktop Services workflows
- Handle subscription status monitoring
- User association management with instances

**Example Operations**:
```python
# Start a Visual Studio subscription
start_product_subscription(
    username='testuser1@example.com',
    domain='example.com',
    product='VISUAL_STUDIO_PROFESSIONAL',
    identity_provider=identity_provider
)

# Associate user with EC2 instance
associate_user(
    username='testuser1@example.com',
    domain='example.com',
    instance_id='i-1234567890abcdef0',
    identity_provider=identity_provider
)
```

**Purpose**: Manage license server endpoints for user subscriptions

**Features**:
- Create new license server endpoints
- List existing license server endpoints with pagination
- Delete license server endpoints
- Generate comprehensive endpoint reports
- Support for RDS License Server configuration
- Endpoint lifecycle management

**Example Output** (with dummy data):
```
--- License Server Endpoint 1 ---
Endpoint ID: lse-12345678-1234-1234-1234-123456789012
ARN: arn:aws:license-manager-user-subscriptions:us-east-1:123456789012:license-server-endpoint/lse-12345678-1234-1234-1234-123456789012
Status: AVAILABLE
Server Type: RDS_SAL
```

## 🔐 Permissions

Your AWS credentials need the following IAM permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "license-manager-user-subscriptions:ListIdentityProviders",
                "license-manager-user-subscriptions:ListInstances",
                "license-manager-user-subscriptions:ListProductSubscriptions",
                "license-manager-user-subscriptions:ListUserAssociations",
                "license-manager-user-subscriptions:RegisterIdentityProvider",
                "license-manager-user-subscriptions:DeregisterIdentityProvider",
                "license-manager-user-subscriptions:UpdateIdentityProviderSettings",
                "license-manager-user-subscriptions:CreateLicenseServerEndpoint",
                "license-manager-user-subscriptions:DeleteLicenseServerEndpoint",
                "license-manager-user-subscriptions:ListLicenseServerEndpoints",
                "license-manager-user-subscriptions:StartProductSubscription",
                "license-manager-user-subscriptions:StopProductSubscription",
                "license-manager-user-subscriptions:AssociateUser",
                "license-manager-user-subscriptions:DisassociateUser",
                "secretsmanager:GetSecretValue"
            ],
            "Resource": "*"
        }
    ]
}
```

## 📊 API Reference

### Key Operations

| Operation | Purpose | Required Parameters |
|-----------|---------|-------------------|
| `list_identity_providers` | List configured identity providers | None |
| `list_instances` | List EC2 instances with subscriptions | `Filters` (optional) |
| `list_product_subscriptions` | List product subscriptions | `IdentityProvider` |
| `list_user_associations` | List user associations | `IdentityProvider`, `InstanceId` |
| `create_license_server_endpoint` | Create license server endpoint | `IdentityProviderArn`, `LicenseServerSettings` |
| `delete_license_server_endpoint` | Delete license server endpoint | `LicenseServerEndpointArn`, `ServerType` |
| `list_license_server_endpoints` | List license server endpoints | None (all optional) |
| `start_product_subscription` | Start user product subscription | `Username`, `Domain`, `Product`, `IdentityProvider` |
| `stop_product_subscription` | Stop user product subscription | `Username`, `Domain`, `Product`, `IdentityProvider` |
| `associate_user` | Associate user with EC2 instance | `Username`, `Domain`, `InstanceId`, `IdentityProvider` |
| `disassociate_user` | Remove user association from instance | `Username`, `Domain`, `InstanceId`, `IdentityProvider` |

### Supported Products

- `VISUAL_STUDIO_PROFESSIONAL`
- `VISUAL_STUDIO_ENTERPRISE`
- `OFFICE_PROFESSIONAL_PLUS`
- `REMOTE_DESKTOP_SERVICES`

### Filter Operations

- `Equals`: Exact match
- `geq`: Greater than or equal
- `leq`: Less than or equal

## 🛠️ Configuration

### Dummy Resource Reference Mapping

Before using these scripts, replace the following dummy values with your actual AWS resources:

| Dummy Value | Description | Replace With |
|-------------|-------------|--------------|
| `123456789012` | AWS Account ID | Your actual AWS account ID |
| `d-1234567890` | AWS Managed AD Directory ID | Your directory ID (format: `d-xxxxxxxxxx`) |
| `sd-1234567890` | Self-Managed AD Directory ID | Your self-managed directory ID |
| `example.com` | Primary domain name | Your actual domain name |
| `corp.example.com` | Corporate domain name | Your corporate domain name |
| `testuser1`, `testuser2` | Sample usernames | Your actual usernames |
| `subnet-12345678` | VPC Subnet ID | Your actual subnet ID |
| `sg-12345678` | Security Group ID | Your actual security group ID |
| `10.0.1.10`, `10.0.1.11` | IP Addresses | Your domain controller IP addresses |
| `secret-name-AbCdEf` | Secrets Manager secret suffix | Your actual secret name/ARN |

### Environment Variables

```bash
# AWS Configuration
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

# Optional: For temporary credentials
export AWS_SESSION_TOKEN=your_session_token
```

### Script Configuration

You can modify the default region in each script:

```python
# Default AWS region
DEFAULT_REGION = 'us-east-1'  # Change as needed
```

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure AWS credentials are properly configured
   - Verify IAM permissions are sufficient
   - Check if credentials have expired

2. **Region Issues**
   - Ensure License Manager User Subscriptions is available in your region
   - Verify identity providers are configured in the correct region

3. **Dummy Resource References**
   - All scripts contain placeholder values for security
   - Replace dummy account IDs, directory IDs, domain names, etc.
   - See [Configuration](#configuration) section for complete mapping
   - Check `PRODUCTIONIZATION_SUMMARY.md` for detailed replacement guide

4. **Missing Required Resources**
   - Confirm identity providers are registered
   - Verify instances have user subscriptions enabled
   - Check product subscriptions are active
   - Ensure Active Directory is properly configured
   - Verify Secrets Manager secrets exist and are accessible

5. **Network Connectivity Issues**
   - Check VPC configuration and routing
   - Verify security group rules allow required traffic
   - Ensure subnets have proper connectivity to domain controllers
   - Confirm DNS resolution for domain names

### Debug Mode

Enable debug logging by setting the environment variable:

```bash
export BOTO_DEBUG=1
python3 script_name.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📚 Additional Resources

- [AWS License Manager User Subscriptions Documentation](https://docs.aws.amazon.com/license-manager/latest/userguide/user-subscriptions.html)
- [AWS License Manager User Subscriptions API Reference](https://docs.aws.amazon.com/license-manager-user-subscriptions/latest/APIReference/)
- [AWS CLI License Manager User Subscriptions Commands](https://docs.aws.amazon.com/cli/latest/reference/license-manager-user-subscriptions/)
- [AWS SDK for Python (Boto3) Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 📄 License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues related to these sample scripts:
1. Check the [troubleshooting section](#troubleshooting)
2. Review the [documentation](docs/)
3. Open an issue in this repository

For AWS License Manager User Subscriptions service issues:
- Contact [AWS Support](https://aws.amazon.com/support/)
- Visit the [AWS License Manager User Subscriptions forum](https://forums.aws.amazon.com/)

---

**Note**: These are sample scripts for demonstration purposes with **dummy resource references** for safe public distribution. 

**⚠️ IMPORTANT**: Before using in any environment:
1. Replace ALL dummy values (account IDs, directory IDs, domain names, etc.) with your actual AWS resources
2. Review and test thoroughly in a development environment first
3. Ensure proper IAM permissions and network connectivity
4. Configure Secrets Manager with actual Active Directory credentials
5. See `PRODUCTIONIZATION_SUMMARY.md` for complete details on required replacements

For a complete mapping of dummy values to replace, see the [Configuration](#configuration) section above.
