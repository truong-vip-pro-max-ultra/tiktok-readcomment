import requests
import utils
from huggingface_hub import InferenceClient
tk="f_lNPhDRzetAhMOtfnbYPgdagAOazDiSCznX"

client = InferenceClient(
    api_key='h'+tk
)

chat_id = '682b3ee541ec7ac370e5f706'
session_id = '455fe8c3-a7d6-47c1-9760-96c8b590ee3a'
url = f'https://huggingface.co/chat/conversation/{chat_id}'
cookie = '__stripe_mid=30ddbe51-4c91-4640-9c53-b1e5a406bcaf732983; token=SYuDTDqMVzkJaRkpGSITVBGBXUUACLSwkLMuEYVycORHvcVvKLREeaIXAVavYmiWwtsImzwKuCtHQePZDeBZrmkaHSPDeBcWsQBiRuOJLaSRhKsSWooEVCWDoammqSFp; aws-waf-token=6e6547a0-6a3b-4978-9d93-aaf17754a736:AAoAYJJP5f46AAAA:G5q9vdqvj9MGvuT7BI+scKfpSiI7OOCUzAwEMC/E68LEaTMHO+l3FMJZePRcbTFgEGK0EKN0pdnJiEhzynxkkUohP44AgM7AffQxs3BCnNQWX3xz38meUyLw3wmaknKikE1drBeNUx2q+pNqdJcS3xAVCFdCKtvWIh1kscF3iIdEU81iuIpDiqosTuEjmK6Af/f242uv0p8n8h2rHudm21BwKtOE6nsQAP8DdooxwSbbyRAloea+g6PWFtnPC/4QptLWA2A=; hf-chat=713d5e65-b8bb-4b8b-aace-81c30474b26d'
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "cookie": cookie,
    "origin": "https://huggingface.co",
    "priority": "u=1, i",
    "referer": f"https://huggingface.co/chat/conversation/{chat_id}",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

def process(name,comment):
    data = {
        'data': '{"inputs":"Tôi là '+name+' xem livestream của bạn, còn bạn là người livestream, tôi comment như sau: `'+comment+'` -> bạn hãy trả lời lại một cách tối ưu ngắn gọn","id":"'+session_id+'","is_retry":false,"is_continue":false,"web_search":false,"tools":[]}'
    }
    p = requests.post(url, data=data, headers = headers)
    # print(p.text)
    result = utils.cut_string(p.text, '{"type":"finalAnswer","text":"', '","interrupted":false}')
    return result

def process_v2(name,comment):
    try:
        content = f'Tôi là {name} đang xem livestream của bạn, còn bạn là người livestream, tôi comment như sau: "{comment}" -> bạn hãy trả lời lại một cách tối ưu ngắn gọn và dễ thương'
        output = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct",
            messages=[
                {"role": "user", "content": content},
            ],
            stream=True,
            max_tokens=1024,
        )
        result = ''
        for chunk in output:
            result += chunk.choices[0].delta.content
        return result
    except:
        return ''

