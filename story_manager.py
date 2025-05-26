"""
執筆管理システム
- 章立て管理
- 執筆進捗追跡
- 一貫性チェック
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ChapterStatus(Enum):
    PLANNED = "planned"      # 計画中
    OUTLINE = "outline"      # アウトライン作成済み
    DRAFTING = "drafting"    # 執筆中
    DRAFT = "draft"          # 初稿完了
    REVISION = "revision"    # 推敲中
    COMPLETED = "completed"  # 完成

@dataclass
class Scene:
    """シーン（場面）"""
    id: str
    name: str
    description: str
    location: str
    characters: List[str]
    purpose: str  # このシーンの目的
    content: str = ""  # 実際の文章
    word_count: int = 0
    notes: str = ""
    plot_threads: List[str] = None  # 関連する伏線
    
    def __post_init__(self):
        if self.plot_threads is None:
            self.plot_threads = []
        if self.content:
            self.word_count = len(self.content)

@dataclass
class Chapter:
    """章"""
    id: str
    number: int
    title: str
    summary: str
    scenes: List[Scene]
    status: ChapterStatus = ChapterStatus.PLANNED
    target_word_count: int = 3000
    actual_word_count: int = 0
    notes: str = ""
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at
        self._update_word_count()
    
    def _update_word_count(self):
        """実際の文字数を更新"""
        self.actual_word_count = sum(scene.word_count for scene in self.scenes)

@dataclass
class Story:
    """物語全体"""
    id: str
    title: str
    genre: str
    summary: str
    chapters: List[Chapter]
    target_word_count: int = 50000
    current_word_count: int = 0
    status: str = "planning"
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at
        self._update_word_count()
    
    def _update_word_count(self):
        """総文字数を更新"""
        self.current_word_count = sum(chapter.actual_word_count for chapter in self.chapters)

class StoryManager:
    """執筆管理システム"""
    
    def __init__(self, data_dir: str = "story_data"):
        self.data_dir = data_dir
        self.stories_file = os.path.join(data_dir, "stories.json")
        
        # ディレクトリ作成
        os.makedirs(data_dir, exist_ok=True)
        
        # データ読み込み
        self.stories: Dict[str, Story] = self._load_stories()
        self.current_story_id: Optional[str] = None
    
    def _load_stories(self) -> Dict[str, Story]:
        """物語データを読み込み"""
        if os.path.exists(self.stories_file):
            try:
                with open(self.stories_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                stories = {}
                for story_id, story_data in data.items():
                    # Chapterオブジェクトを復元
                    chapters = []
                    for chapter_data in story_data.get('chapters', []):
                        # Sceneオブジェクトを復元
                        scenes = []
                        for scene_data in chapter_data.get('scenes', []):
                            scenes.append(Scene(**scene_data))
                        
                        chapter_data['scenes'] = scenes
                        chapter_data['status'] = ChapterStatus(chapter_data['status'])
                        chapters.append(Chapter(**chapter_data))
                    
                    story_data['chapters'] = chapters
                    stories[story_id] = Story(**story_data)
                
                return stories
            except Exception as e:
                print(f"物語データ読み込みエラー: {e}")
        return {}
    
    def save_stories(self):
        """物語データを保存"""
        try:
            # dataclassを辞書に変換（Enumも文字列に変換）
            data = {}
            for story_id, story in self.stories.items():
                story_dict = asdict(story)
                # ChapterStatusをstringに変換
                for chapter in story_dict['chapters']:
                    chapter['status'] = chapter['status'].value
                data[story_id] = story_dict
            
            with open(self.stories_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"物語データ保存エラー: {e}")
    
    def create_story(self, title: str, genre: str, summary: str) -> str:
        """新しい物語を作成"""
        story_id = f"story_{len(self.stories) + 1}_{int(datetime.now().timestamp())}"
        story = Story(
            id=story_id,
            title=title,
            genre=genre,
            summary=summary,
            chapters=[]
        )
        self.stories[story_id] = story
        self.current_story_id = story_id
        self.save_stories()
        return story_id
    
    def add_chapter(self, story_id: str, title: str, summary: str) -> str:
        """章を追加"""
        if story_id not in self.stories:
            raise ValueError(f"物語 {story_id} が見つかりません")
        
        story = self.stories[story_id]
        chapter_number = len(story.chapters) + 1
        chapter_id = f"{story_id}_chapter_{chapter_number}"
        
        chapter = Chapter(
            id=chapter_id,
            number=chapter_number,
            title=title,
            summary=summary,
            scenes=[]
        )
        
        story.chapters.append(chapter)
        story.updated_at = datetime.now().isoformat()
        self.save_stories()
        return chapter_id
    
    def add_scene(self, story_id: str, chapter_number: int, name: str, 
                  description: str, location: str, characters: List[str], purpose: str) -> str:
        """シーンを追加"""
        if story_id not in self.stories:
            raise ValueError(f"物語 {story_id} が見つかりません")
        
        story = self.stories[story_id]
        if chapter_number > len(story.chapters):
            raise ValueError(f"章 {chapter_number} が見つかりません")
        
        chapter = story.chapters[chapter_number - 1]
        scene_id = f"{chapter.id}_scene_{len(chapter.scenes) + 1}"
        
        scene = Scene(
            id=scene_id,
            name=name,
            description=description,
            location=location,
            characters=characters,
            purpose=purpose
        )
        
        chapter.scenes.append(scene)
        story.updated_at = datetime.now().isoformat()
        self.save_stories()
        return scene_id
    
    def update_scene_content(self, story_id: str, chapter_number: int, 
                           scene_index: int, content: str):
        """シーンの内容を更新"""
        story = self.stories[story_id]
        chapter = story.chapters[chapter_number - 1]
        scene = chapter.scenes[scene_index]
        
        scene.content = content
        scene.word_count = len(content)
        chapter._update_word_count()
        story._update_word_count()
        story.updated_at = datetime.now().isoformat()
        self.save_stories()
    
    def get_story_context(self, story_id: str) -> str:
        """AIに渡す物語コンテキストを生成"""
        if story_id not in self.stories:
            return ""
        
        story = self.stories[story_id]
        context_parts = []
        
        context_parts.append(f"=== 物語: {story.title} ===")
        context_parts.append(f"ジャンル: {story.genre}")
        context_parts.append(f"あらすじ: {story.summary}")
        context_parts.append(f"進捗: {story.current_word_count}/{story.target_word_count}文字")
        context_parts.append("")
        
        # 章構成
        context_parts.append("=== 章構成 ===")
        for chapter in story.chapters:
            context_parts.append(f"第{chapter.number}章: {chapter.title}")
            context_parts.append(f"  概要: {chapter.summary}")
            context_parts.append(f"  状態: {chapter.status.value}")
            context_parts.append(f"  進捗: {chapter.actual_word_count}/{chapter.target_word_count}文字")
            
            # シーン一覧
            if chapter.scenes:
                context_parts.append("  シーン:")
                for i, scene in enumerate(chapter.scenes, 1):
                    context_parts.append(f"    {i}. {scene.name} ({scene.location})")
                    context_parts.append(f"       目的: {scene.purpose}")
                    if scene.content:
                        context_parts.append(f"       文字数: {scene.word_count}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def get_current_chapter_context(self, story_id: str) -> str:
        """現在執筆中の章のコンテキストを取得"""
        story = self.stories[story_id]
        
        # 執筆中の章を探す
        current_chapter = None
        for chapter in story.chapters:
            if chapter.status in [ChapterStatus.DRAFTING, ChapterStatus.OUTLINE]:
                current_chapter = chapter
                break
        
        if not current_chapter:
            # 最新の章を取得
            current_chapter = story.chapters[-1] if story.chapters else None
        
        if not current_chapter:
            return ""
        
        context_parts = []
        context_parts.append(f"=== 現在の章: 第{current_chapter.number}章 {current_chapter.title} ===")
        context_parts.append(f"概要: {current_chapter.summary}")
        context_parts.append("")
        
        # 既存のシーン内容
        for i, scene in enumerate(current_chapter.scenes, 1):
            context_parts.append(f"【シーン{i}: {scene.name}】")
            context_parts.append(f"場所: {scene.location}")
            context_parts.append(f"登場人物: {', '.join(scene.characters)}")
            context_parts.append(f"目的: {scene.purpose}")
            if scene.content:
                context_parts.append("内容:")
                context_parts.append(scene.content)
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def get_writing_suggestions(self, story_id: str) -> List[str]:
        """執筆のための提案を生成"""
        story = self.stories[story_id]
        suggestions = []
        
        # 進捗チェック
        if story.current_word_count < story.target_word_count * 0.1:
            suggestions.append("物語の導入部分をもっと詳しく描写しましょう")
        elif story.current_word_count < story.target_word_count * 0.5:
            suggestions.append("キャラクターの関係性を深く掘り下げましょう")
        elif story.current_word_count < story.target_word_count * 0.8:
            suggestions.append("クライマックスに向けて緊張感を高めましょう")
        else:
            suggestions.append("結末に向けて伏線を回収していきましょう")
        
        # 章の状態チェック
        for chapter in story.chapters:
            if chapter.status == ChapterStatus.PLANNED:
                suggestions.append(f"第{chapter.number}章のアウトラインを作成しましょう")
            elif chapter.status == ChapterStatus.OUTLINE:
                suggestions.append(f"第{chapter.number}章の執筆を開始しましょう")
        
        return suggestions

# グローバルインスタンス
story_manager = StoryManager()