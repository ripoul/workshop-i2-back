import json
import io
import base64
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from analyser.models import UserData
from analyser.utils import extract_keywords

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
def index(request):
    if request.method == 'POST':

        body=json.loads(request.body.decode("utf-8"))

        format, imgstr = body["file"].split(';base64,') 
        ext = format.split('/')[-1] 

        image = Image.open(io.BytesIO(base64.b64decode(imgstr)))

        raw_data = (pytesseract.image_to_string(image, lang="fra"))
        print(raw_data)
        keywords_list = json.dumps(extract_keywords(raw_data))
        UserData.objects.create(keywords=keywords_list)
        return HttpResponse(raw_data)
    return HttpResponse("Hello, world. You're at the polls index.")
