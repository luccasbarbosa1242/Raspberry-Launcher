# Validação

Validação realizada em Linux, Python 3.12, utilizando as versões diretas registradas em `requirements/backend.txt` e `requirements/frontend.txt`. As telas foram exercitadas com CustomTkinter real em uma tela virtual Xvfb.

## Resultado

**43 testes automatizados aprovados, sem testes ignorados na execução com tela virtual.**

Também passaram a compilação dos módulos Python e a verificação estática configurada no `pyproject.toml`. As telas inicial e de detalhes foram inspecionadas visualmente com os dados e capas fornecidos no ZIP.

## Cobertura

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

## Limites práticos

Os testes de download e instalação utilizaram arquivos locais reproduzíveis. Não foi baixado cada jogo das URLs externas do catálogo, nem executado o PCSX2 real com uma ROM comercial. A disponibilidade desses provedores, dos pacotes e do ambiente do usuário continua necessária para os downloads/execuções correspondentes.

Não houve execução em Windows ou macOS. O caminho de código existente para plataformas e os arquivos de configuração foram mantidos; a validação executável foi realizada no ambiente Linux indicado acima.

## Reproduzir

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

## Correção posterior: argumento `fuzzy`

O primeiro ZIP reestruturado continha uma chamada `gdown.download(..., fuzzy=True)`. A versão 6.1.0 fixada nos requirements não aceita esse argumento. A falha foi reproduzida com a função real dessa versão, e o argumento foi removido sem alterar as dependências.

Os testes iniciais de instalação usavam arquivos locais e não detectavam essa incompatibilidade. Os novos testes de Google Drive mantêm a função real de download e substituem apenas a sessão HTTP por uma resposta controlada, para detectar incompatibilidades na API e verificar os bytes gravados e o registro da instalação.

## Correção posterior: menu de três pontos

O projeto original oferecia `Desinstalar` no popup de três pontos dos jogos instalados que não eram web. A reestruturação havia limitado a disponibilidade à pasta `installed/<id>` do projeto e trocado o popup CustomTkinter por um menu nativo.

O popup CustomTkinter e a ação `Desinstalar` foram restaurados. O backend informa a disponibilidade quando o executável/ROM existe, inclusive em outro local, ou quando há uma pasta gerenciada que pode ser removida. Jogos web continuam sem essa opção. A interface envia apenas o ID ao controlador; não consulta caminhos ou o banco.

O backend também aceita a ação para ROMs, como o original. A desinstalação remove a pasta gerenciada e atualiza os registros. Arquivos externos ao diretório gerenciado não são apagados, mantendo a política do código original.

Os testes cobrem jogos locais sem pasta gerenciada, ROMs, ausência da ação em jogos web, abertura do popup, clique no botão, remoção efetiva da instalação e fechamento do popup ao mudar de tela.

A atualização incremental contém somente `backend/api.py` e `frontend/cards.py`. Para aplicá-la, feche o launcher e substitua esses dois arquivos na cópia atual do projeto.
