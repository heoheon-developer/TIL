from django.utils.translation import gettext_lazy as _

# 사용법 : 딕셔너리, 또는 클래스타입으로 코드들을 정의해서 사용할것 #
# 클래스에 getCodeDict만들어주면 템플릿에서 사용할떄 일일이 view에서 딕셔너리 안만들어줘도됨.

# 사용/미사용
class USED_FLG:
    USED    = "Y"
    UNUSED  = "N"

# 일반적인 삭제플래그.
class DELETE_FLG:
    DELETE  = "Y"
    USE     = "N"

# 계정 권한타입(N:일반, M:관리자, S:시스템관리자)
class MEMBER_TYPE:
    NOMAL   = "N"
    MANAGER = "M"
    SYSTEM  = "S"

# 유저 삭제플래그
class MEMBER_DELETED:
    NO  = "N"
    YES = "Y"

# 유저 첫 메일인증 플래그
class MEMBER_MAIL_CHECK:
    NO      = "N"
    DONE    = "Y"

# 공지사항 로그인화면 표시구분(N로그인화면에서 표시, Y로그인화면에서 안표시)
class NOTICE_TYPE:
    LOGIN       = "N"
    AFTER_LOGIN = "Y"

# 공지사항 로그인화면 상단고정여부(N미고정, Y고정)
class NOTICE_HEADER:
    NO = "N"
    YES = "Y"

# 계약서 블록체인 사용유무
class CONTRACT_TYPE:
    NORMAL      = "N"
    BLOCKCHAIN  = "B"

    @staticmethod
    def getCodeDict():
        return {
            'NORMAL'     : CONTRACT_TYPE.NORMAL,
            'BLOCKCHAIN'  : CONTRACT_TYPE.BLOCKCHAIN,
        }

# 계약서 태그 공개유무
class PRIVATE_CONTRACT_TAG:
    NO  = "N"
    YES = "Y"

#계약서 EOS업로드 상태
class CONTRACT_EOS:
    NO = "N"
    UPLOAD = "U"

#쿠키 암호화 키
class AESCipher_KEY:
    COOKIE_KEY = 'KeiyakuCookie'

# 컨트랙트USE Status
class CONTRACT_USE_STATUS:
    USE     = "N"
    DELETE  = "Y"
    CANCEL  = "C"
    PAUSE   = "P"

    @staticmethod
    def getCodeDict():
        return {
            'USE'     : CONTRACT_USE_STATUS.USE,
            'DELETE'  : CONTRACT_USE_STATUS.DELETE,
            'CANCEL'  : CONTRACT_USE_STATUS.CANCEL,
            'PAUSE'   : CONTRACT_USE_STATUS.PAUSE,
        }

#계약상태(실제DB 코드)
class CONTRACT_STATUS:
    WRITTING        = "1" #작성중
    CONFIRMING      = "2" #확인중
    CONFIRMED       = "3" #확인완료(승인의뢰)
    APPROVAL_FINISH = "4" #승인완료
    BC_UPLOAD_FAIL  = "5" #등록실패
    CONTRACTED      = "6" #체결완료

    @staticmethod
    def getCodeList():
        return [
            CONTRACT_STATUS.WRITTING,
            CONTRACT_STATUS.CONFIRMING,
            CONTRACT_STATUS.CONFIRMED,
            CONTRACT_STATUS.APPROVAL_FINISH,
            CONTRACT_STATUS.BC_UPLOAD_FAIL,
            CONTRACT_STATUS.CONTRACTED
        ]

