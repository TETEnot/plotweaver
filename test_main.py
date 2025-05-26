from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

app = FastAPI(title="PlotWeaver API (Test Mode)", description="創作支援AI API - テストモード")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストモデル
class PlotGenerationRequest(BaseModel):
    prompt: str
    genre: str = "fantasy"
    character_names: Optional[List[str]] = None
    max_tokens: int = 512
    temperature: float = 0.7

class CharacterRequest(BaseModel):
    name: str
    description: str
    traits: Optional[List[str]] = None
    background: Optional[str] = ""
    relationships: Optional[Dict[str, str]] = None

class MultipleGenerationRequest(BaseModel):
    prompt: str
    genre: str = "fantasy"
    num_variations: int = 3
    character_names: Optional[List[str]] = None

# モックデータ
mock_characters = {}
mock_genres = {
    "fantasy": "ファンタジー",
    "romance": "恋愛",
    "mystery": "ミステリー",
    "sci_fi": "SF",
    "horror": "ホラー",
    "slice_of_life": "日常系",
    "adventure": "冒険"
}

@app.get("/")
async def root():
    return {
        "message": "PlotWeaver API (テストモード) へようこそ！",
        "status": "running",
        "model_ready": True,
        "note": "これはテストモードです。実際のLLMは使用されていません。"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_ready": True,
        "available_genres": list(mock_genres.keys()),
        "test_mode": True
    }

@app.post("/generate")
async def generate_plot(request: PlotGenerationRequest):
    """
    ジャンル別プロット生成（モック版）
    """
    try:
        # モックレスポンス生成
        genre_name = mock_genres.get(request.genre, "ファンタジー")
        
        mock_response = f"""
# {genre_name}プロット: {request.prompt}

## 1. 導入部
{request.prompt}という設定で物語が始まります。主人公は平凡な日常を送っていましたが、ある出来事をきっかけに非日常の世界に足を踏み入れることになります。

## 2. 発端
予期せぬ事件が発生し、主人公は重要な選択を迫られます。この選択が物語全体の方向性を決定づけることになります。

## 3. 展開
主人公は様々な困難に直面しながらも、新たな仲間との出会いや自身の成長を通じて、徐々に問題の核心に近づいていきます。

## 4. 転換点
物語の中盤で大きな試練が待ち受けています。主人公の信念や能力が試される重要な局面です。

## 5. クライマックス
これまでの経験と成長を活かし、主人公は最終的な困難に立ち向かいます。仲間との絆や自身の決意が勝利の鍵となります。

## 6. 結末
問題が解決され、主人公は成長した姿で新たな日常を迎えます。しかし、この経験は彼/彼女の人生に永続的な変化をもたらします。

---
*このプロットは{genre_name}ジャンルのテンプレートに基づいて生成されました。*
*使用されたキャラクター: {', '.join(request.character_names) if request.character_names else 'なし'}*
        """
        
        return {
            "response": mock_response.strip(),
            "genre": request.genre,
            "character_memory_used": bool(request.character_names),
            "test_mode": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成エラー: {str(e)}")

@app.post("/generate/multiple")
async def generate_multiple_plots(request: MultipleGenerationRequest):
    """
    複数のプロット案を生成（モック版）
    """
    try:
        variations = []
        genre_name = mock_genres.get(request.genre, "ファンタジー")
        
        for i in range(request.num_variations):
            temperature = 0.6 + (i * 0.1)
            
            mock_response = f"""
# {genre_name}プロット バリエーション{i+1}: {request.prompt}

## アプローチ{i+1}
このバリエーションでは、{request.prompt}を{['伝統的', '革新的', '実験的'][i % 3]}な手法で描きます。

## 特徴
- 温度設定: {temperature:.1f}
- 創造性レベル: {['安定', '中程度', '高創造性'][i % 3]}
- 物語の焦点: {['キャラクター重視', 'プロット重視', 'テーマ重視'][i % 3]}

## あらすじ
{request.prompt}という設定から始まり、{['予想通りの展開', '意外な展開', '複雑な展開'][i % 3]}を経て、{['ハッピーエンド', 'ビターエンド', 'オープンエンド'][i % 3]}で締めくくられます。

---
*バリエーション{i+1}の特色: {['王道展開', '斬新なアイデア', '深いテーマ性'][i % 3]}*
            """
            
            variations.append({
                "variation": i + 1,
                "response": mock_response.strip(),
                "temperature": temperature
            })
        
        return {
            "variations": variations,
            "genre": request.genre,
            "total_variations": len(variations),
            "test_mode": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"複数生成エラー: {str(e)}")

@app.get("/genres")
async def get_genres():
    """
    利用可能なジャンル一覧を取得
    """
    return {
        "genres": list(mock_genres.keys()),
        "display_names": mock_genres
    }

@app.post("/characters")
async def add_character(request: CharacterRequest):
    """
    新しいキャラクターを追加
    """
    try:
        mock_characters[request.name] = {
            "description": request.description,
            "traits": request.traits or [],
            "background": request.background,
            "relationships": request.relationships or {},
            "story_appearances": [],
            "development_notes": []
        }
        
        return {
            "message": f"キャラクター '{request.name}' が追加されました",
            "character": mock_characters[request.name],
            "test_mode": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"キャラクター追加エラー: {str(e)}")

@app.get("/characters")
async def get_characters():
    """
    全キャラクター情報を取得
    """
    return {
        "characters": mock_characters,
        "total_count": len(mock_characters),
        "test_mode": True
    }

@app.get("/characters/{character_name}")
async def get_character(character_name: str):
    """
    特定のキャラクター情報を取得
    """
    character = mock_characters.get(character_name)
    if not character:
        raise HTTPException(status_code=404, detail="キャラクターが見つかりません")
    
    return {
        "name": character_name,
        "character": character,
        "test_mode": True
    }

@app.get("/memory/conversation")
async def get_conversation_history():
    """
    会話履歴を取得（モック版）
    """
    return {
        "recent_conversation": "テストモードでは会話履歴は保存されません",
        "total_messages": 0,
        "test_mode": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 