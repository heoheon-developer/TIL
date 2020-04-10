from django.db.models import Q
from common_py.models import contract, member, contract_folder, customer, contract_member, contract_info
from common_py.utils import getNowData, getNowDataTime
from common_py.CodeDict import CONTRACT_STATUS, CONTRACT_STATUS_FOR_PROGRAM, APPROVAL_FLG, CONTRACT_USE_STATUS, CONTRACT_MEMBER_AUTH, COMPANY_RELATION, SEARCH_TYPE, DELETE_FLG, CONTRACT_USE_STATUS
from common_py.process import contractCommonProcess

# 계약리스트를 습득한다(multiKyword는 ContractMultiSearchKeyword클래스 오브젝트를 사용할것.)
def getContractList(memberId, folderId, status, keyword, keywordType, multiKeyword):
    try:
        print("perform test - get contractlist start", getNowDataTime())
        memberObj = member.objects.get(member_id=memberId)
        customerId = memberObj.customer_id_id
        print("perform test - get contractlist get custoer id", getNowDataTime())
        # 장고모델로 답없으니까 그냥 rawQuery씀.

        # 계약멤버 서브쿼리.하나의 계약서에 하나의 권한 & 메일 & 자사내는 반드시 유니크해야하지만 DB구조상 그렇게 안되있음.
        # 만약을위해 LIMIT걸어줌. 서브쿼리는 2건이상 나오면 에러남.
        whereAuthManager = "   AND cm.cm_auth = '" + CONTRACT_MEMBER_AUTH.MANAGER + "' "
        whereAuthAprover = "   AND cm.cm_auth = '" + CONTRACT_MEMBER_AUTH.APPROVER + "' "
        whereAuthChecker = "   AND cm.cm_auth = '" + CONTRACT_MEMBER_AUTH.CHECKER + "' "
        cmSubQuery = ""\
            " SELECT cm.cm_name"\
            " FROM contract_member cm"\
            " WHERE cm.contract_id = c.contract_id "\
            "   AND cm.cm_relation = '" + COMPANY_RELATION.OURCOMP +"' "\
            "   AND cm.cm_email = '" + memberObj.member_email + "' "
        cmSubQueryOrderBy = " ORDER BY update_date DESC LIMIT 1 "

        # 현재는 계약서는 반드시 폴더를 선택해야 하는 사양이므로 폴더 삭제플래그가 N인것만 검색대상으로함.
        # 폴더가 삭제되면 안에있는 계약서도 리스트에 안나오게됨.folder는 INNER JOIN이므로 플래그도 보는게 사실상 맞다고 봐야함.
        # 계약에 묶인계약 작성자는 외부결합하고, 유저의 삭제플래그는 안봄. 안그러면 유저를 삭제했을때 계약서가 사라지거나, 작성자명을 알수없게됨.
        sql = ""\
            " SELECT c.*, ci.*, cf.*, cfc.*, m.* "\
            "   ,(" + cmSubQuery + whereAuthManager + cmSubQueryOrderBy + ") AS cmManager"\
            "   ,(" + cmSubQuery + whereAuthAprover + cmSubQueryOrderBy + ") AS cmApprover"\
            "   ,(" + cmSubQuery + whereAuthChecker + cmSubQueryOrderBy + ") AS cmChecker"\
            " FROM  contract AS c"\
            " INNER JOIN contract_folder AS cf ON cf.cf_id = c.cf_id AND cf.cf_deleted = '" + DELETE_FLG.USE + "' "\
            " LEFT OUTER JOIN contract_folder AS cfc ON cfc.cf_id = cf.cf_parent"\
            " LEFT OUTER JOIN contract_info AS ci ON ci.contract_id = c.contract_id"\
            " LEFT OUTER JOIN member AS m ON m.member_id = c.member_id"\
            " WHERE c.customer_id = " + str(customerId) + " AND c.contract_use_status != '" + str(CONTRACT_USE_STATUS.DELETE + "' ")\

        sqlWhere = ""
        if status is not None:
            if status == CONTRACT_STATUS_FOR_PROGRAM.CANCEL:# 선택한 계약사용status가 취소일경우.
                sqlWhere += " AND c.contract_use_status = '" + CONTRACT_USE_STATUS.CANCEL + "'"
            elif status == CONTRACT_STATUS_FOR_PROGRAM.PAUSE:# 선택한 계약사용status가 보류일경우.
                sqlWhere += " AND c.contract_use_status = '" + CONTRACT_USE_STATUS.PAUSE + "'"
            elif status == CONTRACT_STATUS_FOR_PROGRAM.OUR_APPROVAL:# 선택한 계약status가 자사내만 승인완료 상태일경우
                sqlWhere += " AND c.contract_use_status = '" + CONTRACT_USE_STATUS.USE + "'"
                sqlWhere += " AND c.contract_status = '" + CONTRACT_STATUS.CONFIRMED + "' AND c.ct_approval = '" + APPROVAL_FLG.YES + "'"
            elif status == CONTRACT_STATUS_FOR_PROGRAM.OTHER_APPROVAL:# 선택한 계약status가 상대방만 승인완료 상태일경우
                sqlWhere += " AND c.contract_use_status = '" + CONTRACT_USE_STATUS.USE + "'"
                sqlWhere += " AND c.contract_status = '" + CONTRACT_STATUS.CONFIRMED + "' AND c.ct_other_approval = '" + APPROVAL_FLG.YES + "'"
            elif status == CONTRACT_STATUS_FOR_PROGRAM.CONFIRMING_ED:# 선택한 계약status가 확인중 or 확인완료일경우.
                # 계약확인중 또는 확인의뢰완료 & 자사, 상대승인 플래그가 둘다 N인거.
                sqlWhere += " AND c.contract_use_status = '" + CONTRACT_USE_STATUS.USE + "'"
                sqlWhere += " AND c.contract_status = '" + CONTRACT_STATUS.CONFIRMING + "'" \
                    " OR (c.contract_status = '" + CONTRACT_STATUS.CONFIRMED + "' AND c.ct_approval = '" + APPROVAL_FLG.NO + "' AND c.ct_other_approval = '" + APPROVAL_FLG.NO + "')"
            elif status == CONTRACT_STATUS_FOR_PROGRAM.APPROVAL_BC_FAIL:# 선택한 계약status가 등록실패 or 승인완료일경우.
                sqlWhere += " AND c.contract_use_status = '" + CONTRACT_USE_STATUS.USE + "'"
                sqlWhere += " AND (c.contract_status = '" + CONTRACT_STATUS.APPROVAL_FINISH + "' OR c.contract_status = '" + CONTRACT_STATUS.BC_UPLOAD_FAIL + "')"
            else:
                sqlWhere += " AND c.contract_use_status = '" + CONTRACT_USE_STATUS.USE + "'"
                sqlWhere += " AND c.contract_status = '" + status + "'"

        if folderId is not None:
            # 부모 선택시 부모만보이고, 자식 선택시 자식만보이는 사양이므로 폴더ID만 지정해줌.
            sqlWhere += " AND c.cf_id = " + folderId

        # 키워드검색
        if keyword is not None and len(keyword.strip()) != 0:
            if keywordType == SEARCH_TYPE.TITLE:
                sqlWhere += " AND c.contract_name LIKE '%%" + keyword + "%%'"
            elif keywordType == SEARCH_TYPE.TITLE_SUB:
                sqlWhere += " AND c.contract_name LIKE '%%" + keyword + "%%' OR c.contract_content = '%%" + keyword + "%%'"

        # 어드민 페이지 계약서 관리 검색
        # 계약서번호
        contract_num = multiKeyword.lsContractNum
        # 관리번호
        contract_management_number = multiKeyword.lsControlNumber
        # 계약서명
        contract_name = multiKeyword.lsContractName
        # 폴더명
        contract_folder_name = multiKeyword.lsFolderName
        # 관계사
        contract_relative_name = multiKeyword.lsRelative
        # 작성자
        contract_writer = multiKeyword.lsWriter
        # 작성일
        contract_write_date = multiKeyword.lsWriteDate
        # 최종수정일
        contract_modify_date = multiKeyword.lsLastModify

        print("contract_num", contract_num)

        if contract_num is None:
            contract_num = ''

        if contract_management_number is None:
            contract_management_number = ''

        if contract_name is None:
            contract_name = ''

        if contract_folder_name is None:
            contract_folder_name = ''

        if contract_relative_name is None:
            contract_relative_name = ''

        if contract_writer is None:
            contract_writer = ''

        if contract_write_date is None:
            contract_write_date =''

        if contract_modify_date is None:
            contract_modify_date =''


        if contract_num is not '' :
            sqlWhere += " AND c.contract_id LIKE '%%" + contract_num + "%%'"

        if contract_management_number is not '':
            sqlWhere += " AND c.contract_number LIKE '%%" + contract_management_number + "%%'"

        if contract_name is not '':
            sqlWhere += " AND c.contract_name LIKE '%%" + contract_name + "%%'"

        if contract_folder_name is not '':
            sqlWhere += " AND cf.cf_name LIKE '%%" + contract_folder_name + "%%'"

        if contract_relative_name is not '':
            sqlWhere += " AND ci.ci_partner_company_name LIKE '%%" + contract_relative_name + "%%'"

        if contract_writer is not '':
            sqlWhere += " AND ( m.member_kj_lastname LIKE '%%" + contract_writer + "%%' OR m.member_kj_firstname LIKE '%%" + contract_writer + "%%' ) "

        if contract_write_date is not '':
            sqlWhere += " AND  c.reg_date = '" + contract_write_date + "'"

        if contract_modify_date is not '':
            sqlWhere += " AND  c.update_date = '" + contract_modify_date + "'"

        sql += sqlWhere
        print("perform test - get contractlist start contract select", getNowDataTime())
        contractResult = contract.objects.raw(sql)
        print("perform test - get contractlist end contract select", getNowDataTime())
        contractList = []
        print("perform test - get contractlist start loop", getNowDataTime())
        for resultItem in contractResult:
            folderName = resultItem.cf_id.cf_name
            if resultItem.cf_id.cf_parent_id == 0:
                #계약서의 폴더가 부모폴더이면 부모폴더 이름만 적고 끝.
                folderName = resultItem.cf_id.cf_name
                folderId = resultItem.cf_id.cf_id
                childFolderId = ''
            else:
                #계약서 폴더가 자식폴더이면 부모폴더＞자식폴더
                folderName = resultItem.cf_id.cf_parent.cf_name + '＞' + resultItem.cf_id.cf_name
                folderId = resultItem.cf_id.cf_parent_id
                childFolderId = resultItem.cf_id.cf_id
            memberName = resultItem.member_kj_lastname + resultItem.member_kj_firstname
            #계약참여권한 표시순서 담당자>승인자>확인자
            cmAuthResult = ''
            if resultItem.cmApprover is not None:
                cmAuthResult = CONTRACT_MEMBER_AUTH.APPROVER
            elif resultItem.cmChecker is not None:
                cmAuthResult = CONTRACT_MEMBER_AUTH.CHECKER
            elif resultItem.cmManager is not None:
                cmAuthResult = CONTRACT_MEMBER_AUTH.MANAGER

            partnerCompName = resultItem.ci_partner_company_name
            if partnerCompName is None:
                partnerCompName = ''

            # 계약서의 사용상태를 포함한 권한코드 및 이름 습득.
            status = resultItem.contract_status
            ourApproval = resultItem.ct_approval
            otherApproval = resultItem.ct_other_approval
            useStatus = resultItem.contract_use_status
            summaryStatus = contractCommonProcess.getContractSummaryStatus(status, ourApproval, otherApproval, useStatus)
            statusName = summaryStatus.get('sumaryStatusName')
            statusWithUseStatus = summaryStatus.get('statusWithUseStatus')

            contractItem = {
                'contractId':resultItem.contract_id,
                'folderId':folderId,
                'childFolderId':childFolderId,
                'title':resultItem.contract_name,
                'folderName':folderName,
                'regMember':memberName,
                'partnerCompName':partnerCompName,
                'regDate':resultItem.reg_date,
                'updDate':resultItem.update_date,
                'authType':cmAuthResult,
                'useStatus':useStatus,
                'statusName':statusName,
                'statusWithUseStatus':statusWithUseStatus,
                'contractNumber':resultItem.contract_number # 계약서 번호
            }
            contractList.append(contractItem)
        print("perform test - get contractlist end loop", getNowDataTime())

    except Exception as ex:
        msg = "Exception.getContractList(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'conractList':contractList}

    return result

