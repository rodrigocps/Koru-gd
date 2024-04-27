# Como rodar o ambiente virtual

Este repositório contém um guia simples sobre como configurar e ativar um ambiente virtual Python usando o módulo `venv`.

## Pré-requisitos

- Python 3.x instalado em seu sistema. Você pode fazer o download e instalar o Python a partir do [site oficial do Python](https://www.python.org/downloads/).
- Git instalado em seu sistema, se desejar clonar este repositório. Você pode fazer o download e instalar o Git a partir do [site oficial do Git](https://git-scm.com/downloads).

## Passos Ativar o Ambiente Virtual

1. Clone este repositório para o seu sistema local, se ainda não o fez.

    ```bash
    git clone https://github.com/seu_usuario/seu_repositorio.git
    ```

2. Navegue até o diretório do repositório clonado.

    ```bash
    cd seu_repositorio
    ```

4. Ative o ambiente virtual. Os comandos para ativação podem variar dependendo do sistema operacional:

    - No Windows usando CMD:

        ```bash
        nome_do_ambiente\Scripts\activate
        ```

    - No Windows usando PowerShell:

        ```bash
        nome_do_ambiente\Scripts\Activate.ps1
        ```

    - No macOS e Linux:

        ```bash
        source nome_do_ambiente/bin/activate
        ```

6. Quando terminar de trabalhar no projeto e quiser sair do ambiente virtual, basta executar:

    ```bash
    deactivate
    ```

    Isso irá desativar o ambiente virtual e você voltará ao ambiente global do Python.