#계약상태(계약상태 카운트 메뉴에서 사용할 코드. 복수조건 검색등이 필요해서 코드를 따로 정의함.)
#계약상태 + 계약사용상태
class CONTRACT_STATUS_FOR_PROGRAM:
    WRITTING            = CONTRACT_STATUS.WRITTING #작성중
    CONFIRMING          = CONTRACT_STATUS.CONFIRMING #확인중
    CONFIRMED           = CONTRACT_STATUS.CONFIRMED #확인완료(승인의뢰)
    APPROVAL_FINISH     = CONTRACT_STATUS.APPROVAL_FINISH #승인완료
    BC_UPLOAD_FAIL      = CONTRACT_STATUS.BC_UPLOAD_FAIL #등록실패
    CONTRACTED          = CONTRACT_STATUS.CONTRACTED #체결완료
    CONFIRMING_ED       = "90" #확인중 & 확인완료
    OUR_APPROVAL        = "91" #자사내 승인완료
    OTHER_APPROVAL      = "92" #상대승인완료
    APPROVAL_BC_FAIL    = "93" #등록실패 & 승인완료
    USE    = CONTRACT_USE_STATUS.USE #계약사용 상태 사용(작성중)
    DELETE    = CONTRACT_USE_STATUS.DELETE #계약사용 상태 삭제
    CANCEL    = CONTRACT_USE_STATUS.CANCEL #계약사용 상태 취소
    PAUSE    = CONTRACT_USE_STATUS.PAUSE #계약사용 상태 보류

    @staticmethod
    def getCodeDict():
        # 계약상태별 갯수 표시 컴포넌트에서 사용함.
        contractStatusCode = {
            'WRITTING':CONTRACT_STATUS_FOR_PROGRAM.WRITTING,
            'CONFIRMING':CONTRACT_STATUS_FOR_PROGRAM.CONFIRMING,
            'CONFIRMED':CONTRACT_STATUS_FOR_PROGRAM.CONFIRMED,
            'APPROVAL_FINISH':CONTRACT_STATUS_FOR_PROGRAM.APPROVAL_FINISH,
            'BC_UPLOAD_FAIL':CONTRACT_STATUS_FOR_PROGRAM.BC_UPLOAD_FAIL,
            'CONTRACTED':CONTRACT_STATUS_FOR_PROGRAM.CONTRACTED,
            'CONFIRMING_ED':CONTRACT_STATUS_FOR_PROGRAM.CONFIRMING_ED,
            'OUR_APPROVAL':CONTRACT_STATUS_FOR_PROGRAM.OUR_APPROVAL,
            'OTHER_APPROVAL':CONTRACT_STATUS_FOR_PROGRAM.OTHER_APPROVAL,
            'APPROVAL_BC_FAIL':CONTRACT_STATUS_FOR_PROGRAM.APPROVAL_BC_FAIL,
            'USE':CONTRACT_USE_STATUS.USE,
            'DELETE':CONTRACT_USE_STATUS.DELETE,
            'CANCEL':CONTRACT_USE_STATUS.CANCEL,
            'PAUSE':CONTRACT_USE_STATUS.PAUSE,
        }
        return contractStatusCode

    @staticmethod
    def getStatusName(code):
        # 계약상태별 상태명
        contractStatusCode = {
            CONTRACT_STATUS_FOR_PROGRAM.WRITTING:_('작성중'),
            CONTRACT_STATUS_FOR_PROGRAM.CONFIRMING:_('계약확인중'),
            CONTRACT_STATUS_FOR_PROGRAM.CONFIRMED:_('승인의뢰완료'),
            CONTRACT_STATUS_FOR_PROGRAM.APPROVAL_FINISH:_('승인완료'),
            CONTRACT_STATUS_FOR_PROGRAM.BC_UPLOAD_FAIL:_('승인완료'),
            CONTRACT_STATUS_FOR_PROGRAM.CONTRACTED:_('체결완료'),
            CONTRACT_STATUS_FOR_PROGRAM.CONFIRMING_ED:_('계약확인중'),
            CONTRACT_STATUS_FOR_PROGRAM.OUR_APPROVAL:_('자사내승인완료'),
            CONTRACT_STATUS_FOR_PROGRAM.OTHER_APPROVAL:_('상대방승인완료'),
            CONTRACT_STATUS_FOR_PROGRAM.APPROVAL_BC_FAIL:_('승인완료'),
            CONTRACT_STATUS_FOR_PROGRAM.USE:_('작성중'),
            CONTRACT_STATUS_FOR_PROGRAM.DELETE:_('삭제'),
            CONTRACT_STATUS_FOR_PROGRAM.CANCEL:_('취소'),
            CONTRACT_STATUS_FOR_PROGRAM.PAUSE:_('보류'),
        }
        return contractStatusCode.get(code)

# 승인플래그
class APPROVAL_FLG:
    YES = "Y"
    NO  = "N"

    @staticmethod
    def getCodeDict():
        return {
            'YES'    : APPROVAL_FLG.YES,
            'NO'  : APPROVAL_FLG.NO,
        }

# 계약참여자 메일 발송여부
class EMAIL_SEND_FLG:
    YES = "Y"
    NO = "N"

# 템플릿 공개유무
class TEMPLATE_OPEN_FLG:
    OPEN    = "Y"
    PRIVATE = "N"

#계약참가멤버 참가권한.
class CONTRACT_MEMBER_AUTH:
    MANAGER     = "S"
    APPROVER    = "C" #승인자
    CHECKER     = "A" #확인자 DB코드가 거꾸로 된것같은데 그냥 쓰기로함.

    @staticmethod
    def getCodeDict():
        return {
            'MANAGER'    : CONTRACT_MEMBER_AUTH.MANAGER,
            'APPROVER'  : CONTRACT_MEMBER_AUTH.APPROVER,
            'CHECKER'  : CONTRACT_MEMBER_AUTH.CHECKER,
        }

