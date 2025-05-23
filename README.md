# chem-mcp-server

化学構造解析のためのFastMCPサーバー

## 概要

このプロジェクトは、SMILES表記の化学構造を解析し、分子特性を提供するためのMCPサーバーです。RDKitを利用して分子の特性計算を行い、Claude AIと連携して化学情報処理を強化します。

## 機能

- SMILES文字列の抽出と検証
- 分子特性の計算（分子量、分子式、LogP値など）
- Claudeとの連携による化学構造解析

## 開発環境のセットアップ

### 必要条件

- Windows + WSL Ubuntu
- Python （3.12で実施）
- uv
- Claude Desktop


### インストール手順

1. リポジトリをクローンする

```bash
git clone https://github.com/blue-sugar/chem-mcp-server.git
cd chem-mcp-server
```

2. 仮想環境の作成と依存パッケージのインストール

```bash
uv venv
uv pip sync
```

3. サーバー起動スクリプト（`run_server.sh`）の編集

`/path/to/chem-mcp-server`を適切なパスに修正。

## Claude Desktopとの連携

1. 自環境の`claude_desktop_config.json`の`mcpServers`に以下を追記：

```json
"chemistry_properties_tools": {
  "command": "wsl.exe",
  "args": [
    "-d",
    "Ubuntu",
    "zsh",
    "-c",
    "/path/to/run_chem_prop_server.sh"
  ]
}
```

2. Claude Desktopを起動

## 使用方法

Claudeとの会話で、SMILES文字列を`<smi></smi>`タグで囲むことで、その化学構造を解析できます。
（`<smi></smi>`タグで囲まない場合もSMILESとして認識してくれるが、どの程度の精度なのかは未検証。ここではSMILESの認識正確性の向上のため、タグで囲んでいる。）

入力：
```
アスピリン <smi>CC(=O)Oc1ccccc1C(=O)O</smi> の分子量と脂溶性を教えてください。
```

出力：
```
アスピリン（アセチルサリチル酸）の計算結果は以下のとおりです：

分子量
分子式: C₉H₈O₄
分子量: 180.159 g/mol

脂溶性
LogP値: 1.31

LogP値（またはオクタノール/水分配係数の対数値）は1.31であり、これはアスピリンが中程度の脂溶性を持つことを示しています。LogP値が正の値であることから、アスピリンは水相よりも油相（オクタノール）にやや溶けやすい性質を持っていることがわかります。
このLogP値は、アスピリンが生体内でどのように吸収・分布するかに影響します。適度な脂溶性により、アスピリンは消化管から吸収されやすく、また血液脳関門のような生体膜も通過することができます。
分子量が比較的小さく（180 g/mol未満）、LogP値が適度な範囲内にあることから、アスピリンはリピンスキーの5原則を満たす医薬品としての特性を持っています。
```

### 利用可能な機能

- `extract_and_analyze_smiles`: テキストから`<smi></smi>`タグで囲まれたSMILES文字列を抽出
- `get_detailed_properties`: 以下の詳細な分子特性を計算
  - 分子式
  - 分子量
  - 精密質量
  - 重原子数
  - 総原子数
  - 環の数
  - 回転可能な結合数
  - 水素結合供与体数
  - 水素結合受容体数
  - LogP値（脂溶性）

## 技術詳細

`server.py`は以下の主要コンポーネントで構成されています：

1. FastMCPサーバーの初期化
2. SMILES文字列の抽出と検証機能
3. 分子特性計算ツール

RDKitライブラリを使用して化学計算を行い、結果をJSON形式で返します。


