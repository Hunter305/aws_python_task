import boto3

mediaconnect_client = boto3.client("mediaconnect")


def stop_mediaconnect_flow(arn):
    try:
        response = mediaconnect_client.describe_flow(FlowArn=arn)
        status = response['Flow']['Status']

        if status == 'STANDBY':
            print("MediaConnect flow is already in standby.")
        else:
            mediaconnect_client.start_flow(FlowArn=arn)
            print("Service stopped.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


arn = 'arn:aws:mediaconnect:us-east-1:891377081681:flow:1-DV0NWwIHBQcHUVgF-9f22481af7fb:amagi_test'

stop_mediaconnect_flow(arn)
