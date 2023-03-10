import { v4 as uuidv4 } from 'uuid';
import AWS from 'aws-sdk';

const SELLER_ACCOUNT_ID = "<YOUR_SELLER_ACCOUNT_ID>";
const BUYER_ACCOUNT_ID = "<YOUR_BUYER_ACCOUNT_ID>";

const createLicense = async () => {
    AWS.config.loadFromPath('./seller_config.json');
    const licenseManager = new AWS.LicenseManager();
    return await licenseManager.createLicense({
        ProductSKU: "My-ProductSKU",
        LicenseName: "My License",
        ProductName: "My Product",
        Issuer: {
            Name: "My Company"
        },
        HomeRegion: "us-east-1",
        Validity: {
            Begin: new Date().toISOString(),
        },
        Entitlements: [
            {
                Name: "My Users",
                MaxCount: 1000,
                Overage: false,
                Unit: "Count",
                AllowCheckIn: true
            }
        ],
        Beneficiary: "My Beneficiary",
        ConsumptionConfiguration: {
            RenewType: "None",
            ProvisionalConfiguration: {
                MaxTimeToLiveInMinutes: 60
            }
        },
        ClientToken: uuidv4(),
    }).promise();
}

const createGrant = async ({ LicenseArn }) => {
    AWS.config.loadFromPath('./seller_config.json');
    const licenseManager = new AWS.LicenseManager();
    return await licenseManager.createGrant({
        LicenseArn,
        GrantName: "My Grant",
        Principals: [
            `arn:aws:iam::${BUYER_ACCOUNT_ID}:root`
        ],
        HomeRegion: "us-east-1",
        AllowedOperations: [
            "ListPurchasedLicenses",
            "CheckoutLicense",
            "CheckInLicense",
            "ExtendConsumptionLicense",
            "CheckoutBorrowLicense",
            "CreateGrant",
            "CreateToken"
        ],
        ClientToken: uuidv4(),
    }).promise();
}

const acceptGrant = async ({ GrantArn }) => {
    AWS.config.loadFromPath('./buyer_config.json');
    const licenseManager = new AWS.LicenseManager();
    return await licenseManager.acceptGrant({
        GrantArn,
    }).promise();
}

const activateGrant = async ({ GrantArn }) => {
    AWS.config.loadFromPath('./buyer_config.json');
    const licenseManager = new AWS.LicenseManager();
    return await licenseManager.createGrantVersion({
        GrantArn,
        Status: "ACTIVE",
        ClientToken: uuidv4(),
    }).promise();
}

const checkoutLicense = async ({ TempCredentials }) => {
    AWS.config.loadFromPath('./buyer_config.json');
    if (TempCredentials) {
        const { AccessKeyId, SecretAccessKey, SessionToken } = TempCredentials;
        AWS.config.update({
            accessKeyId: AccessKeyId,
            secretAccessKey: SecretAccessKey,
            sessionToken: SessionToken,
        });
    }
    const licenseManager = new AWS.LicenseManager();

    return await licenseManager.checkoutLicense({
        CheckoutType: "PROVISIONAL",
        Entitlements: [
            {
                Name: "My Users",
                Unit: "Count",
                Value: "1",
            }
        ],
        KeyFingerprint: `aws:${SELLER_ACCOUNT_ID}:My Company:issuer-fingerprint`,
        ProductSKU: "My-ProductSKU",
        ClientToken: uuidv4(),
    }).promise();
}

const extendLicenseConsumption = async ({ LicenseConsumptionToken, TempCredentials }) => {
    AWS.config.loadFromPath('./buyer_config.json');
    if (TempCredentials) {
        const { AccessKeyId, SecretAccessKey, SessionToken } = TempCredentials;
        AWS.config.update({
            accessKeyId: AccessKeyId,
            secretAccessKey: SecretAccessKey,
            sessionToken: SessionToken,
        });
    }
    const licenseManager = new AWS.LicenseManager();

    return await licenseManager.extendLicenseConsumption({
        LicenseConsumptionToken,
    }).promise();
}

const checkinLicense = async ({ LicenseConsumptionToken, TempCredentials }) => {
    AWS.config.loadFromPath('./buyer_config.json');
    if (TempCredentials) {
        const { AccessKeyId, SecretAccessKey, SessionToken } = TempCredentials;
        AWS.config.update({
            accessKeyId: AccessKeyId,
            secretAccessKey: SecretAccessKey,
            sessionToken: SessionToken,
        });
    }
    const licenseManager = new AWS.LicenseManager();

    return await licenseManager.checkInLicense({
        LicenseConsumptionToken,
    }).promise();
}

const createToken = async ({ LicenseArn }) => {
    AWS.config.loadFromPath('./buyer_config.json');
    const licenseManager = new AWS.LicenseManager();
    return await licenseManager.createToken({
        LicenseArn,  
        ClientToken: uuidv4(),
    }).promise();
}

const createPolicy = async () => {
    AWS.config.loadFromPath('./buyer_config.json');
    const iam = new AWS.IAM();
    return await iam.createPolicy({
        PolicyName: "AWSLicenseManagerConsumptionRolePolicy-Testing",
        PolicyDocument: "{\"Version\":\"2012-10-17\",\"Statement\":{\"Effect\":\"Allow\",\"Action\":[\"license-manager:CheckoutLicense\",\"license-manager:CheckInLicense\",\"license-manager:ExtendLicenseConsumption\",\"license-manager:GetLicense\"],\"Resource\":\"*\"}}",
    }).promise();
}

