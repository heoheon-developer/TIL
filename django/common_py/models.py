from django.db import models
from django.utils import timezone

# Create your models here.
class qa_category(models.Model):

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    qc_id       = models.AutoField('카테고리ID', primary_key=True)
    qc_sort     = models.IntegerField('카테고리순서')
    qc_name     = models.CharField('카테고리명', max_length=100)
    qc_deleted  = models.CharField('삭제여부', max_length=2, choices=deleted, default='N')
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        db_table = 'qa_category'

class customer(models.Model):

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    customer_id             = models.AutoField('고객사 아이디', primary_key=True)
    customer_name           = models.CharField('고객사 명', max_length=200)
    customer_ceo            = models.CharField('대표자명', max_length=100)
    customer_tel1           = models.CharField('전화번호1', max_length=4, null=True)
    customer_tel2           = models.CharField('전화번호2', max_length=4, null=True)
    customer_tel3           = models.CharField('전화번호3', max_length=4, null=True)
    customer_fax1           = models.CharField('팩스1', max_length=4, null=True)
    customer_fax2           = models.CharField('팩스2', max_length=4, null=True)
    customer_fax3           = models.CharField('팩스3', max_length=4, null=True)
    customer_dodobu         = models.CharField('고객사 도도부현', max_length=2)
    customer_post           = models.CharField('고객사 우편번호', max_length=7)
    customer_city           = models.CharField('고객사 주소 - 도시', max_length=100)
    customer_detail_address = models.CharField('고객사 주소 - 상세', max_length=100)
    customer_sign           = models.CharField('고객사 서명', max_length=100, null=True)
    customer_stamp          = models.CharField('고객사 도장', max_length=100, null=True)
    customer_memo           = models.TextField('메모', null=True)
    customer_parson_name    = models.CharField('담당자 이름', max_length=100)
    customer_parson_email   = models.CharField('담당자 이메일', max_length=100)
    customer_parson_tel1    = models.CharField('담당자 전화번호1', max_length=4)
    customer_parson_tel2    = models.CharField('담당자 전화번호2', max_length=4)
    customer_parson_tel3    = models.CharField('담당자 전화번호3', max_length=4)
    start_date              = models.DateField('계약 계시일')
    end_date                = models.DateField('계약 종료일')
    users                   = models.IntegerField('사용자수')
    customer_deleted        = models.CharField('삭제여부', max_length=2, choices=deleted, default='N')
    reg_date                = models.DateTimeField('등록일', default=timezone.now)
    update_date             = models.DateTimeField('수정일', default=timezone.now)


    class Meta:
        db_table = 'customer'

