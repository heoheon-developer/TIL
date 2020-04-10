from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from common_py.models import contract, member, contract_folder, customer, contract_member, contract_info
from common_py.CodeDict import APPROVAL_FLG, COMPANY_RELATION, CONTRACT_MEMBER_AUTH, CONTRACT_STATUS, CONTRACT_STATUS_FOR_PROGRAM, CONTRACT_USE_STATUS, EMAIL_SEND_FLG, TIMELINE_CODE
from common_py.utils import getNowDataTime
from common_py.process import timelineProcess
# About: 계약에관한 상태, 접근권한등에 관한 프로세스.

# 선택한 계약ID의 스테상태를 획득함.
def getOneContractStatus(memberId, contractId):
    try:
        contractResult = contract.objects.get(contract_id = contractId)
        status = contractResult.contract_status
        ourApproval = contractResult.ct_approval
        otherApproval = contractResult.ct_other_approval
        useStatus = contractResult.contract_use_status
        resultStatus = getContractSummaryStatus(status, ourApproval, otherApproval, useStatus).get("summaryStatus")
        if resultStatus is not None:
            result = {'result_code': 0,'msg':'success', 'contractStatus':resultStatus}
        else:
            result = {'result_code': -1,'msg':'fail', 'contractStatus':None}
    except Exception as ex:
        msg = "Exception.getOneContractStatus(contractId:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    
    return result

# 계약ID로 하나의 계약정보를 습득한다.(폴더정보 포함)
def getOneContract(memberId, contractId):
    try:
        resultItem = contract.objects.prefetch_related('cf_id', 'cf_id__cf_parent').get(contract_id=contractId)

        folderName = resultItem.cf_id.cf_name
        cf_parent_name = ''
        if resultItem.cf_id.cf_parent_id == 0:
            #계약서의 폴더가 부모폴더이면 부모폴더 이름만 적고 끝.
            folderName = resultItem.cf_id.cf_name
        else:
            #계약서 폴더가 자식폴더이면 부모폴더＞자식폴더
            folderName = resultItem.cf_id.cf_parent.cf_name + '＞' + resultItem.cf_id.cf_name
            cf_parent_name = resultItem.cf_id.cf_parent.cf_name
        
        tagArray = []
        if resultItem.contract_tag is not None and len(resultItem.contract_tag) != 0:
            tagArray = resultItem.contract_tag.split(',')
        
        # 사용하는곳에서는 사실상 부모, 자식폴더 구성으로 필요하기때문에 가공해서 넣어준다.
        if resultItem.cf_id.cf_parent_id == 0:
            folderId = resultItem.cf_id_id
            childFolderId = ''
        else:
            folderId = resultItem.cf_id.cf_parent_id
            childFolderId = resultItem.cf_id_id
        contractItem = {
            'contract_id':resultItem.contract_id,
            'contract_type':resultItem.contract_type,
            'contract_number':resultItem.contract_type,
            'contract_name':resultItem.contract_name,
            'contract_tag':resultItem.contract_tag,
            'tagArray':tagArray,
            'contract_tag_status':resultItem.contract_tag_status,
            'contract_content':resultItem.contract_content,
            'contract_status':resultItem.contract_status,
            'ct_approval':resultItem.ct_approval,
            'ct_other_approval':resultItem.ct_other_approval,
            'contract_pin':resultItem.contract_pin,
            'contract_pin_key_path':resultItem.contract_pin_key_path,
            'contract_eth_regdate':resultItem.contract_eth_regdate,
            'contract_eth_hash':resultItem.contract_eth_hash,
            'contract_use_status':resultItem.contract_use_status,
            'reg_date':resultItem.reg_date,
            'update_date':resultItem.update_date,
            'cf_id':resultItem.cf_id_id,
            'cf_parent_id':resultItem.cf_id.cf_parent_id,
            'parentFolderId':folderId,
            'childrenFolderId':childFolderId,
            'cf_name':resultItem.cf_id.cf_name,
            'cf_parent_name':cf_parent_name,
            'mixFolderName':folderName,
        }

    except Exception as ex:
        msg = "Exception.getOneContract(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractItem':contractItem}

    return result


