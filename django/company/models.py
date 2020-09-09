from django.db import models


# Create your models here.

class Company(models.Model):
  cp_id = models.AutoField('회사정보 ID', primary_key=True)
  cp_name = models.CharField('회사, 단체명', max_length=200)
  cp_present = models.CharField('대표자 성명', max_length=100)
  cp_tel = models.CharField('전화번호 전체', max_length=3)
  cp_tel1 = models.CharField('전화번호1', max_length=3)
  cp_tel2 = models.CharField('전화번호2', max_length=4)
  cp_tel3 = models.CharField('전화번호3', max_length=4)
  cp_fax = models.CharField('팩스', max_length=45)
  cp_post_code = models.CharField('우편번호', max_length=8)
  cp_county = models.IntegerField('도도부 현')
  cp_city = models.CharField('도시', max_length=100)
  cp_addr = models.CharField('주소', max_length=200)
  cp_iduser = models.IntegerField('사용자 ID')
  cp_manager_firstname = models.CharField('관리자 이름 성', max_length=100)
  cp_manager_lastname = models.CharField('관리자 이름', max_length=100)
  cp_manager_email = models.CharField('관리자 이메일', max_length=100)
  cp_manager_tel1 = models.CharField('관리자 전화번호1', max_length=4)
  cp_manager_tel2 = models.CharField('관리자 전화번호2', max_length=3)
  cp_manager_tel3 = models.CharField('관리자 전화번호3', max_length=3)
  cp_memo = models.TextField('메모')
  cp_num = models.CharField('계약자 수', max_length=100)
  cp_stamppath = models.CharField('스탬프 경로', max_length=200)
  cp_stampname = models.CharField('스탬프 이름', max_length=100)
  cp_signpath = models.CharField('사인 경로', max_length=200)
  cp_signname = models.CharField('사인 이름', max_length=100)
  cp_sdate = models.DateTimeField('계약 개시일')
  cp_edate = models.DateTimeField('계약 종료일')
  cp_regdate = models.DateTimeField('등록일')
  cp_updated = models.DateTimeField('수정일')

  class Meta:
    managed = False
    db_table = 'company'


class UserCompany(models.Model):
  uc_id = models.AutoField('회사정보 ID', primary_key=True)
  cp_id = models.IntegerField('compnay_id')
  cp_name = models.CharField('회사명', max_length=200)
  cp_present = models.CharField('대표자 성명', max_length=100)
  # cp_fax = models.CharField('팩스', max_length=45)
  cp_tel1 = models.CharField('전화번호1', max_length=3)
  cp_tel2 = models.CharField('전화번호2', max_length=4)
  cp_tel3 = models.CharField('전화번호3', max_length=4)
  cp_post_code = models.CharField('우편번호', max_length=8)
  cp_county = models.IntegerField('도도부 현')
  cp_city = models.CharField('도시', max_length=100)
  cp_addr = models.CharField('주소', max_length=200)
  cp_department = models.CharField('부서명', max_length=100)
  cp_iduser = models.IntegerField('사용자 ID')
  cp_regdate = models.DateTimeField('등록일')
  cp_updated = models.DateTimeField('수정일')

  class Meta:
    managed = False
    db_table = 'user_company'
