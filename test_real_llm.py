#!/usr/bin/env python3
"""
実際のLLMモデルテストスクリプト
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_health():
    """ヘルスチェック"""
    print("🔍 ヘルスチェック...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ ヘルスチェック成功!")
            print(f"   ステータス: {data.get('status')}")
            print(f"   モデル準備: {data.get('model_ready')}")
            print(f"   テストモード: {data.get('test_mode', 'なし')}")
            print(f"   利用可能ジャンル: {len(data.get('available_genres', []))}個")
            return True
        else:
            print(f"❌ ヘルスチェック失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ヘルスチェックエラー: {e}")
        return False

def test_plot_generation():
    """実際のプロット生成テスト"""
    print("\n📖 実際のLLMプロット生成テスト...")
    try:
        data = {
            "prompt": "魔法学校に通う少女が、古い図書館で禁断の魔法書を見つける物語",
            "genre": "fantasy",
            "max_tokens": 200,
            "temperature": 0.7
        }
        
        print("   リクエスト送信中...")
        response = requests.post(f"{API_BASE_URL}/generate", json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ プロット生成成功!")
            print(f"   ジャンル: {result.get('genre')}")
            print(f"   実際のモデル使用: {result.get('model_used', False)}")
            print(f"   モデルパス: {result.get('model_path', 'なし')}")
            print(f"   生成されたプロット:")
            print("   " + "="*50)
            plot_text = result.get('response', '')
            print(f"   {plot_text}")
            print("   " + "="*50)
            return True
        else:
            print(f"❌ プロット生成失敗: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return False
    except Exception as e:
        print(f"❌ プロット生成エラー: {e}")
        return False

def main():
    """メインテスト実行"""
    print("🚀 実際のLLMモデルテスト開始")
    print("="*60)
    
    # ヘルスチェック
    if not test_health():
        print("❌ APIサーバーに接続できません")
        return
    
    # プロット生成テスト
    print("\n⏳ LLMモデルでのプロット生成を開始します...")
    print("   ※ 初回生成は時間がかかる場合があります")
    
    if test_plot_generation():
        print("\n🎉 実際のLLMモデルでのプロット生成が成功しました！")
        print("💡 Streamlit UI にアクセス: http://localhost:8501")
        print("💡 API ドキュメント: http://localhost:8000/docs")
    else:
        print("\n⚠️ プロット生成に失敗しました")
    
    print("="*60)

if __name__ == "__main__":
    main() 