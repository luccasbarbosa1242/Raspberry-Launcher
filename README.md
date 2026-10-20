# Raspberry Launcher

Launcher desktop em Python, CustomTkinter e SQLite, com interface gráfica e lógica separadas por contratos explícitos.

## Executar o programa

Use Python 3.10 ou superior com suporte a Tk. Na pasta do projeto:

```bash
python -m pip install -r requirements.txt
python main.py
```

É recomendado executar em um ambiente virtual. O banco, as capas, os banners, as pontuações e os arquivos de configuração fornecidos no ZIP foram preservados.

## Onde editar cada parte

| Pasta/arquivo | Responsabilidade |
| --- | --- |
| `frontend/` | Janelas, telas, cards, cores, imagens renderizadas e estado dos widgets. |
| `backend/` | Biblioteca, SQLite, downloads, instalação, remoção, execução, pontuação e emuladores. |
| `application/` | Coordenação das ações, navegação, tarefas em segundo plano e entrega de resultados à interface. |
| `contracts/` | Dados e interfaces públicas usados pelas camadas. Não depende de GUI ou banco. |
| `main.py` | Montagem do aplicativo: conecta as implementações concretas. |
| `backend/tools/` | Ferramentas administrativas de terminal, executadas como módulos. |
| `ASSETS/`, `DATA/`, `USERDATA/` | Recursos e dados existentes, mantidos nos mesmos locais. |
| `tests/` | Testes de arquitetura, backend, integração, interface e ferramentas administrativas. |

A comunicação acontece por dados e identificadores. Nenhum widget é enviado ao backend; nenhuma tela abre conexões com o banco ou executa downloads.

## Trabalhar somente na interface

```bash
python -m pip install -r requirements/frontend.txt
python -m frontend.preview
```

A prévia usa dados fictícios e permite navegar pelas telas sem importar o backend. Seus botões de instalação, execução e remoção não realizam operações reais.

Para mudar o visual, comece por `frontend/theme.py`, `frontend/cards.py`, `frontend/components.py` e `frontend/views/`.

## Trabalhar somente no backend

```bash
python -m pip install -r requirements/backend.txt
python -m backend --help
python -m backend init
python -m backend list
python -m backend list --collection favorites
python -m backend list --collection search --term Snake
python -m backend show snake
```

A CLI também oferece `install`, `uninstall`, `launch`, `emulator`, `platform` e `scores`. Ela usa a mesma API do aplicativo e funciona sem CustomTkinter, Pillow ou uma tela gráfica. As dependências de rede/extração só são carregadas quando necessárias.

Ferramentas administrativas preservadas:

```bash
python -m backend.tools.add_game
python -m backend.tools.update_game
python -m backend.tools.add_assets
python -m backend.tools.health_check
```

Os antigos comandos `python tools/nome.py` passam a ser `python -m backend.tools.nome`.

Para usar outro diretório de dados, defina `RASPBERRY_LAUNCHER_HOME` antes de iniciar o aplicativo ou utilize `python -m backend --home /caminho init`. Nesse diretório ficam `DATA`, `USERDATA`, as instalações e os downloads. Para instalar emuladores nesse ambiente separado, copie também `DATA/emulator_packages.json`. Os recursos estáticos e os plugins continuam sendo obtidos do projeto.

## Verificar a separação e o funcionamento

```bash
python -m unittest discover -s tests -v
```

Os testes gráficos precisam de uma tela; sem ela, são marcados como ignorados. Em Linux com Xvfb instalado, é possível executar:

```bash
xvfb-run -a python -m unittest discover -s tests -v
```

Os testes criam bancos e instalações temporários. Não usam o banco real do projeto.

## Documentação

- [Arquitetura e pontos de extensão](docs/ARQUITETURA.md)
- [Análise do projeto original e mudanças](docs/ANALISE_E_MUDANCAS.md)
- [Validação realizada e seus limites](docs/VALIDACAO.md)
- [English overview](README_en.md)

Os READMEs e a lista de dependências originais estão em `docs/historico/`, como registro do planejamento anterior. Para executar e editar esta versão, utilize as instruções atuais acima.
