# PlotWeaver - 創作支援AI 🎭📚

**LangChain & llama.cpp による日本語対応創作支援AI**

## 🎉 プロジェクト完成！

PlotWeaverは実際のLLMモデル（DeepSeek-R1-Distill-Qwen-14B-Japanese-Q4_K_M.gguf）を使用した創作支援AIとして完全に動作しています。

## ✨ 主要機能

### 🎯 プロット生成
- **7つのジャンル対応**: ファンタジー、恋愛、ミステリー、SF、ホラー、日常系、冒険
- **構造化プロット**: 6章構成（導入部→発端→展開→転換点→クライマックス→結末）
- **実際のLLM使用**: DeepSeek-R1-Distill-Qwen-14B-Japanese-Q4_K_M（8.4GB）

### 👥 キャラクター管理
- **CRUD操作**: キャラクターの追加、取得、更新、削除
- **詳細情報**: 説明、特徴、背景、関係性
- **記憶機能**: プロット生成時にキャラクター情報を活用

### 📊 複数案生成
- **バリエーション生成**: 同一プロンプトから複数の異なるプロット
- **温度調整**: 創造性レベルを変えた多様な出力

### 💾 出力管理
- **ファイル出力**: Markdown、PDF形式でのダウンロード
- **履歴管理**: 生成したプロットの保存・管理

## 🚀 動作確認済み

### ✅ テスト結果（4/4成功）
1. **ヘルスチェック**: API正常動作
2. **プロット生成**: 実際のLLMで日本語プロット生成成功
3. **キャラクター管理**: CRUD操作成功
4. **キャラクター記憶**: キャラクター情報を活用したプロット生成成功

### 🌐 アクセス先
- **Streamlit UI**: http://localhost:8501
- **FastAPI**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs

## 🛠️ 技術スタック

- **バックエンド**: FastAPI + uvicorn
- **フロントエンド**: Streamlit
- **LLM**: llama.cpp + GGUF形式モデル
- **AI Framework**: LangChain
- **メモリ**: ConversationBufferMemory + JSON永続化
- **言語**: Python 3.12

## 📁 プロジェクト構成と技術詳細

```
plotweaver/
├── main.py                 # FastAPI メインアプリケーション
├── ui.py                   # Streamlit ユーザーインターフェース
├── llama_engine.py         # LLM エンジン（llama.cpp）
├── prompt_templates.py     # ジャンル別プロンプトテンプレート
├── memory_manager.py       # キャラクター・会話メモリ管理
├── requirement.txt        # 依存関係
├── render.yml             # Renderデプロイ設定
├── models/                # LLMモデルファイル
│   └── DeepSeek-R1-Distill-Qwen-14B-Japanese-Q4_K_M.gguf
├── test_main.py           # テスト用API（モック）
├── test_ui.py             # テスト用UI
├── test_api.py            # 自動テストスクリプト
├── test_real_llm.py       # 実LLMテストスクリプト
├── test_real_llm_extended.py # 拡張LLMテストスクリプト
└── README.md              # このファイル
```

### 🔧 各ファイルの詳細な役割と技術

#### **main.py** - FastAPI バックエンドサーバー
**役割**: RESTful API エンドポイントの提供
**使用技術**:
- **FastAPI**: 高速なWeb APIフレームワーク
- **Pydantic**: データバリデーション・シリアライゼーション
- **CORS**: クロスオリジンリソース共有設定
- **uvicorn**: ASGI サーバー

**主要エンドポイント**:
- `GET /health`: システム健康状態チェック
- `POST /generate`: 単一プロット生成
- `POST /generate/multiple`: 複数バリエーション生成
- `GET/POST/PUT/DELETE /characters`: キャラクター管理CRUD
- `GET /genres`: 利用可能ジャンル一覧

#### **llama_engine.py** - LLM推論エンジン
**役割**: llama.cppを使用したローカルLLM推論
**使用技術**:
- **llama-cpp-python**: llama.cppのPythonバインディング
- **GGUF形式**: 量子化されたモデル形式（Q4_K_M）
- **メモリ効率化**: 8.4GBモデルの効率的な読み込み

