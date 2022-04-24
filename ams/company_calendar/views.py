from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from company_calendar.models import Holiday
from company_calendar.serializers import HolidaySerializer
# Create your views here.


class CreateHolidays(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):

    # permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = HolidaySerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewHolidays(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    queryset = Holiday.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = HolidaySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