class member(models.Model):

    auth = (
        ('N', '미지정'),
        ('Y', '지정')
    )

    type = (
        ('N', 'Nomal'),
        ('M', 'Manager'),
        ('S', 'System')
    )

    m_check = (
        ('N', '미인증'),
        ('Y', '인증')
    )

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    terms_check = (
        ('N', '미동의'),
        ('Y', '동의')
    )

    contract_type = (
        ('N', 'Nomal'),
        ('B', 'Blockchain')
    )

    member_id               = models.AutoField('사용자  ID', primary_key=True)
    customer_id             = models.ForeignKey(customer, db_column='customer_id', on_delete=models.PROTECT)
    member_email            = models.CharField('사용자 이메일', max_length=200, null=True)
    member_password         = models.CharField('사용자 패스워드', max_length=100, null=True)
    member_kj_lastname      = models.CharField('한자 성', max_length=50)
    member_kj_firstname     = models.CharField('한자 이름', max_length=50)
    member_fg_lastname      = models.CharField('후리카나 성', max_length=50)
    member_fg_firstname     = models.CharField('후리카나 이름', max_length=50)
    member_eng_lastname     = models.CharField('영어 성', max_length=50, null=True)
    member_eng_firstname    = models.CharField('영어 이름', max_length=50, null=True)
    member_tel1             = models.CharField('전화번호1', max_length=4, null=True)
    member_tel2             = models.CharField('전화번호2', max_length=4, null=True)
    member_tel3             = models.CharField('전화번호3', max_length=4, null=True)
    authority               = models.CharField('담당자 여부', max_length=2, choices=auth, default='N')
    confirmation            = models.CharField('확인자 여부', max_length=2, choices=auth, default='N')
    approval                = models.CharField('승인자 여부', max_length=2, choices=auth, default='N')
    member_zipcode          = models.CharField('우편번호', max_length=7, null=True)
    member_dodobu           = models.CharField('도도부현', max_length=2, null=True)
    member_city             = models.CharField('사용자 도시', max_length=50, null=True)
    member_detail_address   = models.CharField('사용자 상세주소', max_length=100, null=True)
    member_type             = models.CharField('사용자 구분', max_length=2, choices=type, default='N')
    member_maill_check      = models.CharField('사용자 메일인증 여부', max_length=2, choices=m_check, default='N')
    member_deleted          = models.CharField('회원 삭제 여부', max_length=2, choices=deleted, default='N')
    member_sign             = models.CharField('사용자 서명', max_length=50, null=True)
    member_stamp            = models.CharField('사용자 도장', max_length=50, null=True)
    member_pc_code          = models.CharField('패스워드 확인코드', max_length=6, null=True)
    member_token            = models.CharField('메일인증 토큰', max_length=50, null=True)
    member_temp_password    = models.CharField('임시패스워드', max_length=100, null=True)
    member_contract_confirm = models.CharField('계약서 작성 인증여부', max_length=2, choices=m_check, default='N')
    terms_flag              = models.CharField('약관동의 여부', max_length=2, choices=terms_check, default='N')
    member_contract_type    = models.CharField('계약서 등록타입', max_length=2, choices=contract_type, default='N')
    reg_date                = models.DateTimeField('등록일', default=timezone.now)
    update_date             = models.DateTimeField('수정일', default=timezone.now)


    class Meta:
        indexes = [
           models.Index(fields=['customer_id'])
        ]

        db_table = 'member'

class qa(models.Model):

    answer_check = (
        ('N', '미답변'),
        ('Y', '답변')
    )

    qa_id           = models.AutoField('QA ID', primary_key=True)
    qc_id           = models.ForeignKey(qa_category, db_column='qc_id', on_delete=models.PROTECT)
    member_id       = models.ForeignKey(member, db_column='member_id', on_delete=models.PROTECT)
    qa_title        = models.CharField('1:1문의 제목', max_length=255)
    qa_content      = models.TextField('1:1문의 내용')
    qa_answer_check = models.CharField('답변여부', max_length=2, choices=answer_check, default='N')
    reg_date        = models.DateTimeField('등록일', default=timezone.now)
    update_date     = models.DateTimeField('등록일자', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['qc_id']),
           models.Index(fields=['member_id'])
        ]

        db_table = 'qa'

class qa_senders(models.Model):

    confirm = (
        ('N', '미인증'),
        ('Y', '인증')
    )

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    qs_id           = models.AutoField('수신메일ID', primary_key=True)
    qs_name         = models.CharField('수신자이름', max_length=100)
    qs_email        = models.CharField('수신자이메일', max_length=200)
    qs_confirm      = models.CharField('메일인증여부', max_length=2, choices=confirm, default='N')
    qs_deleted      = models.CharField('삭제여부', max_length=2, choices=deleted, default='N')
    qs_auth_token   =  models.CharField('수신자이메일', max_length=50)
    reg_date        = models.DateTimeField('등록일', default=timezone.now)
    update_date     = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        db_table = 'qa_senders'

class faq(models.Model):

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    faq_id      = models.AutoField('FAQ ID', primary_key=True)
    faq_title   = models.CharField('FAQ 제목', max_length=200)
    faq_content = models.TextField('FAQ 내용')
    faq_sort    = models.IntegerField('FAQ 정렬')
    faq_deleted = models.CharField('FAQ 삭제여부', max_length=2, choices=deleted, default='N')
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        db_table = 'faq'

class contract_folder(models.Model):

    public = (
        ('N', '비공개'),
        ('Y', '공개')
    )

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    cf_id       = models.AutoField('계약서 폴더 ID', primary_key=True)
    customer_id = models.ForeignKey(customer, db_column='customer_id', on_delete=models.PROTECT)
    member_id   = models.ForeignKey(member, db_column='member_id', on_delete=models.PROTECT, null=True)
    cf_parent   = models.ForeignKey("self", db_column='cf_parent', on_delete=models.PROTECT, null=True)
    cf_name     = models.CharField('폴더명', max_length=100)
    cf_sort     = models.IntegerField('폴더 순서')
    cf_public   = models.CharField('공개여부', max_length=2, choices=public, default='N')
    cf_deleted  = models.CharField('삭제여부', max_length=2, choices=deleted, default='N')
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['member_id']),
           models.Index(fields=['customer_id']),
           models.Index(fields=['cf_parent'])
        ]

        db_table = 'contract_folder'

