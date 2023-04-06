import boto3
import base64
import datetime
import pprint
import uuid
from boto3.session import Session
from datetime import datetime
from datetime import timedelta

default_region = 'us-east-1'

# Helper method to get linux subscriptions usage metrics
def get_linux_subscriptions_usage_metrics(Namespace, MetricName, StartTime):
    cloudwatch = get_cw_client(default_region)
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': Namespace,
                        'MetricName': MetricName,
                        'Dimensions': [
                            {
                                'Name': 'SubscriptionName',
                                'Value': 'Red Hat Enterprise Linux Server',
                            },
                            {
                                'Name': 'SubscriptionName',
                                'Value': 'SUSE Linux Enterprise Server',
                            },
                        ]
                    },
                    'Period': 3600,
                    'Stat': 'Sum',
                    'Unit': 'Count'
                },
                'ReturnData': True,
            },
        ],
        StartTime = StartTime,
        EndTime = datetime.now(),
    )
    print('Cloud Watch Get Metrics Statistics API response:')
    pprint.pprint(response)
    return

# Helper method to create linux subscriptions usage alarms
def create_linux_subscriptions_usage_alarms(AlarmName, Namespace, MetricName):
    cloudwatch = get_cw_client(default_region)
    response = cloudwatch.put_metric_alarm(
        AlarmName = AlarmName,
        ComparisonOperator = 'GreaterThanThreshold',
        EvaluationPeriods = 1,
        MetricName = MetricName,
        Namespace = Namespace,
        Period = 3600,
        Statistic = 'Sum',
        Threshold = 100.0,
        ActionsEnabled = False,
        AlarmDescription='Alarm when count exceeds 100',
        Dimensions = [
            {
                'Name': 'SubscriptionName',
                'Value': 'Red Hat Enterprise Linux Server',
            }
        ], 
        Unit = 'Count'
    )
    print('Cloud Watch Put Alarm API response:')
    pprint.pprint(response)
    return

# Helper method to describe linux subscriptions usage alarms
def describe_linux_subscriptions_usage_alarms(AlarmNames):
    cloudwatch = get_cw_client(default_region)
    response = cloudwatch.describe_alarms(
        AlarmNames = AlarmNames
    )
    while True:
        print('Cloud Watch Put Alarm API response:')
        pprint.pprint(response)
        if "NextToken" in response:
            next_token = response['NextToken']
            response = cloudwatch.describe_alarms(
            AlarmNames = AlarmNames,
            NextToken = next_token
        )
        else:
            break
    return

# Helper method to get license manager linux subscription settings
def get_linux_subscriptions_settings():
    lm_linux_subscriptions_client = get_lm_client(default_region)
    response = lm_linux_subscriptions_client.get_service_settings()
    print('AWS License Manager Linux Subscriptions - GetServiceSettings API response:')
    pprint.pprint(response)
    return response


def get_cw_client(Region):
    return boto3.client('cloudwatch', Region)

def get_lm_client(Region):
    return boto3.client('license-manager-linux-subscriptions', Region)

def main(command_line=None):
    print("Start of the AWS License Manager Linux Subscriptions samples")
    
    # Get current linux subscriptions settings 
    get_linux_subscriptions_settings()
    
    Statistics=['Sum']
    StartTime = datetime.now() - timedelta(days=1)
    
    # Get current linux subscriptions usage metrics for RHEL and SUSE 
    get_linux_subscriptions_usage_metrics('AWS/LicenseManager/LinuxSubscriptions', 'RunningInstancesCount', StartTime)
    
    AlarmName = 'Sample Linux Usage Alarm'
    # create alarm for linux subscriptions usage metrics
    create_linux_subscriptions_usage_alarms(AlarmName, 'AWS/LicenseManager/LinuxSubscriptions', 'RunningInstancesCount')
    
    # describe alarms for linux subscriptions usage metrics
    describe_linux_subscriptions_usage_alarms([AlarmName])
    
    #For more details on filters please check: https://docs.aws.amazon.com/license-manager/latest/userguide/linux-subscriptions-usage-alarms.html
    
    
if __name__ == '__main__':
    main()
