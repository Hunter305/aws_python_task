import boto3

mediaconnect_client = boto3.client("mediaconnect")


def start_mediaconnect_flow(arn):
    mediaconnect_client.start_flow(
        FlowArn=arn
    )
    print("service started")


arn = 'arn:aws:mediaconnect:us-east-1:891377081681:flow:1-DV0NWwIHBQcHUVgF-9f22481af7fb:amagi_test'

start_mediaconnect_flow(arn)
