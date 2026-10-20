<div align="center">

# 🚀 Launcher PI

🌎 Language:

* 🇧🇷 Português (Atual)
* 🇺🇸 [English Version](README_en.md)

### Launcher de Jogos desenvolvido com Python, CustomTkinter e SQLite

Centralize jogos nativos e ROMs em uma única biblioteca.

### 📈 Desenvolvimento Geral

> **Fase 1 — T00, T01, T03 e T05 • Cadastros integrados • Interface e Lógica Separadas**

<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/CustomTkinter-UI-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=for-the-badge" />

<img src="https://img.shields.io/badge/Linux-Supported-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/Windows-Supported-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/Open%20Source-Yes-blue?style=for-the-badge" />

</div>

---

# 📖 Sobre o Projeto

O **Launcher PI** é um launcher de jogos desenvolvido em **Python**, utilizando **CustomTkinter** para a interface gráfica e **SQLite** como banco de dados principal.

O projeto foi pensado para centralizar diferentes tipos de jogos em uma única biblioteca, permitindo que o usuário instale, organize e execute seus jogos através de uma interface moderna e intuitiva.

O launcher suporta atualmente:

* 🎮 Jogos nativos
* 🕹️ ROMs
* ⚙️ Emuladores

Tudo sendo integrado dentro da mesma biblioteca.

---

## 🎯 Filosofia do Projeto

O Launcher PI foi desenvolvido seguindo alguns princípios desde o início do projeto:

* Arquitetura modular
* Código desacoplado
* Banco de dados como fonte principal
* Instalações automatizadas
* Sistema expansível através de plugins
* Compatibilidade com Linux e Windows
* Facilidade para adicionar novos jogos sem alterar o código-fonte

A ideia é que, futuramente, um novo jogo possa ser adicionado apenas cadastrando suas informações no banco de dados, sem necessidade de modificar arquivos internos do launcher.

---

# ⚠️ Aviso Importante

> [!CAUTION]
>
> ## 🔴 PROTEJA OS DADOS ANTES DE MIGRAR
>
> A **Fase 1 (T00, T01, T03 e T05)** consolida os cadastros no SQLite e integra os formulários às ferramentas de terminal.
>
> O arquivo **games.py** já está fora da execução. JSONs permanecem para dados iniciais, importação/exportação e descritores de plugins.
>
> As migrações preservam os registros existentes; não recrie o banco vazio para atualizar. Jogos HTML/de navegador são arquivados e saem do catálogo ativo. Google Drive e `gdown` continuam disponíveis para downloads.
>
> Consulte a [entrega da Fase 1](docs/FASE1.md) e o [procedimento de recuperação](docs/RECUPERACAO.md) antes de alterar os dados.

---

# 🎯 Prioridades Atuais

> Esta seção representa o foco atual do desenvolvimento.

---

# 🔴 Prioridade Máxima

## Banco de Dados — Fase 1

* [x] Estrutura SQLite criada
* [x] Sistema de migrações
* [x] Banco persistente
* [x] Biblioteca integrada
* [x] GameRepository
* [x] LibraryManager
* [x] AssetRepository
* [x] GameVersionRepository
* [x] Cadastro de jogos
* [x] Atualização de jogos
* [x] Remoção de jogos
* [x] Cadastro de assets
* [x] Sistema de versões (game_versions)
* [x] Plataformas utilizadas em execução consultadas no banco
* [x] Cadastros e pacotes de emuladores consultados no banco
* [x] `games.py` fora da execução

---

## Sistema de Jogos (92%)

* [x] Jogos nativos
* [x] Retirada de jogos HTML/navegador, com histórico arquivado
* [x] Biblioteca dinâmica
* [x] Download automático
* [x] Instalação automática
* [x] Desinstalação automática
* [x] Atualização via banco
* [x] Cadastro via ferramentas
* [x] Suporte para múltiplas versões (Linux / Windows)
* [x] Página individual dos jogos

---

## Emuladores (65%)

* [x] Arquitetura criada
* [x] EmulatorManager
* [x] PackageResolver
* [x] PluginLoader
* [x] PluginRegistry
* [x] RomLauncher
* [x] Estrutura para download automático
* [ ] Download real dos emuladores
* [ ] Instalação automática completa
* [ ] Integração completa com ROMs
* [ ] Biblioteca de emuladores

---

# 🟠 Prioridade Alta

## Interface (80%)

* [x] Biblioteca funcional
* [x] Sistema de cards
* [x] Covers padronizados
* [x] Covers carregados via AssetManager
* [x] Biblioteca integrada ao banco
* [x] Status visual dos jogos
* [x] Favoritos, Recentes e Busca conectados ao backend
* [x] Feedback visual por etapa durante instalação e remoção
* [x] Página individual de jogo
* [ ] Sistema de coleções
* [ ] Melhorias visuais
* [x] Feedback visual durante downloads

---

## Assets (90%)

* [x] AssetManager
* [x] AssetRepository
* [x] Cache local
* [x] Covers remotos
* [x] Covers locais
* [x] Sistema de fallback
* [x] Ferramentas administrativas
* [ ] Screenshots
* [ ] Backgrounds
* [ ] Ícones personalizados

