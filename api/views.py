from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
import base64
import api.src.main as main
import sys
import logging
def base64_to_image(imgstring):
    imgdata = base64.b64decode(imgstring)
    filename = 'source_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

@api_view(["POST"])
def process_image(request):

    parameters = JSONParser().parse(request)
    base64_to_image(parameters['image'])
    #
    #
    #
    try:
       reg_number= main.start()
    except:
        logging.getLogger(__name__).error(sys.exc_info()[0])
        return JsonResponse({"data":{},"status":500})

    #
    #
    #
    content = {"data": {"number":str(reg_number)},"status":200}
    return JsonResponse(content)