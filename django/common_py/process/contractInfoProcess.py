from django.db.models import Q
from common_py.models import contract, contract_info, member
from common_py.CodeDict import TIMELINE_CODE
from common_py.process import timelineProcess
from common_py.utils import getNowDataTime, stringToDate

# 계약정보 습득.
def getContractInfo(memberId, contractId):

    try:
        contractInfo = contract_info.objects.prefetch_related('contract_id').get(contract_id = contractId)

    except Exception as ex:
        msg = "Exception.getContractInfo(memberId:" + str(memberId) + "contract_id:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractInfo':contractInfo}

    return result

# 계약정보 신규추가.
def addContractInfo(memberId, contractId):

    try:
        memberObj = member.objects.select_related('customer_id').get(member_id=memberId)
        name = memberObj.member_kj_lastname + memberObj.member_kj_firstname
        mail = memberObj.member_email
        companyName = memberObj.customer_id.customer_name

        nowDateTime = getNowDataTime()

        contractInfo = contract_info(contract_id=contract.objects.get(contract_id=contractId), ci_parson_name=name, ci_parson_email=mail, ci_company_name=companyName, reg_date=nowDateTime, update_date=nowDateTime)
        contractInfo.save()

        # 타임라인 추가 (계약정보 생성)
        timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.CONTRACT_INFO_ADD, name, None)

    except Exception as ex:
        msg = "Exception.addContractInfo(memberId:" + str(memberId) + "contractId:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success'}

    return result

# 계약정보 수정.
def updateContractInfo(memberId, contractId, contractInfoId, contractInfoModel):

    try:
        nowDateTime = getNowDataTime()

        contractInfo = contract_info.objects.get(ci_id=contractInfoId)
        contractInfo.ci_manage_number = contractInfoModel.ci_manage_number
        contractInfo.ci_parson_name = contractInfoModel.ci_parson_name
        contractInfo.ci_parson_email = contractInfoModel.ci_parson_email

        contractInfo.ci_company_name = contractInfoModel.ci_company_name
        contractInfo.ci_relation = contractInfoModel.ci_relation
        contractInfo.ci_company_address = contractInfoModel.ci_company_address
        contractInfo.ci_ceo = contractInfoModel.ci_ceo
        contractInfo.ci_contractor = contractInfoModel.ci_contractor

        contractInfo.ci_partner_company_name = contractInfoModel.ci_partner_company_name
        contractInfo.ci_partner_relation = contractInfoModel.ci_partner_relation
        contractInfo.ci_partner_company_address = contractInfoModel.ci_partner_company_address
        contractInfo.ci_partner_ceo = contractInfoModel.ci_partner_ceo
        contractInfo.ci_partner_contractor = contractInfoModel.ci_partner_contractor

        contractInfo.ci_currency = contractInfoModel.ci_currency
        #가격은 int로 변환안되면 안넣는다.
        try:
            price = int(contractInfoModel.ci_price)
            contractInfo.ci_price = price
        except:
            pass
        
        try:
            ci_date = stringToDate(contractInfoModel.ci_date, '%Y-%m-%d')
            contractInfo.ci_date = ci_date
        except:
            pass

        try:
            ci_contract_start = stringToDate(contractInfoModel.ci_contract_start, '%Y-%m-%d')
            contractInfo.ci_contract_start = ci_contract_start
        except:
            pass

        try:
            ci_contract_end = stringToDate(contractInfoModel.ci_contract_end, '%Y-%m-%d')
            contractInfo.ci_contract_end = ci_contract_end
        except:
            pass

        try:
            ci_settlement = stringToDate(contractInfoModel.ci_settlement, '%Y-%m-%d')
            contractInfo.ci_settlement = ci_settlement
        except:
            pass

        contractInfo.ci_auto = contractInfoModel.ci_auto
        contractInfo.ci_etc = contractInfoModel.ci_etc
        contractInfo.reg_date = nowDateTime
        contractInfo.update_date = nowDateTime

        contractInfo.save()

        # 타임라인 추가 (계약정보 변경)
        memberObj = member.objects.get(member_id=memberId)
        name = memberObj.member_kj_lastname + memberObj.member_kj_firstname
        timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.CONTRACT_INFO_EDIT, name, None)

    except Exception as ex:
        msg = "Exception.updateContractInfo(memberId:" + str(memberId) + "ci_id:" + str(contractInfoId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success'}

    return result