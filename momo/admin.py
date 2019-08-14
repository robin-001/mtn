# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from momo.models import MomoRequest
from django.contrib import admin

# Register your models here.
class MomoRequestAdmin(admin.ModelAdmin):
    list_display = ['id','msisdn','amount','type','momo_reference','narration','transaction_time','status_code','momo_status','error']

admin.site.register(MomoRequest,MomoRequestAdmin)