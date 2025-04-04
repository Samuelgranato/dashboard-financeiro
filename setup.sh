#!/bin/bash

echo "🚀 Iniciando o setup do ambiente..."

# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.10+, pip e venv se não existirem
echo "🔧 Instalando dependências básicas (Python, pip, venv)..."
sudo apt install -y python3 python3-pip python3-venv

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual (venv)..."
python3 -m venv venv

# Ativar ambiente virtual
echo "✅ Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
echo "📦 Instalando dependências do projeto..."
pip install -r requirements.txt

echo "✅ Setup concluído com sucesso!"

# Sugestão para rodar o Streamlit
echo ""
echo "Para rodar o dashboard:"
echo "----------------------------------------"
echo "source venv/bin/activate"
echo "streamlit run dashboard.py --server.address 0.0.0.0 --server.port 8501"
echo "----------------------------------------"
