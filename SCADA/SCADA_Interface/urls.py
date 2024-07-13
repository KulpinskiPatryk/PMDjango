from django.urls import path
from . import views

app_name = 'SCADA_Interface'

urlpatterns = [
    path("", views.index, name="index"),
    path("MainPage/", views.MainPage, name="MainPage"),
    path("Logout/", views.Logout, name="Logout"),
    path("UsersManage/", views.UsersManage, name="UsersManage"),
    path("Machine_Readings/<id_machine>/", views.Machine_Readings, name="Machine_Readings"),
    path('edit/<int:pk>/', views.edit_machine_line.as_view(), name="edit_machine_line"),
    path('edit_user/<int:pk>/', views.edit_user_data.as_view(), name="edit_user_data"),
    path("Register/", views.RegisterUser, name="RegisterUser"),
    path('add_machine/', views.add_machine.as_view(), name="add_machine"),
]
