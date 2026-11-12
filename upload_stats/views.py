from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from accounts.permissions import operational_access
from . import data


@login_required
def uploads(request):
    if not operational_access(request.user):
        return HttpResponseForbidden('Staff access required.')
    return render(request, 'uploads.html')


@require_GET
def uploads_summary(request):
    if not operational_access(request.user):
        return JsonResponse({'error': 'Staff access required.'}, status=403)
    try:
        return JsonResponse(data.upload_summary(request.GET))
    except data.InvalidUploadFilters as exc:
        return JsonResponse({'error': str(exc)}, status=400)
    except DatabaseError:
        return JsonResponse({'error': 'Upload data is currently unavailable.'}, status=503)


@require_GET
def upload_scopes(request):
    if not operational_access(request.user):
        return JsonResponse({'error': 'Staff access required.'}, status=403)
    try:
        return JsonResponse(data.list_scopes(), safe=False)
    except DatabaseError:
        return JsonResponse({'error': 'Upload data is currently unavailable.'}, status=503)
