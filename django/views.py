<<<<<<< HEAD
import logging
import binascii, hashlib
import onetimepass as otp

from ast import literal_eval
from conf import settings
from datetime import datetime
from rest_framework import views
from rest_framework.response import Response
from django.db import transaction
from django.db.models import CharField, IntegerField, Count
from django.http import JsonResponse
from django.utils import translation
from django.db.models import F, Q, Case, When, Value
from django.db.models.functions import Concat
from django.utils.translation import ugettext_lazy as _

from .models import BoxUsers, BoxUserrole, BoxRoles, BoxUserinfo
from common.type.fieldType import Status
from common.type.exception import Code
from common.service import login_service
from common.service.mail_service import MailService
from common.utils.AESCipher import AESCipher
from common.utils.admin_utils import *
from common.utils.log_utils import *

from ..storage_service.models import Googledrivesettings

logger = logging.getLogger(__name__)

super_admin_br_id = 1
admin_br_id = 2
default_bu_roleid = 3


# 로그인
class login(views.APIView):
    @transaction.atomic
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        language = request.data['language']

        try:
            user = BoxUsers.objects.annotate(
                bu_super_admin=Count('boxRoles', filter=Q(boxRoles__br_id=super_admin_br_id)),
                bu_admin=Count('boxRoles', filter=Q(boxRoles__br_id=admin_br_id)),
                bu_count_admin=Count('boxRoles',
                                     filter=(Q(boxRoles__br_id=super_admin_br_id) | Q(boxRoles__br_id=admin_br_id))),
                bu_admin_yn=Case(
                    When(
                        bu_count_admin__gt=0,
                        then=Value('Y')
                    ),
                    default=Value('N'),
                    output_field=CharField()
                ),
                bu_roleid=Case(
                    When(
                        bu_super_admin=1,
                        then=super_admin_br_id
                    ),
                    When(
                        bu_admin=1,
                        then=admin_br_id
                    ),
                    default=default_bu_roleid,
                    output_field=IntegerField()
                ),
                bu_fullname=Case(
                    When(
                         Q(bu_lastname=None) | Q(bu_lastname=''),
                         then='bu_firstname'
                    ),
                    default=Concat('bu_firstname', Value(' '), 'bu_lastname')),
                ).get(bu_email=email)

        except BoxUsers.DoesNotExist:
            return Response({'code': Code.LOGIN_FAIL.value, 'message': Code.LOGIN_FAIL.name})

        # 유저상태 활성화 체크
        if user.bu_status != Status.ACTIVE.value:
            return Response({'code': Code.DISACTIVE_USER.value, 'message': Code.DISACTIVE_USER.name})

        # 비밀번호 확인
        encoded_password = password.encode()
        hexdigest = hashlib.sha256(encoded_password).hexdigest()

        if user.bu_pw != hexdigest:
            return Response({'code': Code.LOGIN_FAIL.value, 'message': Code.LOGIN_FAIL.name})

        # 2단계 인증 확인
        user_info = BoxUserinfo.objects.filter(boxUsers=user)

        if len(user_info) > 0:
            user_info = user_info[0]

            if user_info.ui_certify is not None and user_info.ui_certify != '':
                return Response({'code': 'secondCertification', 'userId': user.bu_id, 'userName': user.bu_fullname})

        return login_success(request, user)


# 로그아웃
class logout(views.APIView):
    @transaction.atomic
    def post(self, request, format=None):
        tokenName = 'HTTP_X_BOX_ACCESSTOKEN'
        keyName = 'HTTP_X_BOX_ACCESSKEY'

        # delete session
        del request.session[tokenName]
        del request.session[keyName]

        # delete cookie
        result = {'result': True}
        model = response_model(result)
        response = Response(model)
        response.delete_cookie(key='HTTP_X_BOX_ACCESSKEY')
        response.delete_cookie(key='HTTP_X_BOX_ACCESSTOKEN')

        return response


