from django.utils.deprecation import MiddlewareMixin


class HiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('before view works')
        request.test = 'Additional field here'
        response = self.get_response(request)
        print('after works', response.content)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # this code is executed just before the view is called
        print('just before view')

    def process_exception(self, request, exception):
        # this code is executed if an exception is raised
        print('Exception occurs')

    def process_template_response(self, request, response):
        # this code is executed if the response contains a render() method
        print('render method was in response')
        return response
