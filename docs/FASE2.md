# Fase 2 — Perfis locais (T02)

O **T02** implementou perfis e preferências locais, mantendo a instalação e o catálogo globais. A Fase 2 foi ampliada posteriormente com **contas online, sincronização e Lembrar de mim**; consulte [Contas online](CONTAS_ONLINE.md). Todas as entregas fazem parte da branch principal `main` desde a consolidação das fases.

## Dados e migração

A migração `012_local_profiles.sql` cria o perfil `default`, suas
preferências e registros em `profile_game_state`. A cópia inicial
considera **todos** os jogos (inclusive arquivados) e preserva favorito,
tempo acumulado e última execução. A cópia usa `INSERT OR IGNORE` e um
marcador de migração aplicado transacionalmente; novas inicializações não
substituem progresso por valores legados. As colunas de `games` continuam
como espelho compatível do **perfil padrão** para ferramentas antigas.

Novos perfis recebem valores pessoais independentes, sem duplicar
instalações, versões, downloads, emuladores ou o catálogo. O perfil ativo
fica em `settings.active_profile_id`; tema e volume de música apenas
persistem a preferência local, sem ajustar som do sistema.

## Antes de executar sobre um banco existente

Feche o launcher e quaisquer escritores. Descubra primeiro o valor de
`RASPBERRY_LAUNCHER_HOME`; sem ele, a fonte de dados será o checkout.
Não substitua o banco de runtime pelo `DATA/library.db` versionado.

Com caminhos próprios para cada ambiente:

```bash
python -m backend.tools.create_recovery_point --home "$RUNTIME" --destination "$RECOVERY"
python -m backend.tools.restore_recovery_point --recovery-point "$RECOVERY" --destination "$RESTORE_TEST"
```

Verifique a integridade, contagens e histórico no destino de ensaio.
Só depois execute `python -m backend init` no runtime escolhido.

## Limites

Esta implementação **T02** é local; o login e a sincronização de favoritos, tempo de jogo, últimas execuções e preferências foram acrescentados na extensão de **contas online** da mesma Fase 2 (veja [Contas online](CONTAS_ONLINE.md)). Ainda não há sincronização de saves, instalações/ROMs, controles efetivos de música ou volume, FPS, RGSX ou novo adaptador.
A pontuação de jogos mantida em arquivos externos ao SQLite continua
global. Um processo iniciado para um perfil mantém seu histórico de tempo
nesse perfil, mesmo quando a seleção da interface muda.

O tema claro usa paleta de superfícies, menus, cartões, navegação e textos
independente da paleta escura. A troca de tema afeta os widgets já abertos;
a seleção de outro perfil também aplica seu tema imediatamente. Os contrastes
de texto e status são validados por teste automatizado (mínimo 4,5:1).

A `main` foi validada com **143 testes automatizados** (incluindo interface e PostgreSQL): [GitHub Actions](https://github.com/luccasbarbosa1242/Raspberry-Launcher/actions/runs/39707210299). Cadastro, confirmação por e-mail, login e Lembrar de mim também foram testados manualmente. A validação entre dois computadores físicos segue pendente.
