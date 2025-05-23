from fastmcp import FastMCP
from rdkit import Chem, rdBase
from rdkit.Chem import Descriptors, rdMolDescriptors
import re
import json


# RDKitのエラーログを無効化
rdBase.DisableLog('rdApp.error')


# MCPサーバーを初期化
mcp = FastMCP("化学分析ツール")


def extract_smiles_from_text(text: str) -> list[str]:
    """<smi></smi>タグで囲まれたSMILES文字列をテキストから抽出する。"""
    # <smi></smi>タグ内のコンテンツにマッチするパターン
    smiles_pattern = r'<smi>(.*?)</smi>'
    
    # すべてのマッチを検索
    smiles_matches = re.findall(smiles_pattern, text, re.DOTALL)
    
    # 余分な空白を削除
    smiles_matches = [s.strip() for s in smiles_matches]
    
    return smiles_matches


def validate_smiles(smiles_list):
    """RDKitを使用してSMILES文字列のリストを検証する。"""
    valid_smiles = []
    
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            valid_smiles.append(smi)
    
    return valid_smiles


@mcp.tool()
def extract_and_analyze_smiles(text: str) -> str:
    """
    <smi></smi>タグで囲まれたSMILES文字列をテキストから抽出する。
    複数のタグがテキストに含まれる場合も、同時に処理してSMILES文字列のリストが取得できる。
    
    パラメータ:
    text (str): SMILES文字列を含む可能性のあるテキスト
    
    戻り値:
    str: 抽出されたSMILESとその特性を含むJSON文字列
    """
    # SMILES パターンを抽出
    potential_smiles = extract_smiles_from_text(text)
    
    # SMILES文字列を検証
    valid_smiles = validate_smiles(potential_smiles)
    
    if not valid_smiles:
        return json.dumps({"message": "テキスト内に有効なSMILES文字列が見つかりませんでした。"})
    
    return json.dumps([{"smiles": smi} for smi in valid_smiles])


@mcp.tool()
def get_detailed_properties(smiles: str) -> str:
    """
    SMILES文字列の詳細な化学特性を取得する。
    
    パラメータ:
    smiles (str): 化合物のSMILES表現
    
    戻り値:
    str: 詳細な分子特性を含むJSON文字列

    出力されるパラメータ：
    smiles: 化合物のSMILES
    formula: 分子式
    molecular_weight: 分子量
    exact_mass: 精密質量
    heavy_atoms: 重原子の数
    total_atoms: 原子の総数
    ring_count: 環の数
    rotatable_bonds: 回転可能な結合の数
    h_bond_donors: 水素結合供与者の数
    h_bond_acceptors: 水素結合受容体の数
    logp: 脂溶性、LogP値
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return json.dumps({"error": "無効なSMILES文字列です。"})
        
        formula_str = rdMolDescriptors.CalcMolFormula(mol)
        
        result = {
            "smiles": smiles,
            "formula": formula_str,
            "molecular_weight": round(Descriptors.MolWt(mol), 4),
            "exact_mass": round(Descriptors.ExactMolWt(mol), 4),
            "heavy_atoms": mol.GetNumHeavyAtoms(),
            "total_atoms": mol.GetNumAtoms(onlyExplicit=False),
            "ring_count": rdMolDescriptors.CalcNumRings(mol),
            "rotatable_bonds": Descriptors.NumRotatableBonds(mol),
            "h_bond_donors": Descriptors.NumHDonors(mol),
            "h_bond_acceptors": Descriptors.NumHAcceptors(mol),
            "logp": round(Descriptors.MolLogP(mol), 2)
        }
        
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    # サーバーを実行
    mcp.run()