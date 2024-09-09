import json

import paramiko
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# SSH bağlantısı kurma fonksiyonu
def connect_ssh(request):
    if request.method == "POST":
        data = json.loads(request.body)
        hostname = data.get('hostname')
        username = data.get('username')
        password = data.get('password')

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(hostname, username=username, password=password)
            request.session['ssh_client_data'] = {
                'hostname': hostname,
                'username': username,
                'password': password
            }
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def execute_command(request):
    if request.method == "POST":
        data = json.loads(request.body)
        command = data.get('command')
        ssh_client_data = request.session.get('ssh_client_data')

        if not ssh_client_data:
            return JsonResponse({'error': 'SSH connection not established.'})

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                ssh_client_data['hostname'],
                username=ssh_client_data['username'],
                password=ssh_client_data['password']
            )

            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if output:
                return JsonResponse({'output': output})
            elif error:
                return JsonResponse({'error': error})
        except Exception as e:
            return JsonResponse({'error': str(e)})

# Ana sayfa fonksiyonu
def home(request):
    return render(request, "home.html")


# Terminal sayfasını görüntüleme fonksiyonu
def terminal_view(request):
    return render(request, "terminal.html")
