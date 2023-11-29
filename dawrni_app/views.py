from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import *
from .email import *
from .models import Company
from rest_framework import status
from django.utils.translation import gettext as _
from rest_framework import exceptions


def serialize_user(user):
    return {
        "username": user.username,
        "email": user.email,
    }


@api_view(['GET'])
def get_clients(request):
    clents = Client.objects.all()
    serializer = ClientSerializer(clents, many=True, context={'request': request})
    return Response(serializer.data)



class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password: 
        return Response({'message': _('Please provide both username and password.')})
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    s, token = AuthToken.objects.create(user)
    return Response({
        'user_data': serialize_user(user),
        'token': token
    })
        

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email :
        return Response({'message': _('Please provide your username, email, and password.')})
    
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        send_otp(serializer.data['email'])
        s, token = AuthToken.objects.create(user)
        return Response({   
            "user_info": serialize_user(user),
            "token": token
        })


@api_view(['GET'])
def get_user(request):
    try:
        user = request.user
        if user.is_authenticated:
            return Response({
                'user_data': serialize_user(user)
            })
        else:
            return Response({'message':_('this user is not authenticated')}, status=400)
    except exceptions.AuthenticationFailed as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def verify(request):
    email = request.data.get('email')
    code_name = request.data.get('code_name')

    if not email or not code_name:
        return Response({'message': _('Please provide both email and code.')})
    try:
        data = request.data
        serializer = VerifyAccountSerializer(data = data)
        if serializer.is_valid():
            email = serializer.data['email']
            code_name = serializer.data['code_name']

            user = User.objects.filter(email=email)
            if not user.exists():
                return Response({
                    'message': _('User with this email does not exist.'),
                },status=404)
            
            if user[0].first_name != code_name:
                return Response({
                    'message': _('Invalid verification code.'),
                },status=400)
            user = user.first() 
            user.save()
            return Response({
                'message': _('Verification successful.'),
                'status': 200,
            })

    except:
        return Response({
            'message': _('An error occurred.'),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   