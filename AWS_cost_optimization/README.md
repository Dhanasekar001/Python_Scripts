# AWS Cost Optimization - EBS Snapshot Cleanup  

## Overview  
This Python script helps **optimize AWS costs** by automatically deleting **EBS snapshots** that are no longer needed.  

## Deletion Criteria  
The script checks and deletes **EBS snapshots** if they meet **all** of the following conditions:  

- The snapshot is **older than 30 days**.  
- **Any** of the following conditions are met:  
  1. The **associated volume does not exist** (i.e., the volume has been deleted).  
  2. The **volume is not attached** to any EC2 instance.  
  3. The **volume is attached to an inactive EC2 instance** (i.e., the instance is stopped or terminated).  

By removing unnecessary snapshots, this script helps **reduce AWS storage costs**.  

## Usage  
1. Make sure you have **AWS credentials configured** for `boto3` to access your AWS account.  
2. Install required dependencies:  
   ```sh
   pip install boto3 botocore
