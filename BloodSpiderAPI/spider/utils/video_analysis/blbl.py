import requests
import hashlib
import time
import BloodSpiderModel
import urllib.parse
from typing import Optional, Dict, Any
from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderModel.BloodSpiderPrint.blood_spider_print_logger import BloodSpiderPrintLogger
from BloodSpiderModel.CommonFormat.video_analysis import VideoAnalysis as video_analysis_class
# 哔哩哔哩视频解析


# 辅助类
class BilibiliVideoClient:
    """Bilibili 视频相关 API 客户端"""

    def __init__(self):
        self.common_format_video_analysis = video_analysis_class()
        self.wbi_keys = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }

    def get_wbi_keys(self, cookies: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """获取 WBI 签名密钥"""
        try:
            response = requests.get(
                'https://api.bilibili.com/x/web-interface/nav',
                headers=self.headers,
                cookies=cookies
            )
            data = response.json()

            if data['code'] == 0 and 'wbi_img' in data['data']:
                img_url = data['data']['wbi_img']['img_url']
                sub_url = data['data']['wbi_img']['sub_url']

                img_key = img_url.split('/')[-1].split('.')[0]
                sub_key = sub_url.split('/')[-1].split('.')[0]

                self.wbi_keys = {'img_key': img_key, 'sub_key': sub_key}
                return self.wbi_keys
        except Exception as e:
            print(f"获取 WBI 密钥失败: {e}")

        return {}

    def generate_wbi_signature(self, params: Dict[str, Any]) -> str:
        """生成 WBI 签名"""
        if not self.wbi_keys:
            return ""

        # 混合密钥
        mixin_key_enc_tab = [
            46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
            33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
            61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
            36, 20, 34, 44, 52
        ]

        img_key = self.wbi_keys.get('img_key', '')
        sub_key = self.wbi_keys.get('sub_key', '')
        raw_wbi_key = img_key + sub_key

        wbi_key = ''.join([raw_wbi_key[i] for i in mixin_key_enc_tab])[:32]

        # 添加时间戳
        params['wts'] = int(time.time())

        # 过滤特殊字符并排序参数
        filtered_params = {}
        for k, v in params.items():
            # 过滤 value 中的 "!'()*" 字符
            str_v = str(v)
            filtered_v = ''.join(filter(lambda chr: chr not in "!'()*", str_v))
            filtered_params[k] = filtered_v

        sorted_params = sorted(filtered_params.items())
        query_string = urllib.parse.urlencode(sorted_params)

        # 生成签名
        sign_string = query_string + wbi_key
        sign = hashlib.md5(sign_string.encode()).hexdigest()

        return sign

    def get_video_info(self, bvid: Optional[str] = None, aid: Optional[int] = None,
                       cookies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """获取视频信息"""
        if not bvid and not aid:
            return {'code': -400, 'message': '缺少视频 ID 参数'}

        params = {}
        if bvid:
            params['bvid'] = bvid
        if aid:
            params['aid'] = aid

        try:
            response = requests.get(
                'https://api.bilibili.com/x/web-interface/view',
                params=params,
                headers=self.headers,
                cookies=cookies
            )
            return response.json()
        except Exception as e:
            return {'code': -1, 'message': str(e), 'data': {}}

    def get_video_stream_url(self, bvid: str, cid: int, qn: int = 80, cookies: Optional[Dict[str, str]] = None) -> Dict[
        str, Any]:
        """获取视频流地址"""
        # 确保有 WBI 密钥
        if not self.wbi_keys:
            self.get_wbi_keys(cookies)

        params = {
            'bvid': bvid,
            'cid': cid,
            'qn': qn,
            'fnval': 4048,  # 获取所有可用 DASH 格式视频流
            'fnver': 0,
            'fourk': 1,
            'platform': 'html5'
        }

        try:
            # 生成 WBI 签名
            w_sign = self.generate_wbi_signature(params.copy())
            params['w_rid'] = w_sign

            # 尝试使用 WBI 签名的新 API
            response = requests.get(
                'https://api.bilibili.com/x/player/wbi/playurl',
                params=params,
                headers=self.headers,
                cookies=cookies
            )
            result = response.json()

            # 如果新 API 失败，尝试旧 API
            if result.get('code') != 0:
                old_params = {
                    'bvid': bvid,
                    'cid': cid,
                    'qn': qn,
                    'fnval': 16,  # 基础 DASH 格式
                    'fnver': 0,
                    'fourk': 1
                }

                response = requests.get(
                    'https://api.bilibili.com/x/player/playurl',
                    params=old_params,
                    headers=self.headers,
                    cookies=cookies
                )
                result = response.json()

            return result
        except Exception as e:
            print(f"获取视频流异常: {e}")
            return {'code': -1, 'message': str(e), 'data': {}}

class BLBLVideoParse:
    def __init__(self):
        self.blbl_helper = BilibiliVideoClient()
        self.common_utils = GeneralToolkit()
        self.blood_spider_print_logger = BloodSpiderPrintLogger()
    def analysis(self, shared_link: str):
        # 获取BV号
        bv_id = "BV" + shared_link.split("BV")[-1].split("?")[0].split("/")[0]
        video_info = self.blbl_helper.get_video_info(bvid=bv_id)
        cid = video_info["data"]["cid"]
        stream_url = self.blbl_helper.get_video_stream_url(bvid=bv_id, cid=cid)
        if stream_url['code'] != 0:
            raise Exception(f"获取视频流地址失败,请您联系微信: {BloodSpiderModel.contact_method['wexin']} 需求帮助({BloodSpiderModel.athor}免费提供支持)")
        elif len(stream_url['data']['durl']) < 0:
            raise Exception(f"没有找到视频链接,请您联系微信: {BloodSpiderModel.contact_method['wexin']} 需求帮助({BloodSpiderModel.athor}免费提供支持)")
        create_video_analysis = self.blbl_helper.common_format_video_analysis.video_analysis()
        create_video_analysis["video_play_url"] = stream_url['data']['durl'][0]['url']
        return create_video_analysis



if __name__ == '__main__':
    blbl_video_parse = BLBLVideoParse()
    print(blbl_video_parse.analysis('https://www.bilibili.com/video/BV19TgGzaEkd?spm_id_from=333.1007.tianma.4-1-11.click'))