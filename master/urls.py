from django.urls import path,re_path
# from master.views import HomeView,AdminHome,StaffHome,UserLogin,AddMedicineView,AddCategoryView,MedicineListView,AboutView,MedDetailView,logout
from master.views import*
from . import views

urlpatterns=[
path('home/',HomeView.as_view(),name='home'),
path('Panel/',AdminPanel.as_view(),name='panel'),
path('about/',AboutView.as_view(),name='about'),
path('register/', views.adduser, name='reg'),
path('admin/',AdminHome.as_view(),name='adminhome'),
path('staff/',StaffHome.as_view(),name='staffhome'),
path('login/',UserLogin.as_view(),name='userlogin'),
 path("contactus/",ContactUsView.as_view(),name='contactus'),
path('AddMedicine/',AddMedicineView.as_view(),name='AddMedicine'),
path('AddCategory/',AddCategoryView.as_view(),name='AddCategory'),
path('MedicineView/',MedicineListView.as_view(),name='view'),
re_path(r'^detail/(?P<pk>\d+)$',MedDetail.as_view(),name='MedDetail'),
path('logout',views.logout_request,name='logout'),
path('listview/',MedList.as_view(),name='ListView'),
path('addstaff/', views.adduser, name='addstaff'),
re_path(r'^edit/(?P<pk>\d+)$',MedUpdateView.as_view(),name='MedEditView'),
path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
path('pay/', PaymentView.as_view(), name='pay'),
path("password_reset/", views.password_reset_request, name="password_reset"),
re_path(r'^cart/(?P<pk>\d+)/$', AddCartView.as_view(), name='cart'),
path('user/cart/list/', ListCartView.as_view(),name="usercartlist"),
re_path(r'^cart/remove/(?P<pk>\d+)/$', CartRemoveView.as_view(), name='removeprod'),
# re_path(r'^book/remove/(?P<pk>\d+)/$', BookRemoveView.as_view(), name='removebook'),
path('order/history/', OrderHistoryView.as_view(),name="orderhistory"),
# path('orders/', OrderList.as_view(),name="orders"),
re_path(r'^remove/(?P<pk>\d+)/$', MedRemoveView.as_view(), name='removebook'),
re_path(r'^by/category/(?P<pk>\d+)/$', CategorywiseProducts.as_view(), name='category'),
# path('viewstaff/',StaffView.as_view(),name='viewstaff'),
# re_path(r'^edit/(?P<pk>\d+)$',StaffEditView.as_view(),name='staffedit'),
# re_path(r'^detail/(?P<pk>\d+)$',StaffDetailView.as_view(),name='staffdetail'),
path('FeedbackView/',FeedbackList.as_view(),name='feedback'),
path('StaffFeedbackList/',StaffFeedbackList.as_view(),name='StaffFeedback'),
path('OrderList/',OrderList.as_view(),name='OrderList'),  


]
