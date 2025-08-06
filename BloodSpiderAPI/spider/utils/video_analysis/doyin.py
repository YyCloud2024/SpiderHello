import requests
import re
import json
from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderModel.BloodSpiderPrint.blood_spider_print_logger import BloodSpiderPrintLogger
from BloodSpiderModel.CommonFormat.video_analysis import VideoAnalysis as video_analysis_class

# 抖音视频解析
class DouyinVideoParse:

    def __init__(self):
        self.common_format_video_analysis = video_analysis_class()
        self.common_utils = GeneralToolkit()
        self.blood_spider_print_logger = BloodSpiderPrintLogger()

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
        self.blood_spider_print_logger.blood_spider_print_debug("解析抖音视频开始")

        # 第一次请求,后服务器引导跳到得到视频页链接
        video_page_url = requests.get(shared_link, headers=self.common_utils.get_headers("mobile"),
                                      allow_redirects=False)
        # 第二个
        video_data_text = requests.get(video_page_url.headers["Location"].split("?")[0][0:-1],
                                       headers=self.common_utils.get_headers("mobile"))
        # 使用正则表达式提取视频信息
        pattern = re.compile(
            pattern=r"window\._ROUTER_DATA\s*=\s*(.*?)</script>",
            flags=re.DOTALL
        )
        find_res = pattern.search(video_data_text.text)
        if not find_res or not find_res.group(1):
            raise ValueError("parse video json info from html fail")

        video_json_info = json.loads(find_res.group(1))

        data = video_json_info["loaderData"]["video_(id)/page"]["videoInfoRes"]["item_list"][0]
        # 获取无水印视频链接
        video_url = data["video"]["play_addr"]["url_list"][0].replace("playwm", "play")
        create_video_analysis = self.common_format_video_analysis.video_analysis()
        create_video_analysis["video_play_url"] = video_url
        return create_video_analysis


if __name__ == '__main__':
    douyin_video_parse = DouyinVideoParse()
    print(douyin_video_parse.analysis("9.71 03/11 h@o.da ZmQ:/ 今日无事，勾栏听曲！# 赵都礼宴 # 勾栏听曲  https://v.douyin.com/F9X_7G4Rk4U/ 复制此链接，打开Dou音搜索，直接观看视频！"))
