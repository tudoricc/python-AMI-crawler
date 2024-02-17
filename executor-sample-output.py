from concurrent.futures import ThreadPoolExecutor


import boto3 as boto3
import json
import time
import random
AWS_PROFILE = '<<ADD-NAME-PROFILE>>'
AMIDictionary = {}


def retrieveRegionsEC2IsAvailableIn():
    session = boto3.session.Session(profile_name=AWS_PROFILE,region_name='us-east-1')
    ec2 = session.client('ec2')
    # Retrieves all regions/endpoints that work with EC2
    response = ec2.describe_regions()
    regionName = []
    for regionEndpoint in response['Regions']:
        regionName.append(regionEndpoint['RegionName'])
    return regionName


"""
This function will create a basic dictionary for an AMI in the format that we want the output to be
"""
def createBasicAMIDictionary(amiID,instanceId):
   basicDictionary = {}


   basicDictionary["ImageDescription"] = ""
   basicDictionary["ImageName"] = ""
   basicDictionary["ImageOwnerID"] = ""
   basicDictionary["ImageLocation"] = ""
   basicDictionary["InstanceIds"] = [instanceId]
   basicDictionary["countOfInstances"] = 1
   return basicDictionary


"""This method creates mock AMI data based on https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-images.html#examples"""
def createMockDataAMI(amiID):
    mockAMIJson = {
        "Images": [
            {
                "VirtualizationType": "hvm",
                "Description": "Provided by Red Hat, Inc.",
                "PlatformDetails": "Red Hat Enterprise Linux",
                "EnaSupport": "true",
                "Hypervisor": "xen",
                "State": "available",
                "SriovNetSupport": "simple",
                "ImageId": "ami-XXXX",
                "UsageOperation": "RunInstances:0010",
                "BlockDeviceMappings": [
                    {
                        "DeviceName": "/dev/sda1",
                        "Ebs": {
                            "SnapshotId": "snap-111222333444aaabb",
                            "DeleteOnTermination": "true",
                            "VolumeType": "gp2",
                            "VolumeSize": 10,
                            "Encrypted": "false"
                        }
                    }
                ],
                "Architecture": "x86_64",
                "ImageLocation": "123456789012/RHEL-8.0.0_HVM-20190618-x86_64-1-Hourly2-GP2",
                "RootDeviceType": "ebs",
                "OwnerId": "",
                "RootDeviceName": "/dev/sda1",
                "CreationDate": "2019-05-10T13:17:12.000Z",
                "Public": "true",
                "ImageType": "machine",
                "Name": "RHEL-8.0.0_HVM-20190618-x86_64-1-Hourly2-GP2"
            }
        ]
    }
    mockAMIJson["Images"][0]["ImageId"]="ami-" + str(amiID)
    #print(json.dumps(mockAMIJson,indent=2))
    return mockAMIJson


