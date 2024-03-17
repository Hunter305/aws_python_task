from flask import Flask, jsonify
import boto3
import logging

media_client = boto3.client("medialive")

app = Flask(__name__)


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
def start_channel(channelid):
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