class template_folder(models.Model):

    public = (
        ('N', '자사'),
        ('Y', '공개')
    )

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    tf_id       = models.AutoField('템플릿 폴더ID', primary_key=True)
    member_id   = models.ForeignKey(member, db_column='member_id', on_delete=models.PROTECT)
    customer_id = models.ForeignKey(customer, db_column='customer_id', on_delete=models.PROTECT)
    tf_parent   = models.ForeignKey("self", db_column='tf_parent', on_delete=models.PROTECT)
    tf_name     = models.CharField('폴더명', max_length=100)
    tf_sort 	= models.IntegerField('폴더 순서')
    tf_public   = models.CharField('폴더 공개여부', max_length=2, choices=public, default='N')
    tf_deleted  = models.CharField('폴더 삭제여부', max_length=2, choices=deleted, default='N')
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date = models.DateTimeField('수정일', default=timezone.now)

    class Meta:

        indexes = [
           models.Index(fields=['member_id']),
           models.Index(fields=['customer_id']),
           models.Index(fields=['tf_parent'])
        ]

        db_table = 'template_folder'

class template(models.Model):

    type = (
        ('N', '자사'),
        ('Y', '비공개')
    )

    t_id        = models.AutoField('템플릿ID', primary_key=True)
    member_id   = models.ForeignKey(member, db_column='member_id', on_delete=models.PROTECT)
    customer_id = models.ForeignKey(customer, db_column='customer_id', on_delete=models.PROTECT)
    tf_id       = models.ForeignKey(template_folder, db_column='tf_id', on_delete=models.PROTECT)
    t_title     = models.CharField('템플릿 제목', max_length=100)
    t_content   = models.TextField('템플릿 내용')
    t_page      = models.IntegerField('템플릿 페이지 수')
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date = models.DateTimeField('수정일', default=timezone.now)

    class Meta:

        indexes = [
           models.Index(fields=['member_id']),
           models.Index(fields=['tf_id'])
        ]

        db_table = 'template'

class flow(models.Model):

    flow_id	        = models.AutoField('플로워ID', primary_key=True)
    member_id       = models.ForeignKey(member, db_column='member_id', on_delete=models.PROTECT)
    customer_id     = models.ForeignKey(customer, db_column='customer_id', on_delete=models.PROTECT)
    cf_id           = models.ForeignKey(contract_folder, db_column='cf_id', on_delete=models.PROTECT)
    flow_name   	= models.CharField('플로워 명칭', max_length=60)
    flow_comment	= models.CharField('플로워 코멘트', max_length=120)
    reg_date        = models.DateTimeField('등록일', default=timezone.now)
    update_date     = models.DateTimeField('수정일', default=timezone.now)

    class Meta:

        indexes = [
           models.Index(fields=['member_id']),
           models.Index(fields=['customer_id']),
           models.Index(fields=['cf_id'])
        ]

        db_table = 'flow'

