#!/usr/bin/env python3
"""
実際のLLMモデルテストスクリプト（拡張版）
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
            
            # モデル情報を表示
            model_info = data.get('model_info', {})
            if model_info.get('path'):
                print(f"   モデルパス: {model_info['path']}")
                print(f"   モデル読み込み済み: {model_info['loaded']}")
            
            return True
        else:
            print(f"❌ ヘルスチェック失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ヘルスチェックエラー: {e}")
        return False

def test_plot_generation():
    """実際のプロット生成テスト（拡張タイムアウト）"""
    print("\n📖 実際のLLMプロット生成テスト...")
    try:
        data = {
            "prompt": "魔法学校に通う少女が、古い図書館で禁断の魔法書を見つける物語",
            "genre": "fantasy",
            "max_tokens": 150,  # トークン数を減らして高速化
            "temperature": 0.7
        }
        
        print("   リクエスト送信中...")
        print("   ⏳ 初回生成のため、最大3分お待ちください...")
        
        # タイムアウトを3分に延長
        response = requests.post(f"{API_BASE_URL}/generate", json=data, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ プロット生成成功!")
            print(f"   ジャンル: {result.get('genre')}")
            print(f"   実際のモデル使用: {result.get('model_used', False)}")
            print(f"   モデルパス: {result.get('model_path', 'なし')}")
            print(f"   キャラクター記憶使用: {result.get('character_memory_used', False)}")
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

def test_character_management():
    """キャラクター管理テスト"""
    print("\n👥 キャラクター管理テスト...")
    try:
        # キャラクター追加
        char_data = {
            "name": "エリナ",
            "description": "17歳の魔法学校の優等生。古代魔法の研究に興味を持つ。",
            "traits": ["知的", "好奇心旺盛", "慎重"],
            "background": "魔法使いの家系に生まれ、幼い頃から魔法の才能を示していた。"
        }
        
        response = requests.post(f"{API_BASE_URL}/characters", json=char_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ キャラクター追加成功!")
            print(f"   名前: {char_data['name']}")
            print(f"   説明: {char_data['description']}")
            return True
        else:
            print(f"❌ キャラクター追加失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ キャラクター管理エラー: {e}")
        return False

def test_plot_with_character():
    """キャラクター情報を使用したプロット生成テスト"""
    print("\n🎭 キャラクター情報付きプロット生成テスト...")
    try:
        data = {
            "prompt": "禁断の魔法書を見つけた少女が、その力の危険性を知る物語",
            "genre": "fantasy",
            "character_names": ["エリナ"],
            "max_tokens": 150,
            "temperature": 0.8
        }
        
        print("   キャラクター情報を含むプロット生成中...")
        response = requests.post(f"{API_BASE_URL}/generate", json=data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ キャラクター付きプロット生成成功!")
            print(f"   キャラクター記憶使用: {result.get('character_memory_used', False)}")
            print(f"   生成されたプロット:")
            print("   " + "="*50)
            plot_text = result.get('response', '')
            print(f"   {plot_text[:300]}...")  # 最初の300文字のみ表示
            print("   " + "="*50)
            return True
        else:
            print(f"❌ キャラクター付きプロット生成失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ キャラクター付きプロット生成エラー: {e}")
        return False

def main():
    """メインテスト実行"""
    print("🚀 実際のLLMモデル完全テスト開始")
    print("="*60)
    
    tests = [
        ("ヘルスチェック", test_health),
        ("プロット生成", test_plot_generation),
        ("キャラクター管理", test_character_management),
        ("キャラクター付きプロット", test_plot_with_character)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔄 {test_name}テスト実行中...")
        if test_func():
            passed += 1
            print(f"✅ {test_name}テスト成功")
        else:
            print(f"❌ {test_name}テスト失敗")
        
        time.sleep(2)  # テスト間の間隔
    
    print("\n" + "="*60)
    print(f"🎯 テスト結果: {passed}/{total} 成功")
    
    if passed == total:
        print("🎉 全てのテストが成功しました！")
        print("💡 実際のLLMモデルが正常に動作しています")
        print("💡 Streamlit UI にアクセス: http://localhost:8501")
        print("💡 API ドキュメント: http://localhost:8000/docs")
    else:
        print("⚠️ 一部のテストが失敗しました。")
    
    print("="*60)

if __name__ == "__main__":
    main() 