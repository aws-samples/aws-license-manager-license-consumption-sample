## AWS License Manager - Self Managed Licenses Python Sample Code

With License Manager, you can designate a centralized team in your organization to manage software licensing agreements and create rules. These rules can then be used across the organization to govern license usage.

When a new Amazon Elastic Compute Cloud (EC2) instance gets launched, the rules created with License Manager are attached using the console, CLI, or API. Once rules are attached, end users in your organization can launch instances and these can be tracked from dashboards in the License Manager console. Licenses and usage can be tracked throughout the lifecycle of an instance.  License Manager also tracks any violation of the licensing rules and proactively sends an alert to end users and license administrators. When an instance is stopped, licenses are released and are available for reuse. Set hard or soft limits to control license usage and prevent the launch of a new, non-compliant instance. A hard limit blocks the launch of an out-of-compliance instance. A soft limit permits out-of-compliance launches but sends an alert when one occurs.

License Manager provides a mechanism to automatically discover software running on existing EC2 instances using AWS Systems Manager. Rules can then be attached and validated in EC2 instances, and the licenses can then be tracked using  License Manager’s central dashboard.

Administrators can discover software usage on instances using AWS Organizations by going through a one-time multi-account setup and creating policies that centrally control AWS service use across multiple AWS accounts. If users uninstall software purchased on AWS Marketplace, License Manager's automated discovery feature can recognize that uninstall and make the license available for reuse.

In the sample python script (self_managed_licenses_sample.py), we demonstrate the activities that end users can perform to set license terms as rules and perform license tracking enforcement. We perform the below operations in the respective order in us-east-1 region.

For more details: https://github.com/aws-samples/systems-manager-license-manager-license-tracker-for-sql-server 


create_license_configuration

Creates a simple test license configuration as an example. A license configuration is an abstraction of a customer license agreement that can be consumed and enforced by License Manager. Components include specifications for the license type (licensing by instance, socket, CPU, or vCPU), allowed tenancy (shared tenancy, Dedicated Instance, Dedicated Host, or all of these), license affinity to host (how long a license must be associated with a host), and the number of licenses purchased and used. In this example we have created a license configuration with licensing by instance as an example. 

get_license_configuration

Gets the specified license configuration. In this example, we are displaying the sample license configuration we have created in the previous step. This can be used in scenarios to check the properties of an existing license configuration.

update_license_configuration

License Manager uses Systems Manager inventory to discover software usage on Amazon EC2 instances and on-premises instances. You can add product information to your self-managed license, and License Manager will track the instances that have those products installed. Automated discovery can be added to a new license set, to an existing self-managed license, or resources in your inventory. Rules for automated discovery can be edited at any time through the CLI using the UpdateLicenseConfiguration API command (which is covered in the sample code). To edit rules in the console, you must delete the existing self-managed license and create a new one.

To use automated discovery, you must add product information to your self-managed license. You can do so when you create the self-managed license using Inventory search. In this code sample we are adding new ProductInformationList to existing license configuration rule. 

delete_license_configuration

Deletes the specified license configuration. In this sample, we are deleting the sample license configuration we have created. This can be used in scenarios when a license configuration is no longer required.

