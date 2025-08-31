# OLALLMAgent1

ローカル LLM エージェントスタックの参考実装です。Windows 11 Pro + RTX 5080 を想定しつつ、単一 16GB GPU でも動作するよう設計されています。

## 構成
- 20B: Ollama / llama.cpp (GGUF Q4_K_M)
- 120B: vLLM + HuggingFace(AWQ)
- FastAPI 統一エンドポイント `/chat`, `/file/*`, `/rag/query`
- Playwright 経由で Windows VM 内の Edge/Chrome を遠隔操作
- ChromaDB + BGE-base による RAG
- React Native クライアント `apps/ora-mobile`

## クイックスタート (20B, 単一 GPU)
```powershell
# 依存インストール
pip install -r requirements.txt

# モデル設定は config/model.yaml の current=20B でデフォルト
pwsh scripts/start.ps1
```

## 120B モデルに切り替える
```powershell
# config/model.yaml を編集し current: 120B に変更
# 2GPU ない場合は自動で tensor_parallel_size=1 へフォールバック
pwsh scripts/start.ps1
```

## Function Calling の検証
```bash
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"ping"}],"tools":[]}'
```
PowerShell:
```powershell
pwsh tools/verify_function_call.ps1
```

## ブラウザ Executor のデモ
```powershell
# まず VM 側で browser/executor_rpc.py を起動し WS 9222 を公開
python browser/executor_rpc.py

# エージェント側から:
python -m agent.loop
```
これにより、example.com を開いてスクリーンショットを取得する基本フローを実行できます。

## Windows VM セットアップ
```powershell
# ホスト側 (管理者権限)
pwsh scripts/vm_quickcreate.ps1 -Name AgentVM
```
VM 内で Edge/Chrome + Playwright をインストールし、`ws://<vm>:9222` を開放してください。

## トラブルシューティング
- **vLLM の VRAM 不足**: `--tensor-parallel-size 1` + 4bit AWQ モデルで実行します。
- **Ollama が起動しない**: `ollama serve` を手動で実行しログを確認してください。
- **Playwright で接続失敗**: `pwsh` で `playwright install` を実行しブラウザを事前に準備します。

## ライセンス
MIT License
