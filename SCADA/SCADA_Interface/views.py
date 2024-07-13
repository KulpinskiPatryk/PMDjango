import json
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, DeleteView, CreateView
from django import forms
from plotly.offline import plot
from plotly.graph_objs import Scatter
from django.contrib.auth import get_user_model
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
pd.options.plotting.backend = "plotly"

def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/MainPage/")

    return render(request, "index.html", )


def Logout(request):
    logout(request)
    return redirect("/")


def MainPage(request):
    access = check_user(request)
    machines = MachineLine.objects.all()
    return render(request, "main_page.html", {'machines': machines, 'access': access})


class add_machine(CreateView):
    model = MachineLine
    template_name = 'add_machine.html'
    fields = ['machine_name', 'machine_location', 'machine_warehouse', 'machine_ip_address', 'machine_rack',
              'machine_slot']
    success_url = "/MainPage/"


def Machine_Readings(request, id_machine):
    access = check_user(request)
    machine = MachineLine.objects.filter(id=id_machine)
    machine_ip = MachineLine.objects.filter(id=id_machine).values('machine_ip_address')
    machine_ip = list(machine_ip)
    machine_ip = machine_ip[0]
    machine_ip = machine_ip['machine_ip_address']
    print(machine_ip)
    plot_div = MakePlot(machine_ip)
    return render(request, "machines_readings.html", {'plot_div': plot_div.to_html(full_html=False), 'machine': machine, 'access': access })


def MakePlot(name):
    df = pd.read_excel(name)
    #df = df[df.LocalTimeCol > '2024-03-14 10:00:00']
    col_names = list(df.columns)
    fig = go.Figure()
    for i in range(len(col_names)-1):
        df1 = df[[col_names[0]]]
        df1 = df1.squeeze()
        df2 = df[[col_names[i+1]]]
        df2 = df2.squeeze()
        fig.add_trace(go.Scatter(x=df1, y=df2, mode="lines", name=col_names[i+1]))
    return fig


class edit_machine_line(UpdateView):
    model = MachineLine
    template_name = 'edit_machine_line.html'
    fields = ['machine_name', 'machine_location', 'machine_warehouse', 'machine_ip_address', 'machine_rack',
              'machine_slot']
    success_url = "/MainPage/"


def UsersManage(request):
    access = check_user(request)
    if check_user(request) == 3:
        users = Expanded_User_Model.objects.all()
        return render(request, 'user_manage.html', {'users': users, 'access': access})
    return redirect('/MainPage/')


class edit_user_data(UpdateView):
    access = forms.IntegerField(widget=forms.ChoiceField(choices=[[1, "User"], [2, "Technician"], [3, "Admin"]]))
    model = Expanded_User_Model
    template_name = 'edit_user_data.html'
    fields = ['access']
    success_url = "/UsersManage/"


def check_user(request):
    current_user = request.user
    current_user_expand = get_object_or_404(Expanded_User_Model, user=current_user)
    permission = current_user_expand.access
    return permission


def RegisterUser(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Hasła się nie są identyczne')
            return render(request, "register.html")
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            new_user = Expanded_User_Model.objects.create(user=user, access=1)
            new_user.save()
            return redirect("/UsersManage/")
        except:
            pass
    return render(request, "register.html")
