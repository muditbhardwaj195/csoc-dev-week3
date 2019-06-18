from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
# Create your views here.

@csrf_exempt
def loginUserView(request):
    response_data = {
        'message': None,
    }
    print("hiiiii")
    username_temp = request.POST.get("username")
    password_temp = request.POST.get("password")
    print(username_temp,password_temp)
    try:
        login_user = authenticate(username=username_temp, password=password_temp)
        login(request, login_user)
        response_data['message'] = 1
    except:
        response_data["message"] = "failure"
    return JsonResponse(response_data)


@csrf_exempt
def registerUserView(request):
    response_data = {
        'message': None,
    }
    username_temp = request.POST.get("user")
    password_temp = request.POST.get("pass")
    print(username_temp,password_temp)
    try:
        user = User.objects.create_user(username_temp, password = password_temp)
        user.save()
        print("did it")
        login_user = authenticate(username=username_temp, password=password_temp)
        login(request, login_user)
        response_data['message'] = 1
    except:
        response_data["message"] = "failure"
    return JsonResponse(response_data)

def logoutView(request):
    template_name = "authentication/logout.html"
    logout(request)
    return render(request, template_name, {})








