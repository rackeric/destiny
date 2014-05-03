#from django.shortcuts import render
from django.http import HttpResponse
from tasks import ansible_command_run
from tasks import ansible_ping

# Create your views here.

def ansible_command_view(request, job_id, user_id):
    ansible_command_run.delay(job_id, user_id)
    return HttpResponse("ansible_command_run task sent")

def ansible_ping_view(request, job_id, user_id):
    ansible_ping.delay(job_id, user_id)
    return HttpResponse("ansible_ping task sent")
