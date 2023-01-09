from django.shortcuts import render
from django.http import JsonResponse
from bourse.service import bourse
import json
from bson import ObjectId


class ObjectIDJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def index(request):
    return render(request, 'bourse/bourse.html')


def data(request):
    return JsonResponse(bourse, encoder=ObjectIDJsonEncoder)
