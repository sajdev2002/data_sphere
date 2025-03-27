from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('user/',views.user,name='user'),
    path('buss/',views.buss,name='buss'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('buss_register/',views.buss_register,name='buss_register'),
    path('datatable/',views.datatable,name='datatable'),
    path('datatable_buss/',views.datatable_buss,name='datatable_buss'),
    path('buss_accept/<int:id>/',views.buss_accept,name='buss_accept'),
    path('buss_reject/<int:id>/',views.buss_reject,name='buss_reject'),
    path('update_user',views.update_user,name='update_user'),
    path('update_buss',views.update_buss,name='update_buss'),
    path('add_survey',views.add_survey,name='add_survey'),
    path('survey_view',views.survey_view,name='survey_view'),
    path('survey_edit/<int:id>/',views.survey_edit,name='survey_edit'),
    path('survey_delete/<int:id>/',views.survey_delete,name='survey_delete'),
    path('admin_survey/<int:id>/',views.admin_survey,name='admin_survey'),
    path('select_bussiness/',views.select_bussiness,name='select_bussiness'),
    path('select_bussiness_user/',views.select_bussiness_user,name='select_bussiness_user'),
    path('user_survey/<int:id>/',views.user_survey,name='user_survey'),
    path('survey_complete/',views.survey_complete,name='survey_complete'),
   
]
