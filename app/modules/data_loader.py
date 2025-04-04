import pandas as pd
import glob
import os


def carregar_arquivo(caminho_arquivo):
    dados = pd.read_excel(caminho_arquivo, skiprows=4)
    dados.drop(columns=["Unnamed: 0"], inplace=True)
    dados.columns = [
        "data",
        "descricao",
        "categoria",
        "subcategoria",
        "conta",
        "meio_pagamento",
        "valor",
    ]
    dados["data"] = pd.to_datetime(dados["data"], dayfirst=True, errors="coerce")
    dados.dropna(subset=["data"], inplace=True)
    dados.reset_index(drop=True, inplace=True)
    return dados


def carregar_pasta(caminho_pasta="./data"):
    arquivos = glob.glob(os.path.join(caminho_pasta, "*.xlsx"))
    dfs = [carregar_arquivo(arquivo) for arquivo in arquivos]
    dados_concatenados = pd.concat(dfs, ignore_index=True)

    # Remover linhas duplicadas baseado em todos os campos relevantes
    dados_concatenados.drop_duplicates(
        subset=[
            "data",
            "descricao",
            "categoria",
            "subcategoria",
            "conta",
            "meio_pagamento",
            "valor",
        ],
        keep="first",
        inplace=True,
        ignore_index=True,
    )

    return dados_concatenados
