from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.db import IntegrityError
from .models import ItemModel
from requirements import success, error
from .serializers import ItemSerializer
from django.core.exceptions import EmptyResultSet
from brands.models import BrandModel
from brands.serializers import BrandSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
import json

class ItemView(APIView):
    permission_classes = [(IsAuthenticated)]

    def get(self, request, pk=None):
        try:
            if pk is None:
                queryset    =   ItemModel.objects.all()
                serialized  =   ItemSerializer(queryset, many=True)
                if queryset.count() is 0:
                    raise EmptyResultSet("No Item Options")
            else:
                queryset    =   ItemModel.objects.get(pk=pk)
                serialized  =   ItemSerializer(queryset)

            response    =   success.APIResponse(200, serialized.data).respond()
            return Response(response)   

        except EmptyResultSet as empty_error:
            response    =   error.APIErrorResponse(404,str(empty_error)).respond()
            return Response(response)

        except ItemModel.DoesNotExist as not_found_error:
            response    =   error.APIErrorResponse(404, str(not_found_error)).respond()
            return Response(response)

        except Exception as unkown_exception:
            response    =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)


    
    def post(self,request):
        try:
            data        =   request.data
            serialized  =   ItemSerializer(data = data)

            if(serialized.is_valid(raise_exception = True)):
                saved = serialized.save()
            success_message =   f"Item {saved} added Successfully"
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
            instance    =   ItemModel.objects.get(pk = pk)
            serialized  =   ItemSerializer(instance, data, partial = True)
            
            if serialized.is_valid(raise_exception = True):
                saved = serialized.save()
            
            success_message =   f"Item {saved} updated successfully"
            response=success.APIResponse(201,success_message).respond()
            return Response(response)
        
        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
            return Response(response) 
        
        except IntegrityError as integrity_error:
            response        =   error.APIErrorResponse(409,str(integrity_error)).respond()
            return Response(response)    
        
        except ItemModel.DoesNotExist as not_found_error:
            error_message   =  f"Item with id {pk} is Not available"
            response        =  error.APIErrorResponse(404,str(not_found_error)).respond()
            return Response(response,status=404)   
        except Exception as unkown_exception:
            response        =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)

    
    def delete(self,request,pk=None):
        try:
            if pk is None:
                ItemModel.objects.all().delete()
                success_message =   "All Item are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
                return Response(response)
            else:
                data            =   ItemModel.objects.get(pk = pk)
                data.delete()     
                success_message =   f"Item with id {pk} is deleted"
                response        =   success.APIResponse(202,success_message).respond()
                return Response(response)
        
        except ItemModel.DoesNotExist as not_found_error:
            response        =   error.APIErrorResponse(404,str(not_found_error)).respond()
            return Response(response)
        
        except IntegrityError as integrity_error:
            response        =   error.APIErrorResponse(409,str(integrity_error)).respond()
            return Response(response)                                      
        
        except Exception as unknown_exception:
            response        =   error.APIErrorResponse(400,str(unknown_exception)).respond()
            return Response(response,status=400)

@permission_classes([IsAuthenticated])
@api_view(['GET',])
def get_items_and_brands(request):
    try:
        data=[]
        queryset=ItemModel.objects.values()
        serialized=ItemSerializer(queryset,many=True)
        for item in serialized.data:
            item=(dict(item))
            queryset=BrandModel.objects.all().filter(item=item['id'])
            serialized=BrandSerializer(queryset,many=True)
            item['brands']=serialized.data
            data.append(item)
        if len(data) is 0:
            raise EmptyResultSet
        response = success.APIResponse(200, data).respond()
    except EmptyResultSet as empty_error:
        response = error.APIErrorResponse(404,str(empty_error)).respond()
    except Exception as err:
        response    =   error.APIErrorResponse(400, err).respond()
    finally:
        return(Response(response))