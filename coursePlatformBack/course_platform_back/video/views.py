from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from .models import Video
from .services import open_file

def get_list_video(request):
    videos = Video.objects.all().values('id', 'title', 'description', 'image', 'create_at')
    return JsonResponse(list(videos), safe=False)

def get_video(request, pk: int):
    _video = get_object_or_404(Video, id=pk)
    return JsonResponse({
        "id": _video.id,
        "title": _video.title,
        "description": _video.description,
        "image": request.build_absolute_uri(_video.image.url),
        "create_at": _video.create_at,
    })

def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response