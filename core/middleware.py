from django.core.cache import cache

class countermiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        count = cache.get('request_count', 0)
        if count:
            count = count + 1
        else:
            count = 1
        cache.set('request_count', count)
        print("MIDDLEWARE", count)
        response = self.get_response(request)
        
        return response