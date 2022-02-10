'''
Basic views
'''
import os

from django.conf import settings
from django.http import FileResponse
from django.http import HttpResponse
import prometheus_client as prometheus


def serve_static(request, path='index.html'):
    '''
    Return static files,
    as django.contrib.staticfiles is disabled in production mode.

    Actually, static files shall be served separately, for example with nginx.
    '''
    path = '%s/%s' % (getattr(settings, 'STATICFILES_DIR'), path)

    if request.method == "POST":
        if 'data' in request.POST:
            with open(path, 'w') as fout:
                fout.write(request.POST['data'])
        else:
            with open(path, 'wb') as fout:
                fout.write(request.FILES['data'].read())
        return HttpResponse("Successfully updated" + path)

    if os.path.isfile(path):
        return FileResponse(open(path, 'rb'))

    if os.path.isdir(path):
        dirs = os.listdir(path)
        resp = path + " is a dir: "
        for file in dirs:
            resp += str(file) + "; "
        return HttpResponse(resp)

    return HttpResponse("file not found at " + path)
    # HttpResponseNotFound()


def metrics(request):
    '''
    Serve prometheus metrics
    '''
    metrics_page = prometheus.generate_latest(prometheus.REGISTRY)
    return HttpResponse(metrics_page,
                        content_type=prometheus.CONTENT_TYPE_LATEST)
