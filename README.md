<div align="center">

# 🚀 Launcher PI

🌎 Language:

* 🇧🇷 Português (Atual)
* 🇺🇸 [English Version](README_en.md)

### Launcher de Jogos desenvolvido com Python, CustomTkinter e SQLite

Centralize jogos nativos, jogos web e ROMs em uma única biblioteca.

### 📈 Desenvolvimento Geral

> **Fase 1 Completa • Fase 2 em Desenvolvimento (Etapas 1–11 concluídas)**

<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/CustomTkinter-UI-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=for-the-badge" />

<img src="https://img.shields.io/badge/Linux-Supported-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/Windows-Supported-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/Open%20Source-Yes-blue?style=for-the-badge" />
<img src="https://img.shields.io/github/last-commit/SEU_USUARIO/launcher-pi?style=for-the-badge" />
<img src="https://img.shields.io/github/license/SEU_USUARIO/launcher-pi?style=for-the-badge" />

</div>

---

# 📖 Sobre o Projeto

O **Launcher PI** é um launcher de jogos desenvolvido em **Python**, utilizando **CustomTkinter** para a interface gráfica e **SQLite** como banco de dados principal.

O projeto foi pensado para centralizar diferentes tipos de jogos em uma única biblioteca, permitindo que o usuário instale, organize e execute seus jogos através de uma interface moderna e intuitiva.

O launcher suporta atualmente:

* 🎮 Jogos nativos
* 🌐 Jogos Web
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
> ## 🔴 BANCO DE DADOS EM TRANSIÇÃO
>
> O Launcher PI encontra-se atualmente na **Fase 2** de migração para um sistema totalmente baseado em banco de dados.
>
> Durante esta fase, praticamente todo o funcionamento do launcher está sendo migrado para utilizar exclusivamente o SQLite.
>
> O arquivo **games.py** permanece apenas por compatibilidade temporária e será removido futuramente.
>
> As migrações já preservam os dados existentes, portanto o banco não precisa mais ser recriado durante o desenvolvimento.

---

# 🎯 Prioridades Atuais

> Esta seção representa o foco atual do desenvolvimento.

---

# 🔴 Prioridade Máxima

## Banco de Dados (93%)

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
* [ ] Plataformas totalmente baseadas no banco
* [ ] Emuladores totalmente baseados no banco
* [ ] Remoção definitiva do games.py

---

## Sistema de Jogos (92%)

* [x] Jogos nativos
* [x] Jogos Web
* [x] Biblioteca dinâmica
* [x] Download automático
* [x] Instalação automática
* [x] Desinstalação automática
* [x] Atualização via banco
* [x] Cadastro via ferramentas
* [x] Suporte para múltiplas versões (Linux / Windows)
* [ ] Página individual dos jogos

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
* [ ] Página individual de jogo
* [ ] Sistema de coleções
* [ ] Melhorias visuais
* [ ] Feedback visual durante downloads

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

## Navegador Interno

* [ ] Corrigir problemas atuais
* [ ] Melhor integração com o launcher
* [ ] Melhor gerenciamento de abas

---

# 🟡 Prioridade Média

## Biblioteca

* [ ] Página individual dos jogos
* [ ] Descrição
* [ ] Desenvolvedor
* [ ] Gênero
* [ ] Ano de lançamento
* [ ] Tempo jogado
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

## 🌐 Jogos Web

* Navegador interno
* Integração direta ao launcher
* Cadastro totalmente pelo banco

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

# 🏗️ Arquitetura do Projeto

```text
launcher-pi/

CORE/
│
├── assets/
│   ├── asset_downloader.py
│   ├── asset_manager.py
│   └── asset_repository.py
│
├── database/
│   ├── migrations/
│   ├── database.py
│   ├── migration_runner.py
│   └── schema.sql
│
├── download/
│   ├── downloader.py
│   └── native_game_installer.py
│
├── emulators/
│   ├── emulator_manager.py
│   ├── package_resolver.py
│   └── plugins/
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
└── system/
    └── platform_detector.py

DATA/
│
├── library.db
├── emulator_packages.json
└── games_seed.json

DOWNLOADS/

EMULATORS/

USERDATA/
│
├── cache/
├── covers/
├── banners/
└── logos/

UI/
│
├── views/
├── cards.py
├── pages.py
└── window.py

UTILS/

tools/

main.py
```

