# Camada de compatibilidade.

# A UI não deve acessar os launchers diretamente.
# Toda abertura de jogos passa por este módulo.


from backend.launchers.launcher_factory import LauncherFactory


def abrirJogo(game):

    LauncherFactory.launch(game)


def jogoInstalado(game):

    return LauncherFactory.is_installed(game)
