games = [

    {
        "name": "Snake",
        "folder": "snake",
        "icon": "snake.png",
        "score": True,
        "strip_root_folder": False,

        "versions": {
            "Linux": {
                "zip": "snake-linux.zip",
                "url": "https://drive.google.com/uc?export=download&id=1u6Uj5ro5HLFOXxsgIwWBnmmEyrnfq8H4",
                "file": "snake",
                "type": "linux"
            }
        }
    },

    {
        "name": "Daggerfall",
        "folder": "daggerfall",
        "icon": "daggerfall.png",
        "score": False,
        "strip_root_folder": True,

        "versions": {

            "Windows": {
                "zip": "daggerfall.zip",
                "url": "https://github.com/luccasbarbosa1242/game-launcher-files/releases/download/v1.0/daggerfall.zip",
                "file": "DaggerfallUnity.exe",
                "type": "exe"
            },

            "Linux": {
                "zip": "daggerfall-linux.zip",
                "url": "https://drive.google.com/uc?export=download&id=1I5SuMuJbu38Hu968Z7J7g-32-sJyybGX",
                "file": "DaggerfallUnity.x86_64",
                "type": "linux"
            }
        }
    },

    {
        "name": "TicTacToe",
        "folder": "tictactoe",
        "icon": "tictactoe.png",
        "score": False,
        "internal_browser": True,
        "url": "https://poki.com/br/g/tictactoe",

        "versions": {
            "Windows": {},
            "Linux": {}
        }
    },

    {
        "name": "Tetris",
        "folder": "tetris",
        "icon": "tetris.png",
        "score": True,
        "strip_root_folder": False,

        "versions": {
            "Linux": {
                "zip": "tetris-linux.zip",
                "url": "https://drive.google.com/uc?export=download&id=1dLxA6W4CcSFErKDlROgjlRvTs-F3URCM",
                "file": "tetris",
                "type": "linux"
            }
        }
    }
]

from UTILS.system import currentSystem


def getGameVersion(game):

    system = currentSystem()

    versions = game.get("versions", {})

    return versions.get(system)