---

# 📂 Organização do Projeto

O Launcher PI foi dividido em módulos independentes.

Cada módulo possui apenas uma responsabilidade específica, facilitando manutenção, testes e expansão futura.

---

# CORE/assets

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

Nenhuma parte da interface acessa imagens diretamente.

---

# CORE/database

Responsável por toda persistência do launcher.

Inclui:

* SQLite
* Banco principal
* Migrações
* Controle de versão do banco
* Estrutura inicial

É o único módulo responsável por criar ou alterar tabelas.

---

# CORE/download

Responsável pelas instalações.

Controla:

* Downloads
* Extração de arquivos
* Instalação de jogos
* Atualização de status
* Persistência da instalação

O objetivo é que futuramente qualquer instalação utilize apenas informações presentes no banco de dados.

---

# CORE/emulators

Responsável pelos emuladores.

Inclui:

* EmulatorManager
* PackageResolver
* Download de emuladores
* Integração com plugins

Este módulo ainda encontra-se em desenvolvimento.

---

# CORE/launchers

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

# CORE/library

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

# CORE/plugins

Responsável por permitir expansão do launcher.

Cada plugin pode adicionar suporte para:

* Novo emulador
* Nova plataforma
* Novo formato de ROM
* Novo sistema de instalação

Toda a arquitetura foi planejada para que novos plugins possam ser adicionados sem modificar o restante do projeto.

---

# CORE/system

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

Informações sobre downloads dos emuladores.

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

# tools

Ferramentas administrativas utilizadas durante o desenvolvimento.

Atualmente permitem:

* cadastrar jogos
* atualizar jogos
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

No futuro também serão adicionadas:

```text
platforms
emulators
collections
game_collections
```

permitindo que toda a estrutura do launcher seja totalmente orientada ao banco de dados.

---

# 🔄 Fluxo Geral do Sistema

```text
Usuário
      │
      ▼
Interface
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
| Banco de Dados | 🚧 93%    |
| Assets         | 🚧 90%    |
| Downloads      | ✅ 90%     |
| Jogos Web      | ✅ 90%     |
| Jogos Nativos  | 🚧 92%    |
| Emuladores     | 🚧 65%    |
| Plugins        | 🚧 70%    |
| Interface      | 🚧 80%    |

---

# 🚀 Progresso Geral

```text
Launcher Base         ██████████ 100%

Biblioteca            █████████░  90%

Banco de Dados        █████████░  93%

Assets                █████████░  90%

Downloads             █████████░  90%

Jogos Nativos         █████████░  92%

Jogos Web             █████████░  90%

Emuladores            ██████▓░░░  65%

Plugins               ███████░░░  70%

Interface             ████████░░  80%
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

---

## 🚧 Em Desenvolvimento

### Banco de Dados — Fase 2

* [x] Migrações sem apagar banco
* [x] Cadastro de jogos
* [x] Atualização de jogos
* [x] Remoção de jogos
* [x] Cadastro de assets
* [x] Sistema de versões
* [ ] Plataformas no banco
* [ ] Emuladores no banco
* [ ] Remoção definitiva do games.py

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

* [ ] Página individual dos jogos
* [ ] Informações completas
* [ ] Screenshots
* [ ] Banner do jogo
* [ ] Melhorias visuais
* [ ] Sistema de coleções

---

## ⏳ Planejado

### Biblioteca

* [ ] Página individual
* [ ] Descrição
* [ ] Desenvolvedor
* [ ] Publisher
* [ ] Gênero
* [ ] Ano
* [ ] Classificação indicativa
* [ ] Tempo jogado
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

## Fase 1 — Arquitetura Base ✅

Durante a primeira fase foi construída toda a estrutura principal do Launcher PI.

Principais entregas:

* Arquitetura modular
* Biblioteca
* Sistema de downloads
* Instalação automática
* LauncherFactory
* NativeLauncher
* RomLauncher
* Sistema de plugins
* Sistema de assets
* Banco SQLite

