#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20190711 import sms_client, models
# from django.conf import settings
from yuerweb import settings

class MySmsSender:

    def __init__(self):
        self.cred = credential.Credential(settings.SMS_SECRET_ID, settings.SMS_SECRET_KEY)
        self.client = sms_client.SmsClient(self.cred, "ap-guangzhou", )
        self.req = models.SendSmsRequest()
        self.req.SmsSdkAppid = settings.SMS_APPID
        self.req.Sign = settings.SMS_SIGN

    def send(self, phone_number, template_id, sms_code):
        """
        发送短信的功能
        :param phone_number:   手机号
        :param template_id:    短信模板id
        :param sms_code:     短信验证码 (注意：4-6位)
        :return:
        使用示例
        obj = MySmsSender()
        obj.send('手机号',conf.SMS_TEMPLATE_ID['login'],'短信验证码')
        """
        try:
            self.req.PhoneNumberSet = ["+86{}".format(phone_number.strip()), ]
            # 模板 ID: 必须填写已审核通过的模板 ID，可登录 [短信控制台] 查看模板 ID
            self.req.TemplateID = template_id
            # 模板参数: 若无模板参数，则设置为空
            self.req.TemplateParamSet = sms_code
            # 给腾讯云发送请求，让腾讯云发送短信
            resp = self.client.SendSms(self.req)
            # resp发送短信后的响应结果，可以用来判断，短信是否发送成功了
            # print(type(resp), resp)
            # print(resp.SendStatusSet[0].Code) #'Ok'
            print('发送')

            return resp.SendStatusSet[0].Code
            # from tencentcloud.sms.v20190711.models import SendSmsResponse
        except TencentCloudSDKException as err:
            # todo 记录日志等等操作
            return 'error'


# if __name__ == '__main__':
#     sms = MySmsSender()
#     sms.send('15527982569', settings.SMS_TEMPLATE_ID['test2'], ['123456', '10'])
