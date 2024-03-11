import boto3

media_client = boto3.client("medialive")


def stop_channel(channel_id):
    media_client.stop_channel(
        ChannelId=channel_id
    )
    print("media live channel stopped")


channel_id = "3678614"
stop_channel(channel_id)
