"""
该邮件的服务流程
    1. 创建邮箱, 服务器返回该邮箱的cookie用来指向该邮箱
    2. 查询邮件: 需要携带邮箱cookie即可查询,其中最新的数据会在列表第一位
"""

# 导包
import requests

from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderModel.CommonFormat.virtual_email import VirtualMailbox


class AwamailCom:
    base_url = "https://awamail.com"
    common_utils = GeneralToolkit()
    virtual_email = VirtualMailbox()

    # 创建邮箱
    def create_email(self) -> dict:
        response = requests.post(f'{self.base_url}/welcome/change_mailbox',
                                 headers=self.common_utils.get_headers())
        create_email_format = self.virtual_email.create_mailbox()
        create_email_format["email"] = response.json()["data"]["email_address"]
        create_email_format["config"]["cookie"] = response.cookies.get_dict()
        return create_email_format

    # 查询邮件
    def get_email(self, cookie: dict):
        response = requests.get(f'{self.base_url}/welcome/get_emails', cookies=cookie, headers=self.common_utils.get_headers()).json()
        get_email_format = self.virtual_email.get_email()
        for item in response['data']['emails']:
            get_email_format["emails"].append({
                "email_text": item["html_content"],
                "subject": item["subject"],
                "from_address": item["from_address"]
            })
        return get_email_format


if __name__ == "__main__":
    TempEmail = AwamailCom()
    print(TempEmail.get_email({
      'awamail_session': 'arkbeblkbbatvpom7kppsu2jl2frasv9'
    }))


