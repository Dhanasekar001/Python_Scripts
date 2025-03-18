import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get a list of all EBS snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Get all active ec2 instances ID's
    instance_response = ec2.describe_instances(Filters = [{'Name': 'instance-state-name', 'Values': ['running']}])
    active_instances_ids = set()

    for reservation in instance_response['Reservations']:
        for instance in reservation['Instances']:
            active_instances_ids.add(instance['InstanceId'])

    # Iterate through each snapshot and delete if it's not attached to any volume or the volume is not attached to any active instance and is older than 30 days
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot['VolumeId']

        # Delete the snapshot if it's not attached to any volume
        if not volume_id:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted snapshot {snapshot_id} because it has no associated volume.")
            continue
        
        # Check if the snapshot is older than 30 days
        snapshot_date = snapshot['StartTime'].date()
        if snapshot_date >= (datetime.now() - timedelta(days=30)).date():
            print(f"Skipping snapshot {snapshot_id} (created on {snapshot_date}), not older than 30 days.")
            continue

        try:
            volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
            volume = volume_response['Volumes'][0]
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                # Volume does not exist, delete the snapshot
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted snapshot {snapshot_id} because its volume {volume_id} does not exist.")
            else:
                print(f"Error describing volume {volume_id}: {e}")
            continue

        # Check if the volume is attached to an active instance
        attachments = volume.get('Attachments', [])
        if not attachments:
            # Volume is not attached to any instance, delete snapshot
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted snapshot {snapshot_id} because its volume {volume_id} is not attached to any instance.")
        else:
            # Check if the attached instance is active
            instance_id = attachments[0].get('InstanceId')
            if instance_id not in active_instances_ids:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted snapshot {snapshot_id} because its volume {volume_id} is attached to a non-active instance.")
            else:
                print(f"Skipped snapshot {snapshot_id} because it is attached to an active instance {instance_id}.")

