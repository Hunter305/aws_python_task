from flask import Flask, jsonify, request
import boto3
import botocore.exceptions as botoException
import logging
from flask_cors import CORS
import subprocess
import os

media_client = boto3.client("medialive")
mediaconnect_client = boto3.client("mediaconnect")

app = Flask(__name__)

CORS(app)
# list all the channel


@app.route("/api/medialive", methods=["GET"])
def list_channel():
    try:
        response = media_client.list_channels()
        return jsonify({"channels": response["Channels"]}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# channel description


@app.route("/api/medialive/<channelid>", methods=["GET"])
def get_channel(channelid):
    try:
        response = media_client.describe_channel(ChannelId=channelid)
        jsonify({"response": response}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# start a channel


@app.route("/api/medialive/<channelid>/start", methods=["POST"])
def start_channel(channelid):
    try:
        response = media_client.describe_channel(ChannelId=channelid)
        if response["State"] == "IDLE":
            media_client.start_channel(ChannelId=channelid)
            return jsonify({"message": "channel started"}), 200
        elif response["State"] == "RUNNING":
            return jsonify({"message": "channel is ALREADY running"}), 200
        else:
            return jsonify({"message": "Error starting the channel with status: " + response["State"]}), 400
    except botoException.ClientError as error:
        if error.response['Error']['Code'] == 'NotFoundException':
            return jsonify({"message": "channel not found"})
        else:
            return jsonify({"message": "there was client error"})
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# stop a media live channel


@app.route("/api/medialive/<channelid>/stop", methods=["POST"])
def stop_channel(channelid):
    try:
        response = media_client.describe_channel(
            ChannelId=channelid
        )
        if response["State"] == "RUNNING":
            media_client.stop_channel(
                ChannelId=channelid
            )
            return jsonify({"message": "channel has been stopped"}), 200
        elif response["State"] == "IDLE":
            return jsonify({"message": "channel is not ruuning"}), 200
        else:
            return jsonify({"message": "error starting the channel with status :" +
                            response["State"]}), 400
    # except NotFoundException as nf:
    #     return jsonify({"message": "channel not found"}), 404
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# media connect client endpoints

# get all media connect flow


@app.route("/api/mediaconnect", methods=["GET"])
def list_flow():
    try:
        response = mediaconnect_client.list_flows()
        return jsonify({"flows": response["FLOWS"]}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# describe a media connect flow


@app.route("/api/mediaconnect/<flowArn>", methods=["GET"])
def get_media_flow(flowArn):
    try:
        response = mediaconnect_client.describe_flow(FlowArn=flowArn)
        jsonify({"response": response}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


s3_client = boto3.client("s3")


@app.route("/api/s3", methods=["GET"])
def get_s3():
    try:
        response = s3_client.list_buckets()
        return jsonify({"response": response["Buckets"]}), 200
    except Exception as e:
        return jsonify({"message": f"there was an error with error message {str(e)}"}), 500


@app.route('/run-aws-command', methods=['POST'])
def run_aws_command():
    data = request.json
    aws_access_key_id = data.get('aws_access_key_id')
    aws_secret_access_key = data.get('aws_secret_access_key')
    aws_session_token = data.get('aws_session_token')

    os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
    if aws_session_token:
        os.environ['AWS_SESSION_TOKEN'] = aws_session_token

    command = "aws s3 ls"

    try:
        result = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT)
        os.environ.pop('AWS_ACCESS_KEY_ID', None)
        os.environ.pop('AWS_SECRET_ACCESS_KEY', None)
        os.environ.pop('AWS_SESSION_TOKEN', None)

        return jsonify({'output': result.decode('utf-8')}), 200
    except subprocess.CalledProcessError as e:
        os.environ.pop('AWS_ACCESS_KEY_ID', None)
        os.environ.pop('AWS_SECRET_ACCESS_KEY', None)
        os.environ.pop('AWS_SESSION_TOKEN', None)

        return jsonify({'error': 'Failed to execute command', 'details': e.output.decode('utf-8')}), 400
