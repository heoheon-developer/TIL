from django.utils.translation import gettext_lazy as _
from common_py.models import contract, member, contract_folder, contract_folder_member, customer, template_folder
from common_py.CodeDict import DELETE_FLG, USED_FLG, CONTRACT_USE_STATUS

from django.db.models import Q
from django.db.models.functions import Concat
# ↓↓↓↓↓↓계약폴더
# 표시대상이되는 계약 폴더리스트를 습득. Json.folderList(ListType) 드롭다운 설정에서 사용함.
# parentId가 None = 부모폴더, Id가 설정되어있으면 자식폴더임.
def getContractFolderList(memberId):
    try:
        memberObj = member.objects.get(member_id=memberId)
        customerId = memberObj.customer_id_id

        folderListObj = contract_folder.objects.filter(customer_id=customerId, cf_deleted = DELETE_FLG.USE).order_by('cf_sort')

        folderList = []
        for folderItem in folderListObj:
            if folderItem.cf_parent_id == 0:
                folderId = {
                    "folderId":folderItem.cf_id,
                    "folderName":folderItem.cf_name,
                    "parentId":None,
                }
                folderList.append(folderId)
            else:
                folderId = {
                    "folderId":folderItem.cf_id,
                    "folderName":folderItem.cf_name,
                    "parentId":folderItem.cf_parent_id,
                }
                folderList.append(folderId)

    except Exception as ex:
        msg = "Exception.getContractFolderList(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'folderList':folderList}

    return result

# 부모->자식 관계까지 설정된 폴더리스트. 계약목록의 폴더리스트에서 사용함.
def getContractFolderTwoDepth(memberId):
    try:
        folderList = getContractFolderList(memberId).get("folderList")
        folderListResult = []
        for folderItem in folderList:
            if folderItem.get("parentId") == None:
                parentFolder = {
                    "folderId":folderItem.get("folderId"),
                    "folderName":folderItem.get("folderName"),
                    "childFolders": []
                }
                for folderItem2 in folderList:
                    if folderItem2.get("parentId") == folderItem.get("folderId"):
                        childFolder = {
                            "folderId":folderItem2.get("folderId"),
                            "folderName":folderItem2.get("folderName")
                        }
                        parentFolder.get("childFolders").append(childFolder)
                folderListResult.append(parentFolder)

    except Exception as ex:
        msg = "Exception.getContractListTwoDepth(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'folderList':folderListResult}

    return result

# 계약서 폴더ID별 사용유저정보
def getFolderMembers(cf_id, keyword_type, keyword):

    try:
        print('keyword_type===', keyword_type)
        print('keyword===', keyword)
        folderMemberList = contract_folder_member.objects.select_related('member_id').filter(cf_id=cf_id, cfm_deleted=DELETE_FLG.USE)

        if keyword_type is not None and keyword is not None:

            if keyword_type == 'email':
                folderMemberList = folderMemberList.filter(member_id__member_email__icontains=keyword)
            elif keyword_type == 'name':
                folderMemberList = folderMemberList.annotate(
                    search_kj_name=Concat('member_id__member_kj_lastname', 'member_id__member_kj_firstname')
                ).filter(search_kj_name__icontains=keyword)

        folderMemberList = folderMemberList.order_by('-reg_date')

        folderMembers    = []
        print('folderMemberList count==', folderMemberList.count())
        for members in folderMemberList:
            folderMembers.append({
                'cfm_id': members.cfm_id,
                'last_name': members.member_id.member_kj_lastname,
                'first_name': members.member_id.member_kj_firstname,
                'email': members.member_id.member_email,
                'cfm_write': members.cfm_write,
                'cfm_authority': members.cfm_authority,
                'cfm_confirmation': members.cfm_confirmation,
                'cfm_approval': members.cfm_approval
            })


    except Exception as ex:
        msg = "Exception.getFolderMembers(cf_id:" + str(cf_id) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}

    result = {'result_code': 0,'msg':'success', 'folderMemberList':folderMembers}
    return result

