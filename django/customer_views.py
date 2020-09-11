from django.shortcuts import render

import random
import string
from datetime import datetime, timezone

from django.contrib.auth.hashers import check_password, make_password

# Create your views here.
from django.utils import timezone
from rest_framework import views
from rest_framework.response import Response

from common.AESCipher import AESCipher
from common.exception import Code
from common.fieldType import Status, Language, DriveType
from admin.models import Admin

from user.models import Company, CompanyGroup, User
from drive.models import Drive
# Create your views here.
from rest_framework.decorators import api_view
import json

from admin.serializers import CompanySerializer
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import Count, OuterRef


class Customers(views.APIView):
	def post(self, request):

		params = request.POST

		is_desc = params.get('isDesc')
		sortField = params.get('sortField')
		searchContents = params.get('searchContents')

		if is_desc is None:
			is_desc = 'false'

		if is_desc == 'false':
			sort_field = sortField
		else:
			sort_field = '-' + sortField

		try:
			# TODO 개인드라이브, 팀드라이브 사용량 가져와야 함

			if searchContents is None:
				company = Company.objects.all().order_by(sort_field)
				# company = User.objects.values('company_id').annotate(company_cnt=Count('company_id')).order_by(
				# 	sort_field)

			else:
				company = Company.objects.all().filter(name__icontains=searchContents).order_by(sort_field)

			customer_list = CompanySerializer(company, many=True).data

		except Company.DoesNotExist:
			return Response({'code': Code.COMPANY_DOES_NOT_EXIST.value, 'message': Code.COMPANY_DOES_NOT_EXIST.name})

		return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.value, 'data': customer_list})


class Customer(views.APIView):
	def post(self, request):

		params = request.POST
		print("params", params)

		id = params['company_id']

		try:
			company = Company.objects.get(id=id)
			data = {
				'name': company.name,
				'user_limit': company.user_limit,
				'user_unlimited': company.user_unlimited,
				'data_limit': company.data_limit,
				'data_unlimited': company.data_unlimited,
				'cold_limit': company.cold_limit,
				'start_date': company.start_date,
				'end_date': company.end_date
			}

		except Company.DoesNotExist:
			return Response({'code': Code.USER_DOES_NOT_EXIST.value, 'message': Code.USER_DOES_NOT_EXIST.name})

		return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.value, 'data': data})


class CustomerRegistration(views.APIView):
	def post(self, request):

		params = request.POST

		name = params.get('name')
		user_limit = params.get('user_limit')  # 유저수
		user_unlimited = params.get('user_unlimited')  # 유저 무제한
		data_limit = params.get('data_limit')  # 개인, 팀드라이브 토탈 용량 기본단위 GB
		data_unlimited = params.get('data_unlimited')  # 개인, 팀드라이브 토탈 용량 무제한
		cold_limit = params.get('cold_limit')  # 기본단위 TB
		start_date = params.get('startDate') # 시작일
		end_date = params.get('endDate') # 종료일

		if user_unlimited == 'true':
			user_unlimited = 1  # 유저 무제한
		else:
			user_unlimited = 0  # 유저 제한information_schema

		if data_unlimited == 'true':
			data_unlimited = 1  # 개인+팀드라이브 토탈 용량 무제한
		else:
			data_unlimited = 0  # 개인+팀드라이브 토탈 제한

		if user_limit is None or user_limit == '':
			user_limit = 0

		if data_limit is None or data_limit == '':
			data_limit = 0

		# 회사명이 기존에 있을경우 중복체크 안함!
		# 회사 정보 등록
		company_save = Company(name=name, user_limit=user_limit, user_unlimited=user_unlimited,
							   data_limit=data_limit, data_unlimited=data_unlimited, cold_limit=cold_limit,
							   status_type=Status.ACTIVE, start_date=start_date, end_date=end_date)
		company_save.save()

		# 드라이브에 팀드라이브 추가
		drive_save = Drive(drive_type=DriveType.TEAM, name='TEAM_DRIVE', company_id=company_save)
		drive_save.save()

		# 회사 그룹 정보 등록
		company_group_save = CompanyGroup(company_id=company_save, name=name)
		company_group_save.save()

		return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.value})


