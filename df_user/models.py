# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    usjname = models.CharField(max_length=20, default='')
    uaddress = models.CharField(max_length=100, default='')
    upost = models.CharField(max_length=6, default='')
    umobile = models.CharField(max_length=11, default='')
    # default,blank是Python层面的约束，不影响数据库结构，所以不用迁移

