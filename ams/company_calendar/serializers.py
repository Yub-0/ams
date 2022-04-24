from rest_framework import serializers

from company_calendar.models import Holiday


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['id', 'start_date', 'end_date', 'description']