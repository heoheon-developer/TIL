import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keiyaku_project.settings')

django.setup()

from web3 import Web3, HTTPProvider
from django.conf import settings
from common_py.models import eth_upload
from django.forms.models import model_to_dict

import time

list_count  = 1 #현 프로세스가 등록한 계약서 수
minimum_gas = settings.ETH_MINIMUM_GAS


#web3 settings
print('WEB3 Connection Start................')
w3 = Web3(HTTPProvider(settings.ETH_RPC_HOST + ":" + settings.ETH_RPC_PORT))
print('WEB3 Connection Succ................')
#Ethereum account settings
w3.eth.defaultAccount = w3.eth.accounts[settings.ETH_ACCOUNT]
print('Account Setting Finish..................')


#이더리움 대기중 리스트 가져오기
def get_waiting_rows():

    print('Get Wating List..................')
    try:
        return eth_upload.objects.all().order_by('reg_date')
    except Exception as e:
        print('eos_data_upload Exception: {msg}'.format(msg=str(e)))
        print('retry after 1h...............')
        time.sleep(3600)
        get_waiting_rows()

#이더리움 업로드
def ethereum_upload(row):
    print('Ethereum Upload Start..............')

    try:

        row_data = model_to_dict(row)

        #계약서 주소 가져오기
        trans_receipt       = w3.eth.waitForTransactionReceipt(settings.ETH_CONTRACT)
        contract_address    = trans_receipt['contractAddress']
        print('Ethereum Contract Address: {address}'.format(address=contract_address))

        eth_ipfs_hash   = row_data.get('eth_ipfs_hash')
        work_path       = os.path.dirname(os.path.realpath(__file__))

        print('work_path===', work_path.replace('\\', '/'))

        f = open(work_path.replace('\\', '/') + '/' + settings.ETH_ABI_FILE , 'r')
        contract_abi = f.read()
        f.close()

        eth_contract    = w3.eth.contract(address=contract_address, abi=contract_abi)
        transact_hash   = eth_contract.functions.issue(eth_ipfs_hash).transact()
        tx_hax          = w3.toHex(transact_hash)

        print('Ethereum Tranwsact Pending........')
        w3.eth.waitForTransactionReceipt(transact_hash)
        print('Finish Pending............')

        print('Ethereum transact_hash: {hax}'.format(hax=tx_hax))
        row.delete()

    except Exception as e:
        print('ethereum_upload Exception: {msg}'.format(msg=str(e)))
        print('retry after 10s...............')
        time.sleep(10)
        ethereum_upload(row)





#w3.geth.personal.unlockAccount(w3.eth.accounts[settings.ETH_ACCOUNT], settings.ETH_ACCOUNT_PW)
#w3.eth.accounts[settings.ETH_ACCOUNT])
while True:

    ethList = get_waiting_rows()

    if ethList.count() != 0:

        print('Get Waiting Contract Data.............')

        w3.geth.personal.unlockAccount(w3.eth.accounts[settings.ETH_ACCOUNT], settings.ETH_ACCOUNT_PW)
        account_gas = w3.eth.getBalance(w3.eth.accounts[settings.ETH_ACCOUNT])
        print('{account} gas: {gas}'.format(account=w3.eth.accounts[settings.ETH_ACCOUNT], gas=account_gas))

        if minimum_gas > account_gas:
            print('{account} Gas To Lack, now gas: {}'.format(account=w3.eth.accounts[settings.ETH_ACCOUNT], gas=gas))
            print('Retry after 1h............')
            time.sleep(3600)
        else:

            ethereum_upload(ethList[0])

            print('{list_count}번째 데이터 업로드 성공'.format(list_count=list_count))
            print('Next Row............')

            list_count += 1
            #성공시 3s waiting
            time.sleep(3)
    else:
        print('No Waiting Contract Data............')
        print('Retry after 10s')
        time.sleep(10)
