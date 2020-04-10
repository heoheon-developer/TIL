from common_py.models import contract, contract_comment, contract_member
from common_py.utils import getNowDataTime
from common_py.process import contractMemberProcess

#계약 코멘트 습득.
def getContractComment(memberId, contractId):

    try:
        contractComment = contract_comment.objects.filter(contract_id=contractId).order_by('reg_date')
        contractComment = list(contractComment)

        # 갯수를 습득해준다.
        commentCount = len(contractComment)

    except Exception as ex:
        msg = "Exception.getContractComment(memberId:" + str(memberId) + "contract_id:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractComment':contractComment, 'commentCount':commentCount}

    return result


#계약 코멘트 등록.
def addContractComment(memberId, contractId, cmId, comment):

    try:
        contractMember = contract_member.objects.get(contract_id = contractId, cm_id=cmId)

        nowDateTime = getNowDataTime()
        contractComment = contract_comment(contract_id=contract.objects.get(contract_id=contractId), cm_id=contract_member.objects.get(cm_id=contractMember.cm_id), cc_content=comment, reg_date=nowDateTime, update_date=nowDateTime)
        contractComment.save()

    except Exception as ex:
        msg = "Exception.addContractComment(memberId:" + str(memberId) + "contract_id:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success'}

    return result