---

## Jogos HTML e de Navegador

* [x] Modalidade retirada do cadastro, importação, catálogo ativo e execução
* [x] Histórico legado preservado por arquivamento
* [x] Downloads de arquivos por HTTP e Google Drive preservados

---

# 🟡 Prioridade Média

## Biblioteca

* [x] Página individual dos jogos
* [ ] Descrição
* [ ] Desenvolvedor
* [ ] Gênero
* [ ] Ano de lançamento
* [x] Tempo jogado
* [ ] Histórico de atualizações

---

## Conteúdo

* [ ] Adicionar mais jogos
* [ ] Adicionar mais emuladores
* [ ] Adicionar mais plugins
* [ ] Adicionar mais plataformas

---

# 🟢 Prioridade Baixa

## Configurações

* [ ] Tema claro
* [ ] Tema escuro
* [ ] Música de fundo
* [ ] Controle de volume
* [ ] Controle de brilho

---

## Usuários

* [ ] Perfil de usuário
* [ ] Estatísticas individuais
* [ ] Histórico de jogos
* [ ] Backup de configurações

---

## Distribuição

* [ ] Instalador oficial
* [ ] Atualizador automático
* [ ] Assinatura digital
* [ ] Distribuição oficial

---

# 🔵 Ideias Futuras

* [ ] Sistema de conquistas
* [ ] Backup em nuvem
* [ ] Sincronização entre dispositivos
* [ ] Loja de temas
* [ ] Sistema de mods
* [ ] Multiplayer local assistido
* [ ] API pública para plugins

---

# ✨ Funcionalidades

## 🎮 Jogos Nativos

* Instalação automática
* Download automático
* Cadastro via SQLite
* Execução integrada
* Suporte para Linux
* Suporte para Windows
* Suporte para múltiplas versões por jogo

---

## 🌐 Jogos HTML e de Navegador

* Suporte retirado na Fase 1
* Registros antigos preservados como histórico arquivado
* Novos cadastros e importações dessa modalidade são rejeitados

Downloads por Google Drive e `gdown` continuam disponíveis; a retirada se refere à execução de jogos no navegador.

---

## 🕹️ ROMs e Emuladores

* Estrutura preparada para ROMs
* Sistema de plugins
* Download automático de emuladores (em desenvolvimento)
* Integração com múltiplos emuladores
* Arquitetura preparada para expansão

---

## 📚 Biblioteca

* Biblioteca dinâmica
* Jogos cadastrados via banco
* Sistema de score
* Favoritos
* Histórico de uso
* Biblioteca centralizada

---

## 🖼️ Assets

* AssetManager
* AssetRepository
* Cache inteligente
* Covers remotos
* Covers locais
* Sistema de fallback
* Atualização automática
* Ferramentas administrativas

---

# 🆕 Atualização — Interface e Lógica Separadas

> **Fase 1: base recuperável • Cadastros consolidados • Formulários e CLI compartilhados**

## ✅ Entregas desta atualização

* [x] **T00:** baseline, backup consistente e restauração em cópia temporária
* [x] **T01:** cadastros consolidados no banco, com migrações versionadas e instalações locais separadas
* [x] **T03:** adicionar e editar jogos, versões, emuladores e pacotes nos formulários de **Cadastros** e na CLI, usando os mesmos serviços
* [x] **T05:** jogos HTML/navegador arquivados e bloqueados para cadastro, importação e execução

* [x] Interface gráfica isolada em `frontend/`
* [x] Lógica de jogos, banco, downloads, instalações e emuladores concentrada em `backend/`
* [x] Ações, navegação e tarefas em segundo plano coordenadas por `application/`
* [x] Comunicação entre camadas definida por dados e interfaces em `contracts/`
* [x] Montagem e conexão das implementações centralizadas em `main.py`
* [x] Backend sem imports da interface e interface sem imports do backend
* [x] Prévia da interface com dados demonstrativos, sem carregar o backend
* [x] CLI do backend para uso sem interface gráfica
* [x] Dependências separadas em `requirements/frontend.txt` e `requirements/backend.txt`
* [x] Ferramentas administrativas preservadas em `backend/tools/`
* [x] Banco SQLite, capas, banners, pontuações e configurações fornecidos preservados
* [x] Testes de arquitetura, backend, aplicação, downloads, interface e ferramentas administrativas

---

## 📂 Responsabilidade de Cada Camada

| Pasta / Arquivo | Responsabilidade |
| --------------- | ----------------------- |
| `frontend/` | Janelas, telas, cards, estilos, imagens renderizadas e estado dos widgets |
| `backend/` | Regras do programa, SQLite, downloads, instalação, desinstalação, execução e emuladores |
| `application/` | Coordenação das ações, navegação, tarefas em segundo plano e atualização da interface |
| `contracts/` | Dados e interfaces públicas compartilhados pelas camadas |
| `main.py` | Inicialização e conexão das implementações concretas |
| `backend/tools/` | Ferramentas administrativas executadas pelo terminal |
| `ASSETS/`, `DATA/`, `USERDATA/` | Recursos e dados do projeto |