class contract(models.Model):

    tag_status = (
        ('N', '비공개'),
        ('Y', '공개')
    )

    approval = (
        ('N', '미승인'),
        ('Y', '승인')
    )

    blockChainUse = (
        ('N', '미사용'),
        ('Y', '사용')
    )

    contractStatus = (
        ('1', '작성중'),
        ('2', '확인중'),
        ('3', '확인완료'),
        ('4', '승인완료'),
        ('5', '등록에러'),
        ('6', '체결완료')
    )

    contractUseStatus = (
        ('N', '사용'),
        ('Y', '삭제'),
        ('C', '취소'),
        ('P', '보류')
    )

    eos_use = (
        ('N', '미사용'),
        ('U', '업로드중'),
    )

    eth_use = (
        ('N', '미사용'),
        ('U', '업로드중'),
    )

    contract_id             = models.AutoField('계약서ID', primary_key=True)
    member_id               = models.ForeignKey(member, db_column='member_id', on_delete=models.PROTECT)
    customer_id             = models.ForeignKey(customer, db_column='customer_id', on_delete=models.PROTECT)
    cf_id                   = models.ForeignKey(contract_folder, db_column='cf_id', on_delete=models.PROTECT)
    t_id                    = models.ForeignKey(template, db_column='t_id', on_delete=models.PROTECT)
    flow_id                 = models.ForeignKey(flow, db_column='flow_id', on_delete=models.PROTECT)
    contract_type           = models.CharField('계약서 형식', max_length=2, choices=blockChainUse, default='N')
    contract_number         = models.CharField('계약서 관리번호', max_length=20)
    contract_name           = models.CharField('계약서 명', max_length=100)
    contract_tag            = models.CharField('계약서 태그', max_length=200, null=True)
    contract_tag_status     = models.CharField('계약서 태그 공개여부', max_length=2, choices=tag_status, default='N')
    contract_content        = models.TextField('계약서 내용')
    contract_status         = models.CharField('계약상태', max_length=2, choices=contractStatus, default='1')
    ct_approval             = models.CharField('자사내 승인여부', max_length=2, choices=approval, default='N')
    ct_other_approval       = models.CharField('상대방승인여부', max_length=2, choices=approval, default='N')
    contract_pin            = models.TextField('암호화키', null=True)
    contract_pin_key_path   = models.TextField('복호화키', null=True)
    contract_eth_regdate    = models.DateTimeField('이더리움등록일자', default=timezone.now, null=True)
    contract_eth_hash       = models.CharField('이더리움 해쉬', max_length=100, null=True)
    contract_use_status     = models.CharField('계약서 사용상태', max_length=2, choices=contractUseStatus, default='N')
    contract_eos            = models.CharField('계약서 Eos 업로드중 상태', max_length=2, choices=eos_use, default='N')
    contract_eth            = models.CharField('계약서 Ethereum 업로드중 상태', max_length=2, choices=eth_use, default='N')
    contract_timestamp_hash = models.CharField('계약서 타임스탬프 IPFS Hash', max_length=50, null=True)
    contract_audit_trail_hash = models.CharField('계약서 감사추적 IPFS Hash', max_length=50, null=True)
    contract_complete_date  = models.DateTimeField('등록일', null=True)
    contract_size           = models.IntegerField('계약서 용량', default=0)
    contract_hash           = models.CharField('계약서 해쉬', max_length=50, null=True)
    reg_date                = models.DateTimeField('등록일', default=timezone.now)
    update_date             = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['member_id']),
           models.Index(fields=['cf_id']),
           models.Index(fields=['t_id']),
           models.Index(fields=['customer_id']),
           models.Index(fields=['flow_id'])
        ]
        db_table = 'contract'

class contract_version(models.Model):

    cv_id               = models.AutoField('계약서 버전ID', primary_key=True)
    contract_id         = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    contract_name       = models.CharField('계약서 명', max_length=100)
    contract_content    = models.TextField('계약서 내용')
    cv_eos_reg_date     = models.DateTimeField('EOS 등록일자', null=True)
    cv_eos_hash         = models.CharField('EOS hash', max_length=100, null=True)
    version             = models.IntegerField('계약서 버전번호')
    cv_contract_size    = models.IntegerField('계약서 용량', default=0)
    cv_contract_hash    = models.CharField('계약서 hash', max_length=50, null=True)
    reg_date            = models.DateTimeField('등록일', default=timezone.now)
    update_date         = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['contract_id'])
        ]
        db_table = 'contract_version'

class contract_search(models.Model):

    cs_id       = models.AutoField('검색테이블 ID', primary_key=True)
    cv_id       = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    cs_content  = models.TextField('계약서 내용')
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['cv_id'])
        ]
        db_table = 'contract_search'


