from django.db.models import Q
from common_py.models import member, customer, template, template_folder
from common_py.utils import getNowData
from common_py.CodeDict import CONTRACT_STATUS, CONTRACT_STATUS_FOR_PROGRAM, APPROVAL_FLG, TEMPLATE_OPEN_FLG, SEARCH_TYPE

from django.core.paginator import Paginator

# 템플릿리스트를 습득한다
def getTemplateList(memberId, folderId, templateOpenFlg, keyword, keywordType, listSize, pageNum):
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

        if folderId is not None:
            # 부모 선택시 부모만보이고, 자식 선택시 자식만보임.
            query.add(Q(tf_id=folderId), query.AND)

        if templateOpenFlg != TEMPLATE_OPEN_FLG.PRIVATE and templateOpenFlg != TEMPLATE_OPEN_FLG.OPEN:
            templateOpenFlg = None
        if templateOpenFlg is not None:
            query.add(Q(tf_id__tf_public=templateOpenFlg), query.AND)

        # 키워드검색
        if keyword is not None and len(keyword.strip()) != 0:
            if keywordType == SEARCH_TYPE.TITLE:
                query.add(Q(t_title__icontains = keyword), query.AND)
            elif keywordType == SEARCH_TYPE.SUB:
                query.add(Q(t_content__icontains = keyword), query.AND)

        #템플릿 폴더정보와 묶어서 검색해야함.(템플릿폴더, 템플릿폴더->템플릿폴더부모 두개로 외부결합함.) member는 작성자 이름을 습득하기위해 결합
        templateResult = template.objects.prefetch_related('tf_id', 'tf_id__tf_parent', 'member_id').filter(query)
        templateList = []
        for resultItem in templateResult:
            folderName = resultItem.tf_id.tf_name
            if resultItem.tf_id.tf_parent_id == 0:
                #계약서의 폴더가 부모폴더이면 부모폴더 이름만 적고 끝.
                folderName = resultItem.tf_id.tf_name
            else:
                #계약서 폴더가 자식폴더이면 부모폴더＞자식폴더
                folderName = resultItem.tf_id.tf_parent.tf_name + '＞' + resultItem.tf_id.tf_name
            memberName = resultItem.member_id.member_kj_lastname + resultItem.member_id.member_kj_firstname
            templateItem = {
                'tId':resultItem.t_id,
                'tfId':resultItem.tf_id_id,
                'tContent':resultItem.t_content,
                'title':resultItem.t_title,
                'folderName':folderName,
                'publicFlg':resultItem.tf_id.tf_public,
                'page':resultItem.t_page,
                'regMember':memberName,
                'regDate':resultItem.reg_date,
                'content':resultItem.t_content,
            }
            templateList.append(templateItem)

        #페이징 설정
        paginator = Paginator(templateList, listSize)
        listData = paginator.get_page(pageNum)
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        start_index = int((pageNum - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index : end_index]
        totalCnt = templateResult.count()
        
    except Exception as ex:
        msg = "Exception.getTemplateList(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    # result = {'result_code': 0,'msg':'success', 'templateList':templateList}
    #화면으로 보낼 데이터
    result = {
        'result_code': 0,
        'msg':'success',        
        'templateList' : listData,
        # 'sort_field': sort_field,
        # 'sort_type': sort_type,
        'pageNum': pageNum,
        'listSize': listSize,
        'maxPageNum': len(paginator.page_range),
        'totalCnt': totalCnt,
        'page_range' : page_range
    } 

    return result

def getTemplateCount(memberId):
    try:
        memberObj = member.objects.get(member_id=memberId)
        customerId = memberObj.customer_id_id
        #템플릿 폴더정보와 묶어서 검색해야함.(템플릿폴더, 템플릿폴더->템플릿폴더부모 두개로 외부결합함.) member는 작성자 이름을 습득하기위해 결합
        allCount = template.objects.filter(customer_id = customerId).count()
        privateCount = template.objects.prefetch_related('tf_id', 'tf_id__tf_parent').filter(customer_id = customerId, tf_id__tf_public = TEMPLATE_OPEN_FLG.PRIVATE).count()
        publicCount = template.objects.prefetch_related('tf_id', 'tf_id__tf_parent').filter(customer_id = customerId, tf_id__tf_public = TEMPLATE_OPEN_FLG.OPEN).count()

        templateCounts = {
            'allCount':allCount,
            'privateCount':privateCount,
            'publicCount':publicCount,
        }

    except Exception as ex:
        msg = "Exception.getTemplateList(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'templateCounts':templateCounts}

    return result