# 선택 폴더별 사용가능 유저 검색
def getFolderUseMembers(memberId, keyword, cf_id):

    try:

        memberObj           = member.objects.get(member_id=memberId)
        customerId          = memberObj.customer_id_id

        folderUseMemberList = []
        nowUseMembers       = contract_folder_member.objects.values_list('member_id').filter(cf_id=cf_id, cfm_deleted=DELETE_FLG.USE)

        MemberList = member.objects.filter(customer_id=customerId, member_deleted=DELETE_FLG.USE).exclude(member_id__in=nowUseMembers).annotate(
            search_kj_name=Concat('member_kj_lastname', 'member_kj_firstname')
        ).filter(Q(search_kj_name__icontains=keyword)|Q(member_email__icontains=keyword)).order_by('search_fg_name')

        for members in MemberList:
            folderUseMemberList.append({
                'last_name': members.member_kj_lastname,
                'first_name': members.member_kj_firstname,
                'member_id': members.member_id,
                'member_email':members.member_email
            })


    except Exception as ex:
        msg = "Exception.getFolderMembers(cf_id:" + str(cf_id) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}

    result = {'result_code': 0,'msg':'success', 'folderUseMemberList':folderUseMemberList}
    return result


# 1계층으로 작성권한이 있는 폴더 리스트를 습득함.
def getOneDepthAuthFolderList(memberId):
    try:
        memberObj = member.objects.get(member_id=memberId)
        customerId = memberObj.customer_id_id

        folderListObj = contract_folder.objects.filter(customer_id=customerId, cf_deleted = DELETE_FLG.USE)
        folderMemObj = contract_folder_member.objects.select_related("cf_id").filter(member_id = memberObj.member_id, cfm_write = USED_FLG.USED, cfm_deleted = DELETE_FLG.USE).order_by('cf_id__cf_sort')

        folderList = []
        for folderMemItem in folderMemObj:
            if folderMemItem.cf_id.cf_parent_id == 0:
                folderId = {
                    "folderId":folderMemItem.cf_id.cf_id,
                    "folderName":folderMemItem.cf_id.cf_name,
                }
                folderList.append(folderId)
            else:
                # 자식폴더일경우. 부모폴더 이름을 찾아야함.
                for folderItem in folderListObj:
                    # 현재폴더의 부모폴더 ID와 같은녀석을 루프하면서 찾음.
                    if folderMemItem.cf_id.cf_parent_id == folderItem.cf_id:
                        folderId = {
                            "folderId":folderMemItem.cf_id.cf_id,
                            "folderName": folderItem.cf_name + "＞" + folderMemItem.cf_id.cf_name,
                        }
                        folderList.append(folderId)

    except Exception as ex:
        msg = "Exception.getContractFolderList(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'folderList':folderList}

    return result

# 폴더 삭제가능 여부 판단
def checkFolderDelete(cf_id):

    try:
        status  = False
        cfInfo = contract_folder.objects.get(cf_id=cf_id)

        if cfInfo.cf_parent_id == 0:
            contract_count = contract.objects.filter(cf_id=cfInfo.cf_id).exclude(contract_use_status=CONTRACT_USE_STATUS.DELETE).count()
            if contract_count == 0:
                status = True

                if status:
                    #1차 폴더 삭제시 2차 폴더 삭제여부 체크
                    childs = contract_folder.objects.filter(cf_parent=cfInfo.cf_id, cf_deleted=DELETE_FLG.USE)
                    if childs.count() != 0:
                        #자식폴더 존재시 삭제여부 체크
                        chidsIds = contract_folder.objects.values_list('cf_id').filter(cf_parent=cfInfo.cf_id, cf_deleted=DELETE_FLG.USE)
                        child_contract_count = contract.objects.filter(cf_id_in = chidsIds).exclude(contract_use_status=CONTRACT_USE_STATUS.DELETE).count()

                        if child_contract_count != 0:
                            status = False
        else:
            contract_count = contract.objects.filter(cf_id=cfInfo.cf_id).exclude(contract_use_status=CONTRACT_USE_STATUS.DELETE).count()
            if contract_count == 0:
                status = True

    except Exception as ex:
        msg = "Exception.checkFolderDelete(cf_id:" + str(cf_id) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}

    result = {'result_code': 0,'msg':'success', 'status': status}
    return result