---

## Fase 2 — Banco de Dados 🚧

A segunda fase está focada na migração completa para um sistema orientado ao banco de dados.

Objetivos desta fase:

* eliminar a dependência do `games.py`;
* tornar o SQLite a única fonte de dados;
* cadastrar jogos por ferramentas administrativas;
* cadastrar assets pelo banco;
* cadastrar versões de jogos por plataforma;
* preparar plataformas e emuladores para funcionamento totalmente orientado ao banco;
* preservar os dados através de migrações.

---

## Fase 3 — Conteúdo (Planejada)

Após a conclusão da migração, o foco será expandir o conteúdo do launcher.

Incluindo:

* novos jogos;
* novos emuladores;
* novas plataformas;
* novas coleções;
* melhorias visuais;
* documentação completa.

---

## Fase 4 — Distribuição (Planejada)

A última grande fase será dedicada à distribuição oficial do Launcher PI.

Incluindo:

* instalador oficial;
* atualizador automático;
* versões para Linux e Windows;
* documentação definitiva;
* primeiros lançamentos públicos.

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
LibraryManager
      │
      ▼
GameRepository
      │
      ▼
SQLite
```

O `LibraryManager` funciona como uma camada intermediária entre a interface e o banco de dados, evitando que a interface realize consultas SQL diretamente.

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

Nenhuma imagem é carregada diretamente pela interface.

Todo carregamento passa obrigatoriamente pelo AssetManager.

Fluxo:

```text
Card
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

## (Planejado)

Nas próximas etapas serão adicionadas:

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

Essas tabelas completarão a migração da arquitetura para um sistema totalmente orientado ao banco de dados.

---

# 🔄 Fluxo Completo do Launcher

```text
Usuário
      │
      ▼
Interface
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
* 🌐 Jogos Web
* 🕹️ ROMs
* ⚙️ Emuladores
* 🖼️ Assets
* 📚 Biblioteca completa

Tudo através de uma única interface moderna, intuitiva e multiplataforma.

O projeto foi planejado para que praticamente todo o conteúdo seja controlado pelo banco de dados, permitindo que novos jogos sejam adicionados sem alterações no código-fonte.

---

# 🗺️ Planejamento das Fases

## ✅ Fase 1 — Arquitetura Base (Concluída)

A primeira fase foi dedicada à construção da infraestrutura do Launcher PI.

Principais entregas:

* Arquitetura modular
* Biblioteca funcional
* Sistema de downloads
* Sistema de instalação
* Sistema de desinstalação
* LauncherFactory
* NativeLauncher
* RomLauncher
* EmulatorManager
* Sistema de Plugins
* Sistema de Assets
* Banco SQLite
* Interface inicial

Essa etapa criou toda a base necessária para a evolução do projeto.

---

## 🚧 Fase 2 — Migração para Banco de Dados

A fase atual concentra praticamente todo o esforço de desenvolvimento.

Objetivos:

* tornar o SQLite a única fonte de dados do launcher;
* remover completamente a dependência do `games.py`;
* cadastrar jogos por ferramentas administrativas;
* cadastrar assets diretamente no banco;
* permitir múltiplas versões por jogo;
* preservar dados através de migrações;
* preparar o sistema para expansão futura.

Ao final desta fase, praticamente toda a configuração do launcher será realizada através do banco de dados.

---

## ⏳ Fase 3 — Conteúdo

Após concluir a migração, o foco passará para a expansão do conteúdo disponível.

Planejamento:

* adicionar novos jogos;
* adicionar novos emuladores;
* adicionar novas plataformas;
* adicionar coleções;
* adicionar páginas individuais;
* melhorar a interface.

---

## 🚀 Fase 4 — Distribuição

A última grande etapa será voltada para distribuição pública do Launcher PI.

Incluindo:

* instalador oficial;
* atualizador automático;
* distribuição para Linux;
* distribuição para Windows;
* documentação definitiva;
* primeiros lançamentos públicos.

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

Última atualização: Junho de 2026.

</div>
