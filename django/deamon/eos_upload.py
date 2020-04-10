import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keiyaku_project.settings')

django.setup()

from common_py.models import eos_upload, contract, contract_version
from common_py.CodeDict import CONTRACT_EOS
from django.conf import settings
from django.forms.models import model_to_dict
from datetime import datetime

import requests, json
import time
import threading

print('process start...........................')

cpu_status      = 0 #현재 CPU쌍태
cpu_used        = 0 #현재 사용한 CPU
cpu_max         = 0 #사용가능한  CPU
max_contract    = settings.EOS_ONE_MAX_CONTRACT #하루동안 계약서 등록할수 있는 있는 수
today_count     = 0 #하루동안 등록한 계약서 수
group_count     = 0 #10개 등록여부
list_count      = 1 #현 프로세스가 등록한 계약서 수
over_count      = 0

def get_waiting_rows():

    print('Get Wating List..................')
    try:
        return eos_upload.objects.all().order_by('reg_date')
    except Exception as e:
        print('eos_data_upload Exception: {msg}'.format(msg=str(e)))
        print('retry after 1h...............')
        time.sleep(3600)
        get_waiting_rows()

#현제 CPU 상태 계산
def get_eos_cpu(used, max):
    return int((used/max)*100)

#eos상태체크
def eos_get_status():

    print('get eos status start................')

    headers     = {'Content-Type': 'application/json; charset=utf-8'}
    response    = requests.post(settings.EOS_GET_ACCOUNT, headers=headers, data=json.dumps({'account_name': settings.EOS_ACCOUNT}))

    if response.status_code == 200:

        statusInfo = response.json()
        print('statusInfo=====', statusInfo)

        code    = statusInfo.get('code')
        message = statusInfo.get('message')

        global cpu_status

        if code is not None:

            #Api error 5s후 재시작
            msg = 'code: {code}, msg: {msg}'.format(code=code, msg=message)
            print('Api error: 5s sleep start.....................')
            time.sleep(5)
            print('5s sleep end.......................')
            print('eos_get_status restart.....................')

            cpu_status = eos_get_status()
            print('Get Cpu Satus finish....................')

        else:

            try:

                global cpu_used
                global cpu_max

                cpu_limit   = statusInfo.get('cpu_limit')
                print('cpu_limit====', cpu_limit)
                cpu_used    = cpu_limit.get('used')
                cpu_max     = cpu_limit.get('max')
                cpu_status  = get_eos_cpu(cpu_used, cpu_max)
                print('get cpu_status===', cpu_status)

            except Exception as e:
                print('Get data Exception: {msg}'.format(msg=str(e)))

    else:
        #통신 실패시 5s 후 재통신
        print('Http error: 5s sleep start.....................')
        time.sleep(5)
        print('5s sleep end.......................')
        print('eos_get_status restart.....................')
        eos_get_status()


def today_reset():
    while True:
        dt = datetime.now()
        global today_count
        if dt.hour is 0 and dt.minute is 0 and dt.second == 0:
            today_count = 0

        time.sleep(1)

t = threading.Thread(target=today_reset)
t.daemon = True
t.start()

def eos_resetRemove(cont_id):

    print('eos_resetRemove try................')

    account     = settings.EOS_ACCOUNT
    private_key = settings.EOS_PRIVATE_KEY
    end_point   = settings.EOS_END_POINT

    data = {
        'contid': cont_id,
        'private_key': private_key,
        'account': account,
        'end_point': end_point
    }

    response = requests.post(settings.EOS_NODE_REMOVE_URL, data=data)
    if response.status_code == 200:
        info = response.json()
        transaction_id = info.get('transaction_id')

        if transaction_id is None:
            #nodejs remove fail 10s retry
            print('Nodejs eos remove fail retry after 10s')
            time.sleep(10)
            eos_resetRemove(cont_id)
        else:

            global cpu_status
            global cpu_used
            global cpu_max

            cpu_usage_us = info.get('processed').get('receipt').get('cpu_usage_us')
            cpu_used += cpu_usage_us
            cpu_status  = get_eos_cpu(cpu_used, cpu_max)
            print('cpu_status========', cpu_status)

    else:
        #remove nodejs 통신 실패 10s retry
        print('NodeJs call faill retry after 10s')
        time.sleep(10)
        eos_resetRemove(cont_id)

