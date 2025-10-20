# 🎯 AI求人要件整理アシスタント

クライアントヒアリング内容から求人票ドラフトを自動生成するStreamlitアプリケーション

## 機能

- 🎙️ 音声ファイルからの文字起こし（Whisper API使用）
- 📝 テキスト入力によるヒアリング内容入力
- 🤖 OpenAI GPTによる求人票自動生成
- 📥 Markdown形式でのダウンロード機能

## セットアップ

### 1. リポジトリのクローン
```bash
git clone https://github.com/kentaro-seki/job_requirements_assistant.git
cd job_requirements_assistant
```

### 2. 仮想環境の作成・有効化
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# または
.venv\Scripts\activate     # Windows
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定
`.env`ファイルを作成し、OpenAI APIキーを設定：
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. アプリケーションの起動
```bash
streamlit run main.py
```

## 使用方法

1. ブラウザで `http://localhost:8501` にアクセス
2. 音声ファイルをアップロードまたはテキストを入力
3. 「求人票を生成する」ボタンをクリック
4. 生成された求人票をMarkdown形式でダウンロード

## 必要なAPIキー

- OpenAI API キー（GPT-4およびWhisper API用）

## 技術スタック

- Python 3.11+
- Streamlit
- OpenAI API
- python-dotenv
