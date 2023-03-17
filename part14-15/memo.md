# VSCodeのショートカット
⇧⌘O:シンボルへの移動  
結構使えそう

## POSTでRequest Bodyを送信
Content-Type: application/x-www-form-urlencoded  
POSTの時に追加されるヘッダー  
これはデフォルトのもの

POSTのデータのフォーマットを決めているらしい  
このヘッダーだとファイル名は送られるけどファイルの中身は送られない

バリエーション
- application/x-www-form-urlencoded
-- デフォルト
-- nameとvalueを=で連結
-- 複数項目は&で連結
-- 半角スペースは+
-- URLに使えない文字はUTF-8で符号化->パーセントエンコーディング
-- UTF-8で符号化できないバイナリデータは扱えない
- multipart/form-data
-- enctype属性で明示
-- フォームの項目ごとにセパレータと呼ばれる文字列で分割
-- セパレータの内容はContent-Typeで指定する
-- フォームの項目ごとにデータ性質の補助情報がつく(Content-Disposition, Content-Type)
- application/json
-- Ajaxを使う