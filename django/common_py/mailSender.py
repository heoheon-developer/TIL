from django.core.mail import EmailMessage
from django.conf import settings
from django.template import loader

from django.template.loader import render_to_string

STATIC_COMMON_IMG_URL = getattr(settings, 'STATIC_COMMON_IMG_URL', 'STATIC_COMMON_IMG_URL')
MAIL_HEADER_IMG = STATIC_COMMON_IMG_URL + "mail_header.png"
MAIL_ICO_NOTICE_IMG = STATIC_COMMON_IMG_URL + "ico_notice.png"
MAIL_ICO_BULLET_IMG = STATIC_COMMON_IMG_URL + "ico_bullet.png"
BASE_USR_URL = getattr(settings, 'HOST_URL', 'HOST_URL')
BASE_ADM_URL = getattr(settings, 'HOST_URL', 'HOST_URL') + "/admin"

baseContext = {
    'headerImgUrl':MAIL_HEADER_IMG,
    'icoNoticeImgUrl':MAIL_ICO_NOTICE_IMG,
    'icoBulletImgUrl':MAIL_ICO_BULLET_IMG,
}

class MailSenderAdm:
    # mailtype : 같은파일의 MAIL_TYPE클래스안의 Dict.
    # context : 메일에 맞는 템플렛에서 사용되는 변수들을 정의한 xxx_CONTEXT클래스.
    def sendMail(self, to, mailType, context):
        try:
            print("Info.MailSender mail:" + to)

            # baseContext에 context들을 추가해준다.
            fixMailContext(context)

            contents        = render_to_string(mailType.get('template'), baseContext)
            sended_email    = EmailMessage(mailType.get('title'), contents, to=[to])
            sended_email.content_subtype = mailType.get('subtype')

            sended_email.send()

        except Exception as ex:
            msg = "Exception.MailSenderAdm.sendMail() ex:" + str(ex)
            print(msg)
            return {'result_code': -9999,'msg': str(ex)}

        return {'result_code': 0}

class MAIL_SUBTYPE:
    HTML = 'html'

class MAIL_TYPE_ADM:
    # admin - 신규유저 등록.
    NEW_USER_REGIST = {
        'title':'[keiyaku.ai]신규유저가 등록되었습니다',
        'subtype':MAIL_SUBTYPE.HTML,
        'template':'mail/adm/regist_user_first_auth.html',
    }

    # admin - 비밀번호 재설정.
    PASSWORD_RESET = {
        'title':'[keiyaku.ai]비밀번호 재설정',
        'subtype':MAIL_SUBTYPE.HTML,
        'template':'mail/adm/login_pw_reset_auth.html',
    }

    # admin - 1:1문의 담당등록 인증메일.
    QS_SENDER_AUTH = {
        'title':'[Keiyaku.ai] 1：1お問い合わせの受信Eメール認証',
        'subtype':MAIL_SUBTYPE.HTML,
        'template':'mail/adm/cscenter_qa_senders_auth.html',
    }

class NEW_USER_REGIST_CONTEXT:
    temp_pw = ''
    link = ''

class PASSWORD_RESET_CONTEXT:
    authCode = ''
    pageLink = ''

class QS_SENDER_AUTH_CONTEXT:
    name = ''
    date = ''
    email = ''
    link = ''


def fixMailContext(context):
    if type(context) == NEW_USER_REGIST_CONTEXT:
        baseContext['temp_pw'] = context.temp_pw
        baseContext['link'] = context.link
        return
    elif type(context) == PASSWORD_RESET_CONTEXT:
        baseContext['authCode'] = context.authCode
        baseContext['pageLink'] = context.pageLink
        return
    elif type(context) == QS_SENDER_AUTH_CONTEXT:
        baseContext['name'] = context.name
        baseContext['date'] = context.date
        baseContext['email'] = context.email
        baseContext['link'] = context.link
        return