A interface envia ações com identificadores e recebe dados prontos para exibição. Widgets não são enviados ao backend, e as telas não executam consultas SQL, downloads ou instalações.

---

## 🛠️ Correções Incluídas

* [x] Download compatível com o `gdown 6.1.0`, removendo o argumento não suportado `fuzzy`
* [x] Download de assets e instalação de jogos usando a chamada corrigida
* [x] Opção **Desinstalar** preservada no menu de três pontos dos jogos instalados
* [x] Disponibilidade da desinstalação corrigida para jogos locais e ROMs, inclusive fora da pasta gerenciada
* [x] Remoção da instalação gerenciada e atualização dos registros sem apagar executáveis ou ROMs externos

---

## ▶️ Execução por Camada

Aplicativo completo, a partir do checkout deste ambiente:

```bash
cd /workspace/Raspberry-Launcher
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
source /workspace/.launcher-cloud/env.sh
python main.py
```

O `env.sh` preparado na nuvem ativa o ambiente virtual e direciona os dados para `/workspace/.launcher-cloud/runtime`, preservando o banco fornecido no checkout. Em uma sessão sem tela gráfica, use `xvfb-run -a python main.py`. Em uma instalação local com tela, ative seu ambiente virtual e execute `python main.py`; para escolher outro diretório de dados, defina `RASPBERRY_LAUNCHER_HOME` fora do checkout.

Prévia da interface, com dados demonstrativos e sem carregar o backend:

```bash
cd /workspace/Raspberry-Launcher
source /workspace/.launcher-cloud/env.sh
xvfb-run -a python -m frontend.preview
```

Backend pelo terminal e cadastros compartilhados:

```bash
cd /workspace/Raspberry-Launcher
source /workspace/.launcher-cloud/env.sh
python -m backend --help
python -m backend list
python -m backend catalog list game
python -m backend catalog --help
```

Os formulários ficam no grupo **Cadastros** da barra lateral. Cadastrar um emulador ou pacote não implementa seu adaptador nem garante que ele possa executar ROMs. As ferramentas administrativas continuam como módulos, por exemplo `python -m backend.tools.add_game`; exemplos de cadastro e edição estão em [Fase 1](docs/FASE1.md).

Validação em Linux com tela virtual:

```bash
cd /workspace/Raspberry-Launcher
source /workspace/.launcher-cloud/env.sh
xvfb-run -a python -m unittest discover -s tests -v
python -m compileall -q backend frontend application contracts tests main.py
ruff check .
```

O `PYTHONPYCACHEPREFIX` ativado pelo `env.sh` mantém caches fora dos arquivos `.pyc` rastreados. Antes de migrar ou editar dados importantes, crie e ensaie um ponto de recuperação conforme [Recuperação](docs/RECUPERACAO.md).

---

## 🧪 Validação da Atualização

* [x] Testes de backend, migrações, recuperação, cadastros e interface executados em Linux; resultados atuais em [Validação](docs/VALIDACAO.md)
* [x] Compilação dos módulos Python e verificação estática aprovadas
* [x] Histórico da reestruturação: 27 arquivos de dados e recursos comparados byte a byte com o ZIP original; esse registro não substitui os testes atuais da Fase 1

Os testes de download utilizaram arquivos locais e transporte HTTP controlado. A disponibilidade de todos os links externos do catálogo não foi validada, e não houve execução em Windows ou de uma ROM real no PCSX2.

Detalhes: [Arquitetura](docs/ARQUITETURA.md), [Análise e mudanças](docs/ANALISE_E_MUDANCAS.md) e [Validação](docs/VALIDACAO.md).

---

# 🏗️ Arquitetura do Projeto

```text
launcher-pi/

backend/
│
├── assets/
│   ├── asset_downloader.py
│   ├── asset_manager.py
│   └── asset_repository.py
│
├── database/
│   ├── migrations/
│   ├── database.py
│   ├── migrations.py
│   └── schema.sql
│
├── download/
│   ├── download_manager.py
│   ├── downloader.py
│   └── native_game_installer.py
│
├── emulators/
│   ├── emulator_manager.py
│   └── package_resolver.py
│
├── launchers/
│   ├── base_launcher.py
│   ├── launcher_factory.py
│   ├── native_launcher.py
│   └── rom_launcher.py
│
├── library/
│   ├── models/
│   ├── migrations/
│   ├── game_repository.py
│   ├── game_version_repository.py
│   ├── library_manager.py
│   └── game_version_manager.py
│
├── plugins/
│   ├── plugin_loader.py
│   └── plugin_registry.py
│
├── plugin_adapters/
│   └── pcsx2/
│
├── system/
│   └── platform_detector.py
│
├── tools/
├── api.py
├── __main__.py
├── paths.py
├── path_resolver.py
├── score.py
└── uninstaller.py

frontend/
│
├── views/
├── cards.py
├── components.py
├── images.py
├── bindings.py
├── theme.py
├── preview.py
└── window.py

application/
│
├── controller.py
└── tasks.py

contracts/
│
├── models.py
└── ports.py

ASSETS/

DATA/
│
├── library.db
├── emulator_packages.json
└── games_seed.json

USERDATA/
│
├── cache/
├── covers/
├── banners/
└── logos/

requirements/
│
├── backend.txt
└── frontend.txt

docs/

tests/

requirements.txt

main.py
```

