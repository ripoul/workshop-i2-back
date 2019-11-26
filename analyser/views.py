from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
def index(request):
    if request.method == 'POST':
        print(request.FILES)
        print(pytesseract.image_to_string(Image.open(request.FILES[0])))
    return HttpResponse("Hello, world. You're at the polls index.")