
from datetime import datetime
import os
from pprint import pformat
import re
import socket
from threading import Thread
import traceback
from typing import Optional, Tuple
from henango.http.request import HTTPRequest
from henango.http.response import HTTPResponse
from henango.urls.resolver import URLResolver
from urls import url_patterns
import settings

class Worker(Thread):

    # 拡張子とMIME Typeの対応
    MIME_TYPES = {
        "html": "text/html; charset=UTF-8",
        "css": "text/css",
        "png": "image/png",
        "jpg": "image/jpg",
        "gif": "image/gif",
    }

    # ステータスコードとステータスラインの対応
    STATUS_LINES = {
        200: "200 OK",
        404: "404 Not Found",
        405: "405 Method Not Allowed",
    }

    def __init__(self, client_socket: socket, address: Tuple[str, int]):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = address

    def run(self) -> None:
        """
        クライアントと接続済みのsocketを引数として受け取り、
        リクエストを処理してレスポンスを送信
        """
        try:
            request_bytes = self.client_socket.recv(4096)
            with open('server_recv.txt', 'wb') as f:
                f.write(request_bytes)
            # HTTPリクエストをパースする
            request = self.parse_http_request(request_bytes)
            # url解決を試行
            view = URLResolver().resolve(request)
            # レスポンスを生成する
            response = view(request)
            # レスポンスラインを生成
            response_line = self.build_response_line(response)
            # レスポンスヘッダーを生成
            response_header = self.build_response_header(request.path, response.body, response.content_type)
            # レスポンス全体を生成
            response_bytes = (response_line + response_header + "\r\n").encode() + response.body
            # クライアントへレスポンスを送信
            self.client_socket.send(response_bytes)
        except Exception:
            print('===Worker:リクエストの処理中にエラーが発生しました===')
            traceback.print_exc()
        finally:
            print("===Worker:クライアントとの通信を終了します===")
            self.client_socket.close()


    def parse_http_request(self, request: bytes) ->  HTTPRequest:
        """
        HTTPリクエストを
        1. method: str
        2. path: str
        3. http_version: str
        4. request_header: bytes
        5. request_body: bytes
        """
        request_line, remain = request.split(b"\r\n", maxsplit=1)
        request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)
        # リクエストラインを文字列に変換してパースする
        method, path, http_version = request_line.decode().split(' ')
        # リクエストヘッダーを辞書にパース
        headers = {}
        for header_row in request_header.decode().split("\r\n"):
            key, value = re.split(r": *", header_row, maxsplit=1)
            headers[key] = value
        return HTTPRequest(
            path,
            method,
            http_version,
            headers,
            request_body
        )

    def build_response_line(self, response: HTTPResponse)-> str:
        """
        レスポンスラインの構築
        """
        status_line = self.STATUS_LINES[response.status_code]
        return f"HTTP/1.1 {status_line}"

    def build_response_header(self, path: str, response_body: bytes, content_type: Optional[str] = None) -> str:
        """
        レスポンスヘッダーを構築する
        """
        if content_type is None:
            if "." in path:
                ext = path.split(".", maxsplit=1)[-1]
            else:
                ext = ""
            content_type = self.MIME_TYPES.get(ext, "application/octet-stream")
        response_header = f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response_header += "Server: Sawaikei/0.1\r\n"
        response_header += f"Content-Length: {len(response_body)}\r\n"
        response_header += "Connection: Close\r\n"
        response_header += f"Content-Type: {content_type}\r\n"
        return response_header    

