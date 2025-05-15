from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, LikeEvent, GiftEvent
import threading
import asyncio
import random
from deep_translator import GoogleTranslator


latest_comments = {}
lock = threading.Lock()
clients_threads = {}

def translate_text(text):
    return GoogleTranslator(source='auto', target='vi').translate(text)

def start_client(username):
    if username in clients_threads:
        return

    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        client = TikTokLiveClient(unique_id=username)

        @client.on(ConnectEvent)
        async def on_connect(event):
            print(f"✅ Kết nối tới @{username} (Room ID: {client.room_id})")

        @client.on(CommentEvent)
        async def on_comment(event):
            comment = event.comment
            with lock:
                latest_comments[username] = f"{event.user.nickname} : {comment}"
            # print(f"[{username}] {event.user.nickname} bình luận: {comment}")

        @client.on(LikeEvent)
        async def on_like(event):
            with lock:
                latest_comments[username] = f"Cảm ơn {event.user.nickname} : đã thả tim!"
            # print(f"[{username}] {event.user.nickname} đã thả tim! ❤️")

        @client.on(GiftEvent)
        async def on_gift(event):
            with lock:
                # latest_comments[username] = f"{event.user.nickname} đã tặng quà : {event.gift.name}"
                love = ['yêu lắm luôn','moa moa moa','dễ thương quá trời ơi','cảm ơn rất nhiều','ôi trời ơi']
                latest_comments[username] = f"Cảm ơn {event.user.nickname} đã tặng {translate_text(event.gift.name)} cho mình ạ ..... {random.choice(love)} "
            # print(f"[{username}] {event.user.nickname} đã tặng quà: {event.gift.name}")

        client.run()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    clients_threads[username] = thread

def get_latest_comment(username):
    with lock:
        return latest_comments.get(username, "")

