import socket
import os
import traceback
from datetime import datetime
from typing import Tuple

from workerthread import WorkerThread

class WebServer:

    def create_server_socket(self, host_name: str = 'localhost', port: int = 8080) -> socket:
        """
        通信を待ち受けるためのserver_socketを生成する
        """
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host_name, port))
        server_socket.listen(10)
        return server_socket

    def serve(self):
        print("===Server:サーバー起動===")
        try:
            server_socket = self.create_server_socket(port=8080)
            while True:
                # 外部からの接続を待ち、接続があったらコネクションを確立する
                print('===Server:クライアントからの接続を待ちます===')
                (client_socket, address) = server_socket.accept()
                print(f"===Server:クライアントとの接続が完了しました remote_address: {address} ===")               
                try:
                    thread = WorkerThread(client_socket, ('localhost', 8080))
                    thread.start()
                except Exception:
                    print("===Server:リクエスト処理中にエラーが発生しました===")
                    traceback.print_exc()
                finally:
                    client_socket.close()
        finally:
            print('===Server:サーバーを停止します===')

if __name__ == '__main__':
    server = WebServer()
    server.serve()
