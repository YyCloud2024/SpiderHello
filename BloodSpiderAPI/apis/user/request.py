from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict

from BloodSpiderAPI import models

from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict, get_first_error
from BloodSpiderAPI import models
from django import forms
from django.db.models import Q
from BloodSpiderAPI.apis.user.urils import model_to_dict_with


class UserIdentityForm(forms.ModelForm):
    class Meta:
        model = models.UserIdentity
        fields = ["user_name", "is_continue_use"]


# 创建用户身份API
def create_user_identity(request):
    if request.method != 'POST':
        return response_dict(message="请使用POST请求", code=1)

    form = UserIdentityForm(request.POST)
    if not form.is_valid():
        return response_dict(data=get_first_error(form), code=1, message="参数错误")

    try:
        user_identity = form.save()
        response = model_to_dict_with(user_identity)
        return response_dict(data=response, message="用户身份创建成功")
    except Exception as e:
        return response_dict(message=f"创建失败: {str(e)}", code=1)


# 删除用户身份API
def delete_user_identity(request):
    if request.method != 'POST':
        return response_dict(message="请使用POST请求", code=1)

    uid = request.POST.get('uid')
    if not uid:
        return response_dict(message="缺少uid参数", code=1)

    try:
        user_identity = models.UserIdentity.objects.get(uid=uid)
        user_identity.delete()
        return response_dict(message="用户身份删除成功")
    except models.UserIdentity.DoesNotExist:
        return response_dict(message="用户身份不存在", code=1)
    except Exception as e:
        return response_dict(message=f"删除失败: {str(e)}", code=1)


# 更新用户身份API
def update_user_identity(request):
    if request.method != 'POST':
        return response_dict(message="请使用POST请求", code=1)

    uid = request.POST.get('uid')
    if not uid:
        return response_dict(message="缺少uid参数", code=1)

    try:
        user_identity = models.UserIdentity.objects.get(uid=uid)
        update_data = {}

        if 'user_name' in request.POST:
            update_data['user_name'] = request.POST['user_name']
        if 'is_continue_use' in request.POST:
            update_data['is_continue_use'] = request.POST['is_continue_use'].lower() == 'true'

        if not update_data:
            return response_dict(message="没有提供可更新字段", code=1)

        for field, value in update_data.items():
            setattr(user_identity, field, value)

        user_identity.save()
        response = model_to_dict_with(user_identity)
        return response_dict(data=response, message="用户身份更新成功")
    except models.UserIdentity.DoesNotExist:
        return response_dict(message="用户身份不存在", code=1)
    except Exception as e:
        return response_dict(message=f"更新失败: {str(e)}", code=1)


# 查询单个用户身份API
def get_user_identity(request):
    if request.method != 'GET':
        return response_dict(message="请使用GET请求", code=1)

    uid = request.GET.get('uid')
    if not uid:
        return response_dict(message="缺少uid参数", code=1)

    try:
        user_identity = models.UserIdentity.objects.get(uid=uid)
        response = model_to_dict_with(user_identity)
        return response_dict(data=response, message="查询成功")
    except models.UserIdentity.DoesNotExist:
        return response_dict(message="用户身份不存在", code=1)
    except Exception as e:
        return response_dict(message=f"查询失败: {str(e)}", code=1)


# 搜索用户身份API（支持模糊搜索）
def search_user_identities(request):
    if request.method != 'GET':
        return response_dict(message="请使用GET请求", code=1)

    try:
        query = Q()

        # 用户名模糊搜索
        user_name = request.GET.get('user_name')
        if user_name:
            query &= Q(user_name__icontains=user_name)

        # 状态筛选
        is_continue_use = request.GET.get('is_continue_use')
        if is_continue_use is not None:
            query &= Q(is_continue_use=is_continue_use.lower() == 'true')

        user_identities = models.UserIdentity.objects.filter(query).order_by('-create_time')

        response = [model_to_dict_with(identity) for identity in user_identities]
        return response_dict(data=response, message="搜索成功")
    except Exception as e:
        return response_dict(message=f"搜索失败: {str(e)}", code=1)


# 切换用户身份使用状态API
def toggle_user_identity_status(request):
    if request.method != 'POST':
        return response_dict(message="请使用POST请求", code=1)

    uid = request.POST.get('uid')
    if not uid:
        return response_dict(message="缺少uid参数", code=1)

    try:
        user_identity = models.UserIdentity.objects.get(uid=uid)
        user_identity.is_continue_use = not user_identity.is_continue_use
        user_identity.save()

        status_text = "开启" if user_identity.is_continue_use else "关闭"
        response = model_to_dict_with(user_identity)
        return response_dict(data=response, message=f"用户身份状态已{status_text}")
    except models.UserIdentity.DoesNotExist:
        return response_dict(message="用户身份不存在", code=1)
    except Exception as e:
        return response_dict(message=f"状态切换失败: {str(e)}", code=1)