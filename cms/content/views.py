from django.db.models import Q
from .models import contents
from .serializers import ContentSerializer,AllContentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user_auth.jwt import userJWTAuthentication
import datetime


class ContentViewSet(viewsets.ModelViewSet):
    serializer_class = ContentSerializer
    queryset = contents.objects.all()
    authentication_classes = [userJWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role.name == 'author':
            self.queryset = self.queryset.filter(user=user.id)
        self.serializer_class = AllContentSerializer
        return super().list(request, *args, **kwargs)
    
    
    def retrive(self, request, *args, **kwargs):
        request_data = request.data
        user = request.user
        if user.role.name == 'author':
            self.queryset = self.queryset.filter(user=user.id)
        self.queryset = self.queryset.filter(Q(title__contains=request_data.get('search_term'))|Q(body__contains=request_data.get('search_term'))|Q(summary__contains=request_data.get('search_term'))|Q(categories__contains=request_data.get('search_term')))
        return super().list(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        user = request.user
        request_data['user'] = user.id
        request_data['created_by'] = user.id
        serializer_obj = self.serializer_class(data=request_data)
        if serializer_obj.is_valid():       
            serializer_obj.save()
            return Response(status=200,data={'status':'SUCCESS','data':serializer_obj.data})
        return Response(status=400,data={'status':'Failed','data':serializer_obj.errors})
    
    
    def put(self, request, *args, **kwargs):
        request_data = request.data
        user = request.user
        request_data['updated_by'] = user.id
        request_data['updated_at'] = datetime.datetime.now()
        content_obj = self.queryset.filter(id=request_data.get('id','')).first()
        if user.role.name == 'author':
            if content_obj.user !=user.id:
                return Response(status=200,data={'status':'SUCCESS','data':'author does not have permission to update'})
        serializer_obj = self.serializer_class(content_obj,data=request_data)
        if serializer_obj.is_valid():       
            serializer_obj.save()
            return Response(status=200,data={'status':'SUCCESS','data':serializer_obj.data})
        return Response(status=400,data={'status':'Failed','data':serializer_obj.errors})
    
    
    def delete(self, request, *args, **kwargs):
        request_data = request.data
        user = request.user
        content_obj = self.queryset.filter(id=request_data.get('id','')).first()
        if content_obj and user.role.name == 'author':
            if content_obj.user !=user.id:
                return Response(status=200,data={'status':'SUCCESS','data':'author does not have permission to delete'})
        content_obj.delete()
        return Response(status=200,data={'status':'SUCCESS','data':'content sucessfully deleted'})
            