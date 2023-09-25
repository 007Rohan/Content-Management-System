from .models import get_password_regex, role,rootUser,userToken
from .serializers import RoleSerializer,UserSerializer,LoginSerializer,AllUserSerializer
from rest_framework.response import Response
from rest_framework import viewsets,generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
    



class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = role.objects.all()
    permission_classes = [AllowAny]
    
    def list(self,request,*args, **kwargs):
        return super().list(request,*args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        request_data = request.data
        role_obj = self.queryset.filter(name = request_data.get('name')).first()
        if role_obj:
            return Response(status=400,data={'status':'FAILED','data':'this role already exits'})
        else:
            serializer_obj = self.serializer_class(data=request_data)
            if serializer_obj.is_valid():       
                serializer_obj.save()
                return Response(status=200,data={'status':'SUCCESS','data':serializer_obj.data})
            return Response(status=400,data={'status':'Failed','data':serializer_obj.errors})


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = rootUser.objects.all()
    permission_classes = [AllowAny]
    
    def list(self,request,*args, **kwargs):
        self.serializer_class = AllUserSerializer
        return super().list(request,*args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        request_data = request.data
        user_obj = self.queryset.filter(email = request_data.get('email'),phone = request_data.get('phone')).first()
        if user_obj:
            return Response(status=400,data={'status':'FAILED','data':'user with this email or phone already exits'})
        else:
            if len(request_data.get('full_name').split(' ')) > 2:
                return Response(status=400,data={'status':'FAILED','data':'Please enter a valid name(two words only)'})
            verify_password = get_password_regex(request_data.get('password'))
            if verify_password is False:
                return Response(status=400,data={'status':'Failed','data':'password must contain one uppercase one lowercase and lenght should be min 8'})
            serializer_obj = self.serializer_class(data=request_data)
            if serializer_obj.is_valid():       
                serializer_obj.save()
                return Response(status=200,data={'status':'SUCCESS','data':serializer_obj.data})
            return Response(status=400,data={'status':'Failed','data':serializer_obj.errors})
            


class LoginAPIView(generics.GenericAPIView):
    authentication_classes = []

    serializer_class = LoginSerializer

    def post(self, request):
        request_data = request.data
        email = request_data.get('email', None)
        input_pw = request_data.get('password', None)
        user = rootUser.objects.filter(email = email).first()
        if user:
            usercheck = rootUser.objects.filter(email=email).values('password')
            for c in usercheck:
                saved_pw = c['password']
            userpassword = check_password(input_pw,saved_pw)
            if userpassword is True:
                userTok = userToken.objects.create(authToken = user.token,user=user.id)
                userTok.save()
                userSerializer = self.serializer_class(user)
                return Response(userSerializer.data, status=200)
        return Response({"message":"Invalid credentials, try again"}, status=401)
