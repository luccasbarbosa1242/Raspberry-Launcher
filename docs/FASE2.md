# Fase 2 — Perfis locais (T02)

Implementação iniciada sobre `96a283d`, mantendo a instalação e o catálogo globais.

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

Os perfis são locais; não há login ou sincronização, saves isolados por
usuário, controles efetivos de música ou volume, FPS, RGSX ou novo adaptador.
A pontuação de jogos mantida em arquivos externos ao SQLite continua
global. Um processo iniciado para um perfil mantém seu histórico de tempo
nesse perfil, mesmo quando a seleção da interface muda.

Verifique testes e comportamento gráfico no ambiente com Python, Tk e
CustomTkinter instalados antes de mesclar esta branch.
