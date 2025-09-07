from typing import Union

from flask import (
    Response,
    make_response,
    request,
)
from werkzeug.datastructures import Authorization


def make_forbidden_response() -> Response:
    res = make_response("Permission denied")
    res.status_code = 403
    return res


def authenticate_request_basic_auth() ->  Union[Authorization, Response]:
    """Authenticate the request using basic auth."""
    if request.authorization and request.authorization.username == "admin":
        print("admin 来了")
        obj = Authorization("basic", {"username": "admin"})
        return obj

    xId = request.headers["X-HW-ID"]
    obj = Authorization("basic", {"username": xId})


    if obj.username == "wze.com":
        return obj
    else:
        # let user attempt login again
        return make_forbidden_response()