# 계약갯수를 상태별로 습득한다.
def getContactCount(memberId):
    try:
        memberObj = member.objects.get(member_id=memberId)
        customerId = memberObj.customer_id_id
        cnt = 0
        # 사용상태 삭제인것은 검색하지않음.
        contractResult = contract.objects.filter(customer_id = customerId).exclude(contract_use_status = CONTRACT_USE_STATUS.DELETE)
        wrttingCnt = 0
        confirmingCnt = 0
        ourApprovalCnt = 0
        otherApprovalCnt = 0
        approvaledCnt = 0
        contractedCnt = 0
        pauseCnt = 0
        cancelCnt = 0
        # TODO 회사의 모든 계약서에 대해서 루프하는건데...서브쿼리 날리도록 수정하는게 성능적으로 좋아보임.
        for contractItem in contractResult:
            status = contractItem.contract_status
            ourApproval = contractItem.ct_approval
            otherApproval = contractItem.ct_other_approval
            useStatus = contractItem.contract_use_status
            resultStatus = contractCommonProcess.getContractSummaryStatus(status, ourApproval, otherApproval, useStatus).get("statusWithUseStatus")
            if resultStatus == CONTRACT_USE_STATUS.CANCEL:#취소
                cancelCnt += 1
            elif resultStatus == CONTRACT_USE_STATUS.PAUSE:#체결완료
                pauseCnt += 1
            elif resultStatus == CONTRACT_STATUS.CONTRACTED:#체결완료
                contractedCnt += 1
            elif resultStatus == CONTRACT_STATUS.APPROVAL_FINISH or \
                    resultStatus == CONTRACT_STATUS.BC_UPLOAD_FAIL:#승인완료(등록실패는 승인완료로 카운트)
                approvaledCnt += 1
            elif resultStatus == CONTRACT_STATUS.CONFIRMING:
                confirmingCnt += 1
            elif resultStatus == CONTRACT_STATUS.CONFIRMED:
                #계약확인중(완료)이면서, 자사 또는 상대방의 승인스테이터스가 Y면 자사(상대)승인완료로함.
                if contractItem.ct_approval == APPROVAL_FLG.YES and \
                        contractItem.ct_other_approval == APPROVAL_FLG.NO:
                    ourApprovalCnt += 1
                elif contractItem.ct_approval == APPROVAL_FLG.NO and \
                        contractItem.ct_other_approval == APPROVAL_FLG.YES:
                    otherApprovalCnt += 1
                else:
                    # 계약확인완료 & 둘다N이면 계약확인중으로 카운트함.
                    # 자사, 상대가 둘다Y면 계약확인완료 스테이터스여서는 안됨. 그건 입력하는 처리쪽의 버그임.
                    confirmingCnt += 1
            elif resultStatus == CONTRACT_STATUS.WRITTING:#작성중
                    wrttingCnt += 1
        contractStatusCnt = {
            'all':len(contractResult),
            'writting':wrttingCnt,
            'confirming':confirmingCnt,
            'ourApproval':ourApprovalCnt,
            'otherApproval':otherApprovalCnt,
            'approval':approvaledCnt,
            'contracted':contractedCnt,
            'pauseCnt':pauseCnt,
            'cancelCnt':cancelCnt,
        }

    except Exception as ex:
        msg = "Exception.getContactCount(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractStatusCnt':contractStatusCnt}

    return result

# 상세검색 키워드 인수 클래스
class ContractMultiSearchKeyword:

    def __init__(self, lsContractNum, lsControlNumber,  lsContractName, lsFolderName, lsRelative, lsWriter, lsWriteDate, lsLastModify):
        self.lsContractNum = lsContractNum
        self.lsControlNumber = lsControlNumber
        self.lsContractName = lsContractName
        self.lsFolderName = lsFolderName
        self.lsRelative = lsRelative
        self.lsWriter = lsWriter
        self.lsWriteDate = lsWriteDate
        self.lsLastModify = lsLastModify


