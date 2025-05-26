#!/usr/bin/env python3
"""
PlotWeaver API テストスクリプト
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_health():
    """ヘルスチェックテスト"""
    print("🔍 ヘルスチェックテスト...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ ヘルスチェック成功!")
            print(f"   ステータス: {data.get('status')}")
            print(f"   モデル準備: {data.get('model_ready')}")
            print(f"   テストモード: {data.get('test_mode')}")
            print(f"   利用可能ジャンル: {len(data.get('available_genres', []))}個")
            return True
        else:
            print(f"❌ ヘルスチェック失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ヘルスチェックエラー: {e}")
        return False

def test_genres():
    """ジャンル取得テスト"""
    print("\n🎭 ジャンル取得テスト...")
    try:
        response = requests.get(f"{API_BASE_URL}/genres")
        if response.status_code == 200:
            data = response.json()
            print("✅ ジャンル取得成功!")
            genres = data.get('display_names', {})
            for key, value in genres.items():
                print(f"   {key}: {value}")
            return True
        else:
            print(f"❌ ジャンル取得失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ジャンル取得エラー: {e}")
        return False

def test_plot_generation():
    """プロット生成テスト"""
    print("\n📖 プロット生成テスト...")
    try:
        data = {
            "prompt": "魔法学校に通う少女が、古い図書館で禁断の魔法書を見つける物語",
            "genre": "fantasy",
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        response = requests.post(f"{API_BASE_URL}/generate", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ プロット生成成功!")
            print(f"   ジャンル: {result.get('genre')}")
            print(f"   テストモード: {result.get('test_mode')}")
            print(f"   生成されたプロット:")
            print("   " + "="*50)
            plot_text = result.get('response', '')
            # 最初の200文字だけ表示
            print(f"   {plot_text[:200]}...")
            print("   " + "="*50)
            return True
        else:
            print(f"❌ プロット生成失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ プロット生成エラー: {e}")
        return False

def test_character_management():
    """キャラクター管理テスト"""
    print("\n👥 キャラクター管理テスト...")
    
    # キャラクター追加
    try:
        char_data = {
            "name": "アリス",
            "description": "16歳の魔法学校の生徒。好奇心旺盛で勇敢な性格。",
            "traits": ["勇敢", "好奇心旺盛", "優しい"],
            "background": "小さな村出身で、魔法の才能を持って生まれた。"
        }
        
        response = requests.post(f"{API_BASE_URL}/characters", json=char_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ キャラクター追加成功!")
            print(f"   名前: {char_data['name']}")
            print(f"   説明: {char_data['description']}")
            print(f"   特徴: {', '.join(char_data['traits'])}")
        else:
            print(f"❌ キャラクター追加失敗: {response.status_code}")
            return False
            
        # キャラクター一覧取得
        response = requests.get(f"{API_BASE_URL}/characters")
        if response.status_code == 200:
            result = response.json()
            print("✅ キャラクター一覧取得成功!")
            print(f"   登録キャラクター数: {result.get('total_count')}")
            return True
        else:
            print(f"❌ キャラクター一覧取得失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ キャラクター管理エラー: {e}")
        return False

def test_multiple_generation():
    """複数案生成テスト"""
    print("\n🎲 複数案生成テスト...")
    try:
        data = {
            "prompt": "時間を操る能力を持つ少年の冒険",
            "genre": "sci_fi",
            "num_variations": 3,
            "character_names": ["アリス"]
        }
        
        response = requests.post(f"{API_BASE_URL}/generate/multiple", json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print("✅ 複数案生成成功!")
            print(f"   生成数: {result.get('total_variations')}")
            print(f"   ジャンル: {result.get('genre')}")
            
            variations = result.get('variations', [])
            for i, variation in enumerate(variations[:2]):  # 最初の2つだけ表示
                print(f"   バリエーション{variation['variation']}:")
                print(f"   {variation['response'][:100]}...")
                print()
            return True
        else:
            print(f"❌ 複数案生成失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 複数案生成エラー: {e}")
        return False

def main():
    """メインテスト実行"""
    print("🚀 PlotWeaver API テスト開始")
    print("="*60)
    
    tests = [
        test_health,
        test_genres,
        test_plot_generation,
        test_character_management,
        test_multiple_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
        time.sleep(1)  # テスト間の間隔
    
    print("\n" + "="*60)
    print(f"🎯 テスト結果: {passed}/{total} 成功")
    
    if passed == total:
        print("🎉 全てのテストが成功しました！")
        print("💡 Streamlit UI にアクセス: http://localhost:8501")
        print("💡 API ドキュメント: http://localhost:8000/docs")
    else:
        print("⚠️  一部のテストが失敗しました。")
    
    print("="*60)

if __name__ == "__main__":
    main() 