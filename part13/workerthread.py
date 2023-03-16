from datetime import datetime
import os
import socket
from threading import Thread
import traceback
from typing import Tuple


class WorkerThread(Thread):
    # このファイルが配置されているディレクトリ名
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 静的ファイルを配置するディレクトリ
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    # 拡張子とMIME Typeの対応
    MIME_TYPES = {
        "html": "text/html",
        "css": "text/css",
        "png": "image/png",
        "jpg": "image/jpg",
        "gif": "image/gif",
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
            request = self.client_socket.recv(4096)
            with open('server_recv.txt', 'wb') as f:
                f.write(request)
            # HTTPリクエストをパースする
            method, path, http_version, request_header, request_body = self.parse_http_request(request)
            try:
                response_body = self.get_static_file_content(path)
                response_line = "HTTP/1.1 200 OK\r\n"
            except OSError:
                response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
                response_line = "HTTP/1.1 404 Not Found\r\n"
            response_header = self.build_response_header(path, response_body)
            # リクエストpathの拡張子をみて、Content-Typeに変換する
            response = (response_line + response_header + "\r\n").encode() + response_body
            # クライアントへレスポンスを送信
            self.client_socket.send(response)
        except Exception:
            print('===Worker:リクエストの処理中にエラーが発生しました===')
            traceback.print_exc()
        finally:
            print("===Worker:クライアントとの通信を終了します===")
            self.client_socket.close()


    def parse_http_request(self, request: bytes) -> Tuple[str, str, str, bytes, bytes]:
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
        return method, path, http_version, request_header, request_body

    def get_static_file_content(self, path:str) -> bytes:
        """
        リクエストpathから、staticファイルの内容を取得する
        """
        relative_path = path.lstrip('/')
        static_file_path = os.path.join(self.STATIC_ROOT, relative_path)
        with open(static_file_path, 'rb') as f:
            return f.read()

    def build_response_header(self, path: str, response_body: bytes) -> str:
        """
        レスポンスヘッダーを構築する
        """
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