**特徴**:
- モデル初期化とキャッシュ
- パラメータ調整（temperature, top_p, max_tokens）
- エラーハンドリングと再試行機能

#### **prompt_templates.py** - プロンプトエンジニアリング
**役割**: ジャンル別構造化プロンプトテンプレート
**使用技術**:
- **LangChain PromptTemplate**: 動的プロンプト生成
- **テンプレート変数**: user_input, character_memory
- **ジャンル特化**: 7つのジャンル専用プロンプト

**プロンプト構造**:
```python
# 例: ファンタジージャンル
template = """
あなたは創作支援AIです。以下の要求に基づいて、魅力的なファンタジー小説のプロットを生成してください。

【ジャンル】: ファンタジー
【要求】: {user_input}
【キャラクター情報】: {character_memory}

【プロット構成】:
1. 導入部: 世界観と主人公の紹介
2. 発端: 冒険の始まり
3. 展開: 困難と成長
4. 転換点: 重要な発見や決断
5. クライマックス: 最大の試練
6. 結末: 解決と成長の確認
"""
```

#### **memory_manager.py** - メモリ・永続化システム
**役割**: キャラクター情報と会話履歴の管理
**使用技術**:
- **LangChain ConversationBufferMemory**: 会話履歴管理
- **JSON永続化**: ファイルベースのデータ保存
- **キャラクター関係性**: グラフ構造での関係管理

**データ構造**:
```python
{
    "characters": {
        "character_name": {
            "description": "キャラクター説明",
            "traits": ["特徴1", "特徴2"],
            "background": "背景設定",
            "relationships": {"other_char": "関係性"},
            "story_appearances": ["出演作品リスト"],
            "development_history": ["成長記録"]
        }
    }
}
```

#### **ui.py** - Streamlit フロントエンド
**役割**: ユーザーインターフェースとインタラクション
**使用技術**:
- **Streamlit**: Webアプリケーションフレームワーク
- **カスタムCSS**: モダンなUI設計
- **リアルタイムAPI通信**: requests ライブラリ
- **ファイル出力**: Markdown, PDF生成

**UI構成**:
- サイドバー: 設定パネル（ジャンル、パラメータ）
- メインエリア: 4つのタブ（生成、管理、複数案、出力）
- レスポンシブデザイン: 幅広いデバイス対応

#### **requirement.txt** - 依存関係管理
**主要パッケージ**:
```
fastapi              # Web APIフレームワーク
uvicorn             # ASGI サーバー
llama-cpp-python    # LLM推論エンジン
langchain           # AI アプリケーションフレームワーク
langchain-community # LangChain コミュニティ拡張
streamlit           # Web UIフレームワーク
requests            # HTTP クライアント
pydantic            # データバリデーション
chromadb            # ベクトルデータベース（将来のRAG用）
sentence-transformers # 文埋め込みモデル（将来のRAG用）
markdown            # Markdown処理
fpdf2               # PDF生成
```

#### **render.yml** - デプロイ設定
**役割**: Render.com での本番環境デプロイ
**構成**:
- **API サーバー**: FastAPI (ポート10000)
- **UI サーバー**: Streamlit (ポート8501)
- **環境変数**: PYTHONPATH, PYTHONUNBUFFERED
- **ヘルスチェック**: /health エンドポイント

### 🧠 AI・機械学習技術の詳細

#### **LangChain フレームワーク**
- **PromptTemplate**: 動的プロンプト生成
- **ConversationBufferMemory**: 会話履歴管理
- **Chain**: 複数のLLM呼び出しの連鎖（将来拡張用）

#### **llama.cpp 推論エンジン**
- **GGUF形式**: 効率的なモデル量子化
- **CPU推論**: GPUなしでの高速推論
- **メモリ最適化**: 大型モデルの効率的な実行

#### **RAG（Retrieval-Augmented Generation）準備**
**現在実装済み**:
- `chromadb`: ベクトルデータベース
- `sentence-transformers`: 文埋め込みモデル

**将来の拡張計画**:
```python
# RAG実装例（準備済み）
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

# ベクトルストア初期化
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(embedding_function=embeddings)

# 関連情報検索
relevant_docs = vectorstore.similarity_search(query, k=3)
```

