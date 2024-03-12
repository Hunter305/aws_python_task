import boto3

mediaconnect_client = boto3.client("mediaconnect")


def start_mediaconnect_flow(arn):
    try:
        response = mediaconnect_client.describe_flow(FlowArn=arn)
        status = response['Flow']['Status']

        if status == 'ACTIVE':
            print("MediaConnect flow is already running.")
        else:
            mediaconnect_client.start_flow(FlowArn=arn)
            print("Service started.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


arn = 'arn:aws:mediaconnect:us-east-1:891377081681:flow:1-DV0NWwIHBQcHUVgF-9f22481af7fb:amagi_test'

start_mediaconnect_flow(arn)
