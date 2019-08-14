# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta, datetime
import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from momo.utils import disburse, collect, worker


# Create your models here.


class MomoRequest(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    msisdn = models.CharField(max_length=12)
    amount = models.DecimalField(decimal_places=2,max_digits=10)
    narration = models.CharField(max_length=50,default='Testing MoMo API')
    type = models.CharField(max_length=16,default="COLLECT");
    momo_reference=models.CharField(max_length=255,null=True,blank=True)
    momo_status=models.CharField(max_length=16,default='PENDING')
    transaction_time=models.DateTimeField(auto_now=True)
    error=models.TextField(null=True,blank=True);
    status_code=models.CharField(max_length=5,null=True,blank=True)

    def __unicode__(self):
        return str(self.id)

@receiver(post_save, sender=MomoRequest)
def send_momo_request(sender, instance, created, **kwargs):
    if created:
        # send request
        if(instance.type=='DISBURSE'):
            disburse(instance)
        elif(instance.type=='COLLECT'):
            collect(instance)

        worker(repeat=30, repeat_until=datetime.now()+timedelta(minutes=5))

