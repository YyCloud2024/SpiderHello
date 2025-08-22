"""
定义函数生成 crypto.randomUUID

"""
import uuid
import requests

from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderModel.CommonFormat.virtual_email import VirtualMailbox


class MinMail:
    def __init__(self):
        self.base_url = "https://minmail.app"
        self.common_utils = GeneralToolkit()
        self.virtual_email = VirtualMailbox()
        self.referer = f"{self.base_url}/cn/email-generator"



    def random_uuid(self):
        """生成一个随机的UUID，格式与crypto.randomUUID()相同"""
        return str(uuid.uuid4())

    # 获取邮箱
    def create_email(self):
        """
        获取邮箱
        :return:
        """
        visitor_id = self.random_uuid()

        headers = {
            'referer': self.referer,
            'visitor-id': visitor_id,
        }
        headers.update(self.common_utils.get_headers("computer"))

        params = {
            'refresh': 'true',
            'expire': '1440',
            'part': 'emailGenerator',
        }

        response = requests.get(f'{self.base_url}/api/mail/address', params=params, headers=headers).json()

        get_email_format = self.virtual_email.create_mailbox()

        get_email_format["email"] = response["address"]
        get_email_format["config"]["headers"] = {
            "visitor-id": visitor_id,
        }

        return get_email_format

    # 获取邮件
    def get_email(self, visitor_id):
        headers = {
            'visitor-id': visitor_id
        }
        headers.update(self.common_utils.get_headers("computer"))

        params = {
            'part': 'emailGenerator',
        }

        response = requests.get(f'{self.base_url}/api/mail/list', params=params, headers=headers).json()
        get_email_format = self.virtual_email.get_email()
        for item in response["message"]:
            get_email_format["emails"].append({
                "email_text": item["content"],
                "subject": item["subject"],
                "from_address": item["from"],
            })
        get_email_format["config"]["headers"] = {
            "visitor-id": visitor_id,
        }
        return get_email_format


if __name__ == '__main__':
    temp_mail_client = MinMail()
    print(temp_mail_client.get_email("06a4aeb7-0f4e-4bd0-9e7d-dcc429faf0b4"))
