import boto3

media_client = boto3.client("medialive")


def stop_channel(channel_id):
    try:
        response = media_client.describe_channel(
            ChannelId=channel_id
        )
        if response["State"] == "RUNNING":
            media_client.stop_channel(
                ChannelId=channel_id
            )
            print("channel has been stopped")
        elif response["State"] == "IDLE":
            print("channel is not ruuning")
        else:
            print("error starting the channel with status :" +
                  response["State"])
    except Exception as e:
        print(f"An error occurred: {str(e)}")


channel_id = "5731283"

stop_channel(channel_id)