class CustomerModification(views.APIView):
	def post(self, request):

		params = request.POST

		id = params.get('company_id')
		name = params.get('name')
		user_limit = params.get('user_limit')  # 유저수
		user_unlimited = params.get('user_unlimited')  # 유저 무제한
		data_limit = params.get('data_limit')  # 개인, 팀드라이브 토탈 용량 기본단위 GB
		data_unlimited = params.get('data_unlimited')  # 개인, 팀드라이브 토탈 용량 무제한
		cold_limit = params.get('cold_limit')  # 기본단위 TB
		start_date = params.get('startDate') # 시작일
		end_date = params.get('endDate') # 종료일

		if user_unlimited == 'true':
			user_unlimited = 1  # 유저 무제한
		else:
			user_unlimited = 0  # 유저 제한information_schema

		if data_unlimited == 'true':
			data_unlimited = 1  # 개인+팀드라이브 토탈 용량 무제한
		else:
			data_unlimited = 0  # 개인+팀드라이브 토탈 제한

		print("user_limit", user_limit)

		if user_limit is None or user_limit == 'null' or user_limit == '':
			user_limit = 0

		if data_limit is None or data_limit == 'null' or data_limit == '':
			data_limit = 0

		# 회사 정보 취득
		company_info = Company.objects.get(id=id)
		company_info.name = name
		company_info.user_limit = user_limit
		company_info.user_unlimited = user_unlimited
		company_info.data_limit = data_limit
		company_info.data_unlimited = data_unlimited
		company_info.cold_limit = cold_limit
		company_info.start_date = start_date
		company_info.end_date = end_date
		company_info.modified_date = datetime.now()
		company_info.save()

		# 회사 그룹 정보 취득
		company_group_info = CompanyGroup.objects.get(company_id=id)
		company_group_info.name = name
		company_group_info.modified_date = datetime.now()
		company_group_info.save()

		return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.value})


class CustomerDelete(views.APIView):
	def post(self, request):
		params = request.POST

		id = params.get('id')
		delte_id = id.split(",")
		# 회사 정보 삭제
		# TODO 회사정보는 완전삭제 하지 않고 status_type에 삭제중이라는 flg를 추가하고
		# 폴더 및 파일이 삭제 완료 되었을시 완전삭제 할것

		print("delte_id", delte_id)

		for item in delte_id:
			company_info = Company.objects.get(id=item)
			company_info.delete()

		return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.value})


class CustomerInactive(views.APIView):
	def post(self, request):
		params = request.POST

		print("params", params)

		id = params['id']

		# 회사 비활성화
		company_info = Company.objects.get(id=id)
		company_info.status_type = Status.INACTIVE
		company_info.modified_date = datetime.now()
		company_info.inactive_date = datetime.now()
		company_info.save()

		return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.value})


class CustomerActive(views.APIView):
	def post(self, request):
		params = request.POST

		id = params['id']
		# 회사 활성화
		company_info = Company.objects.get(id=id)
		company_info.status_type = Status.ACTIVE
		company_info.modified_date = datetime.now()
		company_info.inactive_date = None
		company_info.save()

		return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.value})


class SearchObj(views.APIView):
	def post(self, request):
		params = request.POST
		keyword = params.get("contents")
		is_desc = params.get('isDesc')

		try:
			company = Company.objects.filter(name__icontains=keyword).order_by('-created_date')

			customer_list = CompanySerializer(company, many=True).data

		except Company.DoesNotExist:
			return Response({'code': Code.COMPANY_DOES_NOT_EXIST.value, 'message': Code.COMPANY_DOES_NOT_EXIST.name})

		return Response({'code': Code.SUCCESS.value, 'message': Code.SUCCESS.value, 'data': customer_list})
