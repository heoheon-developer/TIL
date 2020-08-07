# -*- coding: UTF-8 -*-
import logging
from django import template
from datetime import datetime

from bhsn.models import *

register = template.Library()


# TODO:FIXME 동작확인
@register.filter
def empty(args):
    if (args is not None):
        str_return = args
    else:
        str_return = ''

    return str_return


# 작성일자 편집 TODO
@register.filter
def date_to_format(date, mode):
    # {{ counsel|date_to_format:""}}

    date_format = "%Y-%m-%d"

    if mode == "answer":
        mode = "답변"

    # 오늘날짜
    now = datetime.today().strftime(date_format)
    now_date = datetime.strptime(now, date_format).date()

    reg_date = datetime.strptime(datetime.strftime(date.register_date, date_format), date_format).date()
    delta = now_date - reg_date

    rtn_date = "작성됨"

    if delta.days == 0:
        rtn_date = "오늘" + mode + "작성됨"
    elif delta.days in range(1, 30):
        rtn_date = str(delta.days) + "일 전" + mode + " 작성됨"



    return rtn_date


# TODO:FIXME 삭제
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


# 상담사례 진행사항
@register.filter
def get_status(value):
    # object를 받아서 status를 확인후 문자열 상태를 반환
    status = value.counsel_status

    # 템플릿에서의 사용법
    # {{ counsel|get_status }}

    if status == "W":
        status = '대기'
    elif status == "P":
        status = '진행중'
    elif status == "C":
        status = '답변완료'

    return status


# 검색 파라미터 설정
@register.filter
def get_data(cg, sub_keyword):
    url_str = "category=" + str(cg) + "&sub_keyword=" + sub_keyword

    return url_str


# 카테고리 설정
@register.filter
def get_category(value):
    # object를 받아서 해당하는 서브카테고리의 인덱스를 비교후 서브카테코리 문자를 반환함

    category_sub_idx = value.category_sub_idx

    try:
        if category_sub_idx is not None:
            categoryDetail = CategoryDetail.objects.get(category_sub_idx=category_sub_idx)
            categorySubName = categoryDetail.category_sub_name
    except categoryDetail.DoesNotExist:
        categorySubName = ' '
    return categorySubName
