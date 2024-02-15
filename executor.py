from concurrent.futures import ThreadPoolExecutor


import boto3 as boto3
import json
import time
AWS_PROFILE = 'KLAM-'
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


"""
This function will get more information about an AMI in the format mentioned in the documentation
"""
def getAMIInfo(amiID):
   session = boto3.session.Session(profile_name=AWS_PROFILE,region_name='us-east-1')
   ec2 = session.client('ec2')
   response = ec2.describe_images(
       ImageIds=[
           amiID,
       ]
   )
   keysMapping={"Description":"ImageDescription","OwnerId":"ImageOwnerID","Name":"ImageName","ImageLocation":"ImageLocation"}


   for key in keysMapping.keys():
       if response["Images"]:


           if key in response["Images"][0]:
               AMIDictionary[amiID][keysMapping[key]] = response["Images"][0][key]
           else:
               AMIDictionary[amiID][keysMapping[key]] = "null"
       else:
           AMIDictionary[amiID][keysMapping[key]] = "null"


""""
This function will list all AMI instances in a region, and then gets more information about each AMI in parallel
"""
def listEC2InstanceAMIs(region):
   if region not in retrieveRegionsEC2IsAvailableIn():
       raise Exception("Region not available")
   #create a session for the region that we are going to check
   session = boto3.session.Session(profile_name=AWS_PROFILE,region_name=region)
   ec2_resource = session.client('ec2')
   #create a paginator to get all instances and all the information about them
   paginator = ec2_resource.get_paginator('describe_instances')


   #paginate the results so you don't get issues with the 1000 instance limit
   #there might be a way to parallelise this but since it's just an API call to AWS I don't think it's worth it
   for page in paginator.paginate():
       for reservation in page["Reservations"]:
           for instance in reservation["Instances"]:
               if instance["ImageId"] not in AMIDictionary.keys():
                   temporaryDictionary = createBasicAMIDictionary(instance["ImageId"],instance["InstanceId"])
                   AMIDictionary[instance["ImageId"]] = temporaryDictionary
               else:
                   AMIDictionary[instance["ImageId"]]["countOfInstances"]  += 1
                   AMIDictionary[instance["ImageId"]]["InstanceIds"].append(instance["InstanceId"])


   #Now that we have the dictionary with the amiID and the count of instances, we can add more information for each AMI in parallel
   with ThreadPoolExecutor(20) as executor:
       executor.map(getAMIInfo, AMIDictionary.keys())


   #this is the sequential way of doing it that is ugly
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


   listEC2InstanceAMIs('us-east-1')
   print("--- %s seconds ---" % (time.time() - start_time))

