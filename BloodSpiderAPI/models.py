import uuid
from django.db import models

"""
Django 数据库迁移命令: 
python manage.py makemigrations
python manage.py migrate
.venv\Scripts\activate
"""


# 用户身份
class UserIdentity(models.Model):
    """
    用户身份
    """
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=20, unique=True)
    # 是否继续使用
    is_continue_use = models.BooleanField(default=True)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
