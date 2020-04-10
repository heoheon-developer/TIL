from common_py.models import contract, contract_file, member
from common_py.utils import getNowData, ipfs_upload_wrap_directory
from common_py.process import timelineProcess
from common_py.CodeDict import TIMELINE_CODE

# 계약서에 첨부파일추가.
def addContractFile(memberId, name, contractId, file):
    try:
        # ipfs에 등록한다.
        try:
            ipfsRes = ipfs_upload_wrap_directory(file)
        except Exception as ex:
            msg = "ipfsRes Exception.addContractFile(memberId:" + str(memberId) + ", contractId:" + str(contractId) + ")) ex:" + str(ex)
            print(msg)
            return {'result_code': -1,'msg':'ipfs Exception : ' + str(ex)}

        # html에서 image/png 이런형식으로 오는데, office파일등 타입형식이 긴녀석들이 몇글자까지 올지 알 수없으므로 앞에거만 db에 넣기로함.
        fileType = file.content_type.split("/")[0]

        nowDate = getNowData()
        contractFileModel = contract_file(contract_id = contract.objects.get(contract_id=contractId), ipfs_hash=ipfsRes[1].get("Hash"), cf_name=file.name, \
        cf_size=file.size, cf_type=fileType, reg_date=nowDate, update_date=nowDate)
        contractFileModel.save()

        # 파일 카운트도 넘겨준다.
        fileCnt = contract_file.objects.filter(contract_id=contractId).count()

        # 파일추가 타임라인 추가.(TODO 갯수획득 버그때문에 나중에 수정해야함.)
        timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.FILE_ADD, name, fileCnt)

    except Exception as ex:
        msg = "Exception.addContractFile(memberId:" + str(memberId) + ", contractId:" + str(contractId) + ")) ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'fileId':contractFileModel.cf_id, 'fileName':contractFileModel.cf_name, 'fileType':fileType, 'ipfsHash':ipfsRes[1].get("Hash"), 'fileCnt':fileCnt}

    return result

# 계약서 첨부삭제
def contractFileDelete(memberId, name, contractId, cfId):
    try:
        contractFileModel = contract_file.objects.get(cf_id = cfId, contract_id = contract.objects.get(contract_id=contractId))
        contractFileModel.delete()

        # 파일 카운트도 넘겨준다.
        fileCnt = contract_file.objects.filter(contract_id=contractId).count()

        # 파일추가 타임라인 추가.(TODO 갯수획득 버그때문에 나중에 수정해야함.)
        timelineProcess.addTimeLine(memberId, contractId, TIMELINE_CODE.FILE_DEL, name, fileCnt)

    except Exception as ex:
        msg = "Exception.getContractFileDelete(memberId:" + str(memberId) + ", contractId:" + str(contractId) + ", cfId:" + str(cfId) + ")) ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'cfId':cfId, 'fileCnt':fileCnt}

    return result

# 계약서 첨부파일 습득
def getContractFileList(memberId, contractId):
    try:
        nowDate = getNowData()
        contractFileModel = contract_file.objects.filter(contract_id = contractId)

    except Exception as ex:
        msg = "Exception.getContractFileList(memberId:" + str(memberId) + ", contractId:" + str(contractId) + ")) ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'contractFileModel':contractFileModel}

    return result