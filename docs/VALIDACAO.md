# Validação

## Fase 1 — T00, T01, T03 e T05

A base anterior executou **43 testes com sucesso, sem ignorados**. A versão desta
fase executa **106 testes com sucesso, sem falhas e sem ignorados**, em Linux
x86_64, Python 3.12 e Tk/CustomTkinter real sob Xvfb. A compilação dos módulos,
`ruff check .`, `pip check` e `git diff --check` também passaram.

| Área | Evidência atual |
| --- | --- |
| Banco novo e legado | Esquema novo, migração do banco fornecido, preservação de IDs/favoritos/tempo/instalações, repetição sem duplicar e rollback de migração com seed inválido. |
| Fonte dos cadastros | JSON importado uma vez; pacotes/plataformas lidos do SQLite; alterações no banco sobrevivem à reinicialização. |
| Instalações | Estado local normalizado; instalar/remover sincroniza registros; edição de metadados não repõe caminhos legados; SO/arquitetura incompatíveis são recusados antes de instalar/executar. |
| Cadastros | Serviços, CLI JSON/stdin e ferramentas interativas criam/editam jogos, versões, emuladores e pacotes com as mesmas validações. |
| Interface | Oito testes novos de listas/formulários, além dos testes gráficos anteriores; criação/edição real com controlador/backend/SQLite temporários, erros e retry. |
| Coordenação | Tarefas fora da thread gráfica, callbacks antigos descartados, envios duplicados com feedback e novos formulários independentes durante salvamento. |
| HTML | Arquivamento de legado tipo nativo+HTML, preservação de histórico/assets/coleções, jogos mistos, rejeição por CLI/serviços/importação/formulário e bloqueio de execução direta. |
| Downloads e execução | Função real de gdown com HTTP controlado, ZIP local real, processo Python real e instalação/execução/desinstalação preservadas. |
| Recuperação | Dez testes de SQLite/WAL, checksums, manifesto, restauração, caminhos inseguros, destino existente, rollback e preservação de instalações/cache. |
| Runtime atual | Backup e restauração ensaiados; migrações 009–011 aplicadas ao runtime; três títulos ativos renderizados por main.py real e fixture da prévia renderizada sem erros de callback. |

Os testes usam diretórios temporários. O banco original rastreado
`DATA/library.db` permaneceu intacto; a cópia configurada em
`/workspace/.launcher-cloud/runtime` foi migrada. `tictactoe` e suas versões
permanecem arquivados, com histórico; Snake, Daggerfall e Tetris continuam ativos.

Comandos executados na raiz real:

```bash
cd /workspace/Raspberry-Launcher
source /workspace/.launcher-cloud/env.sh
xvfb-run -a python -m unittest discover -s tests -v
python -m compileall -q backend frontend application contracts tests main.py
ruff check .
python -m pip check
git diff --check
```

O log da execução está em `/workspace/.phase1-recovery/final-tests.log`; o baseline
anterior está em `baseline-tests.log` no mesmo diretório. Veja os comandos de
instalação/inicialização em [Fase 1](FASE1.md) e os ensaios de backup/restauração em
[Recuperação](RECUPERACAO.md).

### Limitações da execução atual

- Não foram baixados todos os jogos das URLs externas. Google Drive retornou 403
  do proxy neste ambiente; os testes mantêm o gdown real e controlam o transporte.
- Não houve execução real de PCSX2 com uma ROM nem verificação em Windows,
  macOS ou ARM. SO/arquitetura são validados por fixtures/probes locais.
- A interface foi exercitada em tela virtual. CustomTkinter usa seu fallback de
  desenho porque `~/.fonts` é somente leitura; os testes e startup passaram.
- Cadastros de emuladores não incluem novos adaptadores. Perfis completos,
  sincronização externa e as demais fases do plano não foram implementados.

## Histórico — reestruturação anterior

O registro abaixo descreve a validação anterior à Fase 1, inclusive o suporte
web então existente. Para o comportamento atual, use os resultados acima.

Validação realizada em Linux, Python 3.12, utilizando as versões diretas registradas em `requirements/backend.txt` e `requirements/frontend.txt`. As telas foram exercitadas com CustomTkinter real em uma tela virtual Xvfb.

### Resultado

**43 testes automatizados aprovados, sem testes ignorados na execução com tela virtual.**

Também passaram a compilação dos módulos Python e a verificação estática configurada no `pyproject.toml`. As telas inicial e de detalhes foram inspecionadas visualmente com os dados e capas fornecidos no ZIP.

### Cobertura

