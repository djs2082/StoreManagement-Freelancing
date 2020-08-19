from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.exceptions import EmptyResultSet
from .models import BrandModel
from requirements import success, error
from .serializers import BrandSerializer
from django.core.exceptions import EmptyResultSet
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

class BrandView(APIView):
    permission_classes = [(IsAuthenticated)]
    def get(self, request, pk=None):
        try:
            if pk is None:
                queryset    =   BrandModel.objects.all()
                serialized  =   BrandSerializer(queryset, many=True)
                if queryset.count() is 0:
                    raise EmptyResultSet("No Brand Options")
            else:
                queryset    =   BrandModel.objects.get(pk=pk)
                serialized  =   BrandSerializer(queryset)

            response    =   success.APIResponse(200, serialized.data).respond()
            return Response(response)   

        except EmptyResultSet as empty_error:
            response    =   error.APIErrorResponse(404,str(empty_error)).respond()
            return Response(response)

        except BrandModel.DoesNotExist as not_found_error:
            response    =   error.APIErrorResponse(404, str(not_found_error)).respond()
            return Response(response)

        except Exception as unkown_exception:
            response    =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)


    
    def post(self,request):
        try:
            data        =   request.data
            serialized  =   BrandSerializer(data = data)

            if(serialized.is_valid(raise_exception = True)):
                saved = serialized.save()
            success_message =   f"Brand {saved} added Successfully"
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
            instance    =   BrandModel.objects.get(pk = pk)
            serialized  =   BrandSerializer(instance, data, partial = True)
            
            if serialized.is_valid(raise_exception = True):
                saved = serialized.save()
            
            success_message =   f"Brand {saved} updated successfully"
            response=success.APIResponse(201,success_message).respond()
            return Response(response)
        
        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
            return Response(response) 
        
        except IntegrityError as integrity_error:
            response        =   error.APIErrorResponse(409,str(integrity_error)).respond()
            return Response(response)    
        
        except BrandModel.DoesNotExist as not_found_error:
            error_message   =  f"Brand with id {pk} is Not available"
            response        =  error.APIErrorResponse(404,str(not_found_error)).respond()
            return Response(response,status=404)   
        except Exception as unkown_exception:
            response        =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)

    
    def delete(self,request,pk=None):
        try:
            if pk is None:
                BrandModel.objects.all().delete()
                success_message =   "All Brand are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
                return Response(response)
            else:
                data            =   BrandModel.objects.get(pk = pk)
                data.delete()     
                success_message =   f"Brand with id {pk} is deleted"
                response        =   success.APIResponse(202,success_message).respond()
                return Response(response)
        
        except BrandModel.DoesNotExist as not_found_error:
            response        =   error.APIErrorResponse(404,str(not_found_error)).respond()
            return Response(response)
        
        except IntegrityError as integrity_error:
            response        =   error.APIErrorResponse(409,str(integrity_error)).respond()
            return Response(response)                                      
        
        except Exception as unknown_exception:
            response        =   error.APIErrorResponse(400,str(unknown_exception)).respond()
            return Response(response,status=400)

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def get_brands(request,pk):
    try:
        queryset=BrandModel.objects.all().filter(item=pk)
        serialized=BrandSerializer(queryset,many=True)
        response = success.APIResponse(200, serialized.data).respond()
    except EmptyResultSet as empty_error:
        response = error.APIErrorResponse(404,str(empty_error)).respond()
    except ValidationError as error:
        response        = error.APIErrorResponse(409, str(error)).respond()
    except Exception as err:
        response = error.APIErrorResponse(400, err).respond()
    finally:
        return(Response(response))