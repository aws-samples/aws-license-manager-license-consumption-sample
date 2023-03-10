import boto3
import base64
import datetime
import pprint
import uuid

default_region = 'us-east-1'

def create_license(LicenseName, ProductSKU, ProductKeyEntitlements):
    lm_client = get_client(default_region)
    response = lm_client.create_license(
        LicenseName = LicenseName,
        ProductName = "My Product",
        Beneficiary = "My Beneficiary",
        ConsumptionConfiguration = {
            "ProvisionalConfiguration": {
                "MaxTimeToLiveInMinutes": 60
            }
        },
        Entitlements = ProductKeyEntitlements,
        HomeRegion = default_region,
        Issuer = {
            "Name": "My Company",
        },
        ProductSKU = ProductSKU,
        Validity = {
            "Begin": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        },
        LicenseMetadata = [{
            "Name": "ProductName",
            "Value": "My awesome product"
        }],
        ClientToken = str(uuid.uuid4())
    )
    print('AWS License Manager - Create License API response:')
    pprint.pprint(response)
    return response


def checkout_license(KeyFingerprint, ProductSKU, ProductKeyEntitlementName, ProductKeyUnit, ProductKeyValue):
    lm_client = get_client(default_region)
    response = lm_client.checkout_license(
        CheckoutType = "PROVISIONAL",
        Entitlements = [{
            "Name": ProductKeyEntitlementName,
            "Unit": ProductKeyUnit,
            "Value": ProductKeyValue
        }],
        KeyFingerprint = KeyFingerprint,
        ProductSKU = ProductSKU,
        Beneficiary = "My Beneficiary",
        ClientToken = str(uuid.uuid4())
    )
    print('AWS License Manager - Checkout License API response:')
    pprint.pprint(response)
    return response

def get_license(LicenseArn):
    lm_client = get_client(default_region)
    response = lm_client.get_license(
        LicenseArn = LicenseArn,
    )
    print('AWS License Manager - Get License API response:')
    pprint.pprint(response)
    return response

def check_in_license(LicenseConsumptionToken):
    lm_client = get_client(default_region)
    response = lm_client.check_in_license(
        LicenseConsumptionToken = LicenseConsumptionToken
    )
    print('AWS License Manager - CheckIn License API response:')
    pprint.pprint(response)

def extend_license_consumption(LicenseConsumptionToken):
    lm_client = get_client(default_region)
    response = lm_client.extend_license_consumption(
        LicenseConsumptionToken = LicenseConsumptionToken
    )
    print('AWS License Manager - Extend License Consumption API response:')
    pprint.pprint(response)

def delete_license(LicenseArn, SourceVersion):
    lm_client = get_client(default_region)
    response = lm_client.delete_license(
        LicenseArn = LicenseArn,
        SourceVersion = SourceVersion
    )
    print('AWS License Manager - Delete License API response:')
    pprint.pprint(response)

def get_client(Region):
    return boto3.client('license-manager', Region)

def main(command_line=None):
    print("Start of the sample model 1")
    model1_license_name = "TestLicense1"
    model1_product_sku = "TestProductSKU1"
    model1_entitlement_key = "Users"
    model1_entitlement_count = 1000
    model1_entitlement_unit = "Count"
    model1_entitlement_value = "1"
    model1_source_version = "1"

    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]

    model1_keyfingerprint = f"aws:{account_id}:My Company:issuer-fingerprint"

    product_key_entitlement=[{
     "Name": model1_entitlement_key,
     "Unit": model1_entitlement_unit,
     "MaxCount": model1_entitlement_count,
     "AllowCheckIn": True
     }]

    # Creating a test license for a sample product
    license = create_license(model1_license_name, model1_product_sku,product_key_entitlement)

    # Get the test license details.
    get_license(license['LicenseArn'])

    # Checkout the test license with valid Entitlements.
    checkout_response = checkout_license(model1_keyfingerprint, model1_product_sku, model1_entitlement_key, model1_entitlement_unit, model1_entitlement_value)

    # Extend the test license consumption.
    extend_license_consumption(checkout_response['LicenseConsumptionToken'])

    # Check in the test license
    check_in_license(checkout_response['LicenseConsumptionToken'])

    # Delete the license.
    delete_license(license['LicenseArn'], model1_source_version)

if __name__ == '__main__':
    main()

