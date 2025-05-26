"""
LLaMA エンジン - llama.cpp を使用したテキスト生成
"""

import os
from typing import Optional
from llama_cpp import Llama

class LlamaEngine:
    def __init__(self):
        self.model = None
        self.model_path = None
        self._initialize_model()
    
    def _initialize_model(self):
        """モデルを初期化"""
        try:
            # モデルファイルのパスを設定
            model_file = "models/DeepSeek-R1-Distill-Qwen-14B-Japanese-Q4_K_M.gguf"
            
            if not os.path.exists(model_file):
                print(f"⚠️ モデルファイルが見つかりません: {model_file}")
                return
            
            print(f"🔄 モデルを読み込み中: {model_file}")
            print("📝 これには数分かかる場合があります...")
            
            # モデルを読み込み
            self.model = Llama(
                model_path=model_file,
                n_ctx=2048,  # コンテキスト長
                n_threads=4,  # スレッド数
                verbose=False,  # 詳細ログを無効化
                n_gpu_layers=0  # GPU使用しない（CPUのみ）
            )
            
            self.model_path = model_file
            print(f"✅ モデル読み込み完了: {model_file}")
            
        except Exception as e:
            print(f"❌ モデル読み込みエラー: {e}")
            self.model = None
            self.model_path = None
    
    def is_ready(self) -> bool:
        """モデルが使用可能かチェック"""
        return self.model is not None
    
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7, 
                top_p: float = 0.9, stop: Optional[list] = None) -> str:
        """テキストを生成"""
        if not self.is_ready():
            raise RuntimeError("モデルが初期化されていません")
        
        try:
            # プロンプトを日本語対応で調整
            formatted_prompt = f"以下の指示に従って、日本語で創作的なプロットを生成してください。\n\n{prompt}\n\n回答:"
            
            # テキスト生成
            response = self.model(
                formatted_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stop=stop or ["</s>", "<|endoftext|>", "\n\n---"],
                echo=False  # プロンプトを含めない
            )
            
            # 生成されたテキストを取得
            generated_text = response['choices'][0]['text'].strip()
            
            # 不要な部分を除去
            if "回答:" in generated_text:
                generated_text = generated_text.split("回答:")[-1].strip()
            
            return generated_text
            
        except Exception as e:
            raise RuntimeError(f"テキスト生成エラー: {e}")
    
    def get_model_info(self) -> dict:
        """モデル情報を取得"""
        return {
            "model_path": self.model_path,
            "is_ready": self.is_ready(),
            "model_type": "DeepSeek-R1-Distill-Qwen-14B-Japanese-Q4_K_M"
        }

# グローバルインスタンス
llama_engine = LlamaEngine() 