# 유틸성 함수임. (계약상태별 카운트리스트, 이동할 계약체결 페이지 판단등에 사용됨.)
# DB의 계약상태 코드를 가지고 등록실패->승인완료, 확인완료->계약확인중으로 변환하여 현재 스테이터스를 습득함.
# 인수: DB contract의 계약상태, 자사승인여부(None), 상대승인여부(None) 승인여부는 contract_status가CONFIRMED이외일떈 None보내도됨.
def getContractSummaryStatus(contract_status, our_approval, other_approval, contract_use_status):
    try:
        # sumaaryStatus:계약상태와, 자타사 승인여부만으로 판단한 status.(계약서를 클릭했을때 step몇으로 갈지 판단할때 사용.)
        # statusWithUseStatus:계약서 사용 유무를 포함하여 계약상태를 판단한 status(계약리스트의 계약상태에 표시.)

        summaryStatus = None
        if contract_status == CONTRACT_STATUS_FOR_PROGRAM.CONTRACTED:#체결완료
                summaryStatus = CONTRACT_STATUS_FOR_PROGRAM.CONTRACTED
        elif contract_status == CONTRACT_STATUS_FOR_PROGRAM.APPROVAL_FINISH or \
                contract_status == CONTRACT_STATUS_FOR_PROGRAM.BC_UPLOAD_FAIL:#승인완료(등록실패는 승인완료로 카운트)
            summaryStatus = CONTRACT_STATUS_FOR_PROGRAM.APPROVAL_FINISH
        elif contract_status == CONTRACT_STATUS_FOR_PROGRAM.CONFIRMING:
            summaryStatus = CONTRACT_STATUS_FOR_PROGRAM.CONFIRMING
        elif contract_status == CONTRACT_STATUS_FOR_PROGRAM.CONFIRMED:
            #계약확인중(완료)이면서, 자사 또는 상대방의 승인스테이터스가 Y면 자사(상대)승인완료로함.
            if our_approval == APPROVAL_FLG.YES and \
                    other_approval == APPROVAL_FLG.NO:
                summaryStatus = CONTRACT_STATUS_FOR_PROGRAM.OUR_APPROVAL
            elif our_approval == APPROVAL_FLG.NO and \
                    other_approval == APPROVAL_FLG.YES:
                summaryStatus = CONTRACT_STATUS_FOR_PROGRAM.OTHER_APPROVAL
            else:
                # 계약확인완료 & 둘다N이면 계약확인중으로 카운트함.
                # 자사, 상대가 둘다Y면 계약확인완료 스테이터스여서는 안됨. 그건 입력하는 처리쪽의 버그임.
                summaryStatus = CONTRACT_STATUS_FOR_PROGRAM.CONFIRMING
        elif contract_status == CONTRACT_STATUS_FOR_PROGRAM.WRITTING:#작성중
            summaryStatus = CONTRACT_STATUS_FOR_PROGRAM.WRITTING

        statusWithUseStatus = None
        if contract_use_status == CONTRACT_USE_STATUS.DELETE:
            statusWithUseStatus = CONTRACT_STATUS_FOR_PROGRAM.DELETE
        elif contract_use_status == CONTRACT_USE_STATUS.CANCEL:
            statusWithUseStatus = CONTRACT_STATUS_FOR_PROGRAM.CANCEL
        elif contract_use_status == CONTRACT_USE_STATUS.PAUSE:
            statusWithUseStatus = CONTRACT_STATUS_FOR_PROGRAM.PAUSE
        elif contract_use_status == CONTRACT_USE_STATUS.USE: # 계약사용상태가 사용중일때만.
            statusWithUseStatus = summaryStatus
        
        statusName = ''
        if statusWithUseStatus is not None:
            # 스테이터스 코드별로 표시명을 습득해서 돌려준다.
            statusName = CONTRACT_STATUS_FOR_PROGRAM.getStatusName(statusWithUseStatus)

        if summaryStatus is not None:
            result = {'result_code': 0,'msg':'success', 'summaryStatus':summaryStatus, 'sumaryStatusName':statusName, 'statusWithUseStatus':statusWithUseStatus}
        else:
            msg = "BAD CODE : getContractSummaryStatus(contract_status:" + str(contract_status) + "our_approval:"\
                + str(our_approval) + "other_approval:" + str(other_approval)+ ")"
            print(msg)
            result = {'result_code': -1,'msg':'badCode', 'summaryStatus':contract_status}
    
    except Exception as ex:
        msg = "Exception.getContractSummaryStatus(contract_status:" + str(contract_status) + "our_approval:"\
            + str(our_approval) + "other_approval:" + str(other_approval)+") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}

    return result

