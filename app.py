from flask import Flask, request, jsonify, render_template, send_file, url_for
from tiktok_client import start_client, get_latest_comment, start_cleanup_thread
from youtube_client import start_client_yt, get_latest_comment_yt, start_cleanup_thread_yt
import os
from gtts import gTTS
from threading import Lock
import utils
app = Flask(__name__)

comment_lock = Lock()
audio_dir_tiktok = "audio_files_tiktok"
audio_dir_youtube = "audio_files_youtube"
os.makedirs(audio_dir_tiktok, exist_ok=True)
os.makedirs(audio_dir_youtube, exist_ok=True)



@app.route("/")
def index():
    return render_template("tiktok.html")
@app.route("/youtube")
def youtube():
    return render_template("youtube.html")
@app.route("/tiktok/start", methods=["POST"])
def start():
    username = request.json.get("username")
    if not username:
        return jsonify({"error": "Missing username"}), 400

    start_client(username)
    return jsonify({"message": f"Started TikTok client for {username}"}), 200

@app.route("/tiktok/comment/<username>")
def get_comment(username):
    comment = get_latest_comment(username)
    if comment:
        with comment_lock:
            mp3_path = os.path.join(audio_dir_tiktok, f"{username}.mp3")
            tts = gTTS(comment, lang='vi')
            tts.save(mp3_path)
        audio_url = url_for('get_audio_tiktok', username=username)
    else:
        audio_url = None

    return jsonify({"username": username, "latest_comment": comment, "audio_url": audio_url})

@app.route("/tiktok/audio/<username>")
def get_audio_tiktok(username):
    mp3_path = os.path.join(audio_dir_tiktok, f"{username}.mp3")
    if os.path.exists(mp3_path):
        utils.change_speed(mp3_path,mp3_path, 1.3)
        return send_file(mp3_path, mimetype="audio/mpeg")
    return jsonify({"error": "No audio found"}), 404

## yt

@app.route("/youtube/start", methods=["POST"])
def start_youtube():
    username = request.json.get("username")
    if not username:
        return jsonify({"error": "Missing username"}), 400

    start_client_yt(username)
    return jsonify({"message": f"Started Youtube client for {username}"}), 200

@app.route("/youtube/comment", methods=["POST"])
def get_comment_youtube():
    username = request.json.get("username")
    if not username:
        return jsonify({"error": "Missing username"}), 400
    comment = get_latest_comment_yt(username)
    filename = utils.convert_username_youtube(username) + ".mp3"
    mp3_path = os.path.join(audio_dir_youtube, filename)
    if comment:
        with comment_lock:
            mp3_path = os.path.join(audio_dir_youtube, filename)
            tts = gTTS(comment, lang='vi')
            tts.save(mp3_path)
        audio_url = url_for('get_audio_youtube', username=username)
    else:
        audio_url = None

    return jsonify({"username": username, "latest_comment": comment, "audio_url": audio_url})

@app.route("/youtube/audio", methods=["POST"])
def get_audio_youtube():
    username = request.json.get("username")
    filename = utils.convert_username_youtube(username) + ".mp3"
    mp3_path = os.path.join(audio_dir_youtube, filename)
    if os.path.exists(mp3_path):
        utils.change_speed(mp3_path,mp3_path, 1.3)
        return send_file(mp3_path, mimetype="audio/mpeg")
    return jsonify({"error": "No audio found"}), 404



if __name__ == "__main__":
    start_cleanup_thread()
    start_cleanup_thread_yt()
    app.run(debug=True, host='0.0.0.0', port=80)
