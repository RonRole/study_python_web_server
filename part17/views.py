from ast import Tuple
import datetime
from pprint import pformat
import textwrap
from typing import Optional
from henango.http.request import HTTPRequest
from henango.http.response import HTTPResponse
import urllib

def now(request: HTTPRequest) -> HTTPResponse:
    """
    現在時刻を表示するHTMLを生成する
    """
    html = f"""
        <html>
            <body>
                <h1>Now: {datetime.now()}</h1>
            </body>
        </html>
    """
    response_body = textwrap.dedent(html).encode()
    content_type = "text/html; charset=UTF-8"
    return HTTPResponse(200,content_type, response_body)

def show_request(request: HTTPRequest) -> HTTPResponse:
    """
    HTTPリクエストの内容を表示するHTMLを生成する
    """
    html = f"""
        <html>
            <body>
                <h1>Request Line:</h1>
                <p>
                    {request.method} {request.path} {request.http_version}
                </p>
                <h1>Headers:</h1>
                <pre>{pformat(request.headers)}</pre>
                <h1>Body:</h1>
                <pre>{request.body.decode("utf-8", "ignore")}</pre> 
            </body>
        </html>
    """
    response_body = textwrap.dedent(html).encode()
    content_type = "text/html; charset=UTF-8"
    return HTTPResponse(body=response_body,content_type=content_type, status_code=200)

def parameters(request: HTTPRequest) -> HTTPResponse:
    """
    POSTパラメータを表示するHTMLを生成する
    """
    if request.method == "GET":
        response_body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
        content_type = "text/html; charset=UTF-8"
        status_code = 405

    elif request.method == "POST":
        post_params = urllib.parse.parse_qs(request.body.decode())
        html = f"""
            <html>
            <body>
                <h1>Parameters:</h1>
                <pre>{pformat(post_params)}</pre>
            </body>
            </html>
        """
        response_body = textwrap.dedent(html).encode()
        content_type = "text/html; charset=UTF-8"
        status_code = 200
    return HTTPResponse(body=response_body,content_type=content_type, status_code=status_code)


