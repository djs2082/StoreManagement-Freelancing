from django.shortcuts import render
from .models import Receipts,Sales
import datetime
from brands.models import BrandModel
from payment.models import PaymentModel
from customers.models import Customer
from requirements import success,error
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from io import BytesIO
from django.core.files import File
from .utils import render_to_pdf
from rest_framework.pagination import PageNumberPagination
from .serializers import ReceiptsSerializer,ReceiptsSerializerForSales
from rest_framework.views import APIView
from rest_framework import filters
from django.db.models import Count,Sum
from twilio.rest import Client
from django.conf import settings
import datetime


class StandardResultsSetPagination(PageNumberPagination,APIView):
    page_size = Receipts.objects.all().count()
    page_size_query_param = 'page_size'

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
    		print(response_message);
    	except Exception as e:
    		response_message=error.APIErrorResponse(404,{'error':str(e)}).respond()
    	finally:
    		return Response(response_message)

class Receipt(generics.ListAPIView):
	permission_classes = [(IsAuthenticated)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)
	pagination_class=StandardResultsSetPagination
	date=datetime.datetime.today()
	year=date.year
	month=date.month
	day=date.day
	queryset=Receipts.objects.filter(date_time__gte=datetime.date(year,month,day),date_time__lte=datetime.date(year,month,day+1)).order_by('-id')
	serializer_class=ReceiptsSerializer
	filter_backends = [filters.SearchFilter]
	search_fields  = ['customer__fname','customer__lname','customer__mobile']

	def post(self, request):
		try:
			customer=None
			receipt=None
			total_amount=0.0
			print(request.data)
			if(len(request.data['fname'])>0 and len(request.data['lname'])>0 and len(request.data['mobile'])==10 and request.data['mobile'].isdigit()):
				try:
					customer=Customer.objects.get(mobile=request.data['mobile'])
					customer.fname=request.data['fname']
					customer.lname=request.data['lname']
					customer.save()
				except Customer.DoesNotExist:
					customer=Customer.objects.create(
						mobile=request.data['mobile'],
						fname=request.data['fname'],
						lname=request.data['lname'],
						birth_day=request.data['birth_day']
						)
					customer.save()
				finally:
					receipt=Receipts.objects.create(
						customer=customer,
						payment_method=PaymentModel.objects.get(id=int(request.data['payment_method'])),
						total_discount=float(request.data['total_discount']),
						total_amount=float(request.data['total_amount']),
						amount_payable=float(request.data['amount_payable']),
						date_time=datetime.datetime.now()
						)
					receipt.save()
					out_of_stock_messages=[]
					proceed=True
					for i in request.data['items']:
						brand=BrandModel.objects.get(id=int(i['brand']))
						if int(brand.quantity)<int(i['quantity']):
							proceed=True
							out_of_stock_messages.append('Only '+str(brand.quantity)+" "+brand.item.name+" of the Brand "+brand.name+" are left in Your Stock")
					if(proceed):
						for i in request.data['items']:
							brand=BrandModel.objects.get(id=int(i['brand']))
							if(int(brand.quantity)>0 and int(brand.quantity)-int(i['quantity'])>0):
								brand.quantity-=int(i['quantity'])
								brand.save()
							sales=Sales.objects.create(
								receipt=receipt,
								brand=brand,
								quantity=int(i['quantity']),
								size=i['size'],
								selling_price=float(i['selling_price'])
								)
							sales.save()
						context = {'receipt':receipt,'sales_list':Sales.objects.filter(receipt=receipt)}
						pdf = render_to_pdf('invoice.html',context)
						filename = receipt.customer.fname + "_" + receipt.customer.lname + "_"+ str(receipt.date_time.date())+"_"+str(receipt.date_time.time())+".pdf"

						receipt.receipt_pdf.save(filename, File(BytesIO(pdf.content)))
						receipt.save()
						response_message=success.APIResponse(200,{'success':True,'receipt_link':receipt.receipt_pdf.url}).respond()
					else:
						response_message=error.APIErrorResponse(404,{'success':False,'out_of_stock_messages':out_of_stock_messages}).respond()
			else:
				response_message=error.APIErrorResponse(404,{'invalid_customer_credentials':'Invalid Customer Credentials'}).respond()
		except Exception as e:
			response_message=error.APIErrorResponse(404,{'error3':str(e)}).respond()
		finally:
			print(response_message)
			return Response(response_message)

class SalesForGraph(generics.ListAPIView):
	permission_classes = [(IsAuthenticated)]

	def get(self,request):
		try:
			success_message={}
			total_amount_paid=0.0
			print(Receipts.objects.all().values('date_time__date').order_by('-date_time__date').annotate(total_amount_collected=Sum('amount_payable')))
			date_wise_payment_list=[{'date':str(i['date_time__date']).split('-')[2]+"-"+str(i['date_time__date']).split('-')[1]+"-"+str(i['date_time__date']).split('-')[0],'amount':i['total_amount_collected']} for i in Receipts.objects.all().values('date_time__date').order_by('-date_time__date').annotate(total_amount_collected=Sum('amount_payable'))[:30]]
			success_message.update({'date_wise_payment_list':date_wise_payment_list})
			response=success.APIResponse(200,success_message).respond()
		except Exception as unknown_exception:
			response=error.APIErrorResponse(404,str(unknown_exception)).respond()
		finally:
			return Response(response)