### 🔬 テストファイル群

#### **test_main.py** - モックAPIサーバー
**役割**: llama-cpp-python依存なしのテスト環境
**技術**: FastAPI + モックデータ

#### **test_real_llm.py** - 実LLMテスト
**役割**: 実際のLLMモデルでの動作確認
**テスト項目**: ヘルスチェック、プロット生成、キャラクター管理

#### **test_real_llm_extended.py** - 拡張テスト
**役割**: 包括的な機能テスト
**特徴**: タイムアウト延長、詳細ログ出力

## 🚀 クイックスタート

### 1. 依存関係のインストール
```bash
pip install -r requirement.txt
```

### 2. APIサーバー起動
```bash
python main.py
```

### 3. UIサーバー起動（別ターミナル）
```bash
streamlit run ui.py --server.port 8501
```

### 4. アクセス
- UI: http://localhost:8501
- API: http://localhost:8000

## 🧪 テスト実行

### 完全テスト
```bash
python test_real_llm_extended.py
```

### 基本テスト
```bash
python test_real_llm.py
```

## 📋 API エンドポイント

### プロット生成
- `POST /generate` - 単一プロット生成
- `POST /generate/multiple` - 複数案生成

### キャラクター管理
- `GET /characters` - 全キャラクター取得
- `POST /characters` - キャラクター追加
- `GET /characters/{name}` - 特定キャラクター取得
- `PUT /characters/{name}` - キャラクター更新
- `DELETE /characters/{name}` - キャラクター削除

### システム
- `GET /health` - ヘルスチェック
- `GET /genres` - 利用可能ジャンル一覧
- `GET /memory/conversation` - 会話履歴取得
- `DELETE /memory/conversation` - 会話履歴クリア

## 🎨 使用例

### 基本的なプロット生成
```python
import requests

data = {
    "prompt": "魔法学校に通う少女が、古い図書館で禁断の魔法書を見つける物語",
    "genre": "fantasy",
    "max_tokens": 512,
    "temperature": 0.7
}

response = requests.post("http://localhost:8000/generate", json=data)
plot = response.json()["response"]
```

### キャラクター付きプロット生成
```python
# キャラクター追加
char_data = {
    "name": "エリナ",
    "description": "17歳の魔法学校の優等生",
    "traits": ["知的", "好奇心旺盛", "慎重"]
}
requests.post("http://localhost:8000/characters", json=char_data)

# キャラクター情報を使用したプロット生成
plot_data = {
    "prompt": "禁断の魔法書を見つけた少女の物語",
    "genre": "fantasy",
    "character_names": ["エリナ"]
}
response = requests.post("http://localhost:8000/generate", json=plot_data)
```

## 🔧 カスタマイズ

### 新しいジャンルの追加
`prompt_templates.py`に新しいテンプレートを追加：

```python
"new_genre": PromptTemplate(
    input_variables=["user_input", "character_memory"],
    template="あなたのカスタムプロンプト..."
)
```

### モデルの変更
`llama_engine.py`でモデルパスを変更：

```python
model_file = "models/your-model.gguf"
```

## 🚀 デプロイ

### Render.com
```bash
# render.ymlが設定済み
git push origin main
```

### ローカル本番環境
```bash
# API
uvicorn main:app --host 0.0.0.0 --port 8000

# UI
streamlit run ui.py --server.port 8501 --server.address 0.0.0.0
```

## 📊 パフォーマンス

- **モデルサイズ**: 8.4GB（Q4_K_M量子化）
- **初回生成時間**: 30秒〜3分（モデル読み込み含む）
- **通常生成時間**: 5〜30秒
- **メモリ使用量**: 約10GB RAM推奨

## 🤝 貢献

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 ライセンス

MIT License

## 🙏 謝辞

- **DeepSeek**: 高品質な日本語LLMモデル
- **LangChain**: AI アプリケーションフレームワーク
- **llama.cpp**: 効率的なLLM推論エンジン
- **Streamlit**: 美しいWebアプリケーションフレームワーク
- **FastAPI**: 高速なWeb APIフレームワーク

---

**PlotWeaver** - あなたの創作活動を支援する、実用的なAIツールです。🎭✨ 