<div align="center">

# 🚀 Launcher PI

🌎 Language:

- 🇧🇷 Português (Atual)
- 🇺🇸 [English Version](README_EN.md)

### Launcher de Jogos desenvolvido com Python, CustomTkinter e SQLite

Centralize jogos nativos, jogos web e ROMs em uma única biblioteca.

### 📈 Desenvolvimento Geral

>>fase 1 Completa / Fase 2 em Progresso<<

<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/CustomTkinter-UI-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=for-the-badge" />

</div>

---

# 📖 Sobre o Projeto

O Launcher PI é um launcher de jogos desenvolvido em Python com foco em simplicidade, organização e automação.

O objetivo do projeto é permitir que o usuário gerencie:

- 🎮 Jogos nativos
- 🌐 Jogos web
- 🕹️ ROMs
- ⚙️ Emuladores

Tudo através de uma única interface.

Além disso, o launcher está sendo desenvolvido para realizar downloads, instalações e configurações automaticamente, reduzindo ao máximo a necessidade de intervenção manual do usuário.

---

# ⚠️ Aviso Importante

> [!CAUTION]
>
> ## 🔴 BANCO DE DADOS EM TRANSIÇÃO
>
> O projeto encontra-se atualmente na Fase 2 da migração para um sistema totalmente baseado em SQLite.
>
> O objetivo é remover completamente a dependência do arquivo `games.py`, tornando o banco de dados a única fonte de dados do launcher.
>
> Durante esta fase, alterações manuais no banco não são recomendadas.

---

# 🎯 Prioridades Atuais

> Esta seção representa o foco atual do desenvolvimento.

## 🔴 Prioridade Máxima

### Banco de Dados (85%)

- [x] Estrutura SQLite criada
- [x] Repositórios implementados
- [x] Biblioteca integrada ao banco
- [x] Sistema de assets integrado
- [x] Persistência de instalação
- [ ] Migrações sem apagar banco
- [ ] Remoção total do games.py
- [ ] Ferramentas administrativas do banco

### Emuladores (60%)

- [x] Estrutura criada
- [x] EmulatorManager
- [x] PackageResolver
- [x] PluginLoader
- [x] PluginRegistry
- [x] RomLauncher
- [ ] Download real de emuladores
- [ ] Instalação automática completa
- [ ] Integração final com ROMs
- [ ] Biblioteca de emuladores

### Sistema de Jogos (80%)

- [x] Jogos nativos
- [x] Jogos web
- [x] Instalação automática
- [x] Desinstalação automática
- [x] Biblioteca integrada
- [ ] Cadastro 100% via banco
- [ ] Atualização de jogos

---

## 🟠 Prioridade Alta

### Interface (75%)

- [x] Biblioteca funcional
- [x] Sistema de cards
- [x] Covers via AssetManager
- [x] Status visual dos jogos
- [x] Home integrada ao banco
- [ ] Página individual de jogo
- [ ] Melhorias visuais finais
- [ ] Animações e feedback visual

### Navegador Interno

- [ ] Corrigir problemas atuais
- [ ] Melhorar integração com o launcher

---

## 🟡 Prioridade Média

### Biblioteca

- [ ] Página individual dos jogos
- [ ] Descrição dos jogos
- [ ] Gênero
- [ ] Ano de lançamento
- [ ] Informações do emulador utilizado

### Conteúdo

- [ ] Adicionar mais jogos
- [ ] Adicionar mais emuladores

---

## 🟢 Prioridade Baixa

### Configurações

- [ ] Tema claro/escuro
- [ ] Música de fundo
- [ ] Controle de volume
- [ ] Controle de brilho

### Usuários

- [ ] Perfil de usuário
- [ ] Estatísticas individuais

### Distribuição

- [ ] Corrigir executáveis externos
- [ ] Criar instalador oficial do Launcher PI

---

## 🔵 Ideias Futuras

- [ ] Sistema de conquistas
- [ ] Backup em nuvem
- [ ] Sincronização entre dispositivos
- [ ] Loja de temas

# ✨ Funcionalidades

## 🎮 Jogos Nativos

- Instalação automática
- Download automático
- Execução integrada
- Suporte a Linux
- Suporte a Windows

## 🌐 Jogos Web

- Navegador interno
- Integração direta ao launcher

## 🕹️ ROMs e Emuladores

- Estrutura preparada para integração com ROMs
- Sistema de plugins para emuladores
- Download automático de emuladores (em desenvolvimento)

## 📊 Biblioteca

- Biblioteca centralizada
- Sistema de score
- Gerenciamento de jogos instalados

## 🖼️ Assets

- AssetManager
- AssetRepository
- Cache local
- Covers remotos
- Sistema de fallback

---

# 🏗️ Arquitetura do Projeto

```text
launcher-pi/

CORE/
├── assets/
├── database/
├── download/
├── emulators/
├── launchers/
├── library/
├── plugins/

DATA/
├── library.db
├── emulator_packages.json

DOWNLOADS/
EMULATORS/
USERDATA/

UI/
├── views/
├── cards.py
├── pages.py
├── window.py

UTILS/
tools/

main.py
```

## CORE/database

Responsável por:

- SQLite
- Migrações
- Persistência de dados

## CORE/library