# ↓↓↓↓↓↓템플릿 폴더
# 표시대상이되는 템플릿 폴더리스트를 습득. Json.folderList(ListType) 드롭다운 설정에서 사용함.
# parentId가 None = 부모폴더, Id가 설정되어있으면 자식폴더임.
def getTemplateFolderList(memberId, publicFlg):
    try:
        memberObj = member.objects.get(member_id=memberId)
        customerId = memberObj.customer_id_id

        folderListObj = template_folder.objects.filter(customer_id=customerId, tf_public=publicFlg, tf_deleted = DELETE_FLG.USE).order_by('tf_sort')

        folderList = []
        for folderItem in folderListObj:
            if folderItem.tf_parent_id == 0:
                folderId = {
                    "folderId":folderItem.tf_id,
                    "folderName":folderItem.tf_name,
                    "publicFlg":folderItem.tf_public,
                    "parentId":None,
                }
                folderList.append(folderId)
            else:
                folderId = {
                    "folderId":folderItem.tf_id,
                    "folderName":folderItem.tf_name,
                    "publicFlg":folderItem.tf_public,
                    "parentId":folderItem.tf_parent_id,
                }
                folderList.append(folderId)

    except Exception as ex:
        msg = "Exception.getTemplateFolderList(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'folderList':folderList}

    return result

# 부모->자식 관계까지 설정된 템플릿 폴더리스트. 템플릿목록의 폴더리스트에서 사용함.
def getTemplateFolderTwoDepth(memberId, publicFlg):
    try:
        folderList = getTemplateFolderList(memberId, publicFlg).get("folderList")
        folderListResult = []
        for folderItem in folderList:
            if folderItem.get("parentId") == None:
                parentFolder = {
                    "folderId":folderItem.get("folderId"),
                    "folderName":folderItem.get("folderName"),
                    "publicFlg":folderItem.get("publicFlg"),
                    "childFolders": []
                }
                for folderItem2 in folderList:
                    if folderItem2.get("parentId") == folderItem.get("folderId"):
                        childFolder = {
                            "folderId":folderItem2.get("folderId"),
                            "folderName":folderItem2.get("folderName"),
                            "publicFlg":folderItem.get("publicFlg"),
                        }
                        parentFolder.get("childFolders").append(childFolder)
                folderListResult.append(parentFolder)

    except Exception as ex:
        msg = "Exception.getTemplateListTwoDepth(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'folderList':folderListResult}

    return result

#1계층 탬플릿 폴더 리스트 - 탬플릿수정 드롭다운에서 사용
def getOneDepthTemplateFolderList(memberId, publicFlg):
    try:
        memberObj = member.objects.get(member_id=memberId)
        customerId = memberObj.customer_id_id

        folderListObj = template_folder.objects.filter(customer_id=customerId, tf_public=publicFlg, tf_deleted = DELETE_FLG.USE).order_by('tf_sort')

        folderList = []
        for folderItem in folderListObj:
            if folderItem.tf_parent_id == 0:
                folderId = {
                    "folderId":folderItem.tf_id,
                    "folderName":folderItem.tf_name,
                    "publicFlg":folderItem.tf_public,
                    "parentId":None,
                }
                folderList.append(folderId)
            else:
                for parentFolderItem in folderListObj:
                    if folderItem.tf_parent_id == parentFolderItem.tf_id:
                        folderId = {
                            "folderId":folderItem.tf_id,
                            "folderName":parentFolderItem.tf_name +">"+ folderItem.tf_name,
                            "publicFlg":folderItem.tf_public,
                            "parentId":folderItem.tf_parent_id,
                        }
                        folderList.append(folderId)

    except Exception as ex:
        msg = "Exception.getTemplateFolderList(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'folderList':folderList}

    return result

# 계약서의 작성 권한이 있는 폴더인지 체크한다.
# 계약서 폴더 변경시 먼저 이 체크를 통과하면 진행할것!!!
def checkWriteAuthFolder(memberId, folderId):
    try:
        memberObj = member.objects.get(member_id=memberId)
        authCount = contract_folder_member.objects.select_related("cf_id").filter(\
            member_id = memberObj.member_id, cf_id__cf_id = folderId, cfm_write = USED_FLG.USED, cfm_deleted = DELETE_FLG.USE).count()
        if authCount < 1:
            # 권한이 없는 폴더입니다.
            result = {'result_code': 1,'msg':_('계약서 작성권한이 없는 폴더입니다.')}
            return result

    except Exception as ex:
        msg = "Exception.checkWriteAuthFolder(memberId:" + str(memberId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success'}

    return result