| Área | Evidência de validação |
| --- | --- |
| Dependências | Verificação de imports proibidos entre camadas; backend executado sem GUI e sem pacotes externos; importação do frontend sem backend e sem abrir janela. |
| Banco | Inicialização de banco vazio, migrações repetidas e preservação de registros. |
| Biblioteca | Busca, favoritos, ordenação de recentes e filtro de instalados. |
| Assets | Recuperação do cache com caminhos antigos Linux/Windows e fallback quando a origem não está disponível. |
| Google Drive | Função real do gdown 6.1.0 executada com transporte HTTP controlado, cobrindo links diretos, links compartilhados e instalação até a atualização do banco. |
| Instalação | ZIP local real, progresso, executável instalado, seleção de versão, rejeição de versão de outro jogo e arquivo inválido sem apagar instalação existente. |
| Remoção | Exclusão da instalação gerenciada, atualização do banco e preservação de favoritos, tempo jogado e pontuação persistente. |
| Execução nativa | Processo Python real, diretório de trabalho correto e tempo de jogo gravado após a saída. |
| Jogos web | Chamada ao navegador padrão e atualização do histórico, com abertura do navegador simulada. |
| Emuladores | Instalação de pacote local de teste, reaproveitamento do executável instalado e rejeição de caminho antigo inexistente. |
| ROMs | Carregamento do plugin PCSX2 e argumentos de execução conferidos, com processo do emulador simulado. |
| Controlador | Resultados antigos não substituem telas novas, operações duplicadas são bloqueadas, falhas permitem nova tentativa e callbacks de worker são entregues na thread principal. |
| Interface | Templates de telas, ações por ID, callbacks das versões corretas, pontuação, restauração dos botões após falha e cancelamento de temporizadores no fechamento. |
| Integração gráfica | Instalar, favoritar, buscar e desinstalar usando os widgets reais e o backend real sobre arquivos temporários. |
| Ferramentas administrativas | Os 33 scripts originais de `tools/` e o diagnóstico antes chamado `teste.py` foram exercitados por módulo. Inclui cadastro, atualização, remoção, importação, migrações, assets, coleções, plataformas, backup e restauração. |
| Dados fornecidos | 27 arquivos de dados/recursos comparados byte a byte com o ZIP de origem. |

### Limites práticos

Os testes de download e instalação utilizaram arquivos locais reproduzíveis. Não foi baixado cada jogo das URLs externas do catálogo, nem executado o PCSX2 real com uma ROM comercial. A disponibilidade desses provedores, dos pacotes e do ambiente do usuário continua necessária para os downloads/execuções correspondentes.

Não houve execução em Windows ou macOS. O caminho de código existente para plataformas e os arquivos de configuração foram mantidos; a validação executável foi realizada no ambiente Linux indicado acima.

### Reproduzir

Na raiz do projeto, após instalar as dependências:

```bash
python -m unittest discover -s tests -v
python -m compileall -q backend frontend application contracts tests main.py
```

Com Xvfb disponível em Linux:

```bash
xvfb-run -a python -m unittest discover -s tests -v
```

Sem dependências gráficas ou sem uma tela, os testes gráficos são ignorados e os demais continuam disponíveis. Para a verificação estática opcional, instale Ruff e execute `ruff check .`.

Os bancos e jogos de teste ficam em diretórios temporários separados. O backend permite escolher outro diretório de execução com `RASPBERRY_LAUNCHER_HOME` ou `python -m backend --home DIRETORIO`.

### Correção posterior: argumento `fuzzy`

O primeiro ZIP reestruturado continha uma chamada `gdown.download(..., fuzzy=True)`. A versão 6.1.0 fixada nos requirements não aceita esse argumento. A falha foi reproduzida com a função real dessa versão, e o argumento foi removido sem alterar as dependências.

Os testes iniciais de instalação usavam arquivos locais e não detectavam essa incompatibilidade. Os novos testes de Google Drive mantêm a função real de download e substituem apenas a sessão HTTP por uma resposta controlada, para detectar incompatibilidades na API e verificar os bytes gravados e o registro da instalação.

### Correção posterior: menu de três pontos

O projeto original oferecia `Desinstalar` no popup de três pontos dos jogos instalados que não eram web. A reestruturação havia limitado a disponibilidade à pasta `installed/<id>` do projeto e trocado o popup CustomTkinter por um menu nativo.

O popup CustomTkinter e a ação `Desinstalar` foram restaurados. O backend informa a disponibilidade quando o executável/ROM existe, inclusive em outro local, ou quando há uma pasta gerenciada que pode ser removida. Jogos web continuam sem essa opção. A interface envia apenas o ID ao controlador; não consulta caminhos ou o banco.

O backend também aceita a ação para ROMs, como o original. A desinstalação remove a pasta gerenciada e atualiza os registros. Arquivos externos ao diretório gerenciado não são apagados, mantendo a política do código original.

Os testes cobrem jogos locais sem pasta gerenciada, ROMs, ausência da ação em jogos web, abertura do popup, clique no botão, remoção efetiva da instalação e fechamento do popup ao mudar de tela.

A atualização incremental contém somente `backend/api.py` e `frontend/cards.py`. Para aplicá-la, feche o launcher e substitua esses dois arquivos na cópia atual do projeto.
