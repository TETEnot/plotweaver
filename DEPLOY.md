# 🚀 PlotWeaver Renderデプロイ手順

## 📋 事前準備

### 1. GitHubリポジトリの作成
1. [GitHub](https://github.com)にログイン
2. 「New repository」をクリック
3. リポジトリ名: `plotweaver`
4. 「Public」を選択（Renderの無料プランでは必須）
5. 「Create repository」をクリック

### 2. ローカルからGitHubへプッシュ
```bash
# リモートリポジトリを追加
git remote add origin https://github.com/YOUR_USERNAME/plotweaver.git

# メインブランチに変更
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

## 🌐 Renderでのデプロイ

### 1. Renderアカウント作成
1. [Render](https://render.com)にアクセス
2. 「Get Started」をクリック
3. GitHubアカウントでサインアップ

### 2. APIサーバーのデプロイ
1. Renderダッシュボードで「New +」→「Web Service」
2. GitHubリポジトリを接続
3. 設定:
   - **Name**: `plotweaver-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirement.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Starter` (月$7、無料プランでは8.4GBモデルは厳しい)

4. 環境変数設定:
   ```
   PYTHONPATH=.
   PYTHONUNBUFFERED=1
   TEST_MODE=true
   MODEL_PATH=""
   ```

5. 「Create Web Service」をクリック

### 3. UIサーバーのデプロイ
1. 再度「New +」→「Web Service」
2. 同じGitHubリポジトリを選択
3. 設定:
   - **Name**: `plotweaver-ui`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirement.txt`
   - **Start Command**: `streamlit run ui.py --server.port $PORT --server.address 0.0.0.0`
   - **Plan**: `Free`

4. 環境変数設定:
   ```
   PYTHONPATH=.
   PYTHONUNBUFFERED=1
   API_BASE_URL=https://plotweaver-api.onrender.com
   ```

5. 「Create Web Service」をクリック

## ⚠️ 重要な制限事項

### 無料プラン制限
- **メモリ**: 512MB（8.4GBモデルは不可）
- **CPU**: 0.1 CPU
- **スリープ**: 15分間非アクティブで自動スリープ

### 推奨対策
1. **テストモード運用**: 初期は`TEST_MODE=true`で運用
2. **外部API使用**: OpenAI API、Anthropic Claude API等を検討
3. **軽量モデル**: 1GB以下のGGUFモデルに変更
4. **有料プラン**: Starterプラン（月$7）以上を検討

## 🔧 本番運用のための修正

### 1. 外部API使用（推奨）
```python
# llama_engine.py を修正
import openai

class OpenAIEngine:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate(self, prompt, **kwargs):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 512),
            temperature=kwargs.get("temperature", 0.7)
        )
        return response.choices[0].message.content
```

### 2. 軽量モデル使用
```bash
# 1GB以下のモデルをダウンロード
wget https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/pytorch_model.bin
```

## 📊 デプロイ後の確認

### 1. APIサーバー確認
```bash
curl https://plotweaver-api.onrender.com/health
```

### 2. UIアクセス
```
https://plotweaver-ui.onrender.com
```

### 3. ログ確認
- Renderダッシュボード → サービス → 「Logs」タブ

## 🚀 継続的デプロイ

### 自動デプロイ設定
1. GitHubにプッシュすると自動でRenderにデプロイ
2. `render.yml`の変更は自動反映
3. 環境変数の変更は手動で設定

### 更新手順
```bash
# ローカルで変更
git add .
git commit -m "機能追加: 新機能"
git push origin main

# Renderで自動デプロイ開始
```

## 💡 トラブルシューティング

### よくある問題
1. **メモリ不足**: モデルサイズを削減
2. **ビルド失敗**: requirement.txtの依存関係確認
3. **スリープ**: 有料プランまたは定期的なアクセス

### ログ確認方法
```bash
# Renderダッシュボードでログを確認
# または
curl https://plotweaver-api.onrender.com/health
```

## 🎯 次のステップ

1. **カスタムドメイン**: 独自ドメインの設定
2. **HTTPS証明書**: 自動で提供される
3. **モニタリング**: Renderの監視機能を活用
4. **スケーリング**: 有料プランでのスケールアップ

---

**注意**: 8.4GBのLLMモデルは無料プランでは動作しません。テストモードまたは外部API使用を推奨します。 