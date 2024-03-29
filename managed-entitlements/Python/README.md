## AWS License Manager - Managed Entitlements Python Sample Code

With AWS License Manager, a license administrator can distribute, activate, and track software licenses across accounts and throughout an organization.

Independent software vendors (ISVs) can use AWS License Manager to manage and distribute software licenses and data to end users using Managed Entitlements. You can track the central usage of your seller-issued licenses using AWS License Manager dashboard. ISVs selling through AWS Marketplace benefit from automatic license creation and distribution as a part of the transaction workflow. ISVs can also use AWS License Manager to create bearer tokens and activate licenses for customers without an AWS account.

AWS License Manager uses open, secure, industry standards for representing licenses and allows customers to cryptographically verify their authenticity. AWS License Manager supports a variety of licensing models including perpetual licenses, floating licenses, subscription licenses, and usage-based licenses. If you have licenses that must be node-locked, AWS License Manager provides mechanisms to consume your licenses in that way.

You can create licenses in AWS License Manager and distribute them to end users using an IAM identity or through digitally signed tokens generated by AWS License Manager. End users may choose to redistribute the license entitlements to AWS identities in their respective organizations. End users with distributed entitlements can perform check-out and check-in activities from the specific license through software integration with AWS License Manager. Each license check-out specifies the entitlements, the associated quantity, and check-out time period, for example, ‘checking out 10 admin-users for 1 hour.’ Check-out can be performed based on the underlying IAM identity for the distributed license or based on the bearer tokens generated by AWS License Manager.

When describing your License in Managed Licenses, you should also describe how will those be consumed, take the following use cases as examples below. Note the examples are to better illustrate the differences, license consumption modes are very flexible and enable many other use cases.

1. My software requires internet connectivity, so that it can check out customers entitlements or constantly verify entitlements are currently valid. I should also be able to grant more entitlements or suspend a customer entitlement and that my software should be able to get new state of my license as soon as I verify by calling License Manager.

2. My software does not require internet connectivity, my customers have an air gap environment or my software should be resilient to long periods of disconnectivity or bad connection. In this case, my software should be able to verify entitlements without internet connection.

For first use case, you can use CheckoutLicense API with PROVISIONAL type to consume your entitlements. The API is flexible in terms of entitlements available, if one entitlement is not available, it returns entitlements only ones customer has at the time of checkout. You can also extend your consumption (which verifies the validity) using ExtendLicenseConsumption. At the end, you can also CheckInLicense back at any time to indicate the consumption is no longer happening.


In the sample python script (managed_entitlements_sample.py), we demonstrate the activities that end users can perform to 'check out' or 'check in' the licenses back. We perform the below operations in the respective order in us-east-1 region. 


create_license

Creates a simple test license as an example. We have entitlements called Users and are indicating to AWS License Manager that it should allow license checkout by specifying ConsumptionConfiguration.

checkout_license

Checks out the test license with valid Entitlements. In this sample, we checkout the test license created using Users entitlement. Checkout API ensures user is granted to use a license and the capabilities available for use.

extend_license_consumption

In this sample we are extending the license consumption for the checked out test license. This can be used for scenarios when we are not done with the license consumption and if the expiration time is in the near future. 

check_in_license

Checks in the license if the license is no longer in use. In this sample, we are checking back in the license consumption token that we have checked out in the previous step. This can be used in scenarios when a license is no longer required.  

delete_license

Deletes the license. In this sample, we are deleting the test license we have created. This can be used in scenarios when a license is no longer required. 

For second use case, you can use CheckoutBorrowLicense API, it will return an JWT token that can be verified using a public key. In order to use this API, you will need:

Create a asymmetric key on KMS, when creating your license specify the KMS key in SignKey attribute (under Issuer).
Make the public accessible to your software, once you get the signed token, you can validate it using your public key. All major languages have libraries that can make that easy for you.
As mentioned before this examples are to best illustrate the differences of consumption options, they are not exclusive and you can have both in the same license. 

Key differences:

1. CheckoutBorrowLicense requires customers have all entitlements specified.
2. CheckoutBorrowLicense may allow check ins. You can control check ins with AllowEarlyCheckIn flag.

In the sample python script (managed_entitlements_checkout_borrow_sample.py), we demonstrate the activities that end users can perform to 'check out borrow'. We perform the below operations in the respective order in us-east-1 region. 

create_cmk

Creates an asymmetric key that License Manager uses to sign borrow license data.

create_license

Creates a simple test license as an example. We have entitlements called Users and are indicating to AWS License Manager that it should allow license checkout by specifying ConsumptionConfiguration.

checkout_borrow_license

In this sample, we checkout borrow the test license created using Users entitlement.

For more details: https://docs.aws.amazon.com/license-manager/index.html

