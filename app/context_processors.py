from django.conf import settings
import app.m00_common as m00

def general_context(request):
    return {
        'MEDIA_URL': settings.MEDIA_URL}