---

# 📂 Organização do Projeto

O Launcher PI foi dividido em camadas e módulos com responsabilidades distintas: `frontend/`, `backend/`, `application/` e `contracts/`.

Cada módulo possui apenas uma responsabilidade específica, facilitando manutenção, testes e expansão futura.

---

# backend/assets

Responsável por todo o gerenciamento de imagens do launcher.

Atualmente controla:

* Covers
* Banners
* Logos
* Cache local
* Download automático
* Sistema de fallback

Principais componentes:

```text
AssetManager
↓
AssetRepository
↓
AssetDownloader
```

Todo carregamento de imagens passa obrigatoriamente pelo AssetManager.

A interface recebe os caminhos resolvidos pelo backend e apenas renderiza as imagens, sem gerenciar downloads ou consultar o banco.

---

# backend/database

Responsável por toda persistência do launcher.

Inclui:

* SQLite
* Banco principal
* Migrações
* Controle de versão do banco
* Estrutura inicial

É o único módulo responsável por criar ou alterar tabelas.

---

# backend/download

Responsável pelas instalações.

Controla:

* Downloads
* Extração de arquivos
* Instalação de jogos
* Atualização de status
* Persistência da instalação

O objetivo é que futuramente qualquer instalação utilize apenas informações presentes no banco de dados.

---

# backend/emulators

Responsável pelos emuladores.

Inclui:

* EmulatorManager
* PackageResolver
* Download de emuladores
* Integração com plugins

Este módulo ainda encontra-se em desenvolvimento.

---

# backend/launchers

Responsável por decidir como cada jogo será iniciado.

Fluxo:

```text
LauncherFactory
        │
        ├────────► NativeLauncher
        │
        └────────► RomLauncher
```

O restante do projeto nunca chama diretamente NativeLauncher ou RomLauncher.

Toda decisão passa pela LauncherFactory.

---

# backend/library

É o coração do launcher.

Responsável por:

* Jogos
* Biblioteca
* Repositórios
* Managers
* Modelos
* Consultas ao banco

Atualmente quase toda informação utilizada pela interface já vem deste módulo.

---

# backend/plugins

Responsável por permitir expansão do launcher.

Cada plugin pode adicionar suporte para:

* Novo emulador
* Nova plataforma
* Novo formato de ROM
* Novo sistema de instalação

Toda a arquitetura foi planejada para que novos plugins possam ser adicionados sem modificar o restante do projeto.

---

# backend/system

Responsável por informações do sistema operacional.

Atualmente controla:

* Detecção do sistema
* Linux
* Windows

Essas informações são utilizadas principalmente para selecionar automaticamente a versão correta de um jogo.

---

# DATA

Contém todos os dados persistentes do launcher.

Arquivos atuais:

```text
library.db
```

Banco principal do launcher.

```text
emulator_packages.json
```

Dados iniciais dos pacotes de emuladores, importados uma vez pelas migrações. Em execução, o `PackageResolver` consulta o SQLite; editar este JSON não altera cadastros já migrados.

```text
games_seed.json
```

Arquivo preparado para futuras importações em massa.

---

# USERDATA

Todo conteúdo gerado pelo usuário fica separado do restante do projeto.

Inclui:

```text
cache/
```

Cache de imagens.

```text
covers/
```

Capas baixadas.

```text
banners/
```

Banners.

```text
logos/
```

Logos.

Essa separação facilita backups e limpeza do launcher.

---

# backend/tools

Ferramentas administrativas utilizadas durante o desenvolvimento.

Atualmente permitem:

* cadastrar jogos
* atualizar jogos
* cadastrar e editar emuladores e pacotes pelos mesmos serviços da interface
* remover jogos
* cadastrar assets
* sincronizar assets
* listar jogos
* listar versões
* verificar banco
* importar jogos
* executar migrações

A ideia é que, futuramente, praticamente toda manutenção do banco possa ser feita por essas ferramentas.

---

# 🗄️ Banco de Dados

Atualmente o Launcher PI utiliza um único banco SQLite.

As principais tabelas são:

```text
games
```

Armazena os jogos cadastrados.

---

```text
game_versions
```

Armazena versões específicas para cada plataforma.

Exemplo:

```text
Snake

├── Linux
└── Windows
```

---

```text
assets
```

Armazena:

* covers
* banners
* logos

---

Também estão presentes:

```text
platforms
emulators
collections
game_collections
```

Os cadastros de pacotes e as instalações locais ficam separados em `emulator_packages`, `emulator_installations`, `game_installations` e `game_version_installations`. Estruturas para perfis e fontes externas estão preparadas, sem implementar esses recursos nesta fase.

---

# 🔄 Fluxo Geral do Sistema

