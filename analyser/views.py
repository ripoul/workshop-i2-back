import json
import io
import base64
import traceback
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from analyser.models import UserData
from analyser.utils import extract_keywords

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


@require_http_methods(["OPTIONS", "POST"])
@method_decorator(csrf_exempt, name='dispatch')
def index(request):
    if request.method == 'POST':
        try:
            body=json.loads(request.body.decode("utf-8"))

            format, imgstr = body["file"].split(';base64,') 
            ext = format.split('/')[-1] 

            image = Image.open(io.BytesIO(base64.b64decode(imgstr)))

            raw_data = (pytesseract.image_to_string(image, lang="fra"))
            print(raw_data)
            keywords_list = json.dumps(extract_keywords(raw_data))
            UserData.objects.create(keywords=keywords_list)
            return HttpResponse(raw_data)
        except Exception as e:
            traceback.print_exc()
            return HttpResponse(str(e), status=500)
    return HttpResponse("Hello, world. You're at the polls index.")

@require_http_methods(["GET"])
@method_decorator(csrf_exempt, name='dispatch')
def search(request):
    if request.method == 'GET':
        search_keyword = request.GET.get("keyword", None)
        if not search_keyword:
            return HttpResponseBadRequest("no keywords")

        matching_user_data = UserData.objects.filter(keywords__icontains=search_keyword)

        return JsonResponse([json.loads(user_data.keywords) for user_data in matching_user_data], safe=False)
    return HttpResponse("Hello, world. You're at the polls index.")
