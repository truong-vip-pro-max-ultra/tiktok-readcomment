import requests
import json
def get_new_comment():
    url = 'https://chatroom-live.shopee.vn/api/v1/fetch/chatroom/SPIM-5CD50865108C1/message?uuid=3cadc15b-bc6a-4a22-b7c9-480e1345956c&timestamp=1748625036&version=v2'
    resp = requests.get(url)
    # print(resp.json())

    data = resp.json()['data']['message'][0]['msgs'][0]
    comment = json.loads(data['content'])['content']
    print(data['nickname'], data['display_name'], comment)
def get_room():
    url = 'https://live.shopee.vn/share?from=live&session=22797957&share_user_id=196823605&stm_medium=referral&stm_source=rw&uls_trackid=52ra2ej500aq&viewer=56#copy_link'
    resp = requests.get(url)
    print(resp.text)
# while True:
#     try:
#         get_new_comment()
#     except:
#         pass
get_room()