def eos_data_upload(row):
    try:

        global cpu_status

        row_data = model_to_dict(row)

        eu_id           = row_data.get('eu_id')
        contract_id     = row_data.get('contract_id')
        eu_ipfs_hash    = row_data.get('eu_ipfs_hash')
        reg_date        = row_data.get('reg_date')
        eos_cont_id     = int(str(eu_id) + str(contract_id) + str(reg_date.strftime("%Y%m%d%H%M")))

        if cpu_status > 85:
            print('!!!EOS CPU Danger 85% Over.......................')
            #24시간 대기
            print('Next try after 1m')

            time.sleep(3601)
            #print('eos_data_upload retry')
            cpu_status = 84
            eos_data_upload(row)
            eos_get_status()
        else:
            #EOS 트렌젝션 등록 시작
            account     = settings.EOS_ACCOUNT
            private_key = settings.EOS_PRIVATE_KEY
            memo        = settings.EOS_MEMO
            end_point   = settings.EOS_END_POINT

            data = {
                'contid': eos_cont_id,
                'ipfs': eu_ipfs_hash,
                'memo': memo,
                'private_key': private_key,
                'account': account,
                'end_point': end_point
            }

            response = requests.post(settings.EOS_NODE_REG_URL, data=data)

            print('node js call status==', response.status_code)
            if response.status_code == 200:
                print('Nodejs Call Succ..............')
                info = response.json()
                transaction_id = info.get('transaction_id')
                print('eos translation_id=====', transaction_id)

                if transaction_id is None:
                    #eos 연동 에러 10초s후 재시작
                    print('code: {code}, msg: {msg}'.format(code=info.get('code'), msg=info.get('message')))
                    print('retry after 10s..................')
                    time.sleep(10)
                    eos_data_upload(row)
                else:

                    global cpu_used
                    global cpu_max

                    cpu_usage_us = info.get('processed').get('receipt').get('cpu_usage_us')
                    cpu_used += cpu_usage_us
                    cpu_status  = get_eos_cpu(cpu_used, cpu_max)
                    print('cpu_status========', cpu_status)


                    print('eos updage succ.....................')
                    eos_resetRemove(eos_cont_id)

                    #nodejs remove 호출시 4초 waiting
                    print('nodejs remove 호출시 4s waiting.............')
                    time.sleep(4)

                    print('row===', row)
                    contract_id  = row_data.get('contract_id')
                    print('contract_id=========', contract_id)
                    contractInfo = None
                    try:
                        contractInfo = contract.objects.get(contract_id=125)
                    except:
                        contractInfo = None


                    print('contractInfo', contractInfo)

                    if contractInfo is not None:

                        contractInfo.contract_eos = CONTRACT_EOS.NO
                        contractInfo.save()

                        max_versionInfo = contract_version.objects.filter(contract_id=contract_id).order_by('version').first()
                        if max_versionInfo is not None:
                            max_versionInfo.cv_eos_reg_date = datetime.now()
                            max_versionInfo.cv_eos_hash     = transaction_id
                            max_versionInfo.save()

                    row.delete()
                    #등록 process Finish
            else:
                #Nodejs call fail 10s wating retry
                print('Nodejs Call Fail 10s waiting...................')
                time.sleep(10)
                eos_data_upload(row)
                print('Nodejs Call Fail eos_data_upload retry..............')

    except Exception as e:
        print('eos_data_upload Exception: {msg}'.format(msg=str(e)))
        #Exception 발생시 5s waiting restart
        print('eos_data_upload Exception 5s wait start..................')
        time.sleep(5)
        eos_data_upload(row)

#start process
eos_get_status()
while True:
    if today_count < max_contract:
        #10p 업로드 후 5초 waiting
        if group_count > 9:
            print('10p upload Finish..........')
            print('5s sleep start..........')
            time.sleep(5)
            print('5s sleep end..........')
            #10p 업로드 후 EOS 상태 재체크
            eos_get_status()
            group_count = 0

        # Eos 대기중 리스트 Get - 등록 순
        eosList = get_waiting_rows()

        if eosList.count() == 0:
            print('No Wating Contract Data....................')
            print('No Data 5s Start....................')
            #No Data 10s waiting
            time.sleep(10)
            print('Next Loop.................')

        else:
            eos_data_upload(eosList[0])

            print('{list_count}번째 데이터 업로드 성공'.format(list_count=list_count))
            print('Next Row............')

            list_count += 1
            group_count += 1
            today_count += 1
            #성공시 3s waiting
            time.sleep(3)
    else:
        #하루 등록 수 초화 1h get_waiting
        print('retry after 1h.....................')
        print('Now Waiting Contract Total: {total}개'.format(total=get_waiting_rows().count()))
        time.sleep(3600)
