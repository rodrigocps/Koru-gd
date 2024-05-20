# Projeto Koru Jobs

Este projeto se trata de um MVC(Minimum Viable Concept) fullstack feito em Flask de um sistema de avaliações onde o usuário conta sua experiência sobre a empresa que trabalho. Sendo assim, outros usuários podem consultar informações de experiencias sobre os colaboradores da empresa em que pretende se candidatar para um possível processo seletivo.

## Pré-requisitos

- Python 3.x instalado
- pip (Python package installer) instalado

## Configuração do Projeto

1. **Clonar o repositório**

   ```bash
   git clone https://github.com/rodrigocps/Koru-gd
   cd Koru-gd
   ```

2. **Criar e ativar um ambiente virtual**

   ```bash
   python -m venv venv
   ```

   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No macOS e Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Instalar as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Executar o projeto**

   ```bash
   flask run
   ```

   Por padrão, o Flask roda no endereço `http://127.0.0.1:5000/`.

## Configurando o .gitignore

Certifique-se de adicionar ao seu arquivo `.gitignore` os seguintes itens:

- Arquivos de banco de dados SQLite (*.db)
- Diretórios de ambientes virtuais (geralmente chamados de `venv/` ou `virtualenv/`)
- Diretórios `__pycache__/`

Isso garantirá que esses arquivos e diretórios não sejam incluídos no controle de versão do Git.
```