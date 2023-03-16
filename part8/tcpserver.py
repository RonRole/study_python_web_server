import socket

class TCPServer:
    def serve(self):
        print("===サーバー起動===")
        try:
            # socketを生成
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # socketをlocalhostのポート8080ばんに割り当てる
            server_socket.bind(('localhost', 8080))
            server_socket.listen(10)

            # 外部からの接続を待ち、接続があったらコネクションを確立する
            print('===クライアントからの接続を待ちます===')
            (client_socket, address) = server_socket.accept()
            print(f"===クライアントとの接続が完了しました remote_address: {address} ===")
            
            # クライアントから送られてきたデータを取得する
            # recv実行時にクライアントから送られて溜まっているデータを4096byteずつ、
            # 全て取得するまでブロック
            request = client_socket.recv(4096)
            
            # クライアントから送られてきたデータをファイルに書き出す
            with open('server_recv.txt', 'wb') as f:
                f.write(request)

            # クライアントへ送信するレスポンスデータをファイルから取得
            with open('server_send.txt', 'rb') as f:
                response = f.read()

            # クライアントへレスポンスを送信
            client_socket.send(response)

            # 返事は返さず、通信終了
            client_socket.close()
        finally:
            print('===サーバーを停止します===')

if __name__ == '__main__':
    server = TCPServer()
    server.serve()
