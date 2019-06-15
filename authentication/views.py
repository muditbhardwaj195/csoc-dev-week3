from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
# Create your views here.

def loginView(request):
	template_name = "authentication/login.html"

	return render(request,template_name,{})

def logoutView(request):
	template_name = "authentication/logout.html"
	#template_name = "/"
	logout(request)
	return render(request, template_name, {})

def registerView(request):
    template_name = "authentication/register.html"
    return render(request, template_name, {})

@csrf_exempt
def loginlogicView(request):
    response_data = {
        'message': None,
    }
    username = request.POST['username']
    password = request.POST['password']
    try:
        login_user = authenticate(username=username, password=password)
        login(request, login_user)
        response_data['message'] = 1
    except:
        response_data["message"] = "failure"
    return JsonResponse(response_data)


@csrf_exempt
def registerlogicView(request):
    response_data = {
        'message': None,
    }
    username = request.POST.get("username_do")
    password = request.POST.get("password_do")
    print(username,password)
    try:
        user = User.objects.create_user(username, password = password)
        user.save()
        print("did it")
        login_user = authenticate(username=username, password=password)
        login(request, login_user)
        response_data['message'] = 1
    except:
        response_data["message"] = "failure"
    return JsonResponse(response_data)









