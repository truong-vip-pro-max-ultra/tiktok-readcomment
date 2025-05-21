from flask import Flask, request, jsonify, render_template, send_file, url_for, abort
from tiktok_client import (start_client,
                           get_latest_comment,
                           start_cleanup_thread,
                           is_live_stream,
                           enable_likes,
                           enable_comments,
                           enable_gifts)
from youtube_client import start_client_yt, get_latest_comment_yt, start_cleanup_thread_yt
import os
from gtts import gTTS
from threading import Lock
import utils
import asyncio
import ai

app = Flask(__name__)

comment_lock_tiktok = Lock()
comment_lock_youtube = Lock()
audio_dir_tiktok = "audio_files_tiktok"
audio_dir_youtube = "audio_files_youtube"
os.makedirs(audio_dir_tiktok, exist_ok=True)
os.makedirs(audio_dir_youtube, exist_ok=True)

old_comment_tiktok = {}
old_comment_youtube = {}

ALLOWED_ORIGINS = ['https://livestreamvoice.com']
# ALLOWED_ORIGINS = ['http://localhost']

@app.before_request
def block_external_requests():
    origin = request.headers.get('Origin')
    referer = request.headers.get('Referer')

    if origin and origin not in ALLOWED_ORIGINS:
        abort(403)

    if referer and not referer.startswith(tuple(ALLOWED_ORIGINS)):
        abort(403)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("tiktok.html")
@app.route("/")
def index():
    return render_template("tiktok.html")
@app.route("/youtube")
def youtube():
    return render_template("youtube.html")

@app.route("/tiktok/check/<username>", methods=["GET"])
def check_is_live_stream(username):
    if not username:
        return jsonify({"error": "Missing username"}), 400
    check = asyncio.run(is_live_stream(username))
    if check:
        return jsonify({"message": f"Started TikTok client for {username}"}), 200
    return jsonify({"error": f"{username} not live"}), 400

@app.route("/tiktok/start", methods=["POST"])
def start():
    username = request.json.get("username")
    if not username:
        return jsonify({"error": "Missing username"}), 400

    start_client(username)
    return jsonify({"message": f"Started TikTok client for {username}"}), 200

@app.route("/tiktok/comment/<username>", methods=["POST"])
def get_comment(username):
    reply = request.form.get("reply")

    for key, store in [("like", enable_likes), ("cmt", enable_comments), ("gift", enable_gifts)]:
        store[username] = bool(request.form.get(key))

    if reply:
        enable_likes[username] = False

    has_new_comment = False
    comment = get_latest_comment(username)
    audio_url = url_for('get_audio_tiktok', username=username)

    if comment:
        if username in old_comment_tiktok.keys():
            if old_comment_tiktok[username] != comment:
                old_comment_tiktok[username] = comment
                has_new_comment = True
        else:
            old_comment_tiktok[username] = comment

        if has_new_comment:
            with comment_lock_tiktok:
                mp3_path = os.path.join(audio_dir_tiktok, f"{username}.wav")
                if reply:
                    if not comment.lower().startswith('cảm ơn'):
                        name = utils.cut_string_head(comment, ' : ')
                        content = utils.cut_string_last(comment, ' : ')
                        answer = comment + " . . . " + ai.process_v2(name, content)
                        utils.save_speech(answer, mp3_path)
                    else:
                        comment = ''
                else:
                    utils.save_speech(comment, mp3_path)
        else:
            comment = ''

    return jsonify({"username": username, "latest_comment": comment, "audio_url": audio_url})



@app.route("/tiktok/audio/<username>")
def get_audio_tiktok(username):
    # mp3_path = os.path.join(audio_dir_tiktok, f"{username}.mp3")
    mp3_path = os.path.join(audio_dir_tiktok, f"{username}.wav")
    if os.path.exists(mp3_path):
        utils.change_speed(mp3_path,mp3_path, 1.3)
        # return send_file(mp3_path, mimetype="audio/mpeg")
        return send_file(mp3_path, mimetype="audio/wav")
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

    has_new_comment = False

    comment = get_latest_comment_yt(username)
    audio_url = url_for('get_audio_youtube', username=username)
    # filename = utils.convert_username_youtube(username) + ".mp3"
    filename = utils.convert_username_youtube(username) + ".wav"
    if comment:
        if username in old_comment_youtube.keys():
            if old_comment_youtube[username] != comment:
                old_comment_youtube[username] = comment
                has_new_comment = True
        else:
            old_comment_youtube[username] = comment

        if has_new_comment:
            with comment_lock_youtube:
                mp3_path = os.path.join(audio_dir_youtube, filename)
                utils.save_speech(comment, mp3_path)
        else:
            comment = ''

        # with comment_lock:
        #     mp3_path = os.path.join(audio_dir_youtube, filename)
        #     # tts = gTTS(comment, lang='vi')
        #     # tts.save(mp3_path)
        #     utils.save_speech(comment, mp3_path)

    return jsonify({"username": username, "latest_comment": comment, "audio_url": audio_url})

@app.route("/youtube/audio", methods=["POST"])
def get_audio_youtube():
    username = request.json.get("username")
    # filename = utils.convert_username_youtube(username) + ".mp3"
    filename = utils.convert_username_youtube(username) + ".wav"
    mp3_path = os.path.join(audio_dir_youtube, filename)
    if os.path.exists(mp3_path):
        utils.change_speed(mp3_path,mp3_path, 1.3)
        # return send_file(mp3_path, mimetype="audio/mpeg")
        return send_file(mp3_path, mimetype="audio/wav")
    return jsonify({"error": "No audio found"}), 404



if __name__ == "__main__":
    start_cleanup_thread()
    start_cleanup_thread_yt()
    app.run(debug=True, host='0.0.0.0', port=80)