# 계약서의 "사용"상태를 변경한다.(사용중, 삭제, 취소, 보류)
def changeContractUseStatus(memberId, contractId, useStatus):
    try:
        contractObj = contract.objects.get(contract_id=contractId)
        nowContractStatus = contractObj.contract_status
        nowUseStatus = contractObj.contract_use_status
        
        if nowContractStatus == CONTRACT_STATUS.APPROVAL_FINISH or nowContractStatus == CONTRACT_STATUS.BC_UPLOAD_FAIL \
            or nowContractStatus == CONTRACT_STATUS.CONTRACTED:
            return {'result_code': 1,'msg':_('계약체결, 승인완료된 계약서의 상태는 변경할 수 없습니다.')}

        if nowUseStatus == CONTRACT_USE_STATUS.DELETE or nowUseStatus == CONTRACT_USE_STATUS.CANCEL:
            return {'result_code': 2,'msg':_('삭제, 취소된 계약서의 상태는 변경할 수 없습니다.')}
        
        if useStatus != CONTRACT_USE_STATUS.DELETE and useStatus != CONTRACT_USE_STATUS.CANCEL\
            and useStatus != CONTRACT_USE_STATUS.USE and useStatus != CONTRACT_USE_STATUS.PAUSE:
            return {'result_code': 3,'msg':_('올바르지 않은 상태코드입니다.')}

        # 내가 계약서에 자사내 담당자로 추가되어있는지 체크.
        memberObj =  member.objects.get(member_id = memberId)
        memberMemberAuthCnt = contract_member.objects.filter(contract_id = contractId, \
            cm_relation=COMPANY_RELATION.OURCOMP, cm_auth = CONTRACT_MEMBER_AUTH.MANAGER, cm_email=memberObj.member_email).count()
        
        if memberMemberAuthCnt < 1:
            return {'result_code': 4,'msg':_('상태변경 권한이 없습니다.')}

        nowDate = getNowDataTime()
        contractObj.contract_use_status = useStatus
        contractObj.reg_date = nowDate
        contractObj.save()

    except Exception as ex:
        msg = "Exception.changeContractUseStatus(memberId:" + str(memberId) + ", contractId:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success'}

    return result