"""
This method creates mock describe instances  data  based on https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-instances.html#examples
"""
def createMockDataImages(numberMockInstances):
    
    fullJson={
    "Reservations": [
        {
            "Groups": [],
            "Instances": [
                
            ],
            "OwnerId": "111111111111",
            "ReservationId": "r-1234567890abcdefg"
        }
    ]
    }
     

    ProxyString = "uname--user--country--us--session--"
    
    randomNumbers = random.sample(range(12223, 6666699), numberMockInstances)
    listInstancesKey = []
    for number  in randomNumbers:
        stringInstances={
                    "AmiLaunchIndex": 0,
                    "ImageId": "ami-IMAGEID",
                    "InstanceId": "i-IMGEID2",
                    "InstanceType": "t3.nano",
                    "KeyName": "my-key-pair",
                    "LaunchTime": "2022-11-15T10:48:59+00:00",
                    "Monitoring": {
                        "State": "disabled"
                    },
                    "Placement": {
                        "AvailabilityZone": "us-east-2a",
                        "GroupName": "",
                        "Tenancy": "default"
                    },
                    "PrivateDnsName": "ip-10-0-0-157.us-east-2.compute.internal",
                    "PrivateIpAddress": "10-0-0-157",
                    "ProductCodes": [],
                    "PublicDnsName": "ec2-34-253-223-13.us-east-2.compute.amazonaws.com",
                    "PublicIpAddress": "34.253.223.13",
                    "State": {
                        "Code": "16",
                        "Name": "running"
                    },
                    "StateTransitionReason": "",
                    "SubnetId": "subnet-04a636d18e83cfacb",
                    "VpcId": "vpc-1234567890abcdef0",
                    "Architecture": "x86_64",
                    "BlockDeviceMappings": [
                        {
                            "DeviceName": "/dev/xvda",
                            "Ebs": {
                                "AttachTime": "2022-11-15T10:49:00+00:00",
                                "DeleteOnTermination": "true",
                                "Status": "attached",
                                "VolumeId": "vol-02e6ccdca7de29cf2"
                            }
                        }
                    ],
                    "ClientToken": "1234abcd-1234-abcd-1234-d46a8903e9bc",
                    "EbsOptimized": "true",
                    "EnaSupport": "true",
                    "Hypervisor": "xen",
                    "IamInstanceProfile": {
                        "Arn": "arn:aws:iam::111111111111:instance-profile/AmazonSSMRoleForInstancesQuickSetup",
                        "Id": "111111111111111111111"
                    },
                    "NetworkInterfaces": [
                        {
                            "Association": {
                                "IpOwnerId": "amazon",
                                "PublicDnsName": "ec2-34-253-223-13.us-east-2.compute.amazonaws.com",
                                "PublicIp": "34.253.223.13"
                            },
                            "Attachment": {
                                "AttachTime": "2022-11-15T10:48:59+00:00",
                                "AttachmentId": "eni-attach-1234567890abcdefg",
                                "DeleteOnTermination": "true",
                                "DeviceIndex": "0",
                                "Status": "attached",
                                "NetworkCardIndex": "0"
                            },
                            "Description": "",
                            "Groups": [
                                {
                                    "GroupName": "launch-wizard-146",
                                    "GroupId": "sg-1234567890abcdefg"
                                }
                            ],
                            "Ipv6Addresses": [],
                            "MacAddress": "00:11:22:33:44:55",
                            "NetworkInterfaceId": "eni-1234567890abcdefg",
                            "OwnerId": "104024344472",
                            "PrivateDnsName": "ip-10-0-0-157.us-east-2.compute.internal",
                            "PrivateIpAddress": "10-0-0-157",
                            "PrivateIpAddresses": [
                                {
                                    "Association": {
                                        "IpOwnerId": "amazon",
                                        "PublicDnsName": "ec2-34-253-223-13.us-east-2.compute.amazonaws.com",
                                        "PublicIp": "34.253.223.13"
                                    },
                                    "Primary": "true",
                                    "PrivateDnsName": "ip-10-0-0-157.us-east-2.compute.internal",
                                    "PrivateIpAddress": "10-0-0-157"
                                }
                            ],
                            "SourceDestCheck": "true",
                            "Status": "in-use",
                            "SubnetId": "subnet-1234567890abcdefg",
                            "VpcId": "vpc-1234567890abcdefg",
                            "InterfaceType": "interface"
                        }
                    ],
                    "RootDeviceName": "/dev/xvda",
                    "RootDeviceType": "ebs",
                    "SecurityGroups": [
                        {
                            "GroupName": "launch-wizard-146",
                            "GroupId": "sg-1234567890abcdefg"
                        }
                    ],
                    "SourceDestCheck": "true",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "my-instance"
                        }
                    ],
                    "VirtualizationType": "hvm",
                    "CpuOptions": {
                        "CoreCount": "1",
                        "ThreadsPerCore": "2"
                    },
                    "CapacityReservationSpecification": {
                        "CapacityReservationPreference": "open"
                    },
                    "HibernationOptions": {
                        "Configured": "true"
                    },
                    "MetadataOptions": {
                        "State": "applied",
                        "HttpTokens": "optional",
                        "HttpPutResponseHopLimit": 1,
                        "HttpEndpoint": "enabled",
                        "HttpProtocolIpv6": "disabled",
                        "InstanceMetadataTags": "enabled"
                    },
                    "EnclaveOptions": {
                        "Enabled": "true"
                    },
                    "PlatformDetails": "Linux/UNIX",
                    "UsageOperation": "RunInstances",
                    "UsageOperationUpdateTime": "2022-11-15T10:48:59+00:00",
                    "PrivateDnsNameOptions": {
                        "HostnameType": "ip-name",
                        "EnableResourceNameDnsARecord": "true",
                        "EnableResourceNameDnsAAAARecord": "false"
                    },
                    "MaintenanceOptions": {
                        "AutoRecovery": "default"
                    }
                }
     
        stringInstances["InstanceId"] = "i-" + str(number) 
        stringInstances["ImageId"] = "ami-" + str(number+2)


        listInstancesKey.append(stringInstances)
    fullJson["Reservations"][0]["Instances"] = listInstancesKey
    return fullJson



