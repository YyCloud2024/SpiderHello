from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from BloodSpiderAPI.spider.virtual_emails.minmail_app import MinMail

awamail_com = MinMail()


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
    visitor_id = request.META.get('HTTP_VISITOR_ID', '')
    if not visitor_id:
        return response_dict(message="请先创建邮箱获取 visitor_id ")
    response = awamail_com.get_email(visitor_id)

    return response_dict(data=response, message="邮件获取成功")
