from django.shortcuts import render
import requests 

BACKEND_URL = 'http://127.0.0.1:8000/video/api/'

def home(request):
    try:
        response = requests.get(f'{BACKEND_URL}videos/')
        if response.status_code == 200:
            videos = response.json() 
        else:
            videos = [] 
    except requests.exceptions.RequestException as e:
        videos = [] 
    
    return render(request, 'home.html', {'video_list': videos})
def video_detail(request, pk):
    response = requests.get(f'{BACKEND_URL}videos/{pk}/')
    video = response.json()
    return render(request, 'video.html', {'video': video})