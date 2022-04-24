from rest_framework import authentication, status
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from user.models import MyUser


class ExampleAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        device_id = request.data.get("device_id")
        password = request.data.get("password")
        if not device_id and not password: # no username passed in request headers
            return None # authentication did not succeedResponse(status=status.HTTP_401_UNAUTHORIZED)
            # authentication did not succeed

        try:
            user = MyUser.objects.get(device_id=device_id) # get the user
        except MyUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user') # raise exception if user does not exist
        # print(token)
        return (user, token) # authentication successful





