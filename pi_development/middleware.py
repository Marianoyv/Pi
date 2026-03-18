class CleanHtmlResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        content_type = response.get('Content-Type', '')

        if getattr(response, 'streaming', False) or 'text/html' not in content_type:
            return response

        content = response.content
        cleaned = (
            content
            .replace(b'\xef\xbb\xbf', b'')
            .replace(b'&#xFEFF;', b'')
            .replace(b'&#65279;', b'')
        )

        if cleaned != content:
            response.content = cleaned

        return response
