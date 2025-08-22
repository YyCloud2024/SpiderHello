import requests
import re
import json
from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderModel.CommonFormat.video_analysis import VideoAnalysis as video_analysis_class

# 小红书视频解析
class XiaoHoshuVideoParse:

    def __init__(self):
        self.common_format_video_analysis = video_analysis_class()
        self.common_utils = GeneralToolkit()

    def extract_first_link(self, text):
        """
        从文本中提取第一个出现的链接，支持各种常见链接格式

        参数:
            text: 可能包含链接的文本字符串

        返回:
            str: 提取到的第一个链接，如果没有找到则返回空字符串
        """
        # 通用链接正则表达式模式，支持http/https开头的链接
        # 匹配各种常见的链接字符，包括字母、数字、符号等
        pattern = r'https?://[^\s"\'<]+'

        # 查找第一个匹配的链接
        match = re.search(pattern, text)

        if match:
            return match.group()
        else:
            return ""


    # 解析函数
    def analysis(self, shared_link: str):
        shared_link = self.extract_first_link(shared_link)
        response = requests.get(
            shared_link ,
            headers=self.common_utils.get_headers("computer"),
        ).text

        pattern = r'<meta name="og:video" content="(.*?)">'
        video_json_info = re.findall(pattern, response)[0]
        create_video_analysis = self.common_format_video_analysis.video_analysis()
        create_video_analysis["video_play_url"] = video_json_info
        return create_video_analysis

if __name__ == '__main__':
    douyin_video_parse = KuaiShoVideoParse()
    print(douyin_video_parse.analysis("99 【如果那年没有落榜... - 陆翎羽 | 小红书 - 你的生活兴趣社区】 😆 3gW7FI2vROHVD0Z 😆 https://www.xiaohongshu.com/discovery/item/68860155000000000b01d7b9?source=webshare&xhsshare=pc_web&xsec_token=ABuJP7NdIF8JVk60vU7U28z6dhKqOwdh2IWbSmzH3Scqc=&xsec_source=pc_share"))
