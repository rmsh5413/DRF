from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from jwt.exceptions import ExpiredSignatureError, DecodeError
from .models import User
import jwt,datetime


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self,request):
        phonenumber=request.data['phonenumber']
        password=request.data['password']
        
        user=User.objects.filter(phonenumber=phonenumber).first()
        if user is None:
            raise AuthenticationFailed ('User is not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')
        
        payload={'id':user.id,
                 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5),
                 'iat':datetime.datetime.utcnow()
                 }
        # token=jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response= Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={'jwt':token}
        return response
    


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            # Specify the allowed algorithm (HS256) when decoding the token
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        except DecodeError:
            raise AuthenticationFailed('Invalid token')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)



    
class LogoutView(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie("jwt")
        response.data={
            'message':'success'
        }
        return response
    