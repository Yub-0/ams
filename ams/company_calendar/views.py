from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import mixins, viewsets, status, generics
from rest_framework.response import Response
from company_calendar.models import Holiday
from company_calendar.serializers import HolidaySerializer
# Create your views here.


class CreateHolidays(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


