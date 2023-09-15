from flask import Response, json

def server_res(message, success=False, status=500, location='/books', book_data=None, **kwargs):
    args_copy = locals().copy()

    if 'kwargs' in args_copy:
        args_copy.update(args_copy['kwargs'])
        del args_copy['kwargs']

    del args_copy['location']

    res_body = {key: value for key, value in args_copy.items()
                if value is not None}

    response = Response(
        json.dumps(res_body), status=status, mimetype='application/json')
    response.headers['Location'] = location
    return response


class CustomException(Exception):
    def __init__(self, message, status=500):
        super().__init__(self, message)
        self.message = message
        self.status = int(status)

    def get_exception_obj(self):
        return {'message': self.message, 'status': self.status}
