from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status

from rest_framework.response import Response
from leave.serializers import StaffLeaveSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from leave.models import StaffLeave

from user.models import MyUser

from user import permissions


class UserLeave(viewsets.ViewSet):

    permission_classes = [IsAuthenticated, ]

    def create(self, request):

        serializer = StaffLeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewLeave(viewsets.ViewSet):

    permission_classes = [IsAuthenticated, IsAdminUser ]

    def list(self, request):
        queryset = StaffLeave.objects.all()
        serializer = StaffLeaveSerializer(queryset, many=True)
        return Response(serializer.data)