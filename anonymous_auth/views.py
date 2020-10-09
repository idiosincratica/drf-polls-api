from rest_framework.response import Response
from rest_framework.views import APIView
from anonymous_auth.models import User


class ObtainAnonymousToken(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.create()
        return Response({'token': user.key})