# 비밀번호 찾기 이메일 발송
class SendEmailToResetPassword(views.APIView):
    @transaction.atomic
    def post(self, request, format=None):
        email = request.data['email']

        logger.info(get_request_params(request))

        # 해당 email이 계정 중에 있는지 확인
        try:
            user = BoxUsers.objects.get(bu_email=email)
        except BoxUsers.DoesNotExist:
            return Response({'code': Code.FAILED_TO_SEND_EMAIL.value, 'message': Code.LOGIN_FAIL.name})

        # 유저상태 활성화 체크
        if user.bu_status != Status.ACTIVE.value:
            return Response({'code': Code.DISACTIVE_USER.value, 'message': Code.DISACTIVE_USER.name})

        # 해당 이메일로 이메일 전송
        proc_result = MailService.send_email_reset_password(request)
        model = response_model(proc_result)

        return Response(model)


# 비밀번호 변경
class ResetPassword(views.APIView):
    @transaction.atomic
    def post(self, request, format=None):
        k = request.data['k']
        email = request.data['email']
        password = request.data['password']
        re_password = request.data['rePassword']

        # password 빈 것 or 6자리 이하 검사
        if password is '' or len(password) < 6:
            return Response({'code': Code.PASSWORD_IS_WRONG.value, 'message': Code.PASSWORD_IS_WRONG.name})

        # password 일치 여부 검사
        if password != re_password:
            return Response({'code': Code.NOT_CORRECT_RE_PASSWORD.value, 'message':Code.NOT_CORRECT_RE_PASSWORD.name})
        
        # k 검사
        try:
            code = check_data_and_email(k)
        except Exception as exc:
            code = exc.args[0]

        if code is not Code.SUCCESS:
            return Response({'code': code.value, 'message': code.name})

        # k의 email과 email의 일치 여부 검사
        cipher = AESCipher(key='AOS_BOX_EMAIL_KEY')
        decrypted_k = cipher.decrypt(k)
        decrypted_k_arr = decrypted_k.split('/')
        valid_email = decrypted_k_arr[1]

        if email != valid_email:
            return Response({'code': Code.NO_AUTHORITY.value, 'message': Code.NO_AUTHORITY.name})

        # email의 password 수정
        try:
            user = BoxUsers.objects.get(bu_email=email)
        except BoxUsers.DoesNotExist:
            return Response({'code': Code.NOT_EXIST_USER.value, 'message': Code.NOT_EXIST_USER.name})

        encoded_password = password.encode()
        hexdigest = hashlib.sha256(encoded_password).hexdigest()
        user.bu_pw = hexdigest
        user.save()

        return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.name})


# 메인
class Main(views.APIView):
    @transaction.atomic
    def post(self, request, format=None):
        return Response()


