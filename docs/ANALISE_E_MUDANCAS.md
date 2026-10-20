# Análise e reestruturação

> Registro histórico da reestruturação anterior à Fase 1. As referências abaixo
> a execução web e às fontes JSON descrevem aquele estado. Na entrega atual,
> HTML/navegador foi retirado e os cadastros de runtime estão no SQLite. Consulte
> [Fase 1](FASE1.md), [Arquitetura](ARQUITETURA.md) e [Validação](VALIDACAO.md).

O ZIP original continha 161 arquivos, sendo 121 arquivos Python. Foram analisados os módulos, os dois READMEs, as migrações SQL, os JSONs, o resumo textual do banco e o esquema/conteúdo real de `DATA/library.db`. As imagens foram tratadas como recursos do programa.

O projeto já apresentava uma divisão nominal entre `CORE` e `UI`, mas havia dependências nos dois sentidos. Apenas mover as pastas manteria esses acoplamentos.

## Acoplamentos encontrados e destino das responsabilidades

| Código original | Problema observado | Organização após a reestruturação anterior |
| --- | --- | --- |
| `CORE/download/native_game_installer.py` | Recebia botões, atualizava widgets, criava threads e navegava para a biblioteca. | Instalador síncrono em `backend/download/`; tarefas e navegação em `application/`; estado visual em `frontend/bindings.py`. |
| `CORE/uninstaller.py` | Importava a janela, alterava botões e chamava `showPage`. | Operação sem GUI em `backend/uninstaller.py`; apresentação e atualização da tela pelo controlador. |
| `CORE/score.py` | Mantinha widgets globais e chamava `app.after`. | Leitura/sincronização de arquivos no backend; polling no controlador; rótulos no frontend, identificados pelo ID do jogo. |
| `CORE/launchers/native_launcher.py` | Importava `UI.pages` para jogos HTML. | Usa o navegador padrão por `webbrowser`, sem importar telas. |
| `UI/cards.py` | Instanciava o instalador, o gerenciador de assets, o launcher e o desinstalador. | Recebe `GameSummary` e emite ações contendo apenas IDs. |
| `UI/views/game/details.py` | Consultava jogos e versões, alterava favoritos e instalava jogos dentro da tela. | Apresenta `GameDetails`; o controlador solicita as operações pela API. |
| `UI/views/biblioteca.py`, `jogos.py`, `search.py`, `colecoes/home.py` | Faziam consultas e decisões de estado junto com a montagem dos widgets. | Consultas/filtros no backend; grade e busca visuais em `frontend/views/catalog.py`. |
| `UI/views/plataformas/*` | Repetiam o mesmo layout, acessavam managers e misturavam a instalação do PCSX2 com o botão. | Um template visual de plataforma; dados e exemplos em `PlatformInfo` e `backend/catalog/platforms.json`. |
| `UI/pages.py` | Misturava roteamento, montagem de telas e abertura do navegador. | Navegação em `application/controller.py`; renderização no frontend; execução web no backend. |
| `UI/window.py`, `UI/components.py` | Criavam a janela e widgets durante a importação. | Criação explícita por `LauncherWindow`; composição por `main.py`. |
| `UTILS/` | Misturava caminhos operacionais com funções de apresentação. | Caminhos no backend; tratamento visual de imagens no frontend; recursos estáticos injetados por `UiResources`. |
| `CORE/database`, `library`, `assets`, `emulators`, `plugins` | Continham a maior parte da lógica útil já separada. | Mantidos em `backend/`, com imports e pontos de integração ajustados. |
| `PLUGINS/pcsx2` | Adaptador externo ao núcleo com import do antigo pacote. | `backend/plugin_adapters/pcsx2`, com o contrato do plugin preservado. |
| `tools/` e `teste.py` | Caminhos e comandos dependiam da localização original. | `backend/tools/`, execução por módulo e caminhos centralizados; `teste.py` virou `inspect_platforms.py`. |

## Ajustes necessários para manter os fluxos

- O instalador usa os dados da versão escolhida, inclusive quando o registro principal não possui URL de download.
- A versão solicitada é conferida antes da instalação para impedir associação ao jogo errado.
- A extração e a localização do executável são verificadas antes de substituir uma instalação existente.
- O modelo original de uma pasta instalada por jogo foi mantido. Ao substituir o pacote, o registro de versões instaladas é atualizado para refletir o pacote presente.
- O backend envia fases de operação; o frontend traduz essas fases em textos e estados dos botões.
- A execução nativa usa o diretório do executável como diretório de trabalho e registra tempo após o processo terminar.
- O adaptador PCSX2 devolve o processo iniciado, permitindo acompanhamento de tempo também quando o plugin oferece esse retorno.
- O cache reconhece arquivos incluídos no ZIP mesmo quando o banco contém caminhos absolutos de outro computador, em Linux ou Windows.
- O fallback de imagem retorna um arquivo existente. O ZIP original continha somente `cover.png` entre os placeholders.
- Um emulador marcado como instalado só é considerado disponível quando seu executável existe no computador atual.
- A inicialização cria as tabelas necessárias, aplica migrações de forma idempotente e completa os campos de plataforma usados pelos repositórios.
- O health check usa módulos existentes, o mesmo interpretador Python e códigos de saída que indicam falha. A referência ao inexistente `check_games_dependency.py` foi removida.
- As dependências foram divididas por camada; a lista original completa foi mantida como referência histórica.

## Funcionalidades e partes ainda incompletas

Biblioteca, loja/lista de não instalados, busca, detalhes, versões, favoritos, instalação, remoção, lançamento web/nativo, pontuação, ferramentas administrativas e o caminho de integração PCSX2 continuam conectados à lógica real.

As rotas Favoritos e Recentes, antes sem renderização conectada, agora exibem consultas aos dados que já existiam. As plataformas usam os jogos cadastrados; quando não há jogos, mostram explicitamente os exemplos que antes estavam escritos nas telas. Exemplos de catálogo não são apresentados como jogos instaláveis.

`Finalizados`, filtros de gênero/ano e persistência de configurações não estavam implementados no código original. Continuam identificados como partes incompletas; a reestruturação não simula essas funções. Os controles de configuração demonstrativos ficam desativados.

Somente PCSX2 possui adaptador de plugin fornecido neste ZIP. Cadastros de outras plataformas/emuladores não equivalem à existência de seus adaptadores. O catálogo de pacotes fornecido possui entradas PCSX2 para Linux e Windows e foi preservado.

Os jogos HTML abrem no navegador padrão, como acontecia de fato no código original; não foi acrescentado um navegador embutido. Os READMEs antigos descreviam algumas funções planejadas como se já existissem e listavam como futuras tabelas que já estavam no banco. Por isso, foram arquivados em `docs/historico/` e substituídos por instruções correspondentes ao código atual.

## Preservação dos dados

Os 27 arquivos existentes em `ASSETS/`, `DATA/` e `USERDATA/` foram comparados byte a byte com o ZIP original e preservados. O banco fornecido não foi usado como banco de testes. A inicialização normal do aplicativo aplicará as migrações necessárias ao banco usado na execução.

As URLs e a configuração de conteúdo não foram atualizadas para supostas versões mais recentes. Veja em `VALIDACAO.md` o que foi efetivamente testado.
