
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if ('status_code' in response):
        if response.status_code == 400:
            keys = list(response.data.keys())
            response.data['error'] = {
                'description': 'Some data were incorrect',
                'code': 'invalid_request',
                'fields': {}
            }
            for key in keys:
                response.data['error']['fields'][key] = response.data[key]
                response.data.pop(key, None)
        else:
            response.data['error'] = {
                'description': exc.detail,
                'code': exc.get_codes()
            }
            response.data.pop('detail', None)
        # Now add the HTTP status code to the response.
        if response is not None:
            response.data['status_code'] = response.status_code

    return response