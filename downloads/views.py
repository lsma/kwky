from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from downloads.models import Document

def downloads_get(request, name):
    doc = get_object_or_404(Document, name=name)
    return HttpResponseRedirect(doc.document.url)