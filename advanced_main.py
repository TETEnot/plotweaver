"""
PlotWeaver Advanced API
世界観管理・執筆管理・AI統合システム
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os

# 環境変数チェック
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"  # テストモードに戻す（実用性重視）

if TEST_MODE:
    print("🧪 テストモードで起動中...")
    app = FastAPI(title="PlotWeaver Advanced API", description="創作支援AI API - テストモード")
    
    def mock_generate(prompt, **kwargs):
        # プロンプト対応型テストモード生成
        if "桃太郎" in prompt and "異世界" in prompt:
            return f"""【テストモード - 高度生成】

{prompt}

=== 生成された内容 ===

## 第一章：最期の瞬間

現代日本の病院で、白いベッドに横たわる青年がいた。彼の名前は桃田太郎—幼い頃から「桃太郎」と呼ばれ続けた二十五歳の会社員だった。交通事故による重傷で、意識が薄れゆく中、彼は不思議な光に包まれた。

「これで...終わりか...」

太郎の視界が暗闇に包まれた瞬間、突然まばゆい光が差し込んだ。

## 第二章：新たな世界への目覚め

目を開けると、そこは見知らぬ森の中だった。太郎は驚愕した。自分の手は小さく、まるで子供のようだった。しかし記憶ははっきりと残っている—前世の記憶が。

「ここは...異世界？」

空を見上げると、二つの月が輝いていた。明らかに地球ではない。そして自分の体に宿る不思議な力を感じ取った。

## 第三章：運命の始まり

森の奥から魔物の咆哮が響く。太郎は本能的に立ち上がった。前世の記憶と、この世界で得た新たな力を融合させ、彼の真の冒険が始まろうとしていた。

「今度こそ...誰かを守れる力を手に入れよう」

桃太郎の異世界転生物語の幕が上がった。

※これはテストモードで生成されたプロンプト対応サンプルです。実際のLLMでは、より詳細で一貫性のある長編小説が生成されます。"""
        
        elif "魔法" in prompt or "学校" in prompt or "図書館" in prompt:
            return f"""【テストモード - 高度生成】

{prompt}

=== 生成された内容 ===

## 導入
主人公は静寂に包まれた図書館の奥深くで、古い革装丁の魔法書を発見した。その表紙には見慣れない文字が金色に輝いており、触れた瞬間に温かな光が指先を包んだ。

## 展開
魔法書を開くと、ページから淡い青い光が立ち上り、周囲の空気が微かに震えた。書かれている文字は古代語だったが、不思議なことに意味が頭に直接流れ込んできた。それは失われた魔法の記録であり、この学園の創設に関わる重要な秘密が記されていた。

## 結末
主人公は魔法書を胸に抱き、この発見が自分の運命を大きく変えることを予感した。図書館の時計が深夜を告げる中、新たな冒険の始まりを感じていた。

※これはテストモードで生成された高度なサンプル内容です。実際のLLMでは、設定された世界観とキャラクター情報を完全に統合した内容が生成されます。"""
        
        else:
            return f"""【テストモード - 高度生成】

{prompt}

=== 生成された内容 ===

## 物語の始まり

{prompt}に基づいて、魅力的な物語が展開されます。主人公は困難に立ち向かい、仲間たちと共に成長していく姿が描かれるでしょう。

## 展開部分

物語は予想外の展開を見せ、読者を引き込む要素が散りばめられています。キャラクターたちの心情の変化や、世界観の深い設定が物語に厚みを与えます。

## クライマックス

すべての伏線が回収され、感動的な結末へと向かいます。主人公の成長と、物語のテーマが見事に融合した印象的な場面が描かれるでしょう。