```text
Usuário
      │
      ▼
Interface
      │
      ▼
LauncherController
      │
      ▼
LauncherService
      │
      ▼
LibraryManager
      │
      ▼
SQLite
      │
      ▼
LauncherFactory
      │
      ├──────────────► NativeLauncher
      │                     │
      │                     ▼
      │               NativeGameInstaller
      │                     │
      │                     ▼
      │               Executável
      │
      └──────────────► RomLauncher
                            │
                            ▼
                     EmulatorManager
                            │
                            ▼
                     PluginLoader
                            │
                            ▼
                           ROM
```

---

# 🖼️ Fluxo dos Assets

```text
Card
    │
    ▼
LauncherController
    │
    ▼
LauncherService
    │
    ▼
AssetManager
    │
    ▼
AssetRepository
    │
    ▼
Tabela assets
    │
    ▼
Cache Local
    │
    ▼
Imagem exibida
```

---

# 🎮 Fluxo de Instalação

```text
Botão Instalar
        │
        ▼
LauncherController
        │
        ▼
LauncherService
        │
        ▼
NativeGameInstaller
        │
        ▼
GameVersionManager
        │
        ▼
game_versions
        │
        ▼
Download
        │
        ▼
Extração
        │
        ▼
Atualização do Banco
        │
        ▼
Jogo Instalado
```
---

# 🛠️ Tecnologias Utilizadas

| Tecnologia      | Utilização              |
| --------------- | ----------------------- |
| Python          | Backend                 |
| CustomTkinter   | Interface               |
| SQLite3         | Banco de Dados          |
| Pillow          | Manipulação de imagens  |
| Requests        | Downloads               |
| Git             | Versionamento           |
| GitHub          | Hospedagem              |
| GitHub Releases | Distribuição            |
| Google Drive    | Distribuição temporária |

---

# 📊 Status Atual

| Área           | Progresso |
| -------------- | --------- |
| Launcher Base  | ✅ 100%    |
| Biblioteca     | 🚧 90%    |
| Banco de Dados | ✅ Cadastros consolidados na Fase 1 |
| Assets         | 🚧 90%    |
| Downloads      | ✅ 90%     |
| Jogos HTML/navegador | ✅ Retirados; histórico arquivado |
| Jogos Nativos  | 🚧 92%    |
| Emuladores     | 🚧 65%    |
| Plugins        | 🚧 70%    |
| Interface      | 🚧 80%    |
| Separação UI / Backend | ✅ 100% |
| CLI e Prévia de UI | ✅ 100% |
| Testes desta atualização | Resultados em [Validação](docs/VALIDACAO.md) |

---

# 🚀 Progresso Geral

```text
Launcher Base         ██████████ 100%

Biblioteca            █████████░  90%

Banco de Dados        cadastros consolidados (Fase 1)

Assets                █████████░  90%

Downloads             █████████░  90%

Jogos Nativos         █████████░  92%

HTML / Navegador      retirados; histórico arquivado

Emuladores            ██████▓░░░  65%

Plugins               ███████░░░  70%

Interface             ████████░░  80%

Separação UI/Backend  ██████████ 100%

CLI / Prévia de UI    ██████████ 100%
```

---

# 📋 Roadmap

## ✅ Concluído

### Arquitetura

* [x] Arquitetura modular
* [x] LauncherFactory
* [x] NativeLauncher
* [x] RomLauncher
* [x] EmulatorManager
* [x] Sistema de Plugins
* [x] SQLite integrado
* [x] Sistema de Assets
* [x] AssetManager
* [x] AssetRepository
* [x] Sistema de Cache
* [x] GameRepository
* [x] LibraryManager
* [x] GameVersionRepository
* [x] GameVersionManager
* [x] Separação entre interface gráfica e lógica do programa
* [x] Camada de aplicação e contratos entre módulos
* [x] Backend executável pelo terminal e prévia independente da interface
* [x] Dependências separadas por camada
* [x] Testes automatizados para verificar a separação e os fluxos integrados

---

### Banco de Dados

* [x] Banco persistente
* [x] Sistema de migrações
* [x] Cadastro de jogos
* [x] Atualização de jogos
* [x] Remoção de jogos
* [x] Cadastro de assets
* [x] Sistema de versões
* [x] Ferramentas administrativas
* [x] Compatibilidade entre versões do banco

---

### Biblioteca

* [x] Biblioteca dinâmica
* [x] Cards
* [x] Covers padronizados
* [x] Covers via AssetManager
* [x] Cache automático
* [x] Favoritos
* [x] Persistência
* [x] Biblioteca integrada ao SQLite

---

### Instalação

* [x] Download automático
* [x] Instalação automática
* [x] Desinstalação automática
* [x] Persistência da instalação
* [x] Compatibilidade Linux
* [x] Compatibilidade Windows
* [x] Suporte para múltiplas versões por jogo
* [x] Compatibilidade de download com gdown 6.1.0
* [x] Menu de três pontos com desinstalação restaurada

---

## 🚧 Em Desenvolvimento

### Banco de Dados — Fase 1

* [x] Migrações sem apagar banco
* [x] Cadastro de jogos
* [x] Atualização de jogos
* [x] Remoção de jogos
* [x] Cadastro de assets
* [x] Sistema de versões
* [x] Plataformas no banco
* [x] Emuladores e pacotes no banco
* [x] `games.py` fora da execução