"""
This function will get more information about an AMI in the format mentioned in the documentation
"""
def getAMIInfo(amiID):
    responseMockAmi = createMockDataAMI(amiID)
    keysMapping={"Description":"ImageDescription","OwnerId":"ImageOwnerID","Name":"ImageName","ImageLocation":"ImageLocation"}


    for key in keysMapping.keys():
        if responseMockAmi["Images"]:
            if key in responseMockAmi["Images"][0]:
                AMIDictionary[amiID][keysMapping[key]] = responseMockAmi["Images"][0][key]
            if not responseMockAmi["Images"][0][key]:
                AMIDictionary[amiID][keysMapping[key]] = "null"
        else:
            AMIDictionary[amiID][keysMapping[key]] = "null"


""""
This function will list all AMI instances in a region, and then gets more information about each AMI in parallel
"""
def listEC2InstanceAMIs(region):

    #Let's generate some mock data maybewe don't have an aws account
    #open the json with mock data and start going through the Reservations key
    json_input = createMockDataImages(20)


    for reservation in json_input["Reservations"]:
            for instance in reservation["Instances"]:
                if instance["ImageId"] not in AMIDictionary.keys():
                    temporaryDictionary = createBasicAMIDictionary(instance["ImageId"],instance["InstanceId"])
                    AMIDictionary[instance["ImageId"]] = temporaryDictionary
                else:
                    AMIDictionary[instance["ImageId"]]["countOfInstances"]  += 1
                    AMIDictionary[instance["ImageId"]]["InstanceIds"].append(instance["InstanceId"])


    #Now that we have the dictionary with the amiID and the count of instances, we can add more information for each AMI in parallel
    with ThreadPoolExecutor() as executor:
       executor.map(getAMIInfo, AMIDictionary.keys())


   #this is the sequential way of doing it that is ugly and was used to compare time
   # for amiID in AMIDictionary.keys():
   #     getAMIInfo(amiID)


    print(json.dumps(AMIDictionary,indent=2))


''''
This function will list all AMI instances in all regions
We can use this method for a quick check of all AMIs in all regions in a more parallel way
'''
def listInstancesInAllRegions():
    regions = ['us-east-1']  # Add all regions you want to check
    with ThreadPoolExecutor() as executor:
        executor.map(listEC2InstanceAMIs, regions)


if __name__ == "__main__":


    start_time = time.time()
    #create_mock_data_AMI("1234")
    #create_mock_data_Images()
    listEC2InstanceAMIs('us-east-1')
    print("--- %s seconds ---" % (time.time() - start_time))