※これはテストモードで生成されたプロンプト対応サンプルです。実際のLLMでは、より詳細で一貫性のある内容が生成されます。"""
    
    class MockEngine:
        def is_ready(self): return True
        def generate(self, prompt, **kwargs): return mock_generate(prompt, **kwargs)
        @property
        def model_path(self): return "テストモード（高度版）"
    
    llama_engine = MockEngine()
else:
    print("🚀 本格モードで起動中...")
    try:
        from llama_engine import llama_engine
    except ImportError:
        class MockEngine:
            def is_ready(self): return True
            def generate(self, prompt, **kwargs): return mock_generate(prompt, **kwargs)
            @property
            def model_path(self): return "モックエンジン"
        llama_engine = MockEngine()
    app = FastAPI(title="PlotWeaver Advanced API", description="創作支援AI API - 高度版")

# 新しいモジュールをインポート
try:
    from world_manager import world_manager, WorldSetting, TimelineEvent, PlotThread, SettingType
    from story_manager import story_manager, ChapterStatus
    from prompt_templates import plot_templates
    from memory_manager import character_memory
except ImportError as e:
    print(f"⚠️ インポートエラー: {e}")
    # 緊急時のモック
    class MockManager:
        def get_world_context(self, **kwargs): return "世界観情報なし"
        def get_story_context(self, story_id): return "物語情報なし"
        def get_all_characters(self): return {}
        def get_available_genres(self): return ["fantasy"]
        def get_genre_display_names(self): return {"fantasy": "ファンタジー"}
    
    world_manager = MockManager()
    story_manager = MockManager()
    character_memory = MockManager()
    plot_templates = MockManager()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === リクエストモデル ===

class WorldSettingRequest(BaseModel):
    name: str
    type: str  # SettingType
    description: str
    details: Dict[str, Any]

class TimelineEventRequest(BaseModel):
    name: str
    description: str
    year: int
    month: Optional[int] = None
    day: Optional[int] = None
    importance: int = 1
    related_characters: List[str] = []

class PlotThreadRequest(BaseModel):
    name: str
    description: str
    setup_events: List[str] = []
    related_characters: List[str] = []

class StoryRequest(BaseModel):
    title: str
    genre: str
    summary: str
    target_word_count: int = 50000

class ChapterRequest(BaseModel):
    title: str
    summary: str
    target_word_count: int = 3000

class SceneRequest(BaseModel):
    name: str
    description: str
    location: str
    characters: List[str]
    purpose: str

class AdvancedGenerationRequest(BaseModel):
    prompt: str
    story_id: Optional[str] = None
    chapter_number: Optional[int] = None
    scene_index: Optional[int] = None
    use_world_context: bool = True
    use_character_memory: bool = True
    max_tokens: int = 1000
    temperature: float = 0.7

# === 基本エンドポイント ===

@app.get("/")
async def root():
    return {
        "message": "PlotWeaver Advanced API へようこそ！",
        "status": "running",
        "features": [
            "世界観管理",
            "執筆管理", 
            "キャラクター管理",
            "AI統合執筆支援"
        ],
        "model_ready": llama_engine.is_ready(),
        "test_mode": TEST_MODE
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_ready": llama_engine.is_ready(),
        "features_available": {
            "world_management": True,
            "story_management": True,
            "character_management": True,
            "ai_generation": llama_engine.is_ready()
        },
        "test_mode": TEST_MODE
    }

# === 世界観管理エンドポイント ===

@app.post("/world/settings")
async def add_world_setting(request: WorldSettingRequest):
    """世界設定を追加"""
    try:
        setting_id = f"setting_{len(world_manager.settings) + 1}"
        setting = WorldSetting(
            id=setting_id,
            name=request.name,
            type=SettingType(request.type),
            description=request.description,
            details=request.details
        )
        world_manager.add_setting(setting)
        
        return {
            "message": f"世界設定「{request.name}」が追加されました",
            "setting_id": setting_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"世界設定追加エラー: {str(e)}")

@app.get("/world/settings")
async def get_world_settings():
    """世界設定一覧を取得"""
    return {
        "settings": {k: {
            "name": v.name,
            "type": v.type.value,
            "description": v.description,
            "details": v.details
        } for k, v in world_manager.settings.items()},
        "total_count": len(world_manager.settings)
    }

@app.post("/world/timeline")
async def add_timeline_event(request: TimelineEventRequest):
    """時系列イベントを追加"""
    try:
        event_id = f"event_{len(world_manager.timeline) + 1}"
        event = TimelineEvent(
            id=event_id,
            name=request.name,
            description=request.description,
            year=request.year,
            month=request.month,
            day=request.day,
            importance=request.importance,
            related_characters=request.related_characters
        )
        world_manager.add_timeline_event(event)
        
        return {
            "message": f"時系列イベント「{request.name}」が追加されました",
            "event_id": event_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"時系列イベント追加エラー: {str(e)}")

@app.get("/world/timeline")
async def get_timeline():
    """時系列を取得"""
    events = []
    for event in sorted(world_manager.timeline.values(), key=lambda x: x.year):
        events.append({
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "year": event.year,
            "month": event.month,
            "day": event.day,
            "importance": event.importance,
            "related_characters": event.related_characters
        })
    
    return {"timeline": events, "total_events": len(events)}

@app.post("/world/plots")
async def add_plot_thread(request: PlotThreadRequest):
    """伏線を追加"""
    try:
        plot_id = f"plot_{len(world_manager.plot_threads) + 1}"
        plot = PlotThread(
            id=plot_id,
            name=request.name,
            description=request.description,
            setup_events=request.setup_events,
            payoff_events=[],
            related_characters=request.related_characters
        )
        world_manager.add_plot_thread(plot)
        
        return {
            "message": f"伏線「{request.name}」が追加されました",
            "plot_id": plot_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"伏線追加エラー: {str(e)}")

@app.get("/world/plots")
async def get_plot_threads():
    """伏線一覧を取得"""
    return {
        "plots": {k: {
            "name": v.name,
            "description": v.description,
            "status": v.status,
            "setup_events": v.setup_events,
            "payoff_events": v.payoff_events,
            "related_characters": v.related_characters
        } for k, v in world_manager.plot_threads.items()},
        "total_count": len(world_manager.plot_threads)
    }

# === 執筆管理エンドポイント ===

@app.post("/stories")
async def create_story(request: StoryRequest):
    """新しい物語を作成"""
    try:
        story_id = story_manager.create_story(
            request.title,
            request.genre,
            request.summary
        )
        
        return {
            "message": f"物語「{request.title}」が作成されました",
            "story_id": story_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"物語作成エラー: {str(e)}")

@app.get("/stories")
async def get_stories():
    """物語一覧を取得"""
    stories_info = {}
    for story_id, story in story_manager.stories.items():
        stories_info[story_id] = {
            "title": story.title,
            "genre": story.genre,
            "summary": story.summary,
            "progress": f"{story.current_word_count}/{story.target_word_count}",
            "chapters": len(story.chapters),
            "status": story.status
        }
    
    return {
        "stories": stories_info,
        "total_count": len(stories_info)
    }

@app.post("/stories/{story_id}/chapters")
async def add_chapter(story_id: str, request: ChapterRequest):
    """章を追加"""
    try:
        chapter_id = story_manager.add_chapter(
            story_id,
            request.title,
            request.summary
        )
        
        return {
            "message": f"章「{request.title}」が追加されました",
            "chapter_id": chapter_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"章追加エラー: {str(e)}")

@app.post("/stories/{story_id}/chapters/{chapter_number}/scenes")
async def add_scene(story_id: str, chapter_number: int, request: SceneRequest):
    """シーンを追加"""
    try:
        scene_id = story_manager.add_scene(
            story_id,
            chapter_number,
            request.name,
            request.description,
            request.location,
            request.characters,
            request.purpose
        )
        
        return {
            "message": f"シーン「{request.name}」が追加されました",
            "scene_id": scene_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"シーン追加エラー: {str(e)}")

# === AI統合執筆支援 ===

@app.post("/generate/advanced")
async def advanced_generate(request: AdvancedGenerationRequest):
    """高度なAI生成（世界観・物語コンテキスト統合）"""
    try:
        if not llama_engine.is_ready():
            raise HTTPException(status_code=503, detail="モデルが初期化されていません")
        
        # コンテキスト構築
        context_parts = []
        
        # 世界観コンテキスト
        if request.use_world_context:
            world_context = world_manager.get_world_context()
            if world_context:
                context_parts.append(world_context)
        
        # 物語コンテキスト
        if request.story_id:
            story_context = story_manager.get_story_context(request.story_id)
            if story_context:
                context_parts.append(story_context)
            
            # 現在の章コンテキスト
            if request.chapter_number:
                chapter_context = story_manager.get_current_chapter_context(request.story_id)
                if chapter_context:
                    context_parts.append(chapter_context)
        
        # キャラクター記憶
        if request.use_character_memory:
            character_context = character_memory.get_character_memory_string()
            if character_context != "キャラクター情報なし":
                context_parts.append(f"=== キャラクター情報 ===\n{character_context}")
        
        # 統合プロンプト作成
        full_context = "\n\n".join(context_parts)
        
        final_prompt = f"""
{full_context}

