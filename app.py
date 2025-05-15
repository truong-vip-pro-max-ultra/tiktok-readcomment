from flask import Flask, request, jsonify, render_template, send_file, url_for
from tiktok_client import start_client, get_latest_comment
import os
from gtts import gTTS
from threading import Lock
import soundfile as sf
import scipy.signal as signal
app = Flask(__name__)

comment_lock = Lock()
audio_dir = "audio_files"
os.makedirs(audio_dir, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    username = request.json.get("username")
    if not username:
        return jsonify({"error": "Missing username"}), 400

    start_client(username)
    return jsonify({"message": f"Started TikTok client for {username}"}), 200

@app.route("/comment/<username>")
def get_comment(username):
    comment = get_latest_comment(username)
    if comment:
        with comment_lock:
            mp3_path = os.path.join(audio_dir, f"{username}.mp3")
            tts = gTTS(comment, lang='vi')
            tts.save(mp3_path)
        audio_url = url_for('get_audio', username=username)
    else:
        audio_url = None

    return jsonify({"username": username, "latest_comment": comment, "audio_url": audio_url})

@app.route("/audio/<username>")
def get_audio(username):
    mp3_path = os.path.join(audio_dir, f"{username}.mp3")
    if os.path.exists(mp3_path):
        change_speed(mp3_path,mp3_path, 1.3)
        return send_file(mp3_path, mimetype="audio/mpeg")
    return jsonify({"error": "No audio found"}), 404

def change_speed(input_file, output_file, speed_factor):
    audio, sample_rate = sf.read(input_file)

    adjusted_audio = signal.resample(audio, int(len(audio) / speed_factor))

    sf.write(output_file, adjusted_audio, sample_rate)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
