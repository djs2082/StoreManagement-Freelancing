from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.db import IntegrityError
from .models import SizeModel
from requirements import success, error
from .serializers import SizeSerializer
from django.core.exceptions import EmptyResultSet
from brands.models import BrandModel
from brands.serializers import BrandSerializer
from rest_framework.decorators import api_view
import json

class SizeView(APIView):

    def get(self, request):
        # try:
            queryset    =   SizeModel.objects.all()
            serialized  =   SizeSerializer(queryset,many=True)
            response    =   success.APIResponse(200, serialized.data).respond()
            return Response(response)   

        # except EmptyResultSet as empty_error:
        #     response    =   error.APIErrorResponse(404,str(empty_error)).respond()
        #     return Response(response)

        # except SizeModel.DoesNotExist as not_found_error:
        #     response    =   error.APIErrorResponse(404, str(not_found_error)).respond()
        #     return Response(response)

        # except Exception as unkown_exception:
        #     response    =   error.APIErrorResponse(400,str(unkown_exception)).respond()
        #     return Response(response)


    
    def post(self,request):
        try:
            data        =   request.data
            serialized  =   SizeSerializer(data = data)

            if(serialized.is_valid(raise_exception = True)):
                saved = serialized.save()
            success_message =   f"Size {saved} added Successfully"
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
            instance    =   SizeModel.objects.get(pk = pk)
            serialized  =   SizeSerializer(instance, data, partial = True)
            
            if serialized.is_valid(raise_exception = True):
                saved = serialized.save()
            
            success_message =   f"Size {saved} updated successfully"
            response=success.APIResponse(201,success_message).respond()
            return Response(response)
        
        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
            return Response(response) 
        
        except IntegrityError as integrity_error:
            response        =   error.APIErrorResponse(409,str(integrity_error)).respond()
            return Response(response)    
        
        except SizeModel.DoesNotExist as not_found_error:
            error_message   =  f"Size with id {pk} is Not available"
            response        =  error.APIErrorResponse(404,str(not_found_error)).respond()
            return Response(response,status=404)   
        except Exception as unkown_exception:
            response        =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)

    
    def delete(self,request,pk=None):
        try:
            if pk is None:
                SizeModel.objects.all().delete()
                success_message =   "All Size are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
                return Response(response)
            else:
                data            =   SizeModel.objects.get(pk = pk)
                data.delete()     
                success_message =   f"Size with id {pk} is deleted"
                response        =   success.APIResponse(202,success_message).respond()
                return Response(response)
        
        except SizeModel.DoesNotExist as not_found_error:
            response        =   error.APIErrorResponse(404,str(not_found_error)).respond()
            return Response(response)
        
        except IntegrityError as integrity_error:
            response        =   error.APIErrorResponse(409,str(integrity_error)).respond()
            return Response(response)                                      
        
        except Exception as unknown_exception:
            response        =   error.APIErrorResponse(400,str(unknown_exception)).respond()
            return Response(response,status=400)