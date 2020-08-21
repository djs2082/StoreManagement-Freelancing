from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.db import IntegrityError
from .models import PaymentModel
from requirements import success, error
from .serializers import PaymentSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import EmptyResultSet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import datetime
from django.db.models import Count,Sum
from receipts.models import Receipts
from receipts.serializers import ReceiptsSerializer
from rest_framework import filters

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
        except Exception as e:
            response_message=error.APIErrorResponse(404,{'error':str(e)}).respond()
        finally:
            return Response(response_message)

class PaymentView(APIView):
    permission_classes = [(IsAuthenticated)]

    def get(self, request, pk=None):
        try:
            if pk is None:
                queryset    =   PaymentModel.objects.all()
                serialized  =   PaymentSerializer(queryset, many=True)
                if queryset.count() is 0:
                    raise EmptyResultSet("No Payment Options")
            else:
                queryset    =   PaymentModel.objects.get(pk=pk)
                serialized  =   PaymentSerializer(queryset)

            response    =   success.APIResponse(200, serialized.data).respond()
            return Response(response)   

        except EmptyResultSet as empty_error:
            response    =   error.APIErrorResponse(404,str(empty_error)).respond()
            return Response(response)

        except PaymentModel.DoesNotExist as not_found_error:
            response    =   error.APIErrorResponse(404, str(not_found_error)).respond()
            return Response(response)

        except Exception as unkown_exception:
            response    =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)


    
    def post(self,request):
        try:
            data        =   request.data
            serialized  =   PaymentSerializer(data = data)

            if(serialized.is_valid(raise_exception = True)):
                saved = serialized.save()
            success_message =   f"Payment {saved} added Successfully"
            response        =   success.APIResponse(201,success_message).respond()
            return Response(response)

        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
            return Response(response)

        except IntegrityError as integrity_error:
            response        =   error.APIErrorResponse(409,str(integrity_error)).respond()
            return Response(response)

        except Exception as unkown_exception:
            response        =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)


    
    def put(self,request,pk):
        try:
            data        =   request.data
            instance    =   PaymentModel.objects.get(pk = pk)
            serialized  =   PaymentSerializer(instance, data, partial = True)
            
            if serialized.is_valid(raise_exception = True):
                saved = serialized.save()
            
            success_message =   f"Payment {saved} updated successfully"
            response=success.APIResponse(201,success_message).respond()
            return Response(response)
        
        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
            return Response(response) 
        
        except IntegrityError as integrity_error:
            response        =   error.APIErrorResponse(409,str(integrity_error)).respond()
            return Response(response)    
        
        except PaymentModel.DoesNotExist as not_found_error:
            error_message   =  f"Payment with id {pk} is Not available"
            response        =  error.APIErrorResponse(404,str(not_found_error)).respond()
            return Response(response,status=404)   
        except Exception as unkown_exception:
            response        =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)

    
    def delete(self,request,pk=None):
        try:
            if pk is None:
                PaymentModel.objects.all().delete()
                success_message =   "All Payment are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
                return Response(response)
            else:
                data            =   PaymentModel.objects.get(pk = pk)
                data.delete()     
                success_message =   f"Payment with id {pk} is deleted"
                response        =   success.APIResponse(202,success_message).respond()
                return Response(response)
        
        except PaymentModel.DoesNotExist as not_found_error:
            response        =   error.APIErrorResponse(404,str(not_found_error)).respond()
            return Response(response)
        
        except IntegrityError as integrity_error:
            error_message   =   "Integrity Error Occurred"
            response        =   error.APIErrorResponse(409,str(integrity_error)).respond()
            return Response(response)                                      
        
        except Exception as unknown_exception:
            response        =   error.APIErrorResponse(400,str(unknown_exception)).respond()
            return Response(response,status=400)

class PaymentMethods(generics.ListAPIView):
    permission_classes = [(IsAuthenticated)]
    parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)
    filter_backends = [filters.SearchFilter]

    def get(self,request):
        try:
            success_message={}
            total_amount_paid_today=0.0
            amount_wise_payment_list=[]
            date=datetime.datetime.today()
            year=date.year
            month=date.month
            day=date.day
            for i in Receipts.objects.values('payment_method__name').order_by('payment_method__name').annotate(total_price=Sum('total_amount')).filter(date_time__gte=datetime.date(year,month,day),date_time__lte=datetime.date(year,month,day+1)):
                print(i)
                amount_wise_payment_list.append({"name":i['payment_method__name'],"amount":i['total_price']})
                total_amount_paid_today+=i['total_price']
            success_message.update({'amount_wise_payment_list':amount_wise_payment_list,'total_amount_paid_today':total_amount_paid_today})
            response=success.APIResponse(200,success_message).respond()
        except Exception as unknown_exception:
            response=error.APIErrorResponse(404,str(unknown_exception)).respond()
        finally:
            return Response(response)
