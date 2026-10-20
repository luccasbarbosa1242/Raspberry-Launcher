# Recuperação da Fase 1

O ponto de recuperação cobre `DATA/` inteiro, `USERDATA/config/` e `config/`
do diretório de execução escolhido. O banco principal é copiado pela API
`sqlite3.Connection.backup`: transações confirmadas no WAL entram na cópia;
transações ainda não confirmadas ficam de fora. A cópia é autocontida, sem
depender dos arquivos `library.db-wal`, `library.db-shm` ou `library.db-journal`.
Nenhuma migração é executada ao criar ou restaurar o ponto.

Cada ponto contém `payload/` e `manifest.json`, com inventário de arquivos,
tamanhos, SHA256, data UTC e origem. A restauração confere esses dados e executa
`PRAGMA integrity_check` antes de modificar o destino. SHA256 detecta corrupção;
o manifesto não é uma assinatura de autenticidade. Utilize pontos de origem
conhecida e mantenha-os fora do checkout e fora do diretório que será restaurado.
Links simbólicos, arquivos especiais e caminhos que escapem do escopo são recusados.

## Registro do estado anterior à implementação

- Repositório: `luccasbarbosa1242/Raspberry-Launcher`.
- Ref solicitada: `main`; checkout inicial na branch local `work`.
- Commit de origem: `55c54772ab19359857f04755d3392bfc252367be`.
- Branch de implementação: `codex/phase-1-catalogs`.
- Baseline local: `/workspace/.phase1-recovery/baseline-55c5477/`.

O baseline contém `repository.db`, `runtime.db`, `tracked-files.tar.gz` e um
manifesto de hashes. Seu registro informa checkout inicialmente limpo e 43 testes
aprovados, sem ignorados. Ele preserva também o código anterior; é um arquivo
técnico de baseline, com formato diferente dos novos pontos de recuperação.
Não passe esse diretório diretamente ao comando de restauração abaixo.

## Criar um ponto antes de alterar dados

Feche o launcher e ferramentas que estejam alterando configuração ou arquivos.
SQLite permite copiar um banco ativo com consistência transacional, mas os
outros arquivos não fazem parte da mesma transação: parar os escritores garante
coerência entre banco e configuração. Na raiz do checkout:

```bash
cd /workspace/Raspberry-Launcher
source /workspace/.launcher-cloud/env.sh

# Banco e dados presentes no próprio checkout: origem explícita.
python -m backend.tools.create_recovery_point \
  --home /workspace/Raspberry-Launcher \
  --destination /workspace/.phase1-recovery/catalog-before-change \
  --label 'Antes de alterar o catálogo do checkout'

# Banco usado pelo launcher no ambiente de nuvem: origem distinta.
python -m backend.tools.create_recovery_point \
  --home /workspace/.launcher-cloud/runtime \
  --destination /workspace/.phase1-recovery/runtime-before-change \
  --label 'Antes de alterar o catálogo do runtime'
```

Os destinos devem ser novos; um ponto existente nunca é sobrescrito. Para outro
backup, escolha outro nome. `--home` é obrigatório e não depende do valor atual
de `RASPBERRY_LAUNCHER_HOME`, evitando confundir o banco do checkout com o runtime.
O comando imprime JSON com `recovery_point`. Não coloque credenciais em `--label`.

## Ensaiar a restauração em um novo diretório

```bash
python -m backend.tools.restore_recovery_point \
  --recovery-point /workspace/.phase1-recovery/runtime-before-change \
  --destination /workspace/.phase1-recovery/restore-rehearsal
```

O resultado informa `destination` e `rollback: null`, pois o destino era novo.
Os testes automatizados verificam que registros, configuração e diretórios
vazios são recuperados. É possível conferir o banco restaurado sem migrá-lo:

```bash
python - <<'PY'
from contextlib import closing
from pathlib import Path
import sqlite3

path = Path('/workspace/.phase1-recovery/restore-rehearsal/DATA/library.db')
with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as connection:
    assert connection.execute('PRAGMA integrity_check').fetchall() == [('ok',)]
    print('SQLite íntegro')
PY
```

## Restaurar sobre um runtime existente

Feche o launcher e todas as conexões SQLite do destino. O comando recusa qualquer
diretório existente, inclusive vazio, sem autorização explícita:

```bash
python -m backend.tools.restore_recovery_point \
  --recovery-point /workspace/.phase1-recovery/runtime-before-change \
  --destination /workspace/.launcher-cloud/runtime \
  --overwrite
```

Somente `DATA/`, `USERDATA/config/` e `config/` são substituídos. O conteúdo
anterior desses escopos é movido para um diretório irmão, cujo caminho exato
aparece em `rollback` no JSON. Arquivos desses escopos ausentes no ponto deixam
de existir no destino; permanecem na pasta de rollback. Instalações, downloads,
cache e demais caminhos fora do escopo continuam no destino. Em uma falha de
movimentação, o código tenta recolocar os escopos anteriores automaticamente.
Não é uma transação atômica entre diretórios: em uma interrupção do processo,
preserve e inspecione a pasta de rollback antes de retomar alterações.

O rollback retém os arquivos anteriores e `rollback.json`; ele não é diretamente
um ponto de recuperação verificado. Se precisar voltar ao banco anterior e ele
estiver íntegro, crie um novo ponto usando o caminho retornado como `--home` e
restaure esse novo ponto com os mesmos comandos. Isso mantém também uma cópia do
estado que estiver sendo substituído. Não apague rollbacks antes de conferir
os dados recuperados.

## Escopo e validação

Scores sob `DATA/` são incluídos. Executáveis e saves próprios dos jogos,
`installed/`, `EMULATORS/`, downloads, `USERDATA/cache/` e código-fonte ficam fora
deste mecanismo. A recuperação de dados não recupera esses arquivos, e não
substitui a cópia do código do baseline. O backup completo de jogos e emuladores
fica fora da Fase 1. As ferramentas antigas `backup_database` e
`restore_database` continuam disponíveis por compatibilidade; os novos comandos
são os recomendados para obter a cópia SQLite consistente e verificada.

```bash
python -m unittest tests.test_recovery -v
```

Essa suíte usa apenas diretórios temporários. Cobre WAL confirmado/não confirmado,
restauração de arquivos, integridade de conteúdo e SQLite, caminhos inseguros,
links simbólicos, proteção de destinos existentes, rollback e preservação de
instalações/cache. Não modifica `DATA/library.db` do checkout nem o runtime real.
