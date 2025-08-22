import requests
import re
import json
from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderModel.CommonFormat.video_analysis import VideoAnalysis as video_analysis_class

# 快手视频解析
class KuaiShoVideoParse:

    def __init__(self):
        self.common_format_video_analysis = video_analysis_class()
        self.common_utils = GeneralToolkit()




    # 解析函数
    def analysis(self, shared_link: str):
        cookies = {
            'kpf': 'PC_WEB',
            'clientid': '3',
            'did': 'web_f33056d3d4ae8231ecb55585b3fb0ff3',
            'didv': '1754532876863',
            'kpn': 'KUAISHOU_VISION',
        }

        # 第一次请求,后服务器引导跳到得到视频页链接
        video_page_url = requests.get(shared_link, headers=self.common_utils.get_headers("computer"),
                                      allow_redirects=False)
        # 第二个
        video_id = video_page_url.headers["Location"].split("?")[0].split("/")[-1]
        video_data_text = requests.get(video_page_url.headers["Location"], headers=self.common_utils.get_headers("computer"), cookies=cookies)
        pattern = r"window.__APOLLO_STATE__=(.*?)</script>"
        video_json_info = json.loads(re.findall(pattern, video_data_text.text)[0].replace(";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());", "").split("duration")[2].split(',"representation":[')[-1].split('],"maxBitrate"')[0] + "]}")["url"]
        # 获取无水印视频链接
        create_video_analysis = self.common_format_video_analysis.video_analysis()
        create_video_analysis["video_play_url"] = video_json_info
        return create_video_analysis


if __name__ == '__main__':
    douyin_video_parse = KuaiShoVideoParse()
    print(douyin_video_parse.analysis("https://www.kuaishou.com/f/Xaa8kobe4xh810c"))
