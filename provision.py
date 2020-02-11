#!/usr/bin/python3

import boto3

#Creating VPC, User Needs To Input VPC Deatils When Asked

ec2=boto3.resource('ec2')
name=input("Enter VPC Name")
ip=input("Kindly Enter Cidr For VPC")
vpc=ec2.create_vpc(CidrBlock=ip)
vpc.create_tags(Tags=[{"Key": "Name", "Value": name}])
vpc.wait_until_available()
print(vpc.id)

#Creating Gateway and attaching to VPC

gateway=ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=gateway.id, VpcId=vpc.id)
g_name=input("Kindly Enter GateWay Name \n")
gateway.create_tags(Tags=[{"Key": "Name", "Value": g_name}])
print(gateway.id)

#Creating Route and Route Table

route=ec2.create_route_table(VpcId=vpc.id)
route.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=gateway.id)
route.create_tags(Tags=[{"Key": "Name", "Value": name}])
print(route.id)

#Creating Subnet User Need To Input Details As Asked

s_b=input("Enter Subnet Value")
subnet=ec2.create_subnet(CidrBlock=s_b, VpcId=vpc.id)
s_b2=input("Enter Subnet Value")
subnet2=ec2.create_subnet(CidrBlock=s_b2, VpcId=vpc.id)
subnet.create_tags(Tags=[{"Key": "Name", "Value": name}])
subnet2.create_tags(Tags=[{"Key": "Name", "Value": name}]) 
route.associate_with_subnet(SubnetId=subnet.id)
print(subnet.id) 

#Creating Security Group  

security=ec2.create_security_group(Description="Idea", VpcId=vpc.id, GroupName="idea")
security.authorize_ingress(
CidrIp='0.0.0.0/0',
IpProtocol='tcp',
FromPort=22,
ToPort=22
)
print(security.id)

#Creating EC2 Instances
e_in=input("Kindly Input Image ID")
e_it=input("Kindly Input Instance Type")
new_ec2=ec2.create_instances(InstanceType=e_it, MaxCount=2, MinCount=1, ImageId=e_in, NetworkInterfaces=[{'SubnetId': subnet.id, 'AssociatePublicIpAddress': True, 'DeviceIndex': 0, 'Groups': [security.group_id]}])
new_ec2[0].wait_until_running()
print("All Done Enjoy Your Machine !! Here Is Your Public and Private IP Address")
print(new_ec2[0].private_ip_address)
print(new_ec2[0].public_ip_address)
