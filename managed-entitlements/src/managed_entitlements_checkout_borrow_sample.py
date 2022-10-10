import boto3
import logging
import uuid
import jwt
import base64

region='us-east-1'

# boto3.set_stream_logger(name='botocore',level=10)

def create_license(SignKey):
    """Creates a license.

    For the purposes of this sample, it creates a dummy license only allowing
    to specify the SignKey to be used to signed the response of borrow.

    :SignKey KMS Asymmetric Key Arn
    """

    lm_client = boto3.client('license-manager', region)
    return lm_client.create_license(
        LicenseName="My License",
        ProductName="My Product",
        Beneficiary="My Beneficiary",
        ConsumptionConfiguration={
            "ProvisionalConfiguration": {
                "MaxTimeToLiveInMinutes": 60
            },
            "BorrowConfiguration": {
                "MaxTimeToLiveInMinutes": 1440,
                "AllowEarlyCheckIn": True
            },
        },
        Entitlements=[{
            "Name":"Users",
            "Unit":"Count",
            "MaxCount": 1000,
            "Overage": False,
            "AllowCheckIn": True
        }],
        HomeRegion=region,
        Issuer={
            "Name":"My Company",
            "SignKey": SignKey
        },
        ProductSKU="3688750d24200a4daa2e046732580b30",
        Validity={
            "Begin": "2021-04-12T00:00:00Z"
        },
        LicenseMetadata=[{
            "Name":"ProductName",
            "Value":"My awesome product"
        }],
        ClientToken=str(uuid.uuid4())
    )

def checkout_borrow_license(LicenseArn):
    """Borrow a license for offline usage

    The API returns an SignedToken which is a JWT token encoded using algorithm
    PS384. The data is essentially the same returned as response of this object.
    For more details: https://docs.aws.amazon.com/license-manager/latest/APIReference/API_CheckoutBorrowLicense.html
    """

    lm_client = boto3.client('license-manager', region)
    return lm_client.checkout_borrow_license(
        LicenseArn=LicenseArn,
        Entitlements=[{
            "Name":"Users",
            "Value": "1",
            "Unit":"Count"
        }],
        NodeId="MyNodeId",
        DigitalSignatureMethod="JWT_PS384",
        ClientToken=str(uuid.uuid4()).replace("-","")
    )


def create_cmk(desc='Customer Master Key'):
    """Create a KMS Customer Master Key

    The created CMK is a Customer-managed key stored in AWS KMS.
    """

    kms_client = boto3.client('kms', region)
    response = kms_client.create_key(
                                    Description=desc,
                                    CustomerMasterKeySpec="RSA_4096",
                                    KeyUsage="SIGN_VERIFY"
                                )

    return response['KeyMetadata']['Arn']

def get_public_key(KeyId):
    """Get CMK PublicKey
    """

    kms_client = boto3.client('kms', region)
    response = kms_client.get_public_key(KeyId=KeyId)

    return response['PublicKey']

def main(command_line=None):
    print("Start of the sample model for checkout borrow license")
    # Initially, you should create an asymmetric key that License Manager uses to
    # sign borrow license data. The algorithms are based on JWT standard and all
    # major languages has public libraries to verify signatures. For this sample,
    # we are using PyJwt
    SignKey=create_cmk()
    print(f"Key Created: {SignKey}")

    # For offline verification public key should be stored safely in way that the Software
    # can retrieve it. For more details how to manage your public key, please check
    # KMS docs: https://docs.aws.amazon.com/kms/latest/APIReference/API_GetPublicKey.html
    public_key=f"-----BEGIN PUBLIC KEY-----\n{base64.b64encode(get_public_key(SignKey)).decode()}\n-----END PUBLIC KEY-----\n"
    print(f"Public Key: {public_key}")

    # Creates a simple license for our example. We have an entitlement called Users
    # and are indicating to License Manager that it should allow license borrowing
    # by specifying BorrowConfiguration.
    License=create_license(SignKey=SignKey)
    LicenseArn=License["LicenseArn"]
    print(f"License Created: {LicenseArn}")

    # Borrowing a license. For real scenarios, it should be also accounted the
    # distribution and potential leaks. Use borrowing specifying and validating
    # NodeId if distribution is not safe.
    signed_token=checkout_borrow_license(LicenseArn)["SignedToken"]
    print(f"Signed Token from CheckoutBorrowLicense: {signed_token}")

    # Now that you have signed token in your environment, you can retrieve the public
    # key to verify if it was signed using your KMS key and you should trust it.
    # In case it is valid signature, it will return a dictionary of data included in
    # the token. For instance,
    # {'licenseArn': 'arn:aws:license-manager::575359184979:license:l-bc39444470c642ae9ead0eabe8465bb1',
    # 'licenseConsumptionToken': '0cd7b2bc7c674573a669bea8f5b75f2d',
    # 'entitlementsAllowed': [{'name': 'Users', 'value': '1', 'unit': 'Count'}],
    # 'nodeId': 'MyNodeId', 'issuedAt': '2021-04-13T05:35:47', 'expiration': '2021-04-14T05:35:47'}
    #
    # If it is invalid token, it throws an exception
    #  jwt.exceptions.InvalidSignatureError: Signature verification failed
    #
    checkout_borrow_decoded_response = jwt.decode(signed_token, public_key, algorithms=["PS384"], options={"verify_signature": True})
    print(f"Decoded response (Signature verified): {checkout_borrow_decoded_response}")

if __name__ == '__main__':
    main()
