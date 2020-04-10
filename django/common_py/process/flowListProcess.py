from django.db.models import Q
from common_py.models import member, customer, flow
from common_py.CodeDict import CONTRACT_MEMBER_AUTH

from django.core.paginator import Paginator

# 플로우리스트를 습득한다
def getFlowList(memberId, listSize, pageNum):
    try:
        memberObj = member.objects.get(member_id=memberId)
        customerId = memberObj.customer_id_id
        query = Q(customer_id = customerId)

        #한페이지에 보여줄 목록갯수
        if listSize is None:
            listSize = 10
        else:
            listSize = int(listSize)

        #현재 페이지
        if pageNum is None or pageNum is '':
            pageNum = 1
        else:
            pageNum = int(pageNum)            

        #플로우 폴더정보와 묶어서 검색해야함.(계약폴더, 계약폴더->계약폴더부모 두개로 외부결합함.)
        flowResult = flow.objects.prefetch_related('cf_id', 'cf_id__cf_parent').filter(query)\
            .extra(select={"managerCount":"SELECT COUNT(*) FROM flow_member WHERE flow.flow_id = flow_member.flow_id AND flow_member.fm_auth = '" + CONTRACT_MEMBER_AUTH.MANAGER + "'"})\
            .extra(select={"approvalCount":"SELECT COUNT(*) FROM flow_member WHERE flow.flow_id = flow_member.flow_id AND flow_member.fm_auth = '" + CONTRACT_MEMBER_AUTH.APPROVER + "'"})\
            .extra(select={"checkerCount":"SELECT COUNT(*) FROM flow_member WHERE flow.flow_id = flow_member.flow_id AND flow_member.fm_auth = '" + CONTRACT_MEMBER_AUTH.CHECKER + "'" })\
            .extra(select={"managerName":"SELECT concat(mem.member_kj_lastname,mem.member_kj_firstname) FROM flow_member AS fm, member AS mem WHERE flow.flow_id = fm.flow_id AND fm.cfm_id = mem.member_id AND fm.fm_auth = '" + CONTRACT_MEMBER_AUTH.MANAGER + "' LIMIT 1"})\
            .extra(select={"approvalName":"SELECT concat(mem.member_kj_lastname,mem.member_kj_firstname) FROM flow_member AS fm, member AS mem WHERE flow.flow_id = fm.flow_id AND fm.cfm_id = mem.member_id AND fm.fm_auth = '" + CONTRACT_MEMBER_AUTH.APPROVER + "' LIMIT 1"})\
            .extra(select={"checkerName":"SELECT concat(mem.member_kj_lastname,mem.member_kj_firstname) FROM flow_member AS fm, member AS mem WHERE flow.flow_id = fm.flow_id AND fm.cfm_id = mem.member_id AND fm.fm_auth = '" + CONTRACT_MEMBER_AUTH.CHECKER + "' LIMIT 1"})
        flowList = []
        for resultItem in flowResult:
            folderName = resultItem.cf_id.cf_name
            if resultItem.cf_id.cf_parent_id == 0:
                #계약서의 폴더가 부모폴더이면 부모폴더 이름만 적고 끝.
                folderName = resultItem.cf_id.cf_name
            else:
                #계약서 폴더가 자식폴더이면 부모폴더＞자식폴더
                folderName = resultItem.cf_id.cf_parent.cf_name + '＞' + resultItem.cf_id.cf_name
            managerName = resultItem.managerName
            approvalName = resultItem.approvalName
            checkerName = resultItem.checkerName
            flowItem = {
                'id':resultItem.flow_id,
                'name':resultItem.flow_name,
                'folderName':folderName,
                'managerName':managerName,
                'approvalName':approvalName,
                'checkerName':checkerName,
                'managerCnt':resultItem.managerCount,
                'approvalCnt':resultItem.approvalCount,
                'checkerCnt':resultItem.checkerCount,
                'managerCntMinusOne':resultItem.managerCount - 1,
                'approvalCntMinusOne':resultItem.approvalCount - 1,
                'checkerCntMinusOne':resultItem.checkerCount - 1,
                'comment':resultItem.flow_comment,
                'updDate':resultItem.update_date,
            }
            flowList.append(flowItem)

        #페이징 설정
        paginator = Paginator(flowList, listSize)
        listData = paginator.get_page(pageNum)
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        start_index = int((pageNum - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index : end_index]
        totalCnt = flowResult.count()

    except Exception as ex:
        msg = "Exception.getFlowList(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}

    #화면으로 보낼 데이터
    result = {
        'result_code': 0,
        'msg':'success',        
        'flowList' : listData,
        # 'sort_field': sort_field,
        # 'sort_type': sort_type,
        'pageNum': pageNum,
        'listSize': listSize,
        'maxPageNum': len(paginator.page_range),
        'totalCnt': totalCnt,
        'page_range' : page_range
    } 
    # result = {'result_code': 0,'msg':'success', 'flowList':listData}

    return result