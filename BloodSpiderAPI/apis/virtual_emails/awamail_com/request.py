from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from BloodSpiderAPI.spider.virtual_emails.awamail_com import AwamailCom

awamail_com = AwamailCom()


# 创建邮箱
def create_email(request):
    """
    创建邮箱
    """
    email_info = awamail_com.create_email()
    return response_dict(data=email_info)


# 查询邮件
def get_email(request):
    response = awamail_com.get_email(request.COOKIES)
    return response_dict(data=response)
