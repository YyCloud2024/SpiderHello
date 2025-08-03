from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from BloodSpiderAPI.spider.virtual_emails.internxt_com import InternxtCom

awamail_com = InternxtCom()


# 创建邮箱
def create_email(request):
    """
    创建邮箱
    """
    email_info = awamail_com.create_email()
    return response_dict(data=email_info)


# 查询邮件
def get_email(request):
    """
    查询邮件
    """
    authorization = request.META.get('HTTP_AUTHORIZATION', '')
    account = request.META.get('HTTP_ACCOUNT', '')
    password = request.META.get('HTTP_PASSWORD', '')

    response = awamail_com.get_email(authorization, account, password)

    return response_dict(data=response, message="邮件获取成功")
