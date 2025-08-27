import requests
import time
from requests.exceptions import RequestException
from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderAPI.spider.utils.reccloud_cn.reccloud_upload import RecCloudUploader

# 辅助类
class ReccloudUtils:
    def __init__(self):
        self.common_utils = GeneralToolkit()
        self.base_url = "https://reccloud.cn"
        self.reccloud_upload = RecCloudUploader(self.get_headers())

    # 返回headers
    def get_headers(self, authorization=None):
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': self.base_url,
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': self.base_url,
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'authorization': authorization,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            "user-agent": self.common_utils.get_ua()
        }
        # 如果没有提供authorization就从字典中删除
        if not authorization:
            del headers['authorization']
        # 获取随机的UA
        return headers

    # 创建一个字典，将两个字典合并为一个新的字典
    def merge_dicts(self, primary_dict: dict, secondary_dict=None) -> dict:
        """
        合并两个字典，如果第二个参数不是字典则直接返回第一个字典

        Args:
            primary_dict: 主字典（必须为字典类型）
            secondary_dict: 辅助字典（可以是字典或None，其他类型会被忽略）

        Returns:
            合并后的字典或原始主字典
        """
        if isinstance(secondary_dict, dict):
            # Python 3.9+ 使用 | 操作符合并字典
            return primary_dict | secondary_dict
            # 兼容旧版本的写法: return {**primary_dict, **secondary_dict}
        return primary_dict


class ReccloudMain:
    def __init__(self):
        self.api_base_url = "https://aw.aoscdn.com"
        self.reccloud_utils = ReccloudUtils()
        # 会话对象，用于复用连接
        self.session = requests.Session()

    def make_request(self, method, url, headers=None, data=None, params=None, max_retries=3, retry_delay=1):
        """
        封装请求方法，添加重试机制和异常处理
        """
        retries = 0
        while retries < max_retries:
            try:
                response = None
                if method == 'post':
                    response = self.session.post(url, headers=headers, data=data, params=params)
                elif method == 'get':
                    response = self.session.get(url, headers=headers, data=data, params=params)
                
                if response is not None:
                    response.raise_for_status()  # 检查响应状态码
                    return response.json()
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
            except RequestException as e:
                print(f"Request failed: {e}. Retrying in {retry_delay} seconds...")
                retries += 1
                time.sleep(retry_delay)
        print("Max retries exceeded. Request failed.")
        return None

    # AI 文字转语音
    def stasksks_audio_speech(
            self,
            text,
            voice="XiaoxiaoMultilingual",
            volume=100,
            rate=1,
            background_music: dict | None = None,
    ):
        """
        AI 文字转语音 - 创建任务

        return: {'status': 200, 'message': 'success', 'data': {'task_id': '8c52c86b-4cbf-4910-adaf-659effecb4e8', 'estimated_time': 5}}
        """
        data_dict = self.reccloud_utils.merge_dicts(
            {
                "app_lang": "zh",
                "title": f"reccloud-{self.reccloud_utils.common_utils.get_formatted_time()}",
                "voice": voice,
                "text": text,
                "format": "mp3",
                "return_prohibited_words": 1,
                "volume": volume,
                "rate": rate,
                "device_id": self.reccloud_utils.common_utils.generate_device_id(),
                "language": "zh",
                "version": 1,
                "source": "web",
            },
            background_music
        )
        headers = self.reccloud_utils.get_headers()
        url = f'{self.api_base_url}/app/reccloud/v2/open/ai/audio/speech'
        return self.make_request('post', url, headers=headers, data=data_dict)

    #  文字转语音查询结果
    def tasks_audio_speech_task_id(self, task_id):
        """
        AI 文字转语音 - 查询结果
        """
        headers = self.reccloud_utils.get_headers()
        url = f'{self.api_base_url}/app/reccloud/v2/open/ai/audio/speech/{task_id}'
        return self.make_request('get', url, headers=headers)

    # AI 语音转文字
    def tasks_audio_recognition(self, uniqid, truncation_at = 50):
        # 441892f2-4807-4e2a-adb7-5750a84f5772
        """
        AI 语音转文字 - 创建任务
        如果发现语音转文字的时候没有把语音的全部文本转换出来，那么就是truncation_at设计的不够长，truncation_at就是视频的时间 - 1
        """
        data_dict = {
            "app_lang": "zh",
            "return_type": 0,
            "type": "4",
            "content_type": "1",
            "uniqid": uniqid,
            "truncation_at": truncation_at,
            "source": "web",
            "device_id": self.reccloud_utils.common_utils.generate_device_id(),
            "speaker_identification": 0,
            "summary_type": 1
        }
        headers = self.reccloud_utils.get_headers()
        url = f'{self.api_base_url}/app/reccloud/v2/open/ai/audio/recognition/automatic/documents'
        return self.make_request('post', url, headers=headers, data=data_dict)

    def tasks_audio_recognition_task_id(self, task_id):
        # 441892f2-4807-4e2a-adb7-5750a84f5772
        """
        AI 语音转文字 - 查询结果
        """
        params = {
            'task_ids': task_id,
            'version': '1',
        }
        headers = self.reccloud_utils.get_headers()
        url = f'{self.api_base_url}/app/reccloud/v2/open/ai/audio/recognition/automatic/documents'
        return self.make_request('get', url, headers=headers, params=params)

    # AI 视频翻译
    def tasks_media_video_translation_create(self, uniqid, voice="AvaMultilingual", origin_lang="zh", target_lang="en"):
        """
            AI 视频翻译 - 创建任务
        """
        data = {
            "uniqid": uniqid,
            "target_lang": target_lang,
            "origin_lang": origin_lang,
            "voice": voice,
            "speech_rate": 1,
            "volume": 100,
            "speaker_identification": 0,
            "device_id": self.reccloud_utils.common_utils.generate_device_id(),
            "source": "web",
            "version": 2
        }
        headers = self.reccloud_utils.get_headers()
        url = f'{self.api_base_url}/app/reccloud/v2/open/ai/av/translations/subtitles'
        return self.make_request('post', url, headers=headers, data=data)

    def tasks_tasks_media_video_translation_task_id(self, task_id):
        url = f'{self.api_base_url}/app/reccloud/v2/open/ai/av/translations/subtitles/{task_id}'
        return self.make_request('get', url, headers=self.reccloud_utils.get_headers())

    # AI 人声分离
    def tasks_tasks_media_background_separation_create(self, upload_url):
        """
        AI 人声分离 - 创建任务
        """
        data = {
            "url": upload_url,
            "primary_audio": 1,
            "voice_audio": 1,
            "background_audio": 1,
            "format": "mp3"
        }
        headers = self.reccloud_utils.get_headers()
        url = f'{self.api_base_url}/app/reccloud/v2/open/ai/av/background-separation'
        return self.make_request('post', url, headers=headers, data=data)

    def tasks_tasks_media_background_separation_task_id(self, task_id):
        url = f'{self.api_base_url}/app/reccloud/v2/open/ai/av/background-separation/{task_id}'
        return self.make_request('get', url, headers=self.reccloud_utils.get_headers())


if __name__ == '__main__':
    reccloud = ReccloudMain()
    # 上传文件
    print(reccloud.tasks_audio_recognition("pk7qn64"))