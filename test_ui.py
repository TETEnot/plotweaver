import streamlit as st
import requests
import json
from typing import Dict, List, Optional
import time

# ページ設定
st.set_page_config(
    page_title="PlotWeaver - 創作支援AI (テストモード)",
    page_icon="📚",
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
    }
    .test-mode-banner {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        color: #856404;
    }
    .plot-output {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API設定
API_BASE_URL = "http://localhost:8000"

def check_api_health():
    """APIの健康状態をチェック"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except:
        return False, None

def get_genres():
    """利用可能なジャンルを取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/genres")
        if response.status_code == 200:
            return response.json()
        return {"genres": ["fantasy"], "display_names": {"fantasy": "ファンタジー"}}
    except:
        return {"genres": ["fantasy"], "display_names": {"fantasy": "ファンタジー"}}

def generate_plot(prompt: str, genre: str, character_names: List[str] = None, 
                 max_tokens: int = 512, temperature: float = 0.7):
    """プロット生成"""
    try:
        data = {
            "prompt": prompt,
            "genre": genre,
            "character_names": character_names,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        response = requests.post(f"{API_BASE_URL}/generate", json=data, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def generate_multiple_plots(prompt: str, genre: str, num_variations: int = 3, 
                          character_names: List[str] = None):
    """複数のプロット案を生成"""
    try:
        data = {
            "prompt": prompt,
            "genre": genre,
            "num_variations": num_variations,
            "character_names": character_names
        }
        response = requests.post(f"{API_BASE_URL}/generate/multiple", json=data, timeout=60)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_characters():
    """キャラクター一覧を取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/characters")
        if response.status_code == 200:
            return response.json()
        return {"characters": {}, "total_count": 0}
    except:
        return {"characters": {}, "total_count": 0}

def add_character(name: str, description: str, traits: List[str] = None, 
                 background: str = "", relationships: Dict[str, str] = None):
    """キャラクターを追加"""
    try:
        data = {
            "name": name,
            "description": description,
            "traits": traits or [],
            "background": background,
            "relationships": relationships or {}
        }
        response = requests.post(f"{API_BASE_URL}/characters", json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# メインアプリケーション
def main():
    # ヘッダー
    st.markdown('<h1 class="main-header">📚 PlotWeaver - 創作支援AI</h1>', unsafe_allow_html=True)
    
    # テストモードバナー
    st.markdown("""
    <div class="test-mode-banner">
        🧪 <strong>テストモード</strong> - 実際のLLMは使用されていません。モックデータでの動作確認中です。
    </div>
    """, unsafe_allow_html=True)
    
    # API健康状態チェック
    api_healthy, health_data = check_api_health()
    if not api_healthy:
        st.error("⚠️ APIサーバーに接続できません。サーバーが起動していることを確認してください。")
        st.info("💡 バックエンドを起動するには: `python test_main.py` を実行してください")
        st.stop()
    else:
        if health_data and health_data.get("test_mode"):
            st.success("✅ APIサーバーに接続しました（テストモード）")
        else:
            st.success("✅ APIサーバーに接続しました")
    
    # サイドバー
    with st.sidebar:
        st.header("🎛️ 設定")
        
        # ジャンル選択
        genres_data = get_genres()
        genre_options = genres_data.get("display_names", {})
        selected_genre_display = st.selectbox(
            "📖 ジャンル選択",
            options=list(genre_options.values()),
            help="生成したいプロットのジャンルを選択してください"
        )
        
        # 表示名から内部名に変換
        selected_genre = None
        for key, value in genre_options.items():
            if value == selected_genre_display:
                selected_genre = key
                break
        
        # 生成パラメータ
        st.subheader("⚙️ 生成パラメータ")
        max_tokens = st.slider("最大トークン数", 256, 1024, 512, help="生成するテキストの長さ")
        temperature = st.slider("創造性", 0.1, 1.0, 0.7, help="高いほど創造的だが不安定")
        
        # キャラクター管理
        st.subheader("👥 キャラクター管理")
        characters_data = get_characters()
        characters = characters_data.get("characters", {})
        
        if characters:
            selected_characters = st.multiselect(
                "使用するキャラクター",
                options=list(characters.keys()),
                help="プロット生成に使用するキャラクターを選択"
            )
        else:
            selected_characters = []
            st.info("キャラクターが登録されていません")
    
    # メインコンテンツ
    tab1, tab2, tab3 = st.tabs(["🎯 プロット生成", "👥 キャラクター管理", "📊 複数案生成"])
    
    with tab1:
        st.header("🎯 プロット生成")
        
        # プロンプト入力
        prompt = st.text_area(
            "プロット生成プロンプトを入力してください",
            height=150,
            placeholder="例: 魔法学校に通う少女が、古い図書館で禁断の魔法書を見つける物語",
            help="具体的な設定や要素を含めると、より詳細なプロットが生成されます"
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("🎭 プロット生成", type="primary", use_container_width=True):
                if prompt:
                    with st.spinner("プロットを生成中..."):
                        result = generate_plot(
                            prompt, 
                            selected_genre, 
                            selected_characters,
                            max_tokens,
                            temperature
                        )
                    
                    if "error" in result:
                        st.error(f"エラー: {result['error']}")
                    else:
                        st.success("✅ プロット生成完了！")
                        
                        # 結果表示
                        st.markdown('<div class="plot-output">', unsafe_allow_html=True)
                        st.markdown("### 📖 生成されたプロット")
                        st.markdown(result.get("response", ""))
                        
                        # メタ情報
                        col_meta1, col_meta2, col_meta3 = st.columns(3)
                        with col_meta1:
                            st.info(f"ジャンル: {selected_genre_display}")
                        with col_meta2:
                            memory_used = result.get("character_memory_used", False)
                            st.info(f"キャラクター記憶: {'使用' if memory_used else '未使用'}")
                        with col_meta3:
                            if result.get("test_mode"):
                                st.warning("テストモード")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # セッション状態に保存
                        st.session_state.last_generated_plot = result.get("response", "")
                else:
                    st.warning("プロンプトを入力してください")
        
        with col2:
            if st.button("🔄 サンプル", use_container_width=True):
                sample_prompts = {
                    "fantasy": "魔法の力を失った元勇者が、新たな仲間と共に世界を救う冒険",
                    "romance": "幼馴染との再会から始まる、運命的な恋愛物語",
                    "mystery": "密室で起きた不可解な殺人事件の真相を追う探偵",
                    "sci_fi": "AIが支配する未来世界で、人間性を取り戻そうとする反乱軍",
                    "horror": "古い洋館に住む一家を襲う、超常現象の恐怖",
                    "slice_of_life": "小さな町のカフェで働く青年の、心温まる日常",
                    "adventure": "失われた宝を求めて、危険な秘境を冒険する探検家"
                }
                st.text_area(
                    "サンプルプロンプト",
                    value=sample_prompts.get(selected_genre, sample_prompts["fantasy"]),
                    height=100,
                    key="sample_prompt"
                )
    
    with tab2:
        st.header("👥 キャラクター管理")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("➕ 新しいキャラクター追加")
            
            with st.form("add_character_form"):
                char_name = st.text_input("キャラクター名", placeholder="例: 田中太郎")
                char_description = st.text_area("説明", placeholder="例: 16歳の高校生。明るく元気な性格で...")
                char_traits = st.text_input("特徴 (カンマ区切り)", placeholder="例: 勇敢, 優しい, 頑固")
                char_background = st.text_area("背景", placeholder="例: 小さな村で生まれ育ち...")
                
                if st.form_submit_button("キャラクター追加", type="primary"):
                    if char_name and char_description:
                        traits_list = [trait.strip() for trait in char_traits.split(",") if trait.strip()]
                        result = add_character(char_name, char_description, traits_list, char_background)
                        
                        if "error" in result:
                            st.error(f"エラー: {result['error']}")
                        else:
                            st.success(f"✅ キャラクター '{char_name}' を追加しました！")
                            if result.get("test_mode"):
                                st.info("💡 テストモードでは、キャラクターはセッション中のみ保存されます")
                            st.rerun()
                    else:
                        st.warning("名前と説明は必須です")
        
        with col2:
            st.subheader("📋 登録済みキャラクター")
            
            if characters:
                for char_name, char_data in characters.items():
                    with st.expander(f"👤 {char_name}"):
                        st.write(f"**説明:** {char_data.get('description', '')}")
                        if char_data.get('traits'):
                            st.write(f"**特徴:** {', '.join(char_data['traits'])}")
                        if char_data.get('background'):
                            st.write(f"**背景:** {char_data['background']}")
                        if char_data.get('story_appearances'):
                            st.write(f"**出演作品数:** {len(char_data['story_appearances'])}")
            else:
                st.info("まだキャラクターが登録されていません")
    
    with tab3:
        st.header("📊 複数案生成")
        
        st.write("同じプロンプトから複数のバリエーションを生成します")
        
        multi_prompt = st.text_area(
            "プロンプト",
            height=100,
            placeholder="複数のバリエーションを生成したいプロンプトを入力"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            num_variations = st.slider("生成数", 2, 5, 3)
        with col2:
            if st.button("🎲 複数案生成", type="primary", use_container_width=True):
                if multi_prompt:
                    with st.spinner(f"{num_variations}つのバリエーションを生成中..."):
                        result = generate_multiple_plots(
                            multi_prompt, 
                            selected_genre, 
                            num_variations,
                            selected_characters
                        )
                    
                    if "error" in result:
                        st.error(f"エラー: {result['error']}")
                    else:
                        st.success("✅ 複数案生成完了！")
                        
                        if result.get("test_mode"):
                            st.info("💡 テストモードでの生成結果です")
                        
                        variations = result.get("variations", [])
                        for i, variation in enumerate(variations):
                            with st.expander(f"📝 バリエーション {variation['variation']} (温度: {variation['temperature']:.1f})"):
                                st.markdown(variation['response'])
                else:
                    st.warning("プロンプトを入力してください")
    
    # フッター
    st.markdown("---")
    st.markdown(
        "🤖 **PlotWeaver (テストモード)** - LangChain & llama.cpp による創作支援AI | "
        "💡 現在はモックデータで動作確認中です"
    )

if __name__ == "__main__":
    main() 