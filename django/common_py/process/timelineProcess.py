from django.db.models import Q
from common_py.models import contract, contract_timeline
from common_py.CodeDict import TIMELINE_CODE
from common_py.utils import getNowDataTime

# 타임라인을 습득한다
def getTimeline(memberId, contractId):
    try:
        timelineResult = contract_timeline.objects.filter(contract_id = contractId)
        timelineList = []
        for item in timelineResult:
            timeline = {
                'ct_id':item.ct_id,
                'contract_id':item.contract_id,
                'ct_type':item.ct_type,
                'ct_user_name':item.ct_user_name,
                'ct_files':item.ct_files,
                'reg_date_ori':item.reg_date,
                'reg_date':item.reg_date.strftime("%y/%m/%d"),
                'reg_date_time':item.reg_date.strftime("%H:%M"),
                'update_date':item.update_date,
                'ct_text':TIMELINE_CODE.getTimelineMsg(item.ct_type, item.ct_files)
            }
            timelineList.append(timeline)

    except Exception as ex:
        msg = "Exception.getTimeline(memberId:" + str(memberId) + "contract_id:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'timelineList':timelineList}

    return result

# 타임라인을 저장한다.fileCnt는 첨부파일 추가, 삭제이외에는 None
def addTimeLine(memberId, contractId, timelineType, userName, filesCnt):
    try:
        nowDate = getNowDataTime()
        timeline = contract_timeline.objects.create(contract_id=contract.objects.get(contract_id=contractId), \
        ct_type=timelineType, ct_user_name=userName, ct_files=filesCnt, reg_date=nowDate, update_date=nowDate)

    except Exception as ex:
        msg = "Exception.addTimeLine(memberId:" + str(memberId) + "contract_id:" + str(contractId) + ") ex:" + str(ex)
        print(msg)
        return {'result_code': -9999,'msg':'Exception : ' + str(ex)}
    result = {'result_code': 0,'msg':'success', 'timeline':timeline}

    return result