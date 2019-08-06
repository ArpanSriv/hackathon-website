from django.shortcuts import render

# Solution Upload
def login_solution(request):
    return render(request, 'solutions/upload_login.html')


def upload_solution(request):
    return render(request, 'solutions/upload_solution.html')