# 사용자정보
class UserInfo(views.APIView):
    @transaction.atomic
    def post(self, request, format=None):

        tokenName = 'HTTP_X_BOX_ACCESSTOKEN'
        keyName = 'HTTP_X_BOX_ACCESSKEY'

        accessToken = ''
        accessKey = ''

        try:
            accessToken = request.COOKIES[tokenName]
            accessKey = request.COOKIES[keyName]
        except Exception as e:
            return JsonResponse({'code': Code.ACCESS_IS_NOT_FOUND.value, 'message': Code.ACCESS_IS_NOT_FOUND.name})

        if accessToken == '' or accessKey == '' or accessToken is None or accessKey is None:
            return JsonResponse({'code': Code.ACCESS_IS_NOT_FOUND.value,
                                 'message': Code.ACCESS_IS_NOT_FOUND.name})

        cipher = AESCipher(key=accessKey)

        try:
            decodeToken = cipher.decrypt(enc=accessToken)
        except Exception as e:
            return JsonResponse({'code': Code.INTERNAL_SERVER_ERROR.value, 'message': Code.INTERNAL_SERVER_ERROR.name})

        if decodeToken:
            payload = literal_eval(decodeToken)
            print("payload :", payload)
        else:
            return JsonResponse(
                {'code': Code.INTERNAL_SERVER_ERROR.value, 'message': Code.INTERNAL_SERVER_ERROR.name})

        if request.path.find('admin') < 0:
            user = BoxUsers.objects.annotate(
                bu_super_admin=Count('boxRoles', filter=Q(boxRoles__br_id=super_admin_br_id)),
                bu_admin=Count('boxRoles', filter=Q(boxRoles__br_id=admin_br_id)),
                bu_count_admin=Count('boxRoles', filter=(Q(boxRoles__br_id=super_admin_br_id) | Q(boxRoles__br_id=admin_br_id))),
                bu_admin_yn=Case(
                    When(
                        bu_count_admin__gt=0,
                        then=Value('Y')
                    ),
                    default=Value('N'),
                    output_field=CharField()
                ),
                bu_roleid=Case(
                    When(
                        bu_super_admin=1,
                        then=super_admin_br_id
                    ),
                    When(
                        bu_admin=1,
                        then=admin_br_id
                    ),
                    default=default_bu_roleid,
                    output_field=IntegerField()
                ),
            ).get(pk=payload['userId'])

        # 관리자 권한 설정
        isAdmin = is_admin(user)

        # 2단계 인증 설정 여부
        try:
            user_info = BoxUserinfo.objects.get(boxUsers=user)

            if user_info.ui_certify is None or user_info.ui_certify == '':
                existCertify = False
            else:
                existCertify = True
        except BoxUserinfo.DoesNotExist:
            existCertify = False

        result = {
            'result': True,
            'firstname': user.bu_firstname,
            'lastname': user.bu_lastname,
            'email': user.bu_email,
            'id': user.bu_id,
            'labelid': user.bu_labelid,
            'accountid': user.bu_accountid,
            'isAdmin': isAdmin,
            'existCertify': existCertify,
            'lang': user.boxuserinfo_set.all()[0].ui_lang
        }

        model = response_model(result)

        return Response(model)


# 2단계 인증
class SecondCertification(views.APIView):
    @transaction.atomic
    def post(self, request, format=None):
        valid = False
        user_id = request.data['userId']
        verification_code = request.data['verificationCode']

        user = BoxUsers.objects.annotate(bu_roleid=F('boxuserrole__boxRoles__br_id'),
                                  bu_fullname=Case(
                                      When(
                                          Q(bu_lastname=None) | Q(bu_lastname=''),
                                          then='bu_firstname'
                                      ),
                                      default=Concat('bu_firstname', Value(' '), 'bu_lastname')),
                                  ).get(pk=user_id)
        box_user_info = BoxUserinfo.objects.filter(boxUsers__bu_id=user_id)

        if len(box_user_info) > 0:
            certify = box_user_info[0].ui_certify
            valid = otp.valid_totp(verification_code, certify)

        if valid is False:
            return Response({'code': Code.VERIFICATION_CODE_IS_WRONG.value, 'message': Code.VERIFICATION_CODE_IS_WRONG.name})

        return login_success(request, user)


