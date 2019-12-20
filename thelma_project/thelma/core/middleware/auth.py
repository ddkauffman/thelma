from django.contrib.auth.middleware import RemoteUserMiddleware


class RHEL7CustomHeaderMiddleware(RemoteUserMiddleware):
    header = 'HTTP_REMOTE_USER'
