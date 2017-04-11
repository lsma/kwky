from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from downloads.models import Document

def downloads_get(request, name):
    doc = get_object_or_404(Document, name=name)
    response = HttpResponse(doc.document.read(),content_type='application/pdf')
    response['Content-Disposition'] = 'filename={}'.format(doc)
    return response