Responsável por:

- Biblioteca de jogos
- Repositórios
- Consulta e gerenciamento dos dados

## CORE/launchers

Responsável por:

- NativeLauncher
- RomLauncher
- LauncherFactory

## CORE/emulators

Responsável por:

- Download de emuladores
- Instalação automática
- Gerenciamento de versões

## CORE/plugins

Responsável por:

- Registro de plugins
- Adaptadores de emuladores
- Expansão do sistema

---

# 🔄 Fluxo do Sistema

```text
Usuário
    │
    ▼
Biblioteca
    │
    ▼
LauncherFactory
    │
    ├──────────────► NativeLauncher
    │                    │
    │                    ▼
    │               Executável
    │
    └──────────────► RomLauncher
                         │
                         ▼
                   EmulatorManager
                         │
                         ▼
                       ROM
```

---

# 🛠️ Tecnologias Utilizadas

| Tecnologia | Utilização |
|------------|------------|
| Python | Backend |
| CustomTkinter | Interface |
| SQLite3 | Banco de Dados |
| Git | Versionamento |
| GitHub Releases | Distribuição |
| Google Drive | Distribuição temporária |

---

# 📊 Status Atual

| Área | Progresso |
|--------|--------|
| Launcher Base | ✅ 100% |
| Biblioteca | ✅ 85% |
| Banco de Dados | 🚧 85% |
| Assets | 🚧 80% |
| Downloads | ✅ 90% |
| Jogos Web | ✅ 90% |
| Jogos Nativos | ✅ 85% |
| Emuladores | 🚧 60% |
| Plugins | 🚧 65% |
| Interface | 🚧 75% |

---

# 🚀 Progresso Geral

```text
Launcher Base         ██████████ 100%
Biblioteca            ████████░░  85%
Banco de Dados        ████████░░  85%
Assets                ████████░░  80%
Downloads             █████████░  90%
Jogos Nativos         ████████░░  85%
Jogos Web             █████████░  90%
Emuladores            ██████░░░░  60%
Plugins               ██████░░░░  65%
Interface             ███████░░░  75%
```

---

# 📋 Roadmap

## ✅ Concluído

### Arquitetura

- [x] Modularização completa
- [x] LauncherFactory
- [x] NativeLauncher
- [x] RomLauncher
- [x] EmulatorManager
- [x] Sistema de plugins
- [x] SQLite integrado

### Biblioteca

- [x] Biblioteca via SQLite
- [x] Cards dinâmicos
- [x] Covers remotos
- [x] Cache de assets
- [x] Status visual dos jogos

### Instalação

- [x] Download automático
- [x] Instalação automática
- [x] Desinstalação automática
- [x] Persistência no banco

---

## 🚧 Em Desenvolvimento

### Banco de Dados - Fase 2

- [ ] Migrações sem apagar banco
- [ ] Cadastro de jogos via ferramentas
- [ ] Cadastro de assets via ferramentas
- [ ] Remoção da dependência de games.py

### Emuladores

- [ ] Download real
- [ ] Instalação real
- [ ] Integração completa com ROMs

### Interface

- [ ] Página individual dos jogos
- [ ] Informações detalhadas
- [ ] Screenshots
- [ ] Melhorias visuais

---

## ⏳ Planejado

### 👤 Usuários

- [ ] Perfil de usuário
- [ ] Estatísticas individuais

### 🎮 Biblioteca

- [ ] Página individual dos jogos
- [ ] Descrição dos jogos
- [ ] Gênero
- [ ] Ano de lançamento
- [ ] Informações do emulador utilizado

### 📦 Instalação

- [ ] Instaladores silenciosos
- [ ] Adição manual de jogos
- [ ] Adição manual de instaladores
- [ ] Adição manual de emuladores

### ⚙️ Configurações

- [ ] Tema claro/escuro
- [ ] Música de fundo
- [ ] Controle de volume
- [ ] Controle de brilho
- [ ] Configurações avançadas

### 🕹️ Conteúdo

- [ ] Adicionar novos jogos
- [ ] Adicionar novos emuladores

### 📦 Distribuição

- [ ] Corrigir executáveis externos
- [ ] Criar instalador oficial do Launcher PI

### 🌐 Navegador

- [ ] Melhorar integração
- [ ] Corrigir problemas atuais

---

# 🎯 Objetivo Final

O objetivo do Launcher PI é se tornar uma plataforma única para gerenciamento de jogos, permitindo que o usuário tenha acesso a:

- Jogos nativos
- Jogos web
- ROMs
- Emuladores

Tudo através de uma única interface moderna, simples e automatizada.

O Launcher PI está entrando em sua segunda grande fase de desenvolvimento.

A Fase 1 foi focada em criar toda a arquitetura principal:

- Banco de dados
- Biblioteca
- Downloads
- Instalação
- Assets
- Sistema de emuladores
- Sistema de plugins

A Fase 2 tem como objetivo tornar o SQLite a única fonte de dados do projeto, removendo completamente a dependência do arquivo `games.py` e permitindo que jogos, assets, ROMs e emuladores sejam cadastrados diretamente através do banco de dados.

---

<div align="center">

### 🚀 Projeto em desenvolvimento ativo

Última atualização: Junho de 2026

</div>