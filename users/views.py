from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from face.models import Customers, Menus, Sales
import psycopg2
conn_string = "host='192.168.0.59' dbname ='face_db' user='user' password='password'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/login.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class RegisterView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/register.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ForgotPasswordView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/forgot-password.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/forgot-password.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ChartsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/charts.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class TablesView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/tables.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/forgot-password.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ButtonsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/buttons.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class CardsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/cards.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class PageNotFoundView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/404.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})

# 서비스 페이지
class ServiceView(APIView):
    def get(self, request, *args, **kwargs):
        obj = Menus.objects.all()
        context = {'menuData':obj}
        return render(request, "theme/service.html", context)

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})

# 고객 테이블 페이지
class CustomersView(APIView):
    def get(self, request, *args, **kwargs):
        obj = Customers.objects.all()
        context = {'customerData':obj}
        return render(request, "theme/customers.html", context)
    def post(self, request, *args, **kwargs):

        return Response({'status': 200})

# 메뉴 테이블 페이지
class MenusView(APIView):
    def get(self, request, *args, **kwargs):
        obj = Menus.objects.all()
        context = {'menuData':obj}
        return render(request, "theme/menus.html", context)
    def post(self, request, *args, **kwargs):

        return Response({'status': 200})

# 메뉴 테이블 페이지
class SalesView(APIView):
    def get(self, request, *args, **kwargs):
        obj = Sales.objects.all()
        context = {'saleData':obj}
        return render(request, "theme/sales.html", context)
    def post(self, request, *args, **kwargs):

        return Response({'status': 200})

# 차트 테이블 페이지
class Month_chartView(APIView):
    def get(self, request, *args, **kwargs):
        sql = """
        SELECT *
        FROM month_sum
        """
        cur.execute(sql)
        result = cur.fetchall()
        monthData = [ i[0] for i in result ]
        sumData = [ i[1] for i in result ]
        print(result)
        print(monthData)
        print(sumData)
        context = {'monthData':monthData, 'sumData':sumData}
        return render(request, "theme/month_chart.html", context)
    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class Revenue_chartView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/revenue_chart.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class BlankView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/blank.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ColorsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-color.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class BordersView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-border.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class AnimationsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-animation.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class OthersView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-other.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})



class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "users/dashboard.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})
