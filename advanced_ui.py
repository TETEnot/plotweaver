import streamlit as st
import requests
import json
from typing import Dict, List, Optional
import time

# ページ設定
st.set_page_config(
    page_title="PlotWeaver Advanced - 創作支援プラットフォーム",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .world-setting-card {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    .timeline-event {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
    .plot-thread {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #dc3545;
    }
    .story-card {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #17a2b8;
    }
    .dashboard-metric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        border: 2px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# API設定
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")  # 高度版APIのポート

def check_api_health():
    """APIの健康状態をチェック"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200, response.json()
    except:
        return False, {}

def get_dashboard_data():
    """ダッシュボードデータを取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard")
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

# === 世界観管理関数 ===

def add_world_setting(name: str, setting_type: str, description: str, details: dict):
    """世界設定を追加"""
    try:
        data = {
            "name": name,
            "type": setting_type,
            "description": description,
            "details": details
        }
        response = requests.post(f"{API_BASE_URL}/world/settings", json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_world_settings():
    """世界設定一覧を取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/world/settings")
        if response.status_code == 200:
            return response.json()
        return {"settings": {}, "total_count": 0}
    except:
        return {"settings": {}, "total_count": 0}

def add_timeline_event(name: str, description: str, year: int, importance: int, characters: List[str]):
    """時系列イベントを追加"""
    try:
        data = {
            "name": name,
            "description": description,
            "year": year,
            "importance": importance,
            "related_characters": characters
        }
        response = requests.post(f"{API_BASE_URL}/world/timeline", json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_timeline():
    """時系列を取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/world/timeline")
        if response.status_code == 200:
            return response.json()
        return {"timeline": [], "total_events": 0}
    except:
        return {"timeline": [], "total_events": 0}

# === 執筆管理関数 ===

def create_story(title: str, genre: str, summary: str, target_words: int):
    """物語を作成"""
    try:
        data = {
            "title": title,
            "genre": genre,
            "summary": summary,
            "target_word_count": target_words
        }
        response = requests.post(f"{API_BASE_URL}/stories", json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_stories():
    """物語一覧を取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/stories")
        if response.status_code == 200:
            return response.json()
        return {"stories": {}, "total_count": 0}
    except:
        return {"stories": {}, "total_count": 0}

def advanced_generate(prompt: str, story_id: str = None, use_world: bool = True, use_characters: bool = True):
    """高度なAI生成"""
    try:
        data = {
            "prompt": prompt,
            "story_id": story_id,
            "use_world_context": use_world,
            "use_character_memory": use_characters,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        response = requests.post(f"{API_BASE_URL}/generate/advanced", json=data, timeout=300)  # 5分に延長
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# メインアプリケーション
def main():
    # ヘッダー
    st.markdown('<h1 class="main-header">🌟 PlotWeaver Advanced</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">世界観管理から執筆まで完結する創作支援プラットフォーム</p>', unsafe_allow_html=True)
    
    # API健康状態チェック
    api_healthy, health_data = check_api_health()
    if not api_healthy:
        st.error("⚠️ APIサーバーに接続できません。")
        st.stop()
    else:
        features = health_data.get("features_available", {})
        st.success(f"✅ PlotWeaver Advanced API に接続しました")
        
        # 機能状態表示
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status = "🟢" if features.get("world_management") else "🔴"
            st.info(f"{status} 世界観管理")
        with col2:
            status = "🟢" if features.get("story_management") else "🔴"
            st.info(f"{status} 執筆管理")
        with col3:
            status = "🟢" if features.get("character_management") else "🔴"
            st.info(f"{status} キャラクター管理")
        with col4:
            status = "🟢" if features.get("ai_generation") else "🔴"
            st.info(f"{status} AI生成")
    
    # サイドバー
    with st.sidebar:
        st.header("🎛️ ナビゲーション")
        
        # ダッシュボードデータ
        dashboard = get_dashboard_data()
        if dashboard:
            st.subheader("📊 統計情報")
            
            world_stats = dashboard.get("world_stats", {})
            story_stats = dashboard.get("story_stats", {})
            char_stats = dashboard.get("character_stats", {})
            
            st.metric("世界設定", world_stats.get("settings_count", 0))
            st.metric("時系列イベント", world_stats.get("timeline_events", 0))
            st.metric("物語数", story_stats.get("total_stories", 0))
            st.metric("総文字数", story_stats.get("total_words", 0))
    
    # メインタブ
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 ダッシュボード", 
        "🌍 世界観管理", 
        "📚 執筆管理", 
        "🤖 AI執筆支援",
        "👥 キャラクター管理"
    ])
    
    with tab1:
        st.header("🏠 ダッシュボード")
        
        # 機能紹介カード
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>🌍 世界観管理</h3>
                <p>地理、歴史、文化、魔法体系などの設定を体系的に管理。時系列イベントや伏線も追跡可能。</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3>📚 執筆管理</h3>
                <p>章立てからシーン構成まで段階的に管理。進捗追跡と一貫性チェック機能付き。</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>🤖 AI執筆支援</h3>
                <p>世界観とキャラクター情報を理解したAIが、一貫性のある内容を生成。</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3>👥 キャラクター管理</h3>
                <p>詳細なプロフィールと関係性を管理。AIが記憶して自然な行動を生成。</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 統計情報詳細
        if dashboard:
            st.subheader("📈 詳細統計")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🌍 世界観")
                world_stats = dashboard.get("world_stats", {})
                st.markdown(f"""
                <div class="dashboard-metric">
                    <h4>{world_stats.get('settings_count', 0)}</h4>
                    <p>世界設定</p>
                </div>
                <div class="dashboard-metric">
                    <h4>{world_stats.get('timeline_events', 0)}</h4>
                    <p>歴史イベント</p>
                </div>
                <div class="dashboard-metric">
                    <h4>{world_stats.get('active_plots', 0)}</h4>
                    <p>アクティブな伏線</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 📚 執筆")
                story_stats = dashboard.get("story_stats", {})
                st.markdown(f"""
                <div class="dashboard-metric">
                    <h4>{story_stats.get('total_stories', 0)}</h4>
                    <p>物語数</p>
                </div>
                <div class="dashboard-metric">
                    <h4>{story_stats.get('total_chapters', 0)}</h4>
                    <p>総章数</p>
                </div>
                <div class="dashboard-metric">
                    <h4>{story_stats.get('total_words', 0):,}</h4>
                    <p>総文字数</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("### 👥 キャラクター")
                char_stats = dashboard.get("character_stats", {})
                st.markdown(f"""
                <div class="dashboard-metric">
                    <h4>{char_stats.get('total_characters', 0)}</h4>
                    <p>登録キャラクター</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.header("🌍 世界観管理")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("➕ 新しい世界設定")
            
            with st.form("world_setting_form"):
                setting_name = st.text_input("設定名", placeholder="例: エルフの森")
                setting_type = st.selectbox("種類", [
                    "geography", "history", "culture", "magic", 
                    "technology", "politics", "religion", "economy"
                ])
                setting_description = st.text_area("説明", placeholder="詳細な説明を入力...")
                
                # 詳細設定
                st.subheader("詳細設定")
                detail_key = st.text_input("項目名", placeholder="例: 人口")
                detail_value = st.text_input("値", placeholder="例: 約10万人")
                
                if st.form_submit_button("世界設定を追加", type="primary"):
                    if setting_name and setting_description:
                        details = {}
                        if detail_key and detail_value:
                            details[detail_key] = detail_value
                        
                        result = add_world_setting(setting_name, setting_type, setting_description, details)
                        
                        if "error" in result:
                            st.error(f"エラー: {result['error']}")
                        else:
                            st.success(f"✅ 世界設定「{setting_name}」を追加しました！")
                            st.rerun()
                    else:
                        st.warning("設定名と説明は必須です")
            
            st.subheader("⏰ 時系列イベント追加")
            
            with st.form("timeline_form"):
                event_name = st.text_input("イベント名", placeholder="例: 魔王の復活")
                event_description = st.text_area("説明", placeholder="イベントの詳細...")
                event_year = st.number_input("年", min_value=1, value=1000)
                event_importance = st.slider("重要度", 1, 5, 3)
                
                if st.form_submit_button("イベントを追加", type="primary"):
                    if event_name and event_description:
                        result = add_timeline_event(event_name, event_description, event_year, event_importance, [])
                        
                        if "error" in result:
                            st.error(f"エラー: {result['error']}")
                        else:
                            st.success(f"✅ イベント「{event_name}」を追加しました！")
                            st.rerun()
                    else:
                        st.warning("イベント名と説明は必須です")
        
        with col2:
            st.subheader("📋 登録済み世界設定")
            
            settings_data = get_world_settings()
            settings = settings_data.get("settings", {})
            
            if settings:
                for setting_id, setting in settings.items():
                    st.markdown(f"""
                    <div class="world-setting-card">
                        <h4>🏛️ {setting['name']}</h4>
                        <p><strong>種類:</strong> {setting['type']}</p>
                        <p>{setting['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("まだ世界設定が登録されていません")
            
            st.subheader("📅 時系列")
            
            timeline_data = get_timeline()
            timeline = timeline_data.get("timeline", [])
            
            if timeline:
                for event in timeline:
                    importance_stars = "⭐" * event['importance']
                    st.markdown(f"""
                    <div class="timeline-event">
                        <h4>📅 {event['year']}年: {event['name']}</h4>
                        <p><strong>重要度:</strong> {importance_stars}</p>
                        <p>{event['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("まだ時系列イベントが登録されていません")
    
    with tab3:
        st.header("📚 執筆管理")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📖 新しい物語を作成")
            
            with st.form("story_form"):
                story_title = st.text_input("物語のタイトル", placeholder="例: 魔法学園の秘密")
                story_genre = st.selectbox("ジャンル", [
                    "fantasy", "romance", "mystery", "sci_fi", 
                    "horror", "slice_of_life", "adventure"
                ])
                story_summary = st.text_area("あらすじ", placeholder="物語の概要を入力...")
                target_words = st.number_input("目標文字数", min_value=1000, value=50000, step=1000)
                
                if st.form_submit_button("物語を作成", type="primary"):
                    if story_title and story_summary:
                        result = create_story(story_title, story_genre, story_summary, target_words)
                        
                        if "error" in result:
                            st.error(f"エラー: {result['error']}")
                        else:
                            st.success(f"✅ 物語「{story_title}」を作成しました！")
                            st.session_state.current_story_id = result.get("story_id")
                            st.rerun()
                    else:
                        st.warning("タイトルとあらすじは必須です")
        
        with col2:
            st.subheader("📚 作成済み物語")
            
            stories_data = get_stories()
            stories = stories_data.get("stories", {})
            
            if stories:
                for story_id, story in stories.items():
                    st.markdown(f"""
                    <div class="story-card">
                        <h4>📖 {story['title']}</h4>
                        <p><strong>ジャンル:</strong> {story['genre']}</p>
                        <p><strong>進捗:</strong> {story['progress']} 文字</p>
                        <p><strong>章数:</strong> {story['chapters']} 章</p>
                        <p>{story['summary']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"「{story['title']}」を選択", key=f"select_{story_id}"):
                        st.session_state.current_story_id = story_id
                        st.success(f"物語「{story['title']}」を選択しました")
            else:
                st.info("まだ物語が作成されていません")
    
    with tab4:
        st.header("🤖 AI執筆支援")
        
        # 現在選択中の物語表示
        current_story = st.session_state.get("current_story_id")
        if current_story:
            st.info(f"📖 選択中の物語: {current_story}")
        else:
            st.warning("物語を選択してください（執筆管理タブから選択）")
        
        st.subheader("✍️ 高度なAI生成")
        
        # 生成設定
        col1, col2 = st.columns([2, 1])
        
        with col1:
            prompt = st.text_area(
                "執筆指示",
                height=150,
                placeholder="例: 主人公が魔法学校の図書館で古い魔法書を発見するシーンを詳しく描写してください",
                help="世界観とキャラクター情報を考慮した内容が生成されます"
            )
        
        with col2:
            st.subheader("🎛️ 生成オプション")
            use_world_context = st.checkbox("世界観情報を使用", value=True)
            use_character_memory = st.checkbox("キャラクター記憶を使用", value=True)
            
            if current_story:
                use_story_context = st.checkbox("物語コンテキストを使用", value=True)
            else:
                use_story_context = False
                st.info("物語を選択すると物語コンテキストが利用できます")
        
        if st.button("🎭 AI執筆支援を実行", type="primary", use_container_width=True):
            if prompt:
                with st.spinner("AIが執筆中..."):
                    result = advanced_generate(
                        prompt, 
                        current_story if use_story_context else None,
                        use_world_context,
                        use_character_memory
                    )
                
                if "error" in result:
                    st.error(f"エラー: {result['error']}")
                else:
                    st.success("✅ AI執筆完了！")
                    
                    # 結果表示
                    st.markdown("### 📝 生成された内容")
                    st.markdown(result.get("response", ""))
                    
                    # テストモード表示
                    if result.get("test_mode"):
                        st.info("🧪 テストモードで生成されました（高速処理）")
                    
                    # 使用されたコンテキスト情報
                    context_used = result.get("context_used", {})
                    st.markdown("### ℹ️ 使用されたコンテキスト")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        status = "✅" if context_used.get("world_context") else "❌"
                        st.info(f"{status} 世界観情報")
                    with col2:
                        status = "✅" if context_used.get("story_context") else "❌"
                        st.info(f"{status} 物語コンテキスト")
                    with col3:
                        status = "✅" if context_used.get("character_memory") else "❌"
                        st.info(f"{status} キャラクター記憶")
                    
                    # セッション状態に保存
                    st.session_state.last_generated_content = result.get("response", "")
            else:
                st.warning("執筆指示を入力してください")
        
        # 生成履歴
        if 'last_generated_content' in st.session_state:
            st.subheader("📄 最後に生成された内容")
            st.text_area("内容", st.session_state.last_generated_content, height=200, disabled=True)
            
            if st.button("📋 クリップボードにコピー"):
                st.code(st.session_state.last_generated_content)
                st.success("コピー用のテキストを表示しました")
    
    with tab5:
        st.header("👥 キャラクター管理")
        st.info("キャラクター管理機能は既存のシステムを使用します")
        st.markdown("詳細なキャラクター管理は、サイドバーの基本機能をご利用ください。")
    
    # フッター
    st.markdown("---")
    st.markdown(
        "🌟 **PlotWeaver Advanced** - 世界観管理から執筆まで完結する創作支援プラットフォーム | "
        "💡 AIが世界観とキャラクターを理解して、一貫性のある物語を支援します"
    )

if __name__ == "__main__":
    main() 