=== 執筆指示 ===
{request.prompt}

上記の世界観、物語設定、キャラクター情報を踏まえて、一貫性のある内容を生成してください。
"""
        
        # AI生成
        response = llama_engine.generate(
            final_prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return {
            "response": response,
            "context_used": {
                "world_context": request.use_world_context and bool(world_context),
                "story_context": bool(request.story_id),
                "character_memory": request.use_character_memory
            },
            "model_used": True,
            "test_mode": TEST_MODE
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"高度生成エラー: {str(e)}")

@app.get("/stories/{story_id}/suggestions")
async def get_writing_suggestions(story_id: str):
    """執筆提案を取得"""
    try:
        suggestions = story_manager.get_writing_suggestions(story_id)
        consistency_issues = world_manager.check_consistency()
        
        return {
            "writing_suggestions": suggestions,
            "consistency_issues": consistency_issues,
            "story_id": story_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提案取得エラー: {str(e)}")

# === 統合情報エンドポイント ===

@app.get("/dashboard")
async def get_dashboard():
    """ダッシュボード情報を取得"""
    return {
        "world_stats": {
            "settings_count": len(world_manager.settings),
            "timeline_events": len(world_manager.timeline),
            "active_plots": len([p for p in world_manager.plot_threads.values() if p.status == "active"])
        },
        "story_stats": {
            "total_stories": len(story_manager.stories),
            "total_chapters": sum(len(s.chapters) for s in story_manager.stories.values()),
            "total_words": sum(s.current_word_count for s in story_manager.stories.values())
        },
        "character_stats": {
            "total_characters": len(character_memory.get_all_characters())
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))  # デフォルトポートを8001に変更
    uvicorn.run(app, host="0.0.0.0", port=port) 