class contract_info(models.Model):

    auto = (
        ('N', '미갱신'),
        ('Y', '자동갱신')
    )

    relation = (
        ('F', '갑(Former)'),
        ('L', '을(Latter)')
    )

    ci_id                       = models.AutoField('계약정보 ID', primary_key=True)
    contract_id                 = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    ci_manage_number            = models.CharField('계약관리번호', max_length=15, null=True)
    ci_parson_name              = models.CharField('계약자 담당자 명', max_length=100)
    ci_parson_email             = models.CharField('계약서 담당자 이메일', max_length=200)
    ci_company_name             = models.CharField('자사회사명', max_length=200, null=True)
    ci_relation                 = models.CharField('자사 거래관계', max_length=2, null=True)
    ci_company_address          = models.CharField('자사 회사주소', max_length=100, null=True)
    ci_ceo                      = models.CharField('자사 대표자명', max_length=100, null=True)
    ci_contractor               = models.CharField('자사 계약자명', max_length=100, null=True)
    ci_partner_company_name     = models.CharField('상대방 회사명', max_length=200, null=True)
    ci_partner_relation         = models.CharField('상대방 거래관계', max_length=2, null=True)
    ci_partner_company_address  = models.CharField('상대방 회사주소', max_length=100, null=True)
    ci_partner_ceo              = models.CharField('상대방 대표자명', max_length=100, null=True)
    ci_partner_contractor       = models.CharField('상대방 계약자명', max_length=100, null=True)
    ci_price                    = models.BigIntegerField('거래금액', null=True)
    ci_currency                 = models.CharField('거래금액통화', max_length=5, null=True)
    ci_date                     = models.DateField('계약일', null=True)
    ci_contract_start           = models.DateField('계약시작일', null=True)
    ci_contract_end             = models.DateField('계약종료일', null=True)
    ci_settlement               = models.DateField('계약체결기한', null=True)
    ci_auto                     = models.CharField('자동갱신여부', max_length=2, choices=auto, default='N')
    ci_etc                      = models.CharField('그외', max_length=100, null=True)
    reg_date                    = models.DateTimeField('등록일', default=timezone.now)
    update_date                 = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['contract_id'])
        ]
        db_table = 'contract_info'

class contract_file(models.Model):

    cf_id       = models.AutoField('계약서 첨부파일ID', primary_key=True)
    contract_id = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    ipfs_hash   = models.CharField('첨부파일 Hash', max_length=50)
    cf_size     = models.IntegerField('첨부파일 사이즈')
    cf_name     = models.CharField('첨부파일 명', max_length=100)
    cf_type     = models.CharField('첨부파일 형식', max_length=30)
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['contract_id'])
        ]
        db_table = 'contract_file'

class contract_member(models.Model):

    auth = (
        ('S', '담당자'),
        ('C', '승인자'),
        ('A', '확인자')
    )

    relation = (
        ('S', '자사'),
        ('P', '상대방')
    )

    confirm = (
        ('N', '미승인'),
        ('Y', '승인')
    )

    send = (
        ('N', '미발송'),
        ('Y', '발송')
    )

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    cm_id           = models.AutoField('참여자ID', primary_key=True)
    contract_id     = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    cm_auth         = models.CharField('참여자 권한', max_length=2, choices=auth, default='S')
    cm_relation     = models.CharField('계약관계', max_length=2, choices=relation, default='S')
    cm_email        = models.CharField('참여자이메일', max_length=200)
    cm_name         = models.CharField('참여자 명', max_length=100)
    cm_confirm      = models.CharField('승인여부', max_length=2, choices=confirm, default='N')
    cm_email_send   = models.CharField('메일발송 여부', max_length=2, choices=send, default='N')
    cm_access_code  = models.TextField('액세스 코드', null=True)
    cm_access_key   = models.TextField('액세스코드 키', null=True)
    cm_deleted      = models.CharField('메일발송 여부', max_length=2, choices=deleted, default='N')
    reg_date        = models.DateTimeField('등록일', default=timezone.now)
    update_date     = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['contract_id'])
        ]

        db_table = 'contract_member'

class contract_comment(models.Model):

    cc_id       = models.AutoField('코멘트ID', primary_key=True)
    cm_id       = models.ForeignKey(contract_member, db_column='cm_id', on_delete=models.PROTECT)
    contract_id = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    cc_content  = models.TextField('코멘트내용')
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['contract_id']),
           models.Index(fields=['cm_id'])
        ]
        db_table = 'contract_comment'

