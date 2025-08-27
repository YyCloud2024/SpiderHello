from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from BloodSpiderAPI.spider.virtual_emails.awamail_com import AwamailCom
import json

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
    """
    查询邮件
    支持两种方式获取cookie：
    1. 从请求头Cookie获取（传统方式）
    2. 从请求体cookie_data获取（解决浏览器安全限制）
    """
    cookies = None
    
    # 优先从请求体获取cookie_data
    try:
        if request.body:
            body_data = json.loads(request.body.decode('utf-8'))
            if 'cookie_data' in body_data:
                cookies = body_data['cookie_data']
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass
    
    # 如果请求体没有cookie_data，则从请求头Cookie获取
    if not cookies:
        cookies = request.COOKIES
    
    response = awamail_com.get_email(cookies)
    return response_dict(data=response)
