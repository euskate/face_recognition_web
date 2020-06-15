from django.urls import re_path, path 
from . import views

app_name = "users"


urlpatterns = [
   	# Login, Register, Forgot password, Logout
    re_path(r'^login/$', views.LoginView.as_view(), name="login_url"),
    re_path(r'^register/$', views.RegisterView.as_view(), name="register_url"),
    re_path(r'^forgot-password/$', views.ForgotPasswordView.as_view(), name="forgot_password_url"),
    re_path(r'^logout/$', views.LogoutView.as_view(), name="logout_url"),

    re_path(r'^charts/$', views.ChartsView.as_view(), name="charts_url"),

    re_path(r'^tables/$', views.TablesView.as_view(), name="tables_url"),

    re_path(r'^buttons/$', views.ButtonsView.as_view(), name="buttons_url"),

    re_path(r'^cards/$', views.CardsView.as_view(), name="cards_url"),

	re_path(r'^page_not_found/$', views.PageNotFoundView.as_view(), name="page_not_found_url"),    

	re_path(r'^blank/$', views.BlankView.as_view(), name="blank_page_url"),    
	
    # 얼굴인식 서비스
    re_path(r'^service/$', views.ServiceView.as_view(), name="service_page_url"),    
    # 고객 데이터 테이블
    re_path(r'^customers/$', views.CustomersView.as_view(), name="customers_page_url"),    
    # 메뉴 데이터 테이블
    re_path(r'^menus/$', views.MenusView.as_view(), name="menus_page_url"),    
    # 판매 데이터 테이블
    re_path(r'^sales/$', views.SalesView.as_view(), name="sales_page_url"),    
    # 월별 차트 데이터 테이블
    re_path(r'^month_chart/$', views.Month_chartView.as_view(), name="month_chart_page_url"),    
    # 월별 차트 데이터 테이블
    re_path(r'^revenue_chart/$', views.Revenue_chartView.as_view(), name="revenue_chart_page_url"),    

	# Utilities
	re_path(r'^colors/$', views.ColorsView.as_view(), name="colors_url"),    

	re_path(r'^borders/$', views.BordersView.as_view(), name="borders_url"),    

	re_path(r'^animations/$', views.AnimationsView.as_view(), name="animations_url"),    

	re_path(r'^others/$', views.OthersView.as_view(), name="others_url"),    

]