---

### Emuladores

* [x] Estrutura base
* [x] Sistema de plugins
* [x] PackageResolver
* [x] EmulatorManager
* [ ] Download automático
* [ ] Instalação automática
* [ ] Atualização automática
* [ ] Integração completa com ROMs

---

### Interface

* [x] Página individual dos jogos
* [ ] Informações completas
* [ ] Screenshots
* [x] Banner do jogo
* [ ] Melhorias visuais
* [ ] Sistema de coleções

---

## ⏳ Planejado

### Biblioteca

* [x] Página individual
* [ ] Descrição
* [ ] Desenvolvedor
* [ ] Publisher
* [ ] Gênero
* [ ] Ano
* [ ] Classificação indicativa
* [x] Tempo jogado
* [ ] Histórico de versões

---

### Emuladores

* [ ] Download sob demanda
* [ ] Atualizações automáticas
* [ ] Configuração automática
* [ ] Detecção automática
* [ ] Múltiplos emuladores por plataforma

---

### Assets

* [ ] Screenshots
* [ ] Wallpapers
* [ ] Ícones
* [ ] Vídeos
* [ ] Trailers

---

### Interface

* [ ] Sistema de temas
* [ ] Tema escuro
* [ ] Tema claro
* [ ] Animações
* [ ] Melhor feedback visual
* [ ] Melhorias de performance

---

### Configurações

* [ ] Tema
* [ ] Idioma
* [ ] Pasta padrão
* [ ] Backup
* [ ] Atualizações
* [ ] Downloads

---

### Distribuição

* [ ] Instalador oficial
* [ ] Atualizador automático
* [ ] Releases automáticas
* [ ] Pacote para Linux
* [ ] Pacote para Windows

---

### Futuro

* [ ] Perfil de usuário
* [ ] Conquistas
* [ ] Estatísticas
* [ ] Backup em nuvem
* [ ] Sincronização entre dispositivos
* [ ] API pública
* [ ] Marketplace de plugins
* [ ] Marketplace de temas

---

# 📈 Evolução do Projeto

## Fase 1 — Base, Cadastros e Jogos Suportados

A fase atual reúne **T00, T01, T03 e T05** sobre a arquitetura modular já existente.

Principais entregas:

* baseline identificado e ponto de recuperação validado;
* cadastros de jogos, plataformas, emuladores e pacotes consolidados no SQLite;
* versões e instalações locais separadas;
* serviços compartilhados entre formulários e terminal;
* jogos HTML/de navegador arquivados e retirados da execução;
* camadas `frontend`, `backend`, `application` e `contracts` preservadas.

Escopo, migrações e evidências: [Fase 1](docs/FASE1.md).

---

## Fase 2 — Perfis e Configurações (Planejada)

Seleção de perfis e preferências persistentes são etapas futuras. A Fase 1 prepara apenas as estruturas e contratos necessários, sem implementar perfis completos.

---

## Fase 3 — Downloads, Emuladores e ROMs (Planejada)

Ampliar a instalação e execução por sistema operacional, arquitetura e adaptador, validando uma plataforma por vez. Os fluxos nativos e de ROMs já existentes são preservados na Fase 1.

---

## Fase 4 — Integração RGSX (Planejada)

Catálogo externo, sincronização e ligação com downloads/ROMs ficam para a etapa própria. Nenhuma integração RGSX é implementada na Fase 1.

---

# ⚙️ Funcionamento Interno

O Launcher PI foi desenvolvido utilizando uma arquitetura modular baseada em responsabilidades.

Cada módulo possui uma única função dentro do sistema, reduzindo o acoplamento entre componentes e facilitando futuras expansões.

O fluxo geral do launcher é dividido em cinco grandes sistemas:

* Biblioteca
* Instalação
* Assets
* Launchers
* Emuladores

---

# 📚 Sistema da Biblioteca

A biblioteca é o ponto central do Launcher PI.

Praticamente toda a interface consulta informações através dela.

Fluxo:

```text
Interface
      │
      ▼
LauncherController
      │
      ▼
LauncherService
      │
      ▼
LibraryManager
      │
      ▼
GameRepository
      │
      ▼
SQLite
```

O `LibraryManager` concentra as consultas da biblioteca no backend. A interface recebe os resultados através de `LauncherController`, `LauncherService` e dos dados definidos em `contracts/`, sem realizar consultas SQL diretamente.

Atualmente ele é responsável por:

* listar jogos;
* consultar jogos instalados;
* atualizar status de instalação;
* atualizar favoritos;
* registrar tempo de jogo;
* recuperar informações dos jogos.

---

# 🎮 Sistema de Versões

Cada jogo pode possuir uma ou mais versões.

Exemplo:

```text
Snake

├── Linux
└── Windows
```

Essas versões são armazenadas na tabela:

```text
game_versions
```

Cada versão possui suas próprias informações:

* URL de download;
* arquivo compactado;
* executável;
* tipo de instalação;
* plataforma;
* status de instalação.

Fluxo:

```text
Game
     │
     ▼
GameVersionManager
     │
     ▼
GameVersionRepository
     │
     ▼
game_versions
```

