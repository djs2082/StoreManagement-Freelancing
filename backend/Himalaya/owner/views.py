from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from requirements import success,error


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
            token = Token.objects.get(key=response.data['token'])
            response_message=success.APIResponse(200,{'token':token.key}).respond()
        except Exception as e:
            response_message=error.APIErrorResponse(404,{'error':str(e)}).respond()
        finally:
            return Response(response_message)

