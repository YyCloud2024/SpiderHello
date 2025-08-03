"""
该邮件的服务流程
    1. 创建邮箱:
        首先查询域名
        然后根据这个邮箱域名随机创建5位小写字母 + 数字的邮箱账号
        然后随机创建8位小写字母 + 数字的邮箱密码
        然后携带账号密码发送注册请求
        然后携带账号密码获取token来指向该邮件


    2. 查询邮件:
        先携带token更新一次token
        然后携带新token获取邮箱, 最新邮箱在最前面
        (一次token只能查询一次邮箱)
"""

# 导包
import requests
import random
import string
from BloodSpiderModel.spider_tools.common_utils import GeneralToolkit
from BloodSpiderModel.CommonFormat.virtual_email import VirtualMailbox


class InternxtCom:
    base_url = "https://api.mail.tm"
    common_utils = GeneralToolkit()
    virtual_email = VirtualMailbox()

    # 生成随机邮箱账号和密码
    def _generate_random_email(self, domain: str):
        """
        生成随机邮箱账号和密码

        参数:
            domain: 邮箱域名（例如 'gmail.com'）

        返回:
            tuple: 包含邮箱地址和密码的元组 (email, password)
        """
        # 生成5位小写字母+数字的邮箱账号
        account_length = 5
        account_chars = string.ascii_lowercase + string.digits
        account = ''.join(random.choice(account_chars) for _ in range(account_length))

        # 生成8位小写字母+数字的密码
        password_length = 8
        password_chars = string.ascii_lowercase + string.digits
        password = ''.join(random.choice(password_chars) for _ in range(password_length))

        # 组合成完整邮箱
        email = f"{account}@{domain}"

        return email, password

    # 查询域名
    def _query_domain(self):
        params = {
            'page': '1',
        }
        response = requests.get(f'{self.base_url}/domains', params=params, headers=self.common_utils.get_headers()).json()
        return response[0]['domain']




    # 创建邮箱
    def create_email(self):
        domain = self._query_domain()
        account, password = self._generate_random_email(domain)
        headers = {
            'authorization': 'Bearer',
        }
        headers.update(self.common_utils.get_headers())
        json_data = {
            'address': account,
            'password': password,
        }
        requests.post(f'{self.base_url}/accounts', headers=headers, json=json_data)
        response = requests.post(f'{self.base_url}/token', headers=headers, json=json_data).json()
        create_email_format = self.virtual_email.create_mailbox()
        create_email_format["email"] = account
        create_email_format["config"]["password"] = password
        create_email_format["config"]["authorization"] = "Bearer " + response["token"]
        return create_email_format

    # 获取邮件
    def get_email(self, authorization, account, password):
        headers = {
            'authorization': authorization,
        }
        headers.update(self.common_utils.get_headers())
        params = {
            'page': '1',
        }
        json_data = {
            'address': account,
            'password': password,
        }
        response = requests.post(f'{self.base_url}/token', headers=headers, json=json_data).json()
        headers["authorization"] = "Bearer " + response['token']
        headers['referer'] = 'https://internxt.com/'
        headers['origin'] = 'https://internxt.com/'

        response = requests.get(f'{self.base_url}/messages', params=params, headers=headers).json()
        get_email_format = self.virtual_email.get_email()
        for item in response:
            get_email_format["emails"].append({
                "email_text": item["intro"],
                "subject": item["subject"],
                "from_address": item["from"]["address"]
            })
        get_email_format["config"]["authorization"] = headers["authorization"]

        return get_email_format


if __name__ == '__main__':
    TempEmail = InternxtCom()
    emails = TempEmail.get_email(
        authorization='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3NTQyNTc2MjQsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJhZGRyZXNzIjoieTdsM3RAc29tb2ouY29tIiwiaWQiOiI2ODhmZDhkNmVjNDA1ZDhmNzMwYzMxNzIiLCJtZXJjdXJlIjp7InN1YnNjcmliZSI6WyIvYWNjb3VudHMvNjg4ZmQ4ZDZlYzQwNWQ4ZjczMGMzMTcyIl19fQ.1-N0lR_Qg38Sgx6NNOZDBjHbfV47_EbeHiwUSiRFo-9jGTaZjnY93OAF7HiQHALXxO5Ym3JIqy0CRBLxBiNCMg',
        password="lyap048f",
        account='y7l3t@somoj.com'
    )
    print(emails)
