# Step3 自作クライアントとApacheで通信
Apacheとの通信部分でBad Requestが出たので、そのメモ

## 事象
1. ファイルを作成
1. step2/server_recv.txtの内容をコピー
1. step3/client_send.txtに貼り付け
1. tcpclient.pyを実行してBadRequest

## 原因
改行コード　　
元はCRLFだったけど、LFになっていた

HTTPの改行コードはCRLFと決まっているらしい