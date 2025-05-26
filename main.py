from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os

# 環境変数チェック
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

if TEST_MODE:
    # テストモード: モックデータを使用
    print("🧪 テストモードで起動中...")
    app = FastAPI(title="PlotWeaver API", description="創作支援AI API - テストモード")
    
    # モックレスポンス用の関数
    def mock_generate(prompt, **kwargs):
        return f"【テストモード】{prompt}に基づく生成されたプロット例です。実際のLLMモデルは使用されていません。"
    
    class MockEngine:
        def is_ready(self): return True
        def generate(self, prompt, **kwargs): return mock_generate(prompt, **kwargs)
        @property
        def model_path(self): return "テストモード（モックデータ）"
    
    llama_engine = MockEngine()
else:
    # 本格モード: 実際のLLMを使用
    print("🚀 本格モードで起動中...")
    from llama_engine import llama_engine
    app = FastAPI(title="PlotWeaver API", description="創作支援AI API - 本格モード")

# 共通モジュール
from prompt_templates import plot_templates
from memory_manager import character_memory

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

@app.get("/")
async def root():
    return {
        "message": "PlotWeaver API へようこそ！",
        "status": "running",
        "model_ready": llama_engine.is_ready(),
        "model_path": llama_engine.model_path if llama_engine.is_ready() else "モデル未読み込み",
        "note": "実際のLLMモデルを使用しています。"
    }

@app.get("/health")
async def health_check():
    try:
        return {
            "status": "healthy",
            "model_ready": llama_engine.is_ready(),
            "available_genres": plot_templates.get_available_genres(),
            "model_info": {
                "path": llama_engine.model_path,
                "loaded": llama_engine.is_ready()
            },
            "test_mode": TEST_MODE
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "test_mode": TEST_MODE
        }

@app.post("/generate")
async def generate_plot(request: PlotGenerationRequest):
    """
    ジャンル別プロット生成
    """
    try:
        if not llama_engine.is_ready():
            raise HTTPException(status_code=503, detail="モデルが初期化されていません")
        
        # キャラクター記憶を取得
        character_memory_str = character_memory.get_character_memory_string(request.character_names)
        
        # プロンプトテンプレートを取得
        template = plot_templates.get_template(request.genre)
        
        # プロンプトを生成
        formatted_prompt = template.format(
            user_input=request.prompt,
            character_memory=character_memory_str
        )
        
        # テキスト生成
        response = llama_engine.generate(
            formatted_prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # 会話履歴に追加
        character_memory.add_conversation(request.prompt, response)
        
        return {
            "response": response,
            "genre": request.genre,
            "character_memory_used": character_memory_str != "キャラクター情報なし",
            "model_used": True,
            "model_path": llama_engine.model_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成エラー: {str(e)}")

@app.post("/generate/multiple")
async def generate_multiple_plots(request: MultipleGenerationRequest):
    """
    複数のプロット案を生成
    """
    try:
        if not llama_engine.is_ready():
            raise HTTPException(status_code=503, detail="モデルが初期化されていません")
        
        variations = []
        character_memory_str = character_memory.get_character_memory_string(request.character_names)
        template = plot_templates.get_template(request.genre)
        
        for i in range(request.num_variations):
            # 温度を少しずつ変えて多様性を確保
            temperature = 0.6 + (i * 0.1)
            
            formatted_prompt = template.format(
                user_input=f"{request.prompt} (バリエーション{i+1})",
                character_memory=character_memory_str
            )
            
            response = llama_engine.generate(
                formatted_prompt,
                max_tokens=400,
                temperature=temperature
            )
            
            variations.append({
                "variation": i + 1,
                "response": response,
                "temperature": temperature
            })
        
        return {
            "variations": variations,
            "genre": request.genre,
            "total_variations": len(variations),
            "model_used": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"複数生成エラー: {str(e)}")

@app.get("/genres")
async def get_genres():
    """
    利用可能なジャンル一覧を取得
    """
    return {
        "genres": plot_templates.get_available_genres(),
        "display_names": plot_templates.get_genre_display_names()
    }

@app.post("/characters")
async def add_character(request: CharacterRequest):
    """
    新しいキャラクターを追加
    """
    try:
        character_memory.add_character(
            name=request.name,
            description=request.description,
            traits=request.traits,
            background=request.background,
            relationships=request.relationships
        )
        
        return {
            "message": f"キャラクター '{request.name}' が追加されました",
            "character": character_memory.get_character_info(request.name)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"キャラクター追加エラー: {str(e)}")

@app.get("/characters")
async def get_characters():
    """
    全キャラクター情報を取得
    """
    return {
        "characters": character_memory.get_all_characters(),
        "total_count": len(character_memory.get_all_characters())
    }

@app.get("/characters/{character_name}")
async def get_character(character_name: str):
    """
    特定のキャラクター情報を取得
    """
    character = character_memory.get_character_info(character_name)
    if not character:
        raise HTTPException(status_code=404, detail="キャラクターが見つかりません")
    
    return {
        "name": character_name,
        "character": character
    }

@app.put("/characters/{character_name}")
async def update_character(character_name: str, request: CharacterRequest):
    """
    キャラクター情報を更新
    """
    if character_name not in character_memory.get_all_characters():
        raise HTTPException(status_code=404, detail="キャラクターが見つかりません")
    
    try:
        character_memory.update_character(
            character_name,
            description=request.description,
            traits=request.traits,
            background=request.background,
            relationships=request.relationships
        )
        
        return {
            "message": f"キャラクター '{character_name}' が更新されました",
            "character": character_memory.get_character_info(character_name)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"キャラクター更新エラー: {str(e)}")

@app.delete("/characters/{character_name}")
async def delete_character(character_name: str):
    """
    キャラクターを削除
    """
    if character_name not in character_memory.get_all_characters():
        raise HTTPException(status_code=404, detail="キャラクターが見つかりません")
    
    try:
        del character_memory.characters[character_name]
        character_memory._save_memory()
        
        return {"message": f"キャラクター '{character_name}' が削除されました"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"キャラクター削除エラー: {str(e)}")

@app.get("/memory/conversation")
async def get_conversation_history():
    """
    会話履歴を取得
    """
    return {
        "recent_conversation": character_memory.get_recent_conversation(10),
        "total_messages": len(character_memory.conversation_memory.chat_memory.messages)
    }

@app.delete("/memory/conversation")
async def clear_conversation_history():
    """
    会話履歴をクリア
    """
    character_memory.clear_conversation_history()
    return {"message": "会話履歴がクリアされました"}

@app.post("/characters/{character_name}/development")
async def add_character_development(character_name: str, development: dict):
    """
    キャラクターの成長記録を追加
    """
    if character_name not in character_memory.get_all_characters():
        raise HTTPException(status_code=404, detail="キャラクターが見つかりません")
    
    try:
        character_memory.add_character_development(
            character_name, 
            development.get("note", "")
        )
        
        return {
            "message": f"キャラクター '{character_name}' の成長記録が追加されました",
            "character": character_memory.get_character_info(character_name)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"成長記録追加エラー: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
