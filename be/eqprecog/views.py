from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime
import random
import json
import logging

from . import recog

logger = logging.getLogger(__name__)


def handle_uploaded_file(file):
    [filename, ext] = file.name.split('.')
    now = datetime.now()
    path = 'pics/{date}-{time}-{rand}.{ext}'\
        .format(date=now.strftime('%Y-%m-%d'), time=now.strftime('%H%M%S'), rand=random.randint(10000, 99999), ext=ext.lower())
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return path


def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if file.size > 50000 or file.content_type.find('image/jp') == -1:
            logger.warning('pic_invalid')
            return HttpResponseBadRequest('暂时仅支持JPG格式，50KB以内的图片')
        file_path = handle_uploaded_file(file)
        cells = recog.main(file_path)
        logger.info('pic_recog_successfully')
        return HttpResponse(json.dumps(cells), content_type="application/json")
    else:
        logger.warning('upload_get_query')
