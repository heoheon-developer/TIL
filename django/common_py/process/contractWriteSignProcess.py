from common_py.process import contractCommonProcess, folderProcess, timelineProcess
from common_py.models import contract, contract_folder, contract_member, member
from common_py.utils import getNowData
from common_py.CodeDict import APPROVAL_FLG, COMPANY_RELATION, CONTRACT_MEMBER_AUTH, TIMELINE_CODE, CONTRACT_STATUS
from common_py.process.contractVersionProcess import setContractVersionUp
from common_py.process.timelineProcess import addTimeLine

# 계약서 폴더 업데이트.
def contractFolderUpdate(memberId, contractId, folderId):
    
    # 변경하려는 폴더가 내가 작성권한을 가진 폴더인지 체크.
    folderAuthCheck = folderProcess.checkWriteAuthFolder(memberId, folderId)
    try:
        # 체크결과가 1이면 프론트에서 결과의 msg그대로 표시해주면됨.
        if folderAuthCheck.get('result_code') != 0:
            return folderAuthCheck

        nowDate = getNowData()
        contractObj = contract.objects.get(contract_id = contractId)
        contractObj.cf_id = contract_folder.objects.get(cf_id = folderId)
        contractObj.update_date = nowDate
        contractObj.save()

    except Exception as ex:
        msg = "Exception.contractFolderUpdate(contractId:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    
    result = {'result_code': 0,'msg':'success'}

    return result

# 계약서작성중 상태에서 입력완료버튼 클릭시 계약서 내용 변경 및 버전업 처리.
def contractVersionUP(memberId, contractId, contractTitle, contractContent, contractTags):
    try:
        nowDate = getNowData()
        memberObj = member.objects.get(member_id=memberId)
        name = memberObj.member_kj_lastname + memberObj.member_kj_firstname

        # 계약서 내용 변경.
        contractObj = contract.objects.get(contract_id = contractId)
        contractObj.contract_name = contractTitle
        contractObj.contract_content = contractContent
        contractObj.contract_tag = contractTags
        contractObj.update_date = nowDate
        contractObj.save()

        contractId = contractObj.contract_id

        # 계약서 버전업.
        versionUpResult = setContractVersionUp(contractId, contractTitle, contractContent)
        if versionUpResult.get("result_code") != 0:
            return {'result_code': -9999,'msg':'Exception : ' + str(versionUpResult.get("msg"))} 

        # 타임라인저장.(계약작성완료)
        timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.CONTRACT_WRITE_DONE, name, None)

    except Exception as ex:
        msg = "Exception.contractVersionUP(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractId':contractId}

    return result

# 계약참가자가 계약'확인'했을때 계약확인 처리.(자사, 상대 공용)
def checkeContract(memberId, contractId, mail, compRelation):
    try:
        # 계약서가 확인가능한 상태인지 체크.
        checkResult = contractCommonProcess.contractApproveCheck(memberId, contractId, CONTRACT_MEMBER_AUTH.CHECKER)
        if checkResult.get("result_code") != 0:
            return checkResult

        nowDate = getNowData()
        memberObj = member.objects.get(member_id=memberId)
        name = memberObj.member_kj_lastname + memberObj.member_kj_firstname

        # 계약참가자 테이블의 승인(확인)여부 변경.
        contractMemObj = contract_member.objects.get(contract_id = contract.objects.get(contract_id = contractId) \
            ,cm_relation = compRelation, cm_auth = CONTRACT_MEMBER_AUTH.CHECKER, cm_email = mail)
        
        contractMemObj.cm_confirm = APPROVAL_FLG.YES
        contractMemObj.update_date = nowDate
        contractMemObj.save()

        # 타임라인저장.(계약확인완료)
        # 자사유저, 타사유저 구분.
        if compRelation == COMPANY_RELATION.OURCOMP:
            timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.OUR_CHECK_DONE, name, None)
        elif compRelation == COMPANY_RELATION.OTHERCOMP:
            timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.OTHER_CHECK_DONE, name, None)

    except Exception as ex:
        msg = "Exception.checkeContract(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    
    result = {'result_code': 0,'msg':'success'}
    return result

# 계약참가자가 계약'승인'했을때 계약승인 처리.(자사, 상대 공용)
def approveContract(memberId, contractId, mail, compRelation):
    try:
        # 계약서가 승인가능한 상태인지 체크.
        checkResult = contractCommonProcess.contractApproveCheck(memberId, contractId, CONTRACT_MEMBER_AUTH.APPROVER)
        if checkResult.get("result_code") != 0:
            return checkResult

        nowDate = getNowData()
        memberObj = member.objects.get(member_id=memberId)
        name = memberObj.member_kj_lastname + memberObj.member_kj_firstname

        # 계약참가자 테이블의 승인여부 변경.
        contractMemObj = contract_member.objects.get(contract_id = contract.objects.get(contract_id = contractId) \
            ,cm_relation = compRelation, cm_auth = CONTRACT_MEMBER_AUTH.APPROVER, cm_email = mail)
        
        contractMemObj.cm_confirm = APPROVAL_FLG.YES
        contractMemObj.update_date = nowDate
        contractMemObj.save()

        # 타임라인저장.(계약승인)
        timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.CONTRACT_APPROVE, name, None)

        # 모든 승인자의 승인상태를 체크해서 계약서를 승인완료로 변경.
        allApprovalObj = contract_member.objects.filter(contract_id = contract.objects.get(contract_id = contractId), \
            cm_auth = CONTRACT_MEMBER_AUTH.APPROVER)
        allApprovalList = list(allApprovalObj)
        ourNoApproveCnt = 0
        otherNoApproveCnt = 0
        for item in allApprovalList:
            if item.cm_confirm == APPROVAL_FLG.NO:
                if item.cm_relation == COMPANY_RELATION.OURCOMP:
                    ourNoApproveCnt = ourNoApproveCnt + 1
                elif item.cm_relation == COMPANY_RELATION.OTHERCOMP:
                    otherNoApproveCnt = otherNoApproveCnt + 1
        if ourNoApproveCnt == 0:# 자사내 모든 승인자가 승인완료했으면.
            # 계약서의 자사내 승인 상태를 승인완료로 변경하고.
            nowDate = getNowData()
            contractObj = contract.objects.get(contract_id = contractId)
            contractObj.ct_approval = APPROVAL_FLG.YES
            contractObj.update_date = nowDate
            contractObj.save()
            # 타임라인 등록.
            timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.OUR_APPROVAL_DONE, '', None)
        elif otherNoApproveCnt == 0:# 타사 모든 승인자가 승인완료했으면.
            # 계약서의 자사내 승인 상태를 승인완료로 변경하고.
            nowDate = getNowData()
            contractObj = contract.objects.get(contract_id = contractId)
            contractObj.ct_other_approval = APPROVAL_FLG.YES
            contractObj.update_date = nowDate
            contractObj.save()
            # 타임라인 등록.
            timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.OTHER_APPROVAL_DONE, '', None)

        # 자사, 타사 모두 승인완료됐으면.
        if ourNoApproveCnt == 0 and otherNoApproveCnt == 0:
            # 계약서 상태를 승인완료로 변경함.(프로세스를 이용해서 체크처리를 통해 승인완료로 변경함.)
            contractCommonProcess.changeContractStatus(memberId, contractId, CONTRACT_STATUS.APPROVAL_FINISH)

    except Exception as ex:
        msg = "Exception.approveContract(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    
    result = {'result_code': 0,'msg':'success'}
    return result