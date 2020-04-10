from django.db.models import Q
from common_py.models import contract, member, contract_member
from common_py.CodeDict import COMPANY_RELATION, CONTRACT_MEMBER_AUTH, APPROVAL_FLG
from common_py.process import timelineProcess
from common_py.utils import getNowDataTime, stringToDate

# 계약참가자 리스트습득.
def getContractMember(memberId, contractId):

    try:
        contractMemberList = contract_member.objects.filter(contract_id = contractId).order_by('cm_relation', 'cm_auth')
        
        if contractMemberList is not None:
            contractMemberList = list(contractMemberList)
            print('contractMemberList===========',contractMemberList)

    except Exception as ex:
        msg = "Exception.getContractMember(memberId:" + str(memberId) + "contract_id:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractMemberList':contractMemberList}

    return result

# 한명의 자사내 계약참가자 멤버정보를 습득.(최우선 권한하나만 습득 승인자>확인자>담당자)
# 최우선 권한외에도, 세가지 권한 모두 있는지 없는지 여부도 습득해서 돌려줌.(카운트로)
# 각 권한별 승인상태도 결과에 추가함.
def getOneOurContractMember(contractId, cmEmail):
    # 아래의 키로 중복데이터 있으면 이상한거임.
    try:
        contractMemberList = contract_member.objects.filter(contract_id = contractId, cm_relation=COMPANY_RELATION.OURCOMP, cm_email=cmEmail)
        contractMember = None
        checkerCnt = 0
        approvalCnt = 0
        managerCnt = 0
        # 권한별 승인(승인, 확인) 플래그 습득, 자사내는 담당자는 승인같은거 없음.
        approverConfirm = None
        checkConfirm = None
        # 권한이 복수개 있을 수 있으므로 우선순위별로 하나만 고름.
        for item in contractMemberList:
            if item.cm_auth == CONTRACT_MEMBER_AUTH.APPROVER:
                approvalCnt += 1
                approverConfirm = item.cm_confirm
            elif item.cm_auth == CONTRACT_MEMBER_AUTH.CHECKER:
                checkerCnt += 1
                checkConfirm = item.cm_confirm
            elif item.cm_auth == CONTRACT_MEMBER_AUTH.MANAGER:
                managerCnt += 1

        auth = ''
        if approvalCnt > 0:
            auth = CONTRACT_MEMBER_AUTH.APPROVER
        elif checkerCnt > 0:
            auth = CONTRACT_MEMBER_AUTH.CHECKER
        elif managerCnt > 0:
            auth = CONTRACT_MEMBER_AUTH.MANAGER
        
        for item in contractMemberList:
            if item.cm_auth == auth:
                contractMember = item

    except Exception as ex:
        msg = "Exception.getOneOurContractMember(Email:" + str(cmEmail) + "contract_id:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractMember':contractMember, 'approverAuthCnt':approvalCnt, 'checkerAuthCnt':checkerCnt, 'managerAuthCnt':managerCnt, \
        'approverConfirm':approverConfirm, 'checkConfirm':checkConfirm}

    return result

# 한명의 상대방 계약참가자 멤버를 습득.
def getOneOtherContractMember(contractId, cmEmail, cmAuth):
    # 아래의 키4개로 검색하면 반드시 하나만 있어야함. 복수개있으면 데이터 이상임.
    try:
        contractMember = contract_member.objects.get(contract_id = contractId, cm_auth=cmAuth, cm_relation=COMPANY_RELATION.OTHERCOMP, cm_email=cmEmail)[:1]
    
    except Exception as ex:
        msg = "Exception.getOneOtherContractMember(Email:" + str(cmEmail) + "cmAuth:" + str(cmAuth) + "contract_id:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractMember':contractMember}

    return result

# 자사내유저 계약에 참여자로 등록되어있는지 체크함.(return = count)
def isContractMember(contractId, cmEmail):
    try:
        contractMemberCount = contract_member.objects.filter(contract_id = contractId, cm_relation=COMPANY_RELATION.OURCOMP, cm_email=cmEmail).count()

    except Exception as ex:
        msg = "Exception.isAddedContractMember(Email:" + str(cmEmail) + "contract_id:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractMemberCount':contractMemberCount}

    return result