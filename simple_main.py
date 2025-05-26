from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

# 環境変数チェック
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"

app = FastAPI(title="PlotWeaver API", description="創作支援AI API - シンプル版")

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

@app.get("/")
async def root():
    return {
        "message": "PlotWeaver API へようこそ！",
        "status": "running",
        "model_ready": True,
        "model_path": "テストモード（シンプル版）",
        "test_mode": TEST_MODE
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_ready": True,
        "available_genres": ["fantasy", "romance", "mystery", "sci_fi", "horror", "slice_of_life", "adventure"],
        "model_info": {
            "path": "テストモード（シンプル版）",
            "loaded": True
        },
        "test_mode": TEST_MODE
    }

@app.get("/genres")
async def get_genres():
    return {
        "genres": ["fantasy", "romance", "mystery", "sci_fi", "horror", "slice_of_life", "adventure"],
        "display_names": {
            "fantasy": "ファンタジー",
            "romance": "恋愛",
            "mystery": "ミステリー",
            "sci_fi": "SF",
            "horror": "ホラー",
            "slice_of_life": "日常系",
            "adventure": "冒険"
        }
    }

@app.post("/generate")
async def generate_plot(request: PlotGenerationRequest):
    """シンプルなプロット生成"""
    mock_plot = f"""
【テストモード - {request.genre}】

{request.prompt}に基づく生成されたプロット：

## 導入部
主人公が日常から非日常へと導かれる場面。{request.prompt}の設定が明らかになる。

## 発端
物語の中心となる出来事が発生。主人公が行動を起こすきっかけとなる。

## 展開
困難や障害に直面しながらも、主人公が成長していく過程。

## 転換点
物語の重要な転換点。新たな真実や重要な決断が迫られる。

## クライマックス
最大の試練と対決。これまでの成長が試される場面。

## 結末
問題の解決と主人公の成長の確認。新たな日常への回帰。

※これはテストモードで生成されたサンプルプロットです。
"""
    
    return {
        "response": mock_plot.strip(),
        "genre": request.genre,
        "character_memory_used": bool(request.character_names),
        "model_used": True,
        "model_path": "テストモード（シンプル版）",
        "test_mode": TEST_MODE
    }

@app.get("/characters")
async def get_characters():
    return {
        "characters": {},
        "total_count": 0
    }

@app.post("/characters")
async def add_character(character_data: dict):
    return {
        "message": f"キャラクター '{character_data.get('name', 'Unknown')}' が追加されました（テストモード）",
        "character": character_data
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 