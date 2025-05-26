"""
世界観管理システム
- 設定データベース
- 時系列管理
- 関係性マップ
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class SettingType(Enum):
    GEOGRAPHY = "geography"  # 地理
    HISTORY = "history"      # 歴史
    CULTURE = "culture"      # 文化
    MAGIC = "magic"          # 魔法体系
    TECHNOLOGY = "technology" # 技術
    POLITICS = "politics"    # 政治
    RELIGION = "religion"    # 宗教
    ECONOMY = "economy"      # 経済

@dataclass
class WorldSetting:
    """世界設定の基本クラス"""
    id: str
    name: str
    type: SettingType
    description: str
    details: Dict[str, Any]
    related_settings: List[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.related_settings is None:
            self.related_settings = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at

@dataclass
class TimelineEvent:
    """時系列イベント"""
    id: str
    name: str
    description: str
    year: int
    month: Optional[int] = None
    day: Optional[int] = None
    importance: int = 1  # 1-5の重要度
    related_characters: List[str] = None
    related_settings: List[str] = None
    consequences: List[str] = None
    
    def __post_init__(self):
        if self.related_characters is None:
            self.related_characters = []
        if self.related_settings is None:
            self.related_settings = []
        if self.consequences is None:
            self.consequences = []

@dataclass
class PlotThread:
    """伏線・プロットライン"""
    id: str
    name: str
    description: str
    setup_events: List[str]  # 仕込みイベント
    payoff_events: List[str]  # 回収イベント
    status: str = "active"  # active, resolved, abandoned
    importance: int = 1
    related_characters: List[str] = None
    
    def __post_init__(self):
        if self.related_characters is None:
            self.related_characters = []

class WorldManager:
    """世界観管理システム"""
    
    def __init__(self, data_dir: str = "world_data"):
        self.data_dir = data_dir
        self.settings_file = os.path.join(data_dir, "world_settings.json")
        self.timeline_file = os.path.join(data_dir, "timeline.json")
        self.plots_file = os.path.join(data_dir, "plot_threads.json")
        
        # ディレクトリ作成
        os.makedirs(data_dir, exist_ok=True)
        
        # データ読み込み
        self.settings: Dict[str, WorldSetting] = self._load_settings()
        self.timeline: Dict[str, TimelineEvent] = self._load_timeline()
        self.plot_threads: Dict[str, PlotThread] = self._load_plot_threads()
    
    def _load_settings(self) -> Dict[str, WorldSetting]:
        """世界設定を読み込み"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return {
                    k: WorldSetting(**v) for k, v in data.items()
                }
            except Exception as e:
                print(f"設定読み込みエラー: {e}")
        return {}
    
    def _load_timeline(self) -> Dict[str, TimelineEvent]:
        """時系列を読み込み"""
        if os.path.exists(self.timeline_file):
            try:
                with open(self.timeline_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return {
                    k: TimelineEvent(**v) for k, v in data.items()
                }
            except Exception as e:
                print(f"時系列読み込みエラー: {e}")
        return {}
    
    def _load_plot_threads(self) -> Dict[str, PlotThread]:
        """伏線を読み込み"""
        if os.path.exists(self.plots_file):
            try:
                with open(self.plots_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return {
                    k: PlotThread(**v) for k, v in data.items()
                }
            except Exception as e:
                print(f"伏線読み込みエラー: {e}")
        return {}
    
    def save_all(self):
        """全データを保存"""
        # 設定保存
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            data = {k: asdict(v) for k, v in self.settings.items()}
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 時系列保存
        with open(self.timeline_file, 'w', encoding='utf-8') as f:
            data = {k: asdict(v) for k, v in self.timeline.items()}
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 伏線保存
        with open(self.plots_file, 'w', encoding='utf-8') as f:
            data = {k: asdict(v) for k, v in self.plot_threads.items()}
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_setting(self, setting: WorldSetting):
        """世界設定を追加"""
        self.settings[setting.id] = setting
        self.save_all()
    
    def add_timeline_event(self, event: TimelineEvent):
        """時系列イベントを追加"""
        self.timeline[event.id] = event
        self.save_all()
    
    def add_plot_thread(self, plot: PlotThread):
        """伏線を追加"""
        self.plot_threads[plot.id] = plot
        self.save_all()
    
    def get_world_context(self, relevant_types: List[SettingType] = None) -> str:
        """AIに渡す世界観コンテキストを生成"""
        context_parts = []
        
        # 世界設定
        context_parts.append("=== 世界設定 ===")
        for setting in self.settings.values():
            if relevant_types is None or setting.type in relevant_types:
                context_parts.append(f"【{setting.name}】({setting.type.value})")
                context_parts.append(setting.description)
                if setting.details:
                    for key, value in setting.details.items():
                        context_parts.append(f"  - {key}: {value}")
                context_parts.append("")
        
        # 重要な時系列イベント
        context_parts.append("=== 重要な歴史 ===")
        important_events = sorted(
            [e for e in self.timeline.values() if e.importance >= 3],
            key=lambda x: x.year
        )
        for event in important_events:
            context_parts.append(f"【{event.year}年】{event.name}")
            context_parts.append(event.description)
            context_parts.append("")
        
        # アクティブな伏線
        context_parts.append("=== アクティブな伏線 ===")
        active_plots = [p for p in self.plot_threads.values() if p.status == "active"]
        for plot in active_plots:
            context_parts.append(f"【{plot.name}】")
            context_parts.append(plot.description)
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def get_character_relevant_context(self, character_names: List[str]) -> str:
        """特定キャラクターに関連する世界観情報を取得"""
        context_parts = []
        
        # キャラクター関連の時系列イベント
        relevant_events = []
        for event in self.timeline.values():
            if any(char in event.related_characters for char in character_names):
                relevant_events.append(event)
        
        if relevant_events:
            context_parts.append("=== 関連する歴史的イベント ===")
            for event in sorted(relevant_events, key=lambda x: x.year):
                context_parts.append(f"【{event.year}年】{event.name}")
                context_parts.append(event.description)
                context_parts.append("")
        
        # キャラクター関連の伏線
        relevant_plots = []
        for plot in self.plot_threads.values():
            if any(char in plot.related_characters for char in character_names):
                relevant_plots.append(plot)
        
        if relevant_plots:
            context_parts.append("=== 関連する伏線 ===")
            for plot in relevant_plots:
                context_parts.append(f"【{plot.name}】({plot.status})")
                context_parts.append(plot.description)
                context_parts.append("")
        
        return "\n".join(context_parts)
    
    def check_consistency(self) -> List[str]:
        """設定の一貫性をチェック"""
        issues = []
        
        # 時系列の矛盾チェック
        events_by_year = {}
        for event in self.timeline.values():
            year = event.year
            if year not in events_by_year:
                events_by_year[year] = []
            events_by_year[year].append(event)
        
        # 伏線の未回収チェック
        for plot in self.plot_threads.values():
            if plot.status == "active" and not plot.payoff_events:
                issues.append(f"伏線「{plot.name}」が未回収です")
        
        return issues

# グローバルインスタンス
world_manager = WorldManager() 