class contract_timeline(models.Model):

    ct_id           = models.AutoField('타임라인ID', primary_key=True)
    contract_id     = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    ct_type         = models.CharField('타임라인 구분', max_length=2)
    ct_user_name    = models.CharField('타임라인 유저', max_length=100)
    ct_files        = models.IntegerField('첨부파일수', null=True)
    reg_date        = models.DateTimeField('등록일', default=timezone.now)
    update_date     = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['contract_id'])
        ]

        db_table = 'contract_timeline'

class contract_folder_member(models.Model):

    confirm = (
        ('N', '미사용'),
        ('Y', '사용')
    )

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    cfm_id              = models.AutoField('폴더사용자ID', primary_key=True)
    cf_id               = models.ForeignKey(contract_folder, db_column='cf_id', on_delete=models.PROTECT)
    member_id           = models.ForeignKey(member, db_column='member_id', on_delete=models.PROTECT)
    cfm_write           = models.CharField('권한 - 작성', max_length=2, choices=confirm, default='N')
    cfm_authority       = models.CharField('권한 - 담당자', max_length=2, choices=confirm, default='N')
    cfm_confirmation    = models.CharField('권한 - 확인자', max_length=2, choices=confirm, default='N')
    cfm_approval        = models.CharField('권한 - 승인자', max_length=2, choices=confirm, default='N')
    cfm_deleted         = models.CharField('권한 - 승인자', max_length=2, choices=deleted, default='N')
    reg_date            = models.DateTimeField('등록일', default=timezone.now)
    update_date         = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['cf_id']),
           models.Index(fields=['member_id'])
        ]

        db_table = 'contract_folder_member'

class contract_member_mail_history(models.Model):

    cmmh_id     = models.AutoField('메일내역ID', primary_key=True)
    cv_id       = models.ForeignKey(contract_version, db_column='cv_id', on_delete=models.PROTECT)
    cm_id       = models.ForeignKey(contract_member, db_column='cm_id', on_delete=models.PROTECT)
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['cv_id']),
           models.Index(fields=['cm_id'])
        ]

        db_table = 'contract_member_mail_history'

class customer_history(models.Model):

    ch_id           = models.AutoField('고객사 거래내역 아이디', primary_key=True)
    customer_id     = models.ForeignKey(customer, db_column='customer_id', on_delete=models.PROTECT)
    ch_start_date   = models.DateField('계약내역 - 개시일', null=True)
    ch_end_date     = models.DateField('계약내역 - 종료일', null=True)
    ch_users        = models.IntegerField('계약내역 - 사용자수')
    reg_date        = models.DateTimeField('등록일', default=timezone.now)
    update_date     = models.DateTimeField('수정일', default=timezone.now)


    class Meta:
        indexes = [
           models.Index(fields=['customer_id'])
        ]

        db_table = 'customer_history'

class notice(models.Model):

    type = (
        ('N', '로그인전'),
        ('Y', '로그인후')
    )

    header = (
        ('N', '미고정'),
        ('Y', '고정')
    )

    deleted = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    notice_id        = models.AutoField('공지사항ID', primary_key=True)
    notice_title     = models.CharField('공지사항제목', max_length=4)
    notice_content   = models.TextField('공지사항내용', null=True)
    notice_type      = models.CharField('공지사항 구분', max_length=2, choices=type, default='N')
    notice_header    = models.CharField('공지사항 상단고정여부', max_length=2, choices=header, default='N')
    notice_deleted   = models.CharField('삭제여부', max_length=2, choices=deleted, default='N')
    reg_date        = models.DateTimeField('등록일', default=timezone.now)
    update_date     = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        db_table = 'notice'

class member_company(models.Model):

    mc_id               = models.AutoField('사용자 회사ID', primary_key=True)
    member_id           = models.ForeignKey(member, db_column='member_id', on_delete=models.PROTECT)
    mc_name             = models.CharField('회사명', max_length=200)
    mc_department       = models.CharField('부서명', max_length=200, null=True)
    mc_ceo              = models.CharField('대표자명', max_length=100)
    mc_tel1             = models.CharField('전화번호1', max_length=4, null=True)
    mc_tel2             = models.CharField('전화번호2', max_length=4, null=True)
    mc_tel3             = models.CharField('전화번호3', max_length=4, null=True)
    mc_zipcode          = models.CharField('우편번호', max_length=7)
    mc_dodobu           = models.CharField('도도부현', max_length=2)
    mc_city             = models.CharField('도시', max_length=50)
    mc_detail_address   = models.CharField('상세주소', max_length=100)
    reg_date            = models.DateTimeField('등록일', default=timezone.now)
    update_date         = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        indexes = [
           models.Index(fields=['member_id'])
        ]

        db_table = 'member_company'

