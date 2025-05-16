# tiktok_client.py
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, LikeEvent, GiftEvent
import threading
import asyncio
import random
from deep_translator import GoogleTranslator

latest_comments = {}
lock = threading.Lock()
clients_threads = {}
clients_instances = {}  # Lưu client để dừng

def translate_text(text):
    return GoogleTranslator(source='auto', target='vi').translate(text)

def start_client(username):
    if username in clients_threads:
        return

    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        client = TikTokLiveClient(unique_id=username)
        clients_instances[username] = client

        @client.on(ConnectEvent)
        async def on_connect(event):
            print(f"✅ Kết nối tới @{username} (Room ID: {client.room_id})")

        @client.on(CommentEvent)
        async def on_comment(event):
            comment = event.comment
            with lock:
                latest_comments[username] = f"{event.user.nickname} : {comment}"

        @client.on(LikeEvent)
        async def on_like(event):
            with lock:
                latest_comments[username] = f"Cảm ơn {event.user.nickname} : đã thả tim!"

        @client.on(GiftEvent)
        async def on_gift(event):
            with lock:
                love = ['yêu lắm luôn','moa moa moa','dễ thương quá trời ơi','cảm ơn rất nhiều','ôi trời ơi']
                latest_comments[username] = f"Cảm ơn {event.user.nickname} đã tặng {translate_text(event.gift.name)} cho mình ạ ..... {random.choice(love)} "

        try:
            client.run()
        except Exception as e:
            print(f"❌ Lỗi ở client {username}: {e}")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    clients_threads[username] = thread

def stop_client(username):
    if username in clients_instances:
        try:
            clients_instances[username].stop()
            print(f"🔌 Dừng client cho @{username}")
        except Exception as e:
            print(f"⚠️ Không thể dừng client @{username}: {e}")
        clients_instances.pop(username, None)
    if username in clients_threads:
        clients_threads.pop(username, None)
    if username in latest_comments:
        latest_comments.pop(username, None)

def get_latest_comment(username):
    with lock:
        return latest_comments.get(username, "")