Isso permite que um único jogo suporte múltiplos sistemas operacionais sem duplicação de cadastro.

---

# 📦 Sistema de Instalação

Todo processo de instalação é realizado pelo `NativeGameInstaller`.

Fluxo:

```text
Botão Instalar
        │
        ▼
LauncherController
        │
        ▼
LauncherService
        │
        ▼
NativeGameInstaller
        │
        ▼
GameVersionManager
        │
        ▼
game_versions
        │
        ▼
Download
        │
        ▼
Extração
        │
        ▼
Atualização do Banco
```

Após a instalação são atualizados:

* caminho do executável;
* status de instalação;
* versão instalada;
* biblioteca.

O objetivo é que todo o processo dependa apenas do banco de dados.

---

# 🖼️ Sistema de Assets

A obtenção dos assets e o cache ficam no backend; a interface renderiza as imagens a partir dos caminhos recebidos.

Todo carregamento passa obrigatoriamente pelo AssetManager.

Fluxo:

```text
Card
    │
    ▼
LauncherController
    │
    ▼
LauncherService
    │
    ▼
AssetManager
    │
    ▼
AssetRepository
    │
    ▼
Tabela assets
    │
    ▼
Cache Local
    │
    ▼
Imagem
```

Quando um asset ainda não existe no cache:

* é baixado automaticamente;
* ou copiado de um caminho local;
* armazenado no cache;
* registrado no banco.

Caso nenhuma imagem seja encontrada, o sistema utiliza automaticamente uma imagem padrão (fallback).

---

# 🚀 Sistema de Launchers

O Launcher PI utiliza uma fábrica de launchers (`LauncherFactory`).

Isso significa que a interface nunca precisa saber como um jogo deve ser executado.

Fluxo:

```text
Jogo
    │
    ▼
LauncherFactory
    │
    ├────────► NativeLauncher
    │
    └────────► RomLauncher
```

Cada launcher é responsável apenas pelo tipo de jogo que suporta.

---

## NativeLauncher

Responsável por:

* jogos Linux;
* jogos Windows;
* jogos instaláveis;
* jogos locais.

O launcher recebe apenas um objeto do jogo e executa o arquivo correto.

---

## RomLauncher

Responsável por:

* localizar o emulador;
* localizar a ROM;
* iniciar ambos corretamente.

O funcionamento completo será finalizado nas próximas fases.

---

# 🔌 Sistema de Plugins

Todo suporte a emuladores foi planejado para funcionar através de plugins.

Estrutura:

```text
PluginLoader
      │
      ▼
PluginRegistry
      │
      ▼
Plugin
```

Cada plugin poderá definir:

* instalação;
* atualização;
* localização do executável;
* argumentos de inicialização;
* extensões suportadas;
* configurações específicas.

Essa arquitetura permitirá adicionar novos emuladores sem modificar o restante do launcher.

---

# 🕹️ Sistema de Emuladores

O gerenciamento dos emuladores ficará centralizado no `EmulatorManager`.

Fluxo planejado:

```text
RomLauncher
      │
      ▼
EmulatorManager
      │
      ▼
PackageResolver
      │
      ▼
Plugin
      │
      ▼
Download
```

O objetivo é que o usuário nunca precise instalar um emulador manualmente.

Caso ele não esteja presente, o Launcher PI fará todo o processo automaticamente.

---

# 🗄️ Banco de Dados

Atualmente o banco é dividido em responsabilidades.

## games

Responsável pelos jogos cadastrados.

Guarda informações gerais como:

* título;
* tipo;
* plataforma principal;
* status;
* favoritos;
* tempo jogado.

---

## game_versions

Responsável pelas versões específicas.

Exemplo:

```text
snake_linux
snake_windows
```

Cada versão possui:

* download;
* executável;
* arquivo compactado;
* plataforma;
* status de instalação.

---

## assets

Responsável por:

* covers;
* banners;
* logos.

Cada asset possui:

* origem remota;
* cache local;
* status de download.

---

## Cadastros Consolidados

Além de jogos, versões e assets, o banco já contém:

```text
platforms
```

```text
emulators
```

```text
collections
```

```text
game_collections
```

Esses cadastros são consultados em execução no SQLite. Pacotes de emuladores e instalações locais têm tabelas próprias; JSONs não são uma segunda fonte de cadastro em execução.

---

# 🔄 Fluxo Completo do Launcher

```text
Usuário
      │
      ▼
Interface
      │
      ▼
LauncherController
      │
      ▼
LauncherService
      │
      ▼
LibraryManager
      │
      ▼
SQLite
      │
      ▼
LauncherFactory
      │
      ├──────────────► NativeLauncher
      │                     │
      │                     ▼
      │              NativeGameInstaller
      │                     │
      │                     ▼
      │              GameVersionManager
      │                     │
      │                     ▼
      │                game_versions
      │
      └──────────────► RomLauncher
                            │
                            ▼
                     EmulatorManager
                            │
                            ▼
                     PluginLoader
                            │
                            ▼
                          Plugin
                            │
                            ▼
                           ROM
```

