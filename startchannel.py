import boto3

media_client = boto3.client("medialive")


def start_channel(channel_id):
    media_client.start_channel(
        ChannelId=channel_id
    )
    print("media live channel started")


channel_id = "3678614"
start_channel(channel_id)