#회사관계(자사, 상대방).
class COMPANY_RELATION:
    OURCOMP     = "S"
    OTHERCOMP   = "P"

    @staticmethod
    def getCodeDict():
        return {
            'OURCOMP'    : COMPANY_RELATION.OURCOMP,
            'OTHERCOMP'  : COMPANY_RELATION.OTHERCOMP,
        }

#계약관계(갑, 을).
class CONTRACT_RELATION:
    FORMER = "F"
    LATTER = "L"

# 검색타입.
class SEARCH_TYPE:
    TITLE       = 'T'
    SUB         = "S"
    TITLE_SUB   = "TS"

    @staticmethod
    def getCodeDict():
        return {
            'TITLE'    : SEARCH_TYPE.TITLE,
            'SUB'  : SEARCH_TYPE.SUB,
            'TITLE_SUB'  : SEARCH_TYPE.TITLE_SUB,
        }

#1:1문의 답변여부
class QA_ANSWER_CHECK:
    YES = 'Y'
    NO  = 'N'

#계약정보 자동갱신 사용여부
class CONTRACT_INFO_AUTO_UPD:
    USE = 'Y'
    NO = 'N'

#사용자 계약서 구분
class USER_CONTRACT_TYPE:
    CLOUD       = 'N'
    BLOCKCHAIN  = 'B'

# 화폐단위
class CURRENCY:
    JPY = "JPY"
    KRW = "KRW"
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"
    CNY = "CNY"
    HKD = "HKD"
    THB = "THB"
    AUD = "AUD"
    CAD = "CAD"

# 계약참여 유저 메일 발송완료
class CONTRACT_MEMBER_SEND_MAIL_DONE:
    YES   = "Y"
    NO    = "N"

# 알람 읽음 여부
class ALAM_READ:
    UNREAD  = 'N'
    READ    = 'Y'

# 알람 구분
class ALAM_TYPE:
    CONTRACT    = 'C'
    COMMENT     = 'CM'

