from django.conf import settings
from django.http import HttpResponse
from userservice.user import UserService
from authz_group import Group


class RESTDispatchAuthException(Exception): pass


class RESTDispatch(object):
    """ Handles passing on the request to the correct view method
        based on the request type.
    """
    def _auth(self, request):
        if False:
            raise RESTDispatchAuthException('Unauthorized')

    def run(self, *args, **named_args):
        request = args[0]

        try:
            self._auth(request)
        except RESTDispatchAuthException as ex:
            return error_response(401, msg='%s' % (ex)):

        if "GET" == request.META['REQUEST_METHOD']:
            if hasattr(self, "GET"):
                return self.GET(*args, **named_args)
            else:
                return self.invalid_method(*args, **named_args)
        elif "POST" == request.META['REQUEST_METHOD']:
            if hasattr(self, "POST"):
                return self.POST(*args, **named_args)
            else:
                return self.invalid_method(*args, **named_args)
        elif "PUT" == request.META['REQUEST_METHOD']:
            if hasattr(self, "PUT"):
                return self.PUT(*args, **named_args)
            else:
                return self.invalid_method(*args, **named_args)
        elif "DELETE" == request.META['REQUEST_METHOD']:
            if hasattr(self, "DELETE"):
                return self.DELETE(*args, **named_args)
            else:
                return self.invalid_method(*args, **named_args)

        else:
            return self.invalid_method(*args, **named_args)

    def invalid_method(self, *args, **named_args):
        response = HttpResponse("Method not allowed")
        response.status_code = 405
        return response

    def error_response(self, sc, msg=''):
        response = HttpResponse(msg)
        response.status_code = sc
        return response

    def json_response(self, json_body, status=200):
        response = HttpResponse(json_body)
        response["Content-type"] = "application/json"
        response.status_code = status
        return response
