from django.db import models
from django.contrib.auth.models import User, Group


class MachineLine(models.Model):
    machine_name = models.CharField(max_length=150)
    machine_location = models.CharField(max_length=150)
    machine_warehouse = models.CharField(max_length=150)
    machine_ip_address = models.CharField(max_length=20, default="0")
    machine_rack = models.IntegerField(default=0)
    machine_slot = models.IntegerField(default=0)

    def __str__(self):
        return str(self.machine_name + " " + self.machine_location + " " + self.machine_warehouse)


class MachineLine_Readings(models.Model):
    machine = models.ForeignKey(MachineLine, on_delete=models.SET_NULL, null=True)
    current = models.FloatField()
    voltage = models.FloatField()
    herz = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.machine + " " + self.date)


class Expanded_User_Model(models.Model):
    CHOICES = [(1, 'User'), (2, 'Technician'), (3, 'Admin')]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    access = models.IntegerField(choices=CHOICES)

    def __str__(self):
        return str(self.user)

