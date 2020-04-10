from random import choice
from datetime import datetime
from django.conf import settings

import hashlib
import ipfshttpclient

# 10자리난수 -> md5해쉬화한 메일토큰을 생성.
def makeAuthToken():
    # 이메일 주소에 추가되어 검증 할 10자리 난수
    toekn = ''.join([choice('1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*()') for i in range(10)])
    # 10자리 난수 해시
    md5_token = hashlib.md5(toekn.encode('utf-8')).hexdigest()
    return md5_token

# 6자리 난수생성. 메일인증번호로 사용함.
def makeAuthCode():
    authCode = ''.join([choice('1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*()') for i in range(6)])
    return authCode

# 현재날자 년월일(YYYYmmdd) date형으로 습득
def getNowData():
    return datetime.today().date()

# 현재날자시간 datetime형으로 습득
def getNowDataTime():
    return datetime.today()

# 최종갱신일 포맷으로(yyyy/mm/dd HH:MM:SS) 현재 datetime습득
def getLastLoadedTime():
    return getNowDataTime().strftime("%Y-%m-%d %H:%M:%S")

# string형식 DateTime을 받아서 지정한 포멧으로 변경한다.
def stringToDate(stringDate, format):
    return datetime.strptime(stringDate, format)

#IPFS UPLOAD
def ipfs_upload(file):

    client  = ipfshttpclient.connect(settings.IPFS_API)
    res     = client.add(file)
    return res

#IPFS UPLOAD(그냥 upload는 ppt, excel등 파일이 대응이안됨. 얘는 다됨.)
def ipfs_upload_wrap_directory(file):
    # 업로드하면 배열로 들어감. 배열의 1번주소의 해쉬를 사용하고 해쉬/파일명 으로 url을 달아주면 파일에 접속할 수 있음.
    client  = ipfshttpclient.connect(settings.IPFS_API)
    res     = client.add(file, wrap_with_directory = True)
    return res