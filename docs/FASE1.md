# Fase 1 — base, cadastros e jogos suportados

Entrega limitada a **T00, T01, T03 e T05** do pedido. O PDF de planejamento foi
usado como referência; as fases seguintes não foram implementadas.

## T00 — base e ponto de recuperação

A implementação parte da branch local `work`, commit
`55c54772ab19359857f04755d3392bfc252367be`, correspondente ao checkout solicitado
de `main`. O checkout estava limpo. As alterações ficam na branch
`codex/phase-1-catalogs`, sem worktree adicional.

Os 43 testes anteriores passaram antes de alterar o código, inclusive os
gráficos com Xvfb. Esse baseline exercita download e instalação de arquivos
locais, transporte HTTP controlado, execução de um processo Python real,
desinstalação e navegação da interface. Não comprova a disponibilidade de todos
os provedores externos nem a execução de uma ROM no PCSX2 real.

Antes das migrações foram preservados o código rastreado e cópias SQLite
consistentes do banco fornecido e do runtime. O baseline técnico está em
`/workspace/.phase1-recovery/baseline-55c5477/`, com manifesto SHA256. A
restauração foi ensaiada em um diretório separado. Um ponto no novo formato,
`/workspace/.phase1-recovery/runtime-before-phase1/`, também foi criado e
restaurado antes de atualizar o runtime.

Limitações já presentes: caminhos absolutos de outro computador nos registros
de emuladores; Google Drive bloqueado pelo proxy atual; CustomTkinter usando
fallback de desenho porque `~/.fonts` não é gravável. As duas últimas limitações
não impediram a validação local. Executáveis inexistentes não são considerados
instalações utilizáveis.

O banco rastreado `DATA/library.db` foi preservado; a atualização ocorre por
migrações sobre o banco escolhido para execução. Nenhum banco foi substituído
por um banco vazio.

## T01 — persistência e contratos

| Migração | Responsabilidade |
| --- | --- |
| `009_consolidate_catalog` | Acrescenta SO e arquitetura às versões/pacotes, importa os cadastros iniciais de plataformas/emuladores/pacotes uma vez, separa instalações de emuladores e prepara tabelas de identificação futura. |
| `010_archive_browser_games` | Arquiva jogos e versões HTML/navegador, preserva o histórico e conserva versões nativas de jogos mistos. |
| `011_game_installations` | Migra instalações de jogos/versões e cria views de runtime e triggers de compatibilidade com ferramentas legadas. |

As migrações são versionadas e transacionais; uma falha não registra a migração
como aplicada. Reexecutar a inicialização preserva os registros e as edições.
O executor entende triggers e ponto e vírgula dentro de strings SQL.

O catálogo usa `games`, `platforms` e `emulators`; os pacotes usam
`game_versions` e `emulator_packages`; o estado local usa `game_installations`,
`game_version_installations` e `emulator_installations`. As leituras de jogos
passam por `runtime_games` e `runtime_game_versions`. Colunas antigas de
instalação continuam como interface de escrita compatível, sincronizada por
triggers. Editar apenas metadados não sobrescreve os caminhos de instalação.

`DATA/emulator_packages.json` é importado apenas na migração 009, com fallback
para o seed do checkout se não existir no diretório de execução. Os nomes e
exemplos de `backend/catalog/platforms.json` também entram no banco uma vez.
Depois disso, editar JSON não altera o cadastro ativo: use os serviços, os
formulários ou a CLI. Descritores de plugins continuam em JSON.

As tabelas vazias `profiles`, `profile_game_state`, `catalog_sources` e
`external_game_ids`, com os contratos `ProfileReference` e `ExternalIdentity`,
preparam identificadores/relacionamentos para etapas futuras. Não há seleção
de perfil, migração do estado pessoal para perfis ou sincronização externa nesta
entrega. Favoritos e tempo existentes continuam preservados nos campos atuais.

