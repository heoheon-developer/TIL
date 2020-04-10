from django.core.mail import EmailMessage
from django.conf import settings
from django.template import loader
from enum import Enum

from django.template.loader import render_to_string

STATIC_COMMON_IMG_URL = getattr(settings, 'STATIC_COMMON_IMG_URL', 'STATIC_COMMON_IMG_URL')
MAIL_HEADER_IMG = STATIC_COMMON_IMG_URL + "mail_header.png"
MAIL_ICO_NOTICE_IMG = STATIC_COMMON_IMG_URL + "ico_notice.png"
MAIL_ICO_BULLET_IMG = STATIC_COMMON_IMG_URL + "ico_bullet.png"
BASE_USR_URL = getattr(settings, 'HOST_URL', 'HOST_URL')
BASE_ADM_URL = getattr(settings, 'HOST_URL', 'HOST_URL') + "/admin"

USR_PW_RESET_AUTH_URL = BASE_USR_URL + "/login/pw_confirm"

def loginPwResetAuth(mail, title, authCode, token):
    try:
        msg = "Info.MailSender.usrLoginPwResetAuth() mail:"+mail
        print(msg)
        # 템플릿 습득.
        linkUrl = USR_PW_RESET_AUTH_URL + "?authToken=" + token + "&mail=" + mail
        print('linktUrl========', linkUrl)
        context = {
            'authCode': authCode,
            'pageLink': linkUrl,
            'headerImgUrl':MAIL_HEADER_IMG,
            'icoNoticeImgUrl':MAIL_ICO_NOTICE_IMG,
            'icoBulletImgUrl':MAIL_ICO_BULLET_IMG            
        }
        contents = render_to_string('mail/usr/login_pw_reset_auth.html', context)
        print("MailContent Html",contents)

        sended_email = EmailMessage(title, contents, to=[mail])
        sended_email.content_subtype = "html"

        sended_email.send()

    except Exception as ex:
        msg = "Exception.MailSender.admLoginPwResetAuth() ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'SendMailException : ' + str(ex)}

    return {'result_code': 0,'msg':'success'}

def cscenterEnquiryEmail(mailData, senderList):
    try:
        print('mailData memberName=====', mailData.get('memberName'))
        title = mailData.get('memberName') + "'〜さんが登録した1：1お問い合わせの内容です。"
        contents = render_to_string('mail/usr/cscenter_enquiry_email.html', mailData)
        for sender in senderList:
            sendMail = sender.get('senderEmail')
            sended_email = EmailMessage(title, contents, to=[sendMail])
            sended_email.content_subtype = "html"
            sended_email.send()
            msg = "Info.MailSender.cscenterEnquiryEmail() mail : " + sendMail
            print(msg)
    except Exception as ex:
        msg = "Exception.MailSender.cscenterEnquiryEmail() ex:" + str(ex)
        print(msg)
        
