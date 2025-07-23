@echo off
echo 🚀 Setup Wiki Veloz para Colaboradores
echo ======================================

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Instale Python 3.9+ primeiro.
    pause
    exit /b 1
)

REM Verificar se Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git não encontrado. Instale Git primeiro.
    pause
    exit /b 1
)

echo ✅ Python e Git encontrados

REM Clonar repositório se não existir
if not exist "wiki-veloz" (
    echo 📥 Clonando repositório...
    git clone https://github.com/mathgallina/wiki-veloz.git
    cd wiki-veloz
) else (
    echo 📁 Repositório já existe
    cd wiki-veloz
)

REM Criar ambiente virtual
echo 🐍 Criando ambiente virtual...
python -m venv .venv

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Instalar dependências
echo 📦 Instalando dependências...
pip install -r requirements.txt

REM Criar diretórios necessários
echo 📁 Criando diretórios...
if not exist "data" mkdir data
if not exist "static\uploads" mkdir static\uploads
if not exist "backups" mkdir backups

echo.
echo ✅ Setup concluído!
echo.
echo 🎯 Para iniciar o servidor:
echo    .venv\Scripts\activate.bat
echo    python app.py
echo.
echo �� Acesse: http://localhost:8000
echo 🔑 Login: admin / B@rcelona1998
echo.
echo 📚 Para mais informações, consulte: deploy_guide.md
pause
