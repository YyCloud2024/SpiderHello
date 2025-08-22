import requests

cookies = {
    'kpf': 'PC_WEB',
    'clientid': '3',
    'did': 'web_f33056d3d4ae8231ecb55585b3fb0ff3',
    'didv': '1754532876863',
    'kpn': 'KUAISHOU_VISION',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'kpf=PC_WEB; clientid=3; did=web_f33056d3d4ae8231ecb55585b3fb0ff3; didv=1754532876863; kpn=KUAISHOU_VISION',
}

params = {
    'cc': 'share_copylink',
    'kpf': 'PC_WEB',
    'fid': '0',
    'utm_campaign': 'pc_share',
    'shareMethod': 'token',
    'utm_medium': 'pc_share',
    'kpn': 'KUAISHOU_VISION',
    'subBiz': 'SINGLE_ROW_WEB',
    'ztDid': 'web_f33056d3d4ae8231ecb55585b3fb0ff3',
    'shareId': '18511562613484',
    'shareToken': 'X-1JSIsLl2BXx1TE',
    'shareMode': 'app',
    'shareObjectId': '3xt5wj9i7z9byb6',
    'utm_source': 'pc_share',
}

response = requests.get('https://www.kuaishou.com/short-video/3xt5wj9i7z9byb6', params=params, headers=headers, cookies=cookies).text
with open('kuaishou.html', 'w', encoding='utf-8') as f:
    f.write(response)