class TIMELINE_CODE:
    START_WRITE = 0 #계약서 작성시작
    PREAMBLE_WRITE_DONE = 1 #전문입력완료
    ADD_COMMENT = 2 # 코멘트 추가
    FILE_ADD = 3 # 계약 첨부파일추가
    FILE_DEL = 4 # 계약 첨부파일 삭제
    CONTRACT_INFO_ADD = 5 # 계약정보 작성
    CONTRACT_INFO_EDIT = 6 # 계약정보 수정
    TEXT_WRITE_DONE = 7 #본문입력완료
    OUR_MANAGER_ADD = 8 # 자사 관리자 추가
    OTHER_MANAGER_ADD = 9 #상대 관리자 추가
    OUR_MANAGER_DEL = 10 # 자사 관리자 삭제
    OTHER_MANAGER_DEL = 11 # 타사 관리자 삭제
    OUR_CHECKER_ADD = 12 # 자사 확인자 추가
    OTHERCHECKER_ADD = 13 # 타사 확인자 추가
    OUR_CHECKER_DEL = 14
    OTHER_CHECKER_DEL = 15
    OUR_APPROVER_ADD = 16
    OTHER_APPROVER_ADD = 17
    OUR_APPROVER_DEL = 18
    OTHER_APPROVER_DEL = 19
    CONTRACT_WRITE_DONE = 20 #계약작성완료
    REQUEST_APPROVAL = 21
    OUR_CHECK_DONE = 22
    OTHER_CHECK_DONE = 23
    OUR_APPROVAL_DONE = 24 # 자사내 모든 승인자 승인완료시
    OTHER_APPROVAL_DONE = 25 # 상대방 모든 승인자 승인완료시
    CONTACT_APPROVAL_DONE = 26 # 계약서 완전 승인완료시
    CONTRACT_APPROVE = 38 # 아무나 승인자가 승인완료 눌렀을때
    TIMESTAMP_AUTH = 27
    CONTRACT_SIGNED = 28
    CONTARCT_EDDITED = 29
    CONTARCT_CANCELED = 30
    CONTARCT_PAUSE = 31
    CONTARCT_RESTART = 32
    CONTRACT_DELETE = 33
    ENCODING_DONE = 34
    UPLOAD_EOS = 35
    UPLOAD_ETH = 36
    AUDIT_TRAIL_ISSUED = 37

    #타임라인 구분 코드 및 메세지.
    TIMELINE_CODE_MESSAGE = {
        START_WRITE:_('계약서 작성시작'),
        PREAMBLE_WRITE_DONE:_('전문 입력완료'),
        ADD_COMMENT:_('코멘트 등록'),
        FILE_ADD:_('개 등록'),#첨부파일
        FILE_DEL:_('개 삭제'),#첨부파일
        CONTRACT_INFO_ADD:_('계약정보 입력'),
        CONTRACT_INFO_EDIT:_('계약정보 수정'),
        TEXT_WRITE_DONE:_('본문 입력완료'),
        OUR_MANAGER_ADD:_('자사내 담당자 추가'),
        OTHER_MANAGER_ADD:_('상대방 담당자 추가'),
        OUR_MANAGER_DEL:_('자사내 담당자 삭제'),
        OTHER_MANAGER_DEL:_('상대방 담당자 삭제'),
        OUR_CHECKER_ADD:_('자사내 확인자 추가'),
        OTHER_MANAGER_DEL:_('상대방 확인자 추가'),
        OUR_CHECKER_DEL:_('자사내 확인자 삭제'),
        OTHER_CHECKER_DEL:_('상대방 확인자 삭제'),
        OUR_APPROVER_ADD:_('자사내 승인자 추가'),
        OTHER_APPROVER_ADD:_('상대방 승인자 추가'),
        OUR_APPROVER_DEL:_('자사내 승인자 삭제'),
        OTHER_APPROVER_DEL:_('상대방 승인자 삭제'),
        CONTRACT_WRITE_DONE:_('계약 작성완료'),
        REQUEST_APPROVAL:_('승인요청'),
        OUR_CHECK_DONE:_('자사내 계약 확인완료'),
        OTHER_CHECK_DONE:_('상대방 계약 확인완료'),
        CONTRACT_APPROVE:_('계약승인완료'),
        OUR_APPROVAL_DONE:_('자사내 계약 승인완료'),
        OTHER_APPROVAL_DONE:_('상대방 계약 승인완료'),
        CONTACT_APPROVAL_DONE:_('계약승인완료'), # 시스템로그이므로 사용자명 찍지말것.
        TIMESTAMP_AUTH:_('타임스탬프 인증'),
        CONTRACT_SIGNED:_('체결완료'),
        CONTARCT_EDDITED:_('계약서 수정'),
        CONTARCT_CANCELED:_('계약서 취소'),
        CONTARCT_PAUSE:_('계약서 보류'),
        CONTARCT_RESTART:_('계약서 보류 재개'),
        CONTRACT_DELETE:_('계약서 삭제'),
        ENCODING_DONE:_('계약서 암호화 완료'),
        UPLOAD_EOS:_('EOS에 계약서 등록'),
        UPLOAD_ETH:_('Ethereum에 최종계약서 등록'),
        AUDIT_TRAIL_ISSUED:_('감사추적 인증서 발급완료'),
    }

    @staticmethod
    def getTimelineMsg(code, fileNum):
        message = ''
        if code == 3 or code == 4:
            message = _('첨부파일') + str(fileNum) + str(TIMELINE_CODE.TIMELINE_CODE_MESSAGE.get(code))
        else:
            message = str(TIMELINE_CODE.TIMELINE_CODE_MESSAGE.get(code))
        return message

TODOHUKEN = {
    0:"北海道",
    1:"青森県",
    2:"岩手県",
    3:"宮城県",
    4:"秋田県",
    5:"山形県",
    6:"福島県",
    7:"茨城県",
    8:"栃木県",
    9:"群馬県",
    10:"埼玉県",
    11:"千葉県",
    12:"東京都",
    13:"神奈川県",
    14:"新潟県",
    15:"富山県",
    16:"石川県",
    17:"福井県",
    18:"山梨県",
    19:"長野県",
    20:"岐阜県",
    21:"静岡県",
    22:"愛知県",
    23:"三重県",
    24:"滋賀県",
    25:"京都府",
    26:"大阪府",
    27:"兵庫県",
    28:"奈良県",
    29:"和歌山県",
    30:"鳥取県",
    31:"島根県",
    32:"岡山県",
    33:"広島県",
    34:"山口県",
    35:"徳島県",
    36:"香川県",
    37:"愛媛県",
    38:"高知県",
    39:"福岡県",
    40:"佐賀県",
    41:"長崎県",
    42:"熊本県",
    43:"大分県",
    44:"宮崎県",
    45:"鹿児島県",
    46:"沖縄県",
}