const createRole = async () => {
    AWS.config.loadFromPath('./buyer_config.json');
    const iam = new AWS.IAM();
    return await iam.createRole({
        AssumeRolePolicyDocument: `{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Federated\":\"openid-license-manager.amazonaws.com\"},\"Action\":\"sts:AssumeRoleWithWebIdentity\",\"Condition\":{\"ForAnyValue:StringLike\":{\"openid-license-manager.amazonaws.com:amr\":\"aws:license-manager:token-issuer-account-id:${BUYER_ACCOUNT_ID}\"}}}]}`,
        RoleName: "AWSLicenseManagerConsumptionRole-Testing",
    }).promise();
}

const attachRolePolicy = async () => {
    AWS.config.loadFromPath('./buyer_config.json');
    const iam = new AWS.IAM();
    return await iam.attachRolePolicy({
        RoleName: "AWSLicenseManagerConsumptionRole-Testing",
        PolicyArn: `arn:aws:iam::${BUYER_ACCOUNT_ID}:policy/AWSLicenseManagerConsumptionRolePolicy-Testing`,
    }).promise();
}

const getAccessToken = async ({ Token }) => {
    const licenseManager = new AWS.LicenseManager({
        credentials: null,
    });
    return await licenseManager.getAccessToken({
        Token,
    }).promise();
}

const assumeRoleWithWebIdentity = async ({ AccessToken }) => {
    const sts = new AWS.STS({
        credentials: null,
    });
    return await sts.assumeRoleWithWebIdentity({
        RoleArn: `arn:aws:iam::${BUYER_ACCOUNT_ID}:role/AWSLicenseManagerConsumptionRole-Testing`,
        RoleSessionName: "LicenseConsumptionSession",
        WebIdentityToken: AccessToken,
    }).promise();
}

const run = async () => {
    try {
        // 1. Seller - create a test license
        const { LicenseArn } = await createLicense();
        console.log("Seller successfully created the license", LicenseArn);

        // 2. Seller - create a grant of the test license to buyer
        const { GrantArn } = await createGrant({ LicenseArn });
        console.log("Seller successfully created the grant", GrantArn);

        // 3. Buyer - accept and activate the grant
        await acceptGrant({ GrantArn });
        await activateGrant({ GrantArn });
        console.log("Buyer successfully accepted and activated the grant", GrantArn);

        // 4-1. Buyer - check out, extend and check in license

        // 4-1-1. Buyer - check out the license
        const { LicenseConsumptionToken: LicenseConsumptionToken1 } = await checkoutLicense({});
        console.log("Buyer successfully checked out the license");

        // 4-1-2. Buyer - extend the license consumption
        await extendLicenseConsumption({ LicenseConsumptionToken: LicenseConsumptionToken1 });
        console.log("Buyer successfully extended the license consumption");

        // 4-1-3. Buyer - check in the license
        await checkinLicense({ LicenseConsumptionToken: LicenseConsumptionToken1 });
        console.log("Buyer successfully checked in the license");

        // 4-2. Customers without an AWS account - check out, extend and check in license
        // FYI. https://docs.aws.amazon.com/license-manager/latest/userguide/seller-issued-licenses.html#granting-temporary-credentials

        // 4-2-1. Buyer - create a comsumption IAM role (Or create it in AWS License Manager console)
        try {
            await createPolicy();
        } catch (error) {
            if (!error.message.includes("already exists")) {
                throw error;
            }
        }
        try {
            await createRole();
        } catch (error) {
            if (!error.message.includes("already exists")) {
                throw error;
            }
        }
        await attachRolePolicy();
        console.log("Buyer successfully created the comsumption role");

        // 4-2-2. Buyer - create a token of the license
        const { Token } = await createToken({ LicenseArn });
        console.log("Buyer successfully created the token");

        // 4-2-3. Customer without an AWS account - get acccess token 
        const { AccessToken } = await getAccessToken({ Token });
        console.log("Customer without an AWS account successfully got the access token");

        // 4-2-4. Customer without an AWS account - get the temporary AWS credentials
        const sleep = time => new Promise(resolve => setTimeout(resolve, time));
        let TempCredentials;
        try {
            const { Credentials } = await assumeRoleWithWebIdentity({ AccessToken });
            TempCredentials = Credentials;
            console.log("Customer without an AWS account successfully got the temp credentials");
        } catch (error) {
            if (error.message.includes("Not authorized to perform")) {
                await sleep(5000);
            } else  {
                throw error;
            }
        }

        // 4-2-5. Customer without an AWS account - check out the license
        const { LicenseConsumptionToken: LicenseConsumptionToken2 } =  await checkoutLicense({ TempCredentials });
        console.log("Customer without an AWS account successfully checked out the license");

        // 4-2-6. Customer without an AWS account - extend the license consumption
        await extendLicenseConsumption({ LicenseConsumptionToken: LicenseConsumptionToken2, TempCredentials });
        console.log("Customer without an AWS account successfully extended the license consumption");

        // 4-2-7. Customer without an AWS account - check in the license
        await checkinLicense({ LicenseConsumptionToken: LicenseConsumptionToken2, TempCredentials });
        console.log("Customer without an AWS account successfully checked in the license");

    } catch (err) {
        console.log(err);
    }
}

run();
