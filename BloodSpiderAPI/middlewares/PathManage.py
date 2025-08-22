# Api中间件层, 所以关于Api的请求都必须经过此中间件
from django.utils.deprecation import MiddlewareMixin
from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from BloodSpiderAPI.models import UserIdentity

class PathManage(MiddlewareMixin):
    def process_request(self, request):
        # 获取并验证Authorization头信息
        authorization = request.META.get("HTTP_AUTHORIZATION")

        # 检查是否存在
        if not authorization:
            return response_dict(code=1001, message="请提供身份认证信息")

        # 检查是否为有效字符串（非空且不是仅空白字符）
        stripped_auth = authorization.strip()
        if not stripped_auth:
            return response_dict(code=1002, message="身份认证信息不能为空")

        # 检查是否符合Bearer token格式
        if not stripped_auth.lower().startswith('bearer '):
            return response_dict(code=1003, message="身份认证信息格式不正确，应为Bearer token")

        # 提取token部分
        token = stripped_auth.split(' ', 1)[1].strip()
        if not token:
            return response_dict(code=1004, message="身份认证令牌不能为空")


        # 验证token格式（可根据实际情况调整，例如检查长度、是否为UUID等）
        if len(token) < 36:  # 假设token至少36个字符
            return response_dict(code=1005, message="身份认证令牌格式无效")

        # 根据token寻找用户
        try:
            user_identity = UserIdentity.objects.filter(uid=token).first()

            if not user_identity:
                return response_dict(code=1006, message="用户不存在或令牌无效")

            # 验证用户状态（如果有状态字段）
            if request.path != "/api/user/toggle_status/":
                if not user_identity.is_continue_use:
                    return response_dict(code=1007, message="用户已被禁用")

            # 将找到的用户存储在request中，方便后续使用
            request.user_identity = user_identity

        except Exception as e:
            return response_dict(code=1008, message="身份验证过程出错，请稍后再试", data=str(e))

        # 所有验证通过，确保用户已找到并可用
        return None
    def process_response(self, request, response):
        return response



