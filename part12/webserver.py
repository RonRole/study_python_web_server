import socket
import os
import traceback
from datetime import datetime

class WebServer:

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


    def serve(self):
        print("===サーバー起動===")
        try:
            # socketを生成
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # socketをlocalhostのポート8080ばんに割り当てる
            server_socket.bind(('localhost', 8080))
            server_socket.listen(10)

            while True:
                # 外部からの接続を待ち、接続があったらコネクションを確立する
                print('===クライアントからの接続を待ちます===')
                (client_socket, address) = server_socket.accept()
                print(f"===クライアントとの接続が完了しました remote_address: {address} ===")
                
                try:
                    # クライアントから送られてきたデータを取得する
                    # recv実行時にクライアントから送られて溜まっているデータを4096byteずつ、
                    # 全て取得するまでブロック
                    request = client_socket.recv(4096)
                    
                    # クライアントから送られてきたデータをファイルに書き出す
                    with open('server_recv.txt', 'wb') as f:
                        f.write(request)

                    # クライアントへ送信するレスポンスを作成
                    request_line, remain = request.split(b"\r\n", maxsplit=1)
                    request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)
                    # リクエストラインをパース
                    method, path, http_version = request_line.decode().split(' ')
                    relative_path = path.lstrip('/')
                    static_file_path = os.path.join(self.STATIC_ROOT, relative_path)

                    try:
                        with open(static_file_path, 'r') as f:
                            response_body = f.read()
                    except OSError:
                        response_body = "<html><body><h1>404 Not Found</h1></body></html>"
                        response_line = "HTTP/1.1 404 Not Found\r\n"
                    
                    # リクエストpathの拡張子をみて、Content-Typeに変換する
                    if "." in path:
                        ext = path.split(".", maxsplit=1)[-1]
                    else:
                        ext = ""
                    content_type = self.MIME_TYPES.get(ext, "application/octet-stream")
                    response_line = 'HTTP/1.1 200 OK\r\n'
                    response_header = f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
                    response_header += "Server: Sawaikei/0.1\r\n"
                    response_header += f"Content-Length: {len(response_body.encode())}\r\n"
                    response_header += "Connection: Close\r\n"
                    response_header += f"Content-Type: {content_type}\r\n"
                    response = (response_line + response_header + '\r\n' + response_body).encode()

                    # クライアントへレスポンスを送信
                    client_socket.send(response)
                except Exception:
                    print("===リクエスト処理中にエラーが発生しました===")
                    traceback.print_exc()
                finally:
                    client_socket.close()
        finally:
            print('===サーバーを停止します===')

if __name__ == '__main__':
    server = WebServer()
    server.serve()