---

# 💡 Objetivo da Arquitetura

Toda essa organização foi pensada para que, futuramente, adicionar um novo jogo seja tão simples quanto:

1. cadastrar o jogo no banco;
2. cadastrar as versões;
3. cadastrar os assets.

Nenhuma alteração no código do launcher deverá ser necessária para que o jogo apareça automaticamente na biblioteca e possa ser instalado ou executado.

---

# 🎯 Objetivo Final

O Launcher PI tem como objetivo se tornar uma plataforma completa para gerenciamento de jogos, oferecendo ao usuário uma experiência simples, organizada e automatizada.

Ao final do desenvolvimento, será possível gerenciar em um único lugar:

* 🎮 Jogos nativos
* 🕹️ ROMs
* ⚙️ Emuladores
* 🖼️ Assets
* 📚 Biblioteca completa

Tudo através de uma única interface moderna, intuitiva e multiplataforma.

O projeto foi planejado para que praticamente todo o conteúdo seja controlado pelo banco de dados, permitindo que novos jogos sejam adicionados sem alterações no código-fonte.

---

# 🗺️ Planejamento das Fases

## ✅ Fase 1 — Base, Cadastros e Jogos Suportados

A entrega atual abrange **T00, T01, T03 e T05**:

* recuperação consistente e restauração ensaiada;
* migrações seguras e cadastros consolidados no banco;
* formulários e CLI para adicionar e editar registros com as mesmas validações;
* arquivamento e bloqueio dos jogos HTML/de navegador;
* preservação do menu de ações, desinstalação, jogos nativos, ROMs e downloads por Google Drive.

A ausência de `games.py` na execução já estava resolvida e foi preservada. Consulte [Fase 1](docs/FASE1.md) e [Validação](docs/VALIDACAO.md) para os resultados e limites da entrega.

---

## ⏳ Fase 2 — Perfis e Configurações Persistentes

Perfis locais, estado pessoal e preferências serão implementados em uma etapa posterior. A Fase 1 prepara o modelo e os contratos.

---

## ⏳ Fase 3 — Downloads, Emuladores e ROMs

Completar o fluxo de instalação e execução por SO, arquitetura e adaptador, sem tratar todo emulador cadastrado como automaticamente compatível.

---

## 🚀 Fase 4 — Integração RGSX

Consultar e sincronizar um catálogo externo; conectar downloads e ROMs apenas nas plataformas suportadas. Biblioteca ampliada, estatísticas, versões, temas, música, conquistas e controles do sistema continuam nas fases futuras do plano.

---

# 📚 Filosofia do Projeto

O Launcher PI procura seguir alguns princípios durante todo o desenvolvimento.

## Código modular

Cada módulo possui apenas uma responsabilidade.

Isso facilita manutenção, testes e futuras expansões.

---

## Banco de dados como fonte principal

O banco de dados é responsável por armazenar praticamente todas as informações do launcher.

Isso permite:

* adicionar jogos;
* atualizar jogos;
* cadastrar assets;
* cadastrar versões;
* cadastrar plataformas;
* cadastrar emuladores;

sem necessidade de alterar o código do projeto.

---

## Expansão por Plugins

Novos emuladores deverão ser adicionados através de plugins.

Isso evita modificações internas no launcher e torna a arquitetura muito mais escalável.

---

## Compatibilidade

Desde o início o Launcher PI foi planejado para funcionar tanto em Linux quanto em Windows.

Todo o sistema de versões foi desenvolvido pensando nessa compatibilidade.

---

## Organização

Todo conteúdo do projeto procura seguir uma estrutura organizada.

Cada pasta possui apenas uma responsabilidade específica.

Essa organização facilita o crescimento do projeto sem aumentar excessivamente sua complexidade.

---

# 🚀 Visão de Longo Prazo

A ideia é que, futuramente, o Launcher PI permita ao usuário:

* instalar jogos;
* atualizar jogos;
* instalar emuladores;
* executar ROMs;
* organizar biblioteca;
* visualizar informações completas;
* acompanhar tempo jogado;
* gerenciar favoritos;
* configurar plugins;

tudo sem necessidade de configurações manuais.

---

# 🤝 Contribuições

O Launcher PI ainda está em desenvolvimento ativo.

Sugestões, correções e melhorias são sempre bem-vindas.

Contribuições futuras serão organizadas conforme o amadurecimento da arquitetura do projeto.

---

# 📄 Licença

A licença do projeto será definida antes da primeira versão pública estável.

Até lá, o projeto permanece em desenvolvimento ativo.

---

# ❤️ Agradecimentos

A todos que acompanham e apoiam o desenvolvimento do Launcher PI.

Cada etapa concluída aproxima o projeto de seu objetivo principal: oferecer uma plataforma unificada para gerenciamento de jogos em diferentes plataformas e tecnologias.

---

<div align="center">

## 🚀 Launcher PI

### Um launcher moderno, modular e totalmente orientado a banco de dados.

**Desenvolvido em Python + CustomTkinter + SQLite**

---

⭐ Projeto em desenvolvimento ativo.

Última atualização: 20 de Outubro de 2026.

</div>
