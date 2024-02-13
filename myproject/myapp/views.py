# myapp/views.py
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer


#permission never apply at project level, until necessary for whole default settings for all api's

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:

        return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user:
        # Login successful, create or retrieve a token
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



#now that i have both registered and login the user, this user have token now, since we don't want to
# re-authenticate again and again, we will just use token for this purpose.
#let's use token for the api view that can list all the users.(Only authenticated user can view users).
    

class UserDetailApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.all()
        #raise self.model.DoesNotExist myapp.models.CustomUser.DoesNotExist: CustomUser matching query does not exist.
        # because the user was Anonymous

        #Here i am doing serialization - converting my model instance query to json object
        # if done reverse, i need to pass data=user and then check .is_valid() to deserialize the data
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
