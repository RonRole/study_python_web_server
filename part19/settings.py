import os

# 実行ファイルのあるディレクトリ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 静的配信するファイルを置くディレクトリ
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# htmlテンプレートをは置くディレクトリ
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")