# Contas online do Raspberry-Launcher

O launcher pode usar Supabase Auth (cadastro com e-mail/senha) e PostgreSQL para recuperar as estatísticas em vários computadores. A infraestrutura remota NÃO é implantada automaticamente; é preciso configurar um projeto próprio antes de usar login real.

## 1. Preparar o servidor remoto

1. Crie um projeto em https://supabase.com.
2. Em Authentication, ative o provedor e-mail/senha, confirmação de e-mail, configurações de e-mails/SMTP e proteção contra abuso/rate limiting para uso público.
3. Execute o arquivo supabase/schema.sql **integralmente** no editor SQL do projeto. Ele define as tabelas protegidas por RLS e a função autenticada de gravação idempotente.
4. Habilite a Data API e confirme, com duas contas de teste independentes, que cada uma só consegue ler suas próprias estatísticas.
5. Na configuração do cliente, utilize apenas a URL HTTPS e a chave **publishable/anon pública** do projeto. Nunca distribua chave secret/service_role, senha do banco ou connection string administrativa.

## 2. Conexão dos computadores

A versão desta branch já distribui **a URL do projeto e uma publishable key pública** em `backend/online_defaults.py`. Isso não é uma credencial administrativa; a autenticação de cada usuário e as políticas RLS protegem as estatísticas. Nenhuma senha ou token de usuário é embutido no aplicativo.

Ao iniciar o launcher, abra **Conta online** para entrar ou cadastrar. Um mesmo usuário pode acessar o serviço a partir de computadores diferentes sem configurar o servidor manualmente.

Para usar outro projeto Supabase, as variáveis `RASPBERRY_SUPABASE_URL` e `RASPBERRY_SUPABASE_PUBLISHABLE_KEY` substituem o destino público padrão, sem editar código. Para usar exclusivamente perfis locais, defina `RASPBERRY_ONLINE_DISABLED=1` antes de iniciar.

A configuração hospedada depende da disponibilidade do plano gratuito Supabase; os limites e a possível pausa por inatividade são responsabilidade do serviço.

## 3. Cadastro e uso

1. Clique em Conta online na barra lateral.
2. Cadastre e-mail, senha de pelo menos 8 caracteres e um nome de jogador.
3. Confirme o e-mail recebido, se solicitado, e então faça login.
4. Suas estatísticas são vinculadas ao identificador remoto da conta, e não ao nome de exibição. Cada login ativa o perfil correspondente no SQLite local.
5. Os dados pessoais são atualizados primeiro no SQLite. Uma fila de eventos imutáveis registra favoritos, tempo jogado, última execução e preferências de tema/volume.
6. Clique em Sincronizar agora para enviar os eventos e baixar os dados da conta. Enquanto houver login e o perfil online estiver ativo, também há uma tentativa automática aproximadamente a cada 60 segundos.
7. Em outro PC, configure o mesmo projeto Supabase e entre com o mesmo e-mail e senha. Os jogos com os mesmos IDs de catálogo mostrarão as estatísticas sincronizadas.
8. Se desejar trazer favoritos e tempo do perfil Padrão, use a ação Importar histórico local (uma vez) nas Configurações. Ela não apaga os dados de origem.

## 4. Resolução de conflitos e segurança

- O servidor recebe incrementos de segundos identificados por IDs únicos. Reenviar um evento depois de falha de rede **não duplica** o tempo jogado.
- Favoritos e preferências editados em computadores diferentes obedecem à última alteração processada no servidor; não existe interface de resolução de conflitos neste escopo.
- Mudanças novas que surgem durante uma consulta remota permanecem no outbox e não são sobrescritas pelo download.
- A importação de histórico local é idempotente por computador/perfil. Importar cópias independentes do mesmo histórico em vários PCs pode duplicar os segundos antigos: faça a importação uma única vez a partir de uma origem escolhida.
- Os tokens de login ficam somente na memória. Ao reiniciar o aplicativo é necessário entrar novamente. Nem senhas nem tokens são gravados no SQLite; a cache local de estatísticas **não é criptografada**.
- Ao sair da conta, o perfil local padrão volta a ser selecionado; os eventos pendentes da conta permanecem no banco para envio depois do próximo login.
- A sincronização não inclui instalações, executáveis, emuladores, caminhos de ROM, catálogo global, arquivos de saves nem pontuação externa. Esses elementos continuam locais.
- Não desative RLS nem incorpore chaves administrativas no desktop.

## 5. Verificações

    xvfb-run -a python -m unittest discover -s tests -v
    python -m compileall -q backend frontend application contracts tests main.py
    ruff check .
    python -m pip check

Os testes do servidor remoto utilizam um fake determinístico: eles validam múltiplos clientes, falha de rede, reenvio, isolamento e importação sem credenciais reais. Isso não substitui um teste final com o seu próprio projeto Supabase ativo.

**Antes de migrar um banco real**, identifique o runtime correto e faça backup consistente com ensaio de restauração conforme docs/RECUPERACAO.md. A migração local 013_online_accounts.sql é incremental e não apaga jogos ou perfis anteriores.
