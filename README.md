<div align="center">

# 🚀 Launcher PI

### Launcher de Jogos desenvolvido com Python, CustomTkinter e SQLite

Centralize jogos nativos, jogos web e ROMs em uma única biblioteca.

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
> ## 🔴 FAVOR NÃO MEXER NO BANCO DE DADOS POR ENQUANTO
>
> O sistema de banco de dados encontra-se em uma etapa extremamente sensível de desenvolvimento.
>
> Alterações nessa área podem causar incompatibilidades com funcionalidades já implementadas.
>
> Caso vá contribuir com o projeto, consulte primeiro a documentação interna da estrutura de banco de dados.

---

# 🎯 Prioridades Atuais

> Esta seção representa o foco atual do desenvolvimento.

## 🔴 Prioridade Máxima

### Banco de Dados

- [ ] Finalizar migração para SQLite
- [ ] Integrar completamente a biblioteca ao banco
- [ ] Finalizar persistência dos jogos
- [ ] Finalizar sistema de assets

### Emuladores

- [ ] Download automático
- [ ] Instalação automática
- [ ] Integração completa com ROMs
- [ ] Sistema de plugins

---

## 🟠 Prioridade Alta

### Interface

- [ ] Finalizar aparência do launcher
- [ ] Padronizar componentes visuais
- [ ] Melhorar organização das páginas

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

---

# 🏗️ Arquitetura do Projeto

```text
launcher-pi/

CORE/
├── assets/
├── database/
├── download/
├── emulators/
├── games/
├── launchers/
├── library/
├── plugins/

UI/
├── views/
├── cards/
├── pages/

UTILS/

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

| Área | Status |
|--------|--------|
| Biblioteca | ✅ |
| Downloads | ✅ |
| Sistema de Score | ✅ |
| LauncherFactory | ✅ |
| NativeLauncher | ✅ |
| Navegador Interno | ✅ |
| Banco de Dados | 🚧 |
| Emuladores | 🚧 |
| Sistema de Plugins | 🚧 |
| Interface | 🚧 |

---

# 📋 Roadmap

## ✅ Concluído

### Launcher

- [x] Sistema de downloads
- [x] Instalação automática
- [x] Suporte a arquivos ZIP
- [x] Sistema de score
- [x] Biblioteca de jogos
- [x] Navegador interno
- [x] NativeLauncher
- [x] LauncherFactory

### Estrutura

- [x] Modularização do projeto
- [x] Separação por responsabilidades
- [x] Migração inicial para SQLite

---

## 🚧 Em Desenvolvimento

### Banco de Dados

- [ ] Migração completa para SQLite
- [ ] Integração total da biblioteca
- [ ] Sistema de assets

### Emuladores

- [ ] Download automático
- [ ] Instalação automática
- [ ] Integração com ROMs
- [ ] Sistema de plugins

### Interface

- [ ] Melhorias visuais
- [ ] Padronização dos componentes
- [ ] Ajustes de layout

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

---

<div align="center">

### 🚀 Projeto em desenvolvimento ativo

Última atualização: Junho de 2026

</div>