Os pacotes PCSX2 fornecidos são explicitamente `x86_64`. O resolvedor confere
SO/arquitetura e não seleciona esses pacotes em ARM. O modelo existente de uma
versão por jogo/SO e uma instalação gerenciada por jogo foi mantido.
`games.py` já estava ausente da execução; referências documentais foram corrigidas.

## T03 — cadastro pela interface e pelo terminal

`CatalogService` implementa listagem, criação, edição e validação dos quatro
cadastros: `game`, `game_version`, `emulator` e `emulator_package`. Os formulários,
a CLI JSON, a importação e as ferramentas interativas chamam esse serviço.

Na barra lateral, o grupo **Cadastros** oferece jogos, versões, emuladores e
pacotes. Os formulários enviam dicionários de campos ao controlador. O trabalho
de persistência acontece em um worker; callbacks da interface são entregues na
thread principal. Erros mantêm os valores do formulário e permitem nova tentativa.
O salvamento atualiza a lista, sem sobrepor uma página que o usuário já deixou.

IDs são imutáveis na edição. São validados os campos obrigatórios,
relacionamentos, tipos de execução, SO, arquitetura, arquivos locais e caminhos
de executáveis dentro de pacotes. Alterar títulos preserva favoritos, tempo,
assets não alterados e instalações. Alvos de versões/pacotes instalados são
protegidos contra mudanças incompatíveis; crie outro pacote ou desinstale antes.
Um pacote não pode ser transferido para outro emulador.

Cadastrar um emulador não implementa um adaptador. O único adaptador fornecido
continua sendo o PCSX2; outros cadastros não garantem execução. A interface e a
prévia mostram esse limite.

## T05 — retirada de jogos HTML/navegador

O banco fornecido contém `tictactoe` com `type='native'` e
`launch_type='html'`. A migração marca o jogo e suas versões com `archived=1` e
`archive_reason='unsupported_browser_game'`. IDs, favoritos, tempo, data da
última execução, assets e associações permanecem no banco. O catálogo ativo do
runtime fornecido passa de quatro para três jogos: Snake, Daggerfall e Tetris.

Também são detectados tipos/execuções/plataformas web, URLs de execução e
arquivos `.htm`, `.html` e `.xhtml`. Um jogo misto conserva suas versões
suportadas e recebe um registro principal compatível. Registros HTML inseridos
diretamente por ferramentas externas continuam excluídos das consultas ativas e
não podem ser executados. Novos cadastros e importações HTML são recusados,
inclusive quando o tipo geral é `native`. Uma importação inválida não deixa
inserções parciais.

O caminho `webbrowser` e os estados visuais exclusivos de jogos web foram
removidos. HTTP/HTTPS, Google Drive e `gdown` permanecem disponíveis para
downloads de arquivos e assets. Os JSONs iniciais de jogos já não continham
HTML; não foram apagados jogos nativos desses arquivos.

## Arquivos principais

| Arquivo | Responsabilidade |
| --- | --- |
| `backend/database/migrations.py` e `migrations/009*` a `011*` | Atualização segura e importação inicial. |
| `backend/catalog_service.py` | Regras e transações compartilhadas de cadastro/importação. |
| `backend/emulators/package_resolver.py` | Seleção de pacotes no SQLite por SO/arquitetura. |
| `backend/game_support.py` | Política que recusa execução HTML/navegador. |
| `backend/recovery.py` | Backup SQLite consistente, manifesto e restauração verificada. |
| `backend/__main__.py`, `backend/tools/` | Clientes de terminal dos serviços. |
| `contracts/catalog.py`, `models.py`, `ports.py` | Dados e interfaces entre camadas. |
| `application/controller.py` | Tarefas, navegação, salvamento e proteção contra callbacks antigos. |
| `frontend/views/registry.py`, `window.py`, `preview.py` | Listas/formulários reais e prévia independente. |

## Instalar, iniciar e testar

No ambiente de nuvem já preparado:

```bash
cd /workspace/Raspberry-Launcher
source /workspace/.launcher-cloud/env.sh
python -m pip install -r requirements.txt
python -m backend init
python -m backend list
xvfb-run -a python main.py
```

O `env.sh` ativa `.venv`, Xvfb e caches fora do checkout, e seleciona
`RASPBERRY_LAUNCHER_HOME=/workspace/.launcher-cloud/runtime`. Em um desktop com
display disponível, use `python main.py`; para a prévia, use
`python -m frontend.preview`. Sem o override de diretório, o launcher usa o
`DATA/` do checkout e aplica as mesmas migrações nele. Faça backup antes.

Em outra instalação com Python 3.12, Tk e as bibliotecas gráficas do sistema:

```bash
cd /workspace/Raspberry-Launcher
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Validação completa na nuvem:

```bash
cd /workspace/Raspberry-Launcher
source /workspace/.launcher-cloud/env.sh
xvfb-run -a python -m unittest discover -s tests -v
python -m compileall -q backend frontend application contracts tests main.py
ruff check .
```

Ruff é uma ferramenta adicional (`python -m pip install ruff==0.15.7`), não uma
dependência de execução. Sem display/Xvfb, os testes gráficos são ignorados;
essa execução reduzida não equivale à validação gráfica completa. O checkout
original contém `.pyc` rastreados: o `env.sh` mantém `PYTHONPYCACHEPREFIX` fora do
checkout para não modificá-los durante imports/compilação.

## Operações da CLI

```bash
cd /workspace/Raspberry-Launcher
source /workspace/.launcher-cloud/env.sh
python -m backend catalog list game
python -m backend catalog get game snake
python -m backend catalog list emulator
python -m backend catalog list emulator_package
```

Salvar usa um **objeto JSON de campos**, sem o envelope `values` da saída.
Por exemplo, para criar um emulador apenas no catálogo:

```bash
printf '%s\n' '{"id":"meu_emulador","name":"Meu emulador"}' | \
  python -m backend catalog save emulator --file -
printf '%s\n' '{"name":"Nome atualizado"}' | \
  python -m backend catalog save emulator --file - --edit meu_emulador
```

Para jogos/pacotes, forneça os campos apresentados no formulário equivalente;
caminhos locais precisam existir. `catalog import --file ARQUIVO.json` recebe
uma lista de jogos, com `versions` opcional. A importação insere apenas registros
ausentes e preserva edições locais; para editar, use `catalog save --edit`.

Também continuam disponíveis `python -m backend.tools.add_game` e
`update_game`; `--version` opera uma versão. Os novos pares `add_emulator` /
`update_emulator` e `add_emulator_package` / `update_emulator_package` oferecem
prompts e `--file JSON`/`--id ID`. Use `--help` para cada comando.

## Backup, restauração e resultados

O procedimento completo, inclusive restauração sobre destino existente com
rollback, está em [Recuperação](RECUPERACAO.md). Um ensaio seguro usa destinos novos:

```bash
python -m backend.tools.create_recovery_point \
  --home /workspace/.launcher-cloud/runtime \
  --destination /workspace/.phase1-recovery/meu-ponto
python -m backend.tools.restore_recovery_point \
  --recovery-point /workspace/.phase1-recovery/meu-ponto \
  --destination /workspace/.phase1-recovery/meu-ensaio
```

Não reutilize nomes de pontos já existentes. O mecanismo cobre `DATA/`,
`USERDATA/config/` e `config/`, sem executáveis, caches ou saves próprios dos
jogos. Feche o launcher para restaurar. Código anterior e banco também estão
preservados no baseline técnico de T00.

Consulte [Validação](VALIDACAO.md) para resultados finais e limites. Perfis
completos, RGSX, novos adaptadores, instalação completa de ROMs, estatísticas,
conquistas, FPS, temas e música permanecem fora desta entrega.
