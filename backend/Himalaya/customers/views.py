from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.core.exceptions import ObjectDoesNotExist
import schedule
from rest_framework import generics
from rest_framework import filters
import time
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import time
from requirements import success,error
from .serializers import CustomerSerializer
from .models import Customer as Customer


class StandardResultsSetPagination(PageNumberPagination,APIView):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
    	try:
    		response={
    		'links': {
    		'next': self.get_next_link(),
    		'previous': self.get_previous_link()
    		},
    		'total': self.page.paginator.count,
    		'page_size': int(self.request.GET.get('page_size', self.page_size)),
    		'results': data
    		}
    		response_message=success.APIResponse(200,response).respond()
    	except Exception as e:
    		response_message=error.APIErrorResponse(404,{'error':str(e)}).respond()
    	finally:
    		return Response(response_message)

class Customer(generics.ListAPIView):
	permission_classes = [(IsAuthenticated)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)
	pagination_class=StandardResultsSetPagination
	queryset=Customer.objects.all().order_by('-pk')
	serializer_class=CustomerSerializer
	filter_backends = [filters.SearchFilter]
	search_fields  = ['fname','fname',' mobile']

	def post(self, request):
		try:
			customer_serializer=CustomerSerializer(data=request.data)
			if(customer_serializer.is_valid()):
				customer_serializer.save()
				response_message=success.APIResponse(200,{'customer_created_success':'Customer Created Successfully','data':customer_serializer.data}).respond()
			else:
				response_message=error.APIErrorResponse(404,{'error':customer_serializer.errors}).respond()
		except Exception as e:
			response_message=error.APIErrorResponse(404,{'error':str(e)}).respond()
		finally:
			return Response(response_message)

	def put(self, request):
		try:
			if('mobile' in request.data.keys()):
				try:
					customer=Customer.objects.get( mobile=request.data[' mobile'])
					if('fname' in request.data.keys()):
						customer.fname=request.data['fname']
					if('lname' in request.data.keys()):
						customer.fname=request.data['lname']
					customer.save()
					response_message=success.APIResponse(200,{'customer_updated_success':'customer_updated_success'}).respond()
				except Customer.DoesNotExist:
					response_message=error.APIErrorResponse(404,{'customer_doesnt_exist':'customer_doesnt_exist'}).respond()
			else:
				response_message=error.APIErrorResponse(404,{' mobile':' mobile is mandatory field'}).respond()
		except Exception as e:
			response_message=error.APIErrorResponse(404,{'error1':str(e)}).respond()
		finally:
			return Response(response_message)

	def delete(self, request):
		try:
			if('mobile' in request.data.keys()):
				try:
					customer=Customer.objects.get( mobile=request.data[' mobile'])
					customer.delete()
					response_message=success.APIResponse(200,{'customer_deleted_success':'Customer Deleted Successfully'}).respond()
				except Customer.DoesNotExist:
					response_message=error.APIErrorResponse(404,{'error1':'Customer Doesnt Exist'}).respond()
			else:
				response_message=error.APIErrorResponse(404,{'error2':'Provide Phone Number to delete the corresponding customer'}).respond()
		except Exception as e:
			response_message=error.APIErrorResponse(404,{'error3':str(e)}).respond()
		finally:
			return Response(response_message)