# 메일 링크의 유효한 key인지 확인
class CheckValidKey(views.APIView):
    @transaction.atomic
    def post(self, request):
        k_type = request.data['kType']

        try:
            k = request.data['k']
        except KeyError:
            return Response({'code': Code.INVALID_KEY.value, 'message': Code.INVALID_KEY.name})

        valid_email = None

        # 회원 초대 이메일
        if k_type == 'join':
            # decypt k
            try:
                cipher = AESCipher(key='AOS_BOX_EMAIL_KEY')
                decrypted_k = cipher.decrypt(k)
            except binascii.Error:
                return Response({'code': Code.INVALID_MAIL_LINK.value, 'message': Code.INVALID_MAIL_LINK.name})
            
            # decrypted_k 날짜 형식인지 확인
            try:
                datetime.strptime(decrypted_k, '%Y%m%d')
                now = datetime.now().strftime('%Y%m%d')

                # decrypted_k가 유효한 날짜인지 확인
                if decrypted_k < now:
                    return Response({'code': Code.INVALID_MAIL_LINK.value, 'message': Code.INVALID_MAIL_LINK.name})

            except ValueError:
                return Response({'code': Code.INVALID_MAIL_LINK.value, 'message': Code.INVALID_MAIL_LINK.name})

        # 비밀번호 변경 이메일
        elif k_type == 'password':
            # k가 날짜/이메일 형식인지 확인
            try:
                code = check_data_and_email(k)

                cipher = AESCipher(key='AOS_BOX_EMAIL_KEY')
                decrypted_k = cipher.decrypt(k)
                decrypted_k_arr = decrypted_k.split('/')
                valid_email = decrypted_k_arr[1]
            except Exception as exc:
                code = exc.args[0]

            return Response({'code': code.value, 'message': code.name})

        return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.name, 'email': valid_email})


def login_success(request, user):
    meta = request.META
    language = request.data['language']

    # create session
    result = login_service.login(user, meta, language)
    request.session['HTTP_X_BOX_ACCESSKEY'] = result['accessKey']
    request.session['HTTP_X_BOX_ACCESSTOKEN'] = result['accessToken']
    request.session['LOGGED_IN_USER_ID'] = user.bu_id

    language = language.lower()

    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]

    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language

    # 관리자 권한 설정
    isAdmin = is_admin(user)

    # 스토리지 서비스 연결 정보 확인
    google_drive = False
    # todo 에러 발생 확인하여 수정할것!
    # try:
    #     Googledrivesettings.objects.get(userid=user.bu_id, flag='N')
    #     google_drive = True
    # except Googledrivesettings.DoesNotExist:
    #     pass

    storage_service = {
        'google_drive': google_drive
    }

    data = {
        'code': Code.SUCCESS.value,
        'message': Code.SUCCESS.name,
        'isPass': True,
        'isAdmin': isAdmin,
        'storage_service': storage_service
    }
    response = Response(data)

    # create cookies
    secure = settings.IS_REAL
    response.set_cookie(key='HTTP_X_BOX_ACCESSKEY', value=result['accessKey'], httponly=True, secure=secure)
    response.set_cookie(key='HTTP_X_BOX_ACCESSTOKEN', value=result['accessToken'], httponly=True, secure=secure)

    return response


def check_data_and_email(k):
    # decypt k
    try:
        cipher = AESCipher(key='AOS_BOX_EMAIL_KEY')
        decrypted_k = cipher.decrypt(k)
    except binascii.Error:
        return Code.INVALID_MAIL_LINK

    try:
        decrypted_k_arr = decrypted_k.split('/')
        valid_date = decrypted_k_arr[0]
        valid_email = decrypted_k_arr[1]

        datetime.strptime(valid_date, '%Y%m%d%H%M%S')
        now = datetime.now().strftime('%Y%m%d%H%M%S')

        # valid_date가 유효한 날짜인지 확인
        if decrypted_k < now:
            return Code.INVALID_MAIL_LINK

        # valid_email이 유효한 이메일인지 확인
        try:
            BoxUsers.objects.get(bu_email=valid_email)
        except BoxUsers.DoesNotExist:
            return Code.INVALID_MAIL_LINK

    except ValueError:
        return Code.INVALID_MAIL_LINK

    return Code.SUCCESS


def is_admin(user):
    admin = False

    if user.bu_roleid == super_admin_br_id or user.bu_roleid == admin_br_id:
        admin = True

    return admin
=======
from django.shortcuts import render

# Create your views here.



git config --global user.email "heoheon.dev@gmail.com"
>>>>>>> 932b32ce582f3c23d7830c74e529bff75392e4f1
