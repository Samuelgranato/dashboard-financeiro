# modules/rules.py

# Regras fixas para gastos compartilhados
REGRAS_COMPARTILHADAS = {
    "cartoes": ["ITAU UNICLASS VISA INFINITE"],
    "descricoes": ["CONDOMINIO EDIFICIO ANTURIUS", "QUINTO ANDAR"],
    "categorias": ["moradia"],
}

# Regras complexas de exclusão
REGRAS_EXCLUSAO = {
    "categorias": ["transferências entre contas", "pagamento de fatura", "estorno"],
    "contas": [
        ("Nubank", "Itaú"),
        ("Mercado Pago", "Itaú"),
        ("Itaú", "Nubank"),
        ("Mercado Pago", "Nubank"),
        # adicione mais pares conforme suas contas
    ],
    "descricoes": [
        "Pagamento recebido",
        "Transferência entre contas",
        "Pagamento de fatura",
        "Transferência Pix recebida Samuel Vinicius Granato de Barros",
        "Transferência enviada|Samuel Vinicius Granato de Barros",
        "Transferência Pix recebida SAMUEL VINICIUS GRANATO BARROS",
        "Transferência Pix enviada SAMUEL VINICIUS GRANATO BARROS",
        "MERCADO PAGO INSTITUICAO DE PAGAMENTO LTDA",
        "Dinheiro reservado*",
        "Dinheiro retirado*",
        "Saída de dinheiro",
        "PIX TRANSF Samuel*",
        "PIX TRANSF  SAMUEL*",
        "APL APLIC AUT MAIS AP",
        "RES APLIC AUT MAIS AP",
        "APL APLIC AUT MAIS",
        "RES APLIC AUT MAIS",
        "Pagamento da fatura",
        "itau",
    ],
}


# Obter regras compartilhadas
def obter_regras_compartilhadas():
    return REGRAS_COMPARTILHADAS


# Obter regras de exclusão
def obter_regras_exclusao():
    return REGRAS_EXCLUSAO
