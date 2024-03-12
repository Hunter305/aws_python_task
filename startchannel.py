import boto3

media_client = boto3.client("medialive")


def start_channel(channel_id):
    try:
        response = media_client.describe_channel(
            ChannelId=channel_id
        )
        if response["State"] == "IDLE":
            media_client.start_channel(
                ChannelId=channel_id
            )
            print("channel started")
        elif response["State"] == "RUNNING":
            print("channel is ALREADY running")
        else:
            print("error starting the channel with status :" +
                  response["State"])
    except Exception as e:
        print(f"An error occurred: {str(e)}")


channel_id = "5731283"
start_channel(channel_id)
