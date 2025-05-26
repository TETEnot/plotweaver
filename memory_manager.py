"""
メモリ管理 - キャラクター情報と会話履歴の管理
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from langchain.memory import ConversationBufferMemory

class CharacterMemoryManager:
    def __init__(self, memory_file: str = "character_memory.json"):
        self.memory_file = memory_file
        self.characters = {}
        self.conversation_memory = ConversationBufferMemory(return_messages=True)
        self._load_memory()
    
    def _load_memory(self):
        """メモリファイルから情報を読み込み"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.characters = data.get('characters', {})
                    print(f"✅ キャラクター情報を読み込みました: {len(self.characters)}人")
            else:
                print("📝 新しいキャラクターメモリファイルを作成します")
        except Exception as e:
            print(f"⚠️ メモリ読み込みエラー: {e}")
            self.characters = {}
    
    def _save_memory(self):
        """メモリファイルに情報を保存"""
        try:
            data = {
                'characters': self.characters,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ メモリ保存エラー: {e}")
    
    def add_character(self, name: str, description: str, traits: List[str] = None, 
                     background: str = "", relationships: Dict[str, str] = None):
        """新しいキャラクターを追加"""
        self.characters[name] = {
            "description": description,
            "traits": traits or [],
            "background": background,
            "relationships": relationships or {},
            "story_appearances": [],
            "development_notes": [],
            "created_at": datetime.now().isoformat()
        }
        self._save_memory()
        print(f"✅ キャラクター '{name}' を追加しました")
    
    def update_character(self, name: str, description: str = None, traits: List[str] = None,
                        background: str = None, relationships: Dict[str, str] = None):
        """キャラクター情報を更新"""
        if name not in self.characters:
            raise ValueError(f"キャラクター '{name}' が見つかりません")
        
        if description is not None:
            self.characters[name]["description"] = description
        if traits is not None:
            self.characters[name]["traits"] = traits
        if background is not None:
            self.characters[name]["background"] = background
        if relationships is not None:
            self.characters[name]["relationships"] = relationships
        
        self.characters[name]["updated_at"] = datetime.now().isoformat()
        self._save_memory()
    
    def get_character_info(self, name: str) -> Optional[Dict[str, Any]]:
        """特定のキャラクター情報を取得"""
        return self.characters.get(name)
    
    def get_all_characters(self) -> Dict[str, Any]:
        """全キャラクター情報を取得"""
        return self.characters
    
    def get_character_memory_string(self, character_names: List[str] = None) -> str:
        """キャラクター情報を文字列形式で取得"""
        if not character_names:
            return "キャラクター情報なし"
        
        memory_parts = []
        for name in character_names:
            if name in self.characters:
                char = self.characters[name]
                char_info = f"【{name}】\n"
                char_info += f"説明: {char['description']}\n"
                
                if char['traits']:
                    char_info += f"特徴: {', '.join(char['traits'])}\n"
                
                if char['background']:
                    char_info += f"背景: {char['background']}\n"
                
                if char['relationships']:
                    relationships = [f"{k}: {v}" for k, v in char['relationships'].items()]
                    char_info += f"関係性: {', '.join(relationships)}\n"
                
                memory_parts.append(char_info)
        
        return "\n".join(memory_parts) if memory_parts else "キャラクター情報なし"
    
    def add_story_appearance(self, character_name: str, story_title: str, role: str = ""):
        """キャラクターの物語出演記録を追加"""
        if character_name in self.characters:
            appearance = {
                "story_title": story_title,
                "role": role,
                "date": datetime.now().isoformat()
            }
            self.characters[character_name]["story_appearances"].append(appearance)
            self._save_memory()
    
    def add_character_development(self, character_name: str, development_note: str):
        """キャラクターの成長記録を追加"""
        if character_name in self.characters:
            development = {
                "note": development_note,
                "date": datetime.now().isoformat()
            }
            self.characters[character_name]["development_notes"].append(development)
            self._save_memory()
    
    def add_conversation(self, user_input: str, ai_response: str):
        """会話履歴に追加"""
        self.conversation_memory.chat_memory.add_user_message(user_input)
        self.conversation_memory.chat_memory.add_ai_message(ai_response)
    
    def get_recent_conversation(self, num_messages: int = 10) -> str:
        """最近の会話履歴を取得"""
        messages = self.conversation_memory.chat_memory.messages
        recent_messages = messages[-num_messages:] if len(messages) > num_messages else messages
        
        conversation_text = []
        for message in recent_messages:
            if hasattr(message, 'type'):
                if message.type == 'human':
                    conversation_text.append(f"ユーザー: {message.content}")
                elif message.type == 'ai':
                    conversation_text.append(f"AI: {message.content}")
        
        return "\n".join(conversation_text)
    
    def clear_conversation_history(self):
        """会話履歴をクリア"""
        self.conversation_memory.clear()
    
    def get_character_relationships(self, character_name: str) -> Dict[str, str]:
        """キャラクターの関係性を取得"""
        if character_name in self.characters:
            return self.characters[character_name].get("relationships", {})
        return {}
    
    def add_character_relationship(self, character_name: str, related_character: str, relationship: str):
        """キャラクター間の関係性を追加"""
        if character_name in self.characters:
            self.characters[character_name]["relationships"][related_character] = relationship
            self._save_memory()
    
    def search_characters_by_trait(self, trait: str) -> List[str]:
        """特定の特徴を持つキャラクターを検索"""
        matching_characters = []
        for name, char_data in self.characters.items():
            if trait.lower() in [t.lower() for t in char_data.get("traits", [])]:
                matching_characters.append(name)
        return matching_characters
    
    def get_character_statistics(self) -> Dict[str, Any]:
        """キャラクター統計情報を取得"""
        total_characters = len(self.characters)
        total_appearances = sum(len(char.get("story_appearances", [])) for char in self.characters.values())
        
        trait_counts = {}
        for char in self.characters.values():
            for trait in char.get("traits", []):
                trait_counts[trait] = trait_counts.get(trait, 0) + 1
        
        return {
            "total_characters": total_characters,
            "total_story_appearances": total_appearances,
            "most_common_traits": sorted(trait_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "characters_with_relationships": len([c for c in self.characters.values() if c.get("relationships")])
        }

# グローバルインスタンス
character_memory = CharacterMemoryManager() 