import boto3

mediaconnect_client = boto3.client("mediaconnect")


def stop_mediaconnect_flow(arn):
    response = mediaconnect_client.stop_flow(
        FlowArn=arn
    )
    print("service stopped")


arn = 'arn:aws:mediaconnect:us-east-1:891377081681:flow:1-DV0NWwIHBQcHUVgF-9f22481af7fb:amagi_test'

stop_mediaconnect_flow(arn)