class other_party(models.Model):

    op_id           = models.AutoField('상대방 로그인ID', primary_key=True)
    op_email        = models.CharField('상대방 이메일', max_length=200)
    op_password     = models.CharField('상대방 패스워드', max_length=200)
    op_ac           = models.CharField('상대방 변경 이메일 인증키', max_length=50, null=True)
    op_email_key    = models.CharField('패스워드 변경확인키', max_length=50, null=True)
    reg_date        = models.DateTimeField('등록일', default=timezone.now)
    update_date     = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        db_table = 'other_party'

class alam(models.Model):

    read = (
        ('N', '안읽음'),
        ('Y', '읽음')
    )

    am_check = (
        ('N', '사용'),
        ('Y', '삭제')
    )

    am_type = (
        ('C', '계약서'),
        ('CM', '코멘트')
    )

    alam_id	        = models.AutoField('알람ID', primary_key=True)
    member_id       = models.ForeignKey(member, db_column='member_id', on_delete=models.PROTECT)
    contract_id     = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    alam_type       = models.CharField('알람 구분', max_length=2, choices=am_type, default='C')
    alam_title      = models.CharField('알람제목', max_length=200)
    alam_content    = models.TextField('1:알람 내용')
    alam_read       = models.CharField('알람 읽음여부', max_length=2, choices=read, default='N')
    alam_deleted    = models.CharField('알람 삭제여부', max_length=2, choices=am_check, default='N')
    reg_date        = models.DateTimeField('등록일', default=timezone.now)
    update_date     = models.DateTimeField('수정일', default=timezone.now)


    class Meta:
        indexes = [
           models.Index(fields=['member_id'])
        ]

        db_table = 'alam'

class terms(models.Model):

    terms_id            = models.AutoField('이용규약ID', primary_key=True)
    terms_content       = models.TextField('이용규약 내용')
    terms_mail_title    = models.CharField('이용규약 메일제목', max_length=255, null=True)
    terms_mail_form	    = models.TextField('이용규앾 메일폼', null=True)
    reg_date            = models.DateTimeField('등록일', default=timezone.now)
    update_date	        = models.DateTimeField('수정일', default=timezone.now)

    class Meta:
        db_table = 'terms'


class flow_member(models.Model):

    auth = (
        ('S', '담당자'),
        ('C', '승인자'),
        ('A', '확인자')
    )

    fm_id	    = models.AutoField('플로우ID', primary_key=True)
    flow_id	    = models.ForeignKey(flow, db_column='flow_id', on_delete=models.PROTECT)
    cfm_id	    = models.ForeignKey(contract_folder_member, db_column='cfm_id', on_delete=models.PROTECT)
    fm_auth     = models.CharField('플로우 참여자 권한', max_length=2, choices=auth, default='S')
    reg_date    = models.DateTimeField('등록일', default=timezone.now)
    update_date	= models.DateTimeField('수정일', default=timezone.now)

    class Meta:

        indexes = [
           models.Index(fields=['flow_id']),
           models.Index(fields=['cfm_id'])
        ]

        db_table = 'flow_member'

class eos_upload(models.Model):

    eu_id	        = models.AutoField('EOS업로드ID', primary_key=True)
    contract_id     = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    eu_ipfs_hash    = models.CharField('IFPS hash', max_length=50)
    reg_date        = models.DateTimeField('등록일', default=timezone.now)

    class Meta:

        indexes = [
           models.Index(fields=['contract_id'])
        ]

        db_table = 'eos_upload'

class eth_upload(models.Model):

    eth_id	        = models.AutoField('Ethereum 업로드ID', primary_key=True)
    contract_id     = models.ForeignKey(contract, db_column='contract_id', on_delete=models.PROTECT)
    eth_ipfs_hash   = models.CharField('IFPS hash', max_length=50)
    reg_date        = models.DateTimeField('등록일', default=timezone.now)

    class Meta:

        indexes = [
           models.Index(fields=['contract_id'])
        ]

        db_table = 'eth_upload'