# 계약서의 진행 상태를 변경한다.(작성중, 계약확인중, xx승인완료, 승인완료, 체결완료 등등)
def changeContractStatus(memberId, contractId, contractStatus):
    try:
        contractObj = contract.objects.get(contract_id=contractId)
        nowContractStatus = contractObj.contract_status
        nowUseStatus = contractObj.contract_use_status
        nowOurApprove = contractObj.ct_approval
        nowOtherApprove = contractObj.ct_other_approval

        if nowUseStatus == CONTRACT_USE_STATUS.DELETE or nowUseStatus == CONTRACT_USE_STATUS.CANCEL \
            or nowUseStatus == CONTRACT_USE_STATUS.PAUSE:
            return {'result_code': 1,'msg':_('삭제, 취소, 보류중인 계약서의 상태는 변경할 수 없습니다.')}
        
        # 변경하려는 상태가 작성중으로 되돌리려는 경우의 변경불가상태 체크
        if contractStatus == CONTRACT_STATUS.WRITTING:
            if nowContractStatus == CONTRACT_STATUS.APPROVAL_FINISH or nowContractStatus == CONTRACT_STATUS.BC_UPLOAD_FAIL \
            or nowContractStatus == CONTRACT_STATUS.CONTRACTED:
                return {'result_code': 2,'msg':_('현계약상태에서는 작성중으로 되돌릴 수 없습니다.')}
        # 계약확인중, 계약확인완료로 변경하려는 경우의 변경불가상태 체크
        if contractStatus == CONTRACT_STATUS.CONFIRMING:
            if nowContractStatus == CONTRACT_STATUS.APPROVAL_FINISH or nowContractStatus == CONTRACT_STATUS.BC_UPLOAD_FAIL \
            or nowContractStatus == CONTRACT_STATUS.CONTRACTED:
                return {'result_code': 2,'msg':_('현계약상태에서는 계약확인중으로 되돌릴 수 없습니다.')}
        if contractStatus == CONTRACT_STATUS.CONFIRMED:
            if nowUseStatus == CONTRACT_STATUS.WRITTING:
                return {'result_code': 2,'msg':_('작성중 상태에서는 승인의뢰 할 수 없습니다.')}
            if nowContractStatus == CONTRACT_STATUS.APPROVAL_FINISH or nowContractStatus == CONTRACT_STATUS.BC_UPLOAD_FAIL \
            or nowContractStatus == CONTRACT_STATUS.CONTRACTED:
                return {'result_code': 2,'msg':_('현계약상태에서는 계약확인중으로 되돌릴 수 없습니다.')}
        # 승인완료로 변경하려는 경우의 변경불가 상태체크
        if contractStatus == CONTRACT_STATUS.APPROVAL_FINISH:
            if nowContractStatus == CONTRACT_STATUS.BC_UPLOAD_FAIL or nowContractStatus == CONTRACT_STATUS.CONTRACTED:
                return {'result_code': 2,'msg':_('현계약상태에서는 승인완료 상태로 변경할 수 없습니다.')}
            if nowContractStatus != CONTRACT_STATUS.CONFIRMED or nowOurApprove == APPROVAL_FLG.NO or nowOtherApprove == APPROVAL_FLG.NO:
                return {'result_code': 2,'msg':_('자사와 상대방이 모두 승인완료되지않아 승인완료로 변경할 수 없습니다.')}
            
        # 블록체인 등록실패로 변경할 경우의 변경불가 상태체크
        if contractStatus == CONTRACT_STATUS.BC_UPLOAD_FAIL:
            if nowContractStatus == CONTRACT_STATUS.CONTRACTED:
                return {'result_code': 2,'msg':_('현계약상태에서는 블록체인 등록실패 상태로 변경할 수 없습니다.')}

        codeList = CONTRACT_STATUS.getCodeList()
        if contractStatus in codeList == False:
            return {'result_code': 9,'msg':_('올바르지 않은 상태코드입니다.')}

        # 계약작성중으로 되돌릴경우.
        # 1. 계약 참가자들의 승인의뢰, 승인완료, 확인완료 스테이터스를 전부 클리어.
        # EOS해쉬는 작성중으로 돌아감 -> 작성페이지에서 입력완료를했을때만 클리어함.작성중으로 변경->아무것도 안하고 다시 메일보내서 작성확인중으로 변경할경우 버전과 EOS해쉬는 변화없음.
        # 메일송신플래그, 엑세스코드는 클리어 안한다고함.
        if contractStatus == CONTRACT_STATUS.WRITTING:
            nowDate = getNowDataTime()
            contractObj.contract_status = CONTRACT_STATUS.WRITTING
            contractObj.update_date = nowDate
            contractObj.save()
            
            # 자사, 타사관계 상관없이. 권한에 상관없이 모든 유저의 승인,승인의뢰,확인 플래그를 N으로변경함.
            contractMemgberObj = contract_member.objects.filter(contract_id = contractId)
            for memberItem in contractMemgberObj:
                memberItem.cm_confirm = APPROVAL_FLG.NO
                memberItem.update_date = nowDate
                memberItem.save()
        
        # 계약확인중으로 변경할경우. 작성중->계약확인중
        # 1.작성중에서 변경했을경우 뭐 특별히 없음. 스테이터스만 바꿔주면됨
        elif contractStatus == CONTRACT_STATUS.CONFIRMING:
            nowDate = getNowDataTime()
            contractObj.contract_status = CONTRACT_STATUS.CONFIRMING
            contractObj.update_date = nowDate
            contractObj.save()
        
        # 승인의뢰(확인완료) 완료로 변경할경우 패턴이 두가지.
        # 패턴1.계약확인중에서 변경했을경우 뭐 특별히 없음. 스테이터스만 바꿔주면됨
        # 패턴2.한쪽승인의뢰 -> 계약확인중으로 되돌릴경우(한쪽승인의뢰 상태에서 계약확인중으로 돌리면 실제 스테이터스는 승인의뢰 완료로 되돌린다.)
        # - 이때 승인자들의 승인플래그만 클리어함, 확인플래그는 안하기로 했고, 승인의로완료 이므로 상대 담당자의 승인의뢰 플래그도 당연히 클리어안함.
        elif contractStatus == CONTRACT_STATUS.CONFIRMED:
            # 계약확인중->확인의뢰완료로 변경
            if nowUseStatus == CONTRACT_STATUS.CONFIRMING:
                nowDate = getNowDataTime()
                contractObj.contract_status = CONTRACT_STATUS.CONFIRMED
                contractObj.update_date = nowDate
                contractObj.save()
            # 한쪽승인완료->확인의뢰완료로 변경.
            elif nowUseStatus == CONTRACT_STATUS.CONFIRMED:# Status코드가 같은이유는 한쪽 승인완료는 contract_status컬럼의 코드값자체는 계약확인완료와 같기때문.
                nowDate = getNowDataTime()
                contractObj.contract_status = CONTRACT_STATUS.CONFIRMED#계약상태코드는 그대로이나, 자사와 상대방 승인여부를 N으로 바꿔줌.
                contractObj.ct_approval = APPROVAL_FLG.NO
                contractObj.ct_other_approval = APPROVAL_FLG.NO
                contractObj.update_date = nowDate
                contractObj.save()
            
                # 자사, 타사관계 상관없이 모든 승인자들의 승인플래그를 N으로변경함. 확인자들의 확인상태는 변경하지않음.
                contractMemgberObj = contract_member.objects.filter(contract_id = contractId, cm_auth = CONTRACT_MEMBER_AUTH.APPROVER)
                contractMemgberObj.cm_confirm = APPROVAL_FLG.NO
                contractMemgberObj.save()
        
        # 계약승인. 걍 계약승인함
        elif contractStatus == CONTRACT_STATUS.APPROVAL_FINISH:
            nowDate = getNowDataTime()
            contractObj.contract_status = CONTRACT_STATUS.APPROVAL_FINISH
            contractObj.update_date = nowDate
            contractObj.save()

            # 타임라인 등록.
            timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.CONTACT_APPROVAL_DONE, '', None)

    except Exception as ex:
        msg = "Exception.changeContractStatus(memberId:" + str(memberId) + ", contractId:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success'}

    return result

