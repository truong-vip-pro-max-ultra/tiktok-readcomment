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

def copilot(name,comment):
    authorization = 'GitHub-Bearer zgTsTztTNU7tMwMgCUKRVeTwb5Pc6MW_YryIfW0ZrtTGi-GdDhr8rald8QMVqR482Neo4c0t9PnQhVUVTrK-K8JIkNZEk8tF-paewreG0kY='
    thread_id = 'e3937469-c29d-44a6-824a-295a1330f2c3'
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "authorization": authorization,
        "cache-control": "max-age=0",
        "content-length": "446",
        "content-type": "text/event-stream",
        "copilot-integration-id": "copilot-chat",
        "origin": "https://github.com",
        "priority": "u=1, i",
        "referer": "https://github.com/",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }

    url = f'https://api.individual.githubcopilot.com/github/chat/threads/{thread_id}/messages?'
    content = f'Tôi tên là "{name}" đang xem livestream của bạn, còn bạn là người livestream, tôi comment như sau: "{comment}" -> bạn hãy trả lời lại một cách tối ưu ngắn gọn và dễ thương'
    json = {"responseMessageID":"58fd9c32-2cd4-464e-a48b-1ec8703ddac7","content": content,"intent":"conversation","references":[],"context":[],"currentURL":"https://github.com/copilot/c/e3937469-c29d-44a6-824a-295a1330f2c3","streaming":True,"confirmations":[],"customInstructions":[],"model":"gpt-4.1","mode":"immersive","parentMessageID":"22fe5a9b-1875-44c9-ade5-f082a636066f","tools":[],"mediaContent":[],"skillOptions":{"deepCodeSearch":False}}
    response = requests.post(url, json=json, headers=headers)
    return utils.merge_text(response.text)
