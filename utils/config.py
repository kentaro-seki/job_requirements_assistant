"""OpenAI設定の共通管理"""
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

def get_openai_client():
    """OpenAIクライアントを取得（エラーハンドリング付き）"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ OPENAI_API_KEYが設定されていません。.envファイルを確認してください。")
        st.stop()
    
    return OpenAI(api_key=api_key)