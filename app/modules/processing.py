# modules/processing.py
import pandas as pd
from modules.rules import obter_regras_compartilhadas, obter_regras_exclusao


# Aplicar regras de gastos compartilhados (como já implementado)
def aplicar_regras_compartilhadas(df, regras_adicionais=None):
    if regras_adicionais is None:
        regras_adicionais = {"categorias": [], "cartoes": []}

    regras_fixas = obter_regras_compartilhadas()

    mask_fixo = (
        df["meio_pagamento"].isin(regras_fixas["cartoes"])
        | df["descricao"].str.contains(
            "|".join(regras_fixas["descricoes"]), case=False, na=False
        )
        | df["categoria"]
        .str.lower()
        .isin([c.lower() for c in regras_fixas["categorias"]])
    )

    mask_adicional = df["categoria"].isin(regras_adicionais.get("categorias", [])) | df[
        "meio_pagamento"
    ].isin(regras_adicionais.get("cartoes", []))

    mask_total = mask_fixo | mask_adicional

    df["valor_final"] = df["valor"]
    df.loc[mask_total, "valor_final"] /= 2

    return df, mask_total


def aplicar_regras_exclusao(df):
    regras = obter_regras_exclusao()

    mask_categoria = (
        df["categoria"].str.lower().isin([cat.lower() for cat in regras["categorias"]])
    )

    mask_contas = pd.Series(False, index=df.index)
    for conta_origem, conta_destino in regras["contas"]:
        mask_contas |= (
            df["conta"].str.contains(conta_origem, case=False, na=False)
        ) & (df["descricao"].str.contains(conta_destino, case=False, na=False))

    # Máscaras para descrições e prefixos
    mask_descricao = pd.Series(False, index=df.index)

    descricoes_exatas = [d for d in regras["descricoes"] if not d.endswith("*")]
    prefixos = [d[:-1] for d in regras["descricoes"] if d.endswith("*")]

    if descricoes_exatas:
        mask_descricao |= (
            df["descricao"]
            .str.lower()
            .isin([desc.lower() for desc in descricoes_exatas])
        )

    if prefixos:
        mask_descricao |= df["descricao"].str.startswith(tuple(prefixos), na=False)

    # Combine todas as condições
    mask_exclusao_total = mask_categoria | mask_descricao | mask_contas

    # Aplicar exclusões
    df_filtrado = df[~mask_exclusao_total].reset_index(drop=True)

    return df_filtrado