# 계약서 확인완료, 승인, 확인가능한지 여부를 체크함.(세번째 인자는 참가자 권한코드로 줄것.)
def contractApproveCheck(memberId, contractId, contractMemberAuthCode):
    try:
        contractObj = contract.objects.get(contract_id=contractId)
        nowContractStatus = contractObj.contract_status
        nowUseStatus = contractObj.contract_use_status
        nowOurApprove = contractObj.ct_approval
        nowOtherApprove = contractObj.ct_other_approval

        if nowUseStatus == CONTRACT_USE_STATUS.DELETE or nowUseStatus == CONTRACT_USE_STATUS.CANCEL \
            or nowUseStatus == CONTRACT_USE_STATUS.PAUSE:
            return {'result_code': 1,'msg':_('삭제, 취소, 보류중인 계약서는 변경 불가능합니다.')}
        
        # 계약서 확인일경우.
        # 계약서 확인은 계약확인중, 승인의뢰완료 상태에서만 가능.(승인완료는 자사만승인완료, 타사만승인완료도 포함함.)
        if contractMemberAuthCode == CONTRACT_MEMBER_AUTH.CHECKER:
            if nowContractStatus != CONTRACT_STATUS.CONFIRMING and nowContractStatus != CONTRACT_STATUS.CONFIRMED:
                return {'result_code': 2,'msg':_('현계약상태에서는 계약서확인할 수 없습니다')}
        # 계약서 승인일경우.
        elif contractMemberAuthCode == CONTRACT_MEMBER_AUTH.APPROVER:
            # 이미 승인완료 이후의 스테이터스일 경우.
            if nowContractStatus == CONTRACT_STATUS.APPROVAL_FINISH or nowContractStatus == CONTRACT_STATUS.BC_UPLOAD_FAIL \
                or nowContractStatus == CONTRACT_STATUS.CONTRACTED:
                return {'result_code': 2,'msg':_('이미 승인 또는 체결완료된 계약서입니다.')}
            # 계약서가 승인요청상태가 아니면.
            elif nowContractStatus != CONTRACT_STATUS.CONFIRMED:
                return {'result_code': 2,'msg':_('승인요청이 완료되지 않은 계약서입니다.')}
        # 계약서 승인의뢰일경우.(타사담당자)
        if contractMemberAuthCode == CONTRACT_MEMBER_AUTH.MANAGER:
            # 계약 확인중일때만 승인의뢰 가능함.
            if nowContractStatus != CONTRACT_STATUS.CONFIRMING:
                return {'result_code': 2,'msg':_('현계약상태에서는 승인의뢰할 수 없습니다')}
    except Exception as ex:
        msg = "Exception.contractApproveCheck(memberId:" + str(memberId) + ", contractId:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success'}

    return result