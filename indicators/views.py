from rest_framework.response import Response
from rest_framework.views import APIView
from indicators.utils import build_dashboard_data

class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        data = build_dashboard_data(country_code="BRA")
        return Response(data)
