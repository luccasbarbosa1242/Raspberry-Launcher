import os
import sys
import zipfile
import shutil
import subprocess
import threading
import platform
import gdown
import traceback
import requests


import customtkinter as ctk

from PIL import Image, ImageTk

from tkinterweb import HtmlFrame


# =========================================================
# CONFIG
# =========================================================
ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("green")


# =========================================================
# APP
# =========================================================
app = ctk.CTk()

app.title("Game Launcher")

app.geometry("1100x700")

app.minsize(900, 600)


# =========================================================
# GLOBALS
# =========================================================
bibliotecaFrame = None

jogosFrame = None

scoreLabels = {}


# =========================================================
# PATHS
# =========================================================
def basePath():

    if getattr(sys, 'frozen', False):

        return os.path.dirname(sys.executable)

    return os.path.dirname(
        os.path.abspath(__file__)
    )


def downloadsPath():

    return os.path.join(
        basePath(),
        "downloads"
    )


def installedPath():

    return os.path.join(
        basePath(),
        "installed"
    )


def iconsPath():

    if getattr(sys, 'frozen', False):

        return os.path.join(
            sys._MEIPASS,
            "icons"
        )

    return os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "icons"
    )


# =========================================================
# CREATE DIRS
# =========================================================
os.makedirs(
    downloadsPath(),
    exist_ok=True
)

os.makedirs(
    installedPath(),
    exist_ok=True
)


# =========================================================
# SYSTEM
# =========================================================
def currentSystem():

    return platform.system()

def download_file(url, output):
    temp = output + ".part"

    r = requests.get(url, stream=True)
    r.raise_for_status()

    with open(temp, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    os.replace(temp, output)

# =========================================================
# GAMES DATABASE
# =========================================================
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


# =========================================================
# GAME VERSION
# =========================================================
def getGameVersion(game):

    system = currentSystem()

    versions = game["versions"]

    if system not in versions:

        return None

    return versions[system]


# =========================================================
# LOAD IMAGE
# =========================================================
def loadImage(path, size=(70, 70)):

    if not os.path.isfile(path):

        print("Imagem não encontrada:")
        print(path)

        return None

    image = Image.open(path)

    return ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=size
    )


# =========================================================
# SCORE FILE
# =========================================================
def scoreFile(game):

    return os.path.join(
        installedPath(),
        game["folder"],
        "score.txt"
    )


# =========================================================
# BEST SCORE
# =========================================================
def lerBestScore(game):

    path = getScorePath(game)

    if not os.path.exists(path):

        return "0"

    try:

        with open(path, "r") as file:

            return file.read().strip() or "0"

    except:

        return "0"


# =========================================================
# UPDATE SCORES
# =========================================================
def atualizarScores():

    invalidLabels = []

    for gameName, label in scoreLabels.items():

        try:

            game = next(
                (
                    g for g in games
                    if g["name"] == gameName
                ),
                None
            )

            if not game:

                continue

            text = f"Best Score: {lerBestScore(game)}"

            if label.cget("text") != text:

                label.configure(
                    text=text
                )

        except:

            invalidLabels.append(gameName)

    for item in invalidLabels:

        if item in scoreLabels:

            del scoreLabels[item]

    app.after(
        1000,
        atualizarScores
    )


# =========================================================
# GAME INSTALLED
# =========================================================
def jogoInstalado(game):

    if game.get("internal_browser"):

        return True

    version = getGameVersion(game)

    if not version:

        return False

    path = os.path.join(
        installedPath(),
        game["folder"],
        version["file"]
    )

    return os.path.exists(path)


# =========================================================
# CLEAR FRAME
# =========================================================
def clearFrame(frame):

    for widget in frame.winfo_children():

        widget.destroy()


# =========================================================
# INTERNAL WEBVIEW
# =========================================================
def abrirPaginaInterna(title, url):

    window = ctk.CTkToplevel(app)

    window.title(title)

    window.geometry("1000x700")

    browser = HtmlFrame(window)

    if url.startswith("http://") or url.startswith("https://"):

        browser.load_website(url)

    else:

        browser.load_file(url)

    browser.pack(
        fill="both",
        expand=True
    )


# =========================================================
# TIC TAC TOE
# =========================================================
def abrirJogoVelha():

    abrirPaginaInterna(
        "Jogo da Velha",
        "https://poki.com/br/g/tictactoe"
    )


# =========================================================
# CREATE CARD
# =========================================================
def createCard(parent):

    card = ctk.CTkFrame(
        parent,
        corner_radius=18,
        height=100
    )

    card.pack(
        fill="x",
        padx=20,
        pady=10
    )

    return card


# =========================================================
# OPEN GAME
# =========================================================
def abrirJogo(game):

    if game.get("internal_browser"):

        abrirPaginaInterna(
            game["name"],
            game["url"]
        )

        return

    version = getGameVersion(game)

    if not version:

        print("Sistema não suportado.")

        return

    base = os.path.join(installedPath(), game["folder"])

    gamePath = None

    for root, dirs, files in os.walk(base):
        if version["file"] in files:
            gamePath = os.path.join(root, version["file"])
            break

    if not gamePath or not os.path.exists(gamePath):

        print("Executável não encontrado:")

        print(gamePath)

        return

    # ===================== CORREÇÃO MÍNIMA =====================
    gameType = version["type"].lower()
    # ===========================================================

    try:

        if gameType == "python":

            subprocess.Popen(
                [
                    sys.executable,
                    gamePath
                ],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "exe":

            subprocess.Popen(
                [gamePath],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "linux":

            os.chmod(gamePath, 0o755)

            subprocess.Popen(
                [gamePath],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "html":

            abrirPaginaInterna(
                game["name"],
                gamePath
            )

        elif gameType == "jar":

            subprocess.Popen(
                [
                    "java",
                    "-jar",
                    gamePath
                ],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "sh":

            os.chmod(gamePath, 0o755)

            subprocess.Popen(
                [
                    "bash",
                    gamePath
                ],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "appimage":

            os.chmod(gamePath, 0o755)

            subprocess.Popen(
                [gamePath],
                cwd=os.path.dirname(gamePath)
            )

    except Exception as e:

        print("Erro ao abrir jogo:")

        print(e)


# =========================================================
# INSTALL GAME
# =========================================================
def instalarJogo(game, button):

    version = getGameVersion(game)

    if not version:

        print("Sistema não suportado.")
        return

    button.configure(
        text="Baixando...",
        state="disabled"
    )

    def process():

        try:

            url = version.get("url")

            if not url:

                raise Exception("URL não encontrada.")

            zipPath = os.path.join(
                downloadsPath(),
                version["zip"]
            )

            # ============================================
            # DOWNLOAD
            # ============================================
            system = platform.system()

            if system == "Linux":
                gdown.download(url, zipPath, quiet=False)

            elif system == "Windows":
                download_file(url, zipPath)

            else:
                # fallback seguro
                download_file(url, zipPath)
            if not zipfile.is_zipfile(zipPath):
                raise Exception("Download inválido (Google Drive bloqueou ou retornou HTML).")

            app.after(
                0,
                lambda: button.configure(
                    text="Instalando..."
                )
            )

            # ============================================
            # INSTALL
            # ============================================
            gameFolder = os.path.join(
                installedPath(),
                game["folder"]
            )

            if os.path.exists(gameFolder):

                shutil.rmtree(gameFolder)

            os.makedirs(
                gameFolder,
                exist_ok=True
            )

            with zipfile.ZipFile(zipPath, 'r') as zip_ref:

                zip_ref.extractall(gameFolder)

                    # ============================================
            # REMOVE NESTED FOLDER
            # ============================================
            if game.get("strip_root_folder", False):

                while True:

                    contents = os.listdir(gameFolder)

                    if len(contents) != 1:
                        break

                    nestedPath = os.path.join(
                        gameFolder,
                        contents[0]
                    )

                    if not os.path.isdir(nestedPath):
                        break

                    for item in os.listdir(nestedPath):

                        src = os.path.join(
                            nestedPath,
                            item
                        )

                        dst = os.path.join(
                            gameFolder,
                            item
                        )

                        shutil.move(src, dst)

                    os.rmdir(nestedPath)

            # ============================================
            # DELETE ZIP
            # ============================================
            if os.path.exists(zipPath):

                os.remove(zipPath)

            print(f'{game["name"]} instalado.')

            app.after(
                0,
                afterInstall
            )

        except Exception as e:
            print("Erro instalação:")
            print(e)
            traceback.print_exc()

            app.after(
                0,
                lambda: button.configure(
                    text="Erro",
                    state="normal"
                )
            )

    def afterInstall():

        render()

        showPage("biblioteca")

    threading.Thread(
        target=process,
        daemon=True
    ).start()


# =========================================================
# TIC TAC TOE CARD
# =========================================================
def criarCardVelha(parent):

    card = createCard(parent)

    layout = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    layout.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    iconImage = loadImage(
        os.path.join(
            iconsPath(),
            "tictactoe.png"
        )
    )

    icon = ctk.CTkLabel(
        layout,
        text="",
        image=iconImage
    )

    icon.pack(
        side="left",
        padx=(0, 15)
    )

    title = ctk.CTkLabel(
        layout,
        text="Jogo da Velha",
        font=("Arial", 22, "bold")
    )

    title.pack(side="left")

    button = ctk.CTkButton(
        layout,
        text="Jogar",
        width=120,
        height=45,
        command=abrirJogoVelha
    )

    button.pack(side="right")


# =========================================================
# GAME CARD
# =========================================================
def criarCardJogo(parent, game, installed):

    card = createCard(parent)

    layout = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    layout.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    iconImage = loadImage(
        os.path.join(
            iconsPath(),
            game["icon"]
        )
    )

    icon = ctk.CTkLabel(
        layout,
        text="",
        image=iconImage
    )

    icon.pack(
        side="left",
        padx=(0, 15)
    )

    textFrame = ctk.CTkFrame(
        layout,
        fg_color="transparent"
    )

    textFrame.pack(side="left")

    title = ctk.CTkLabel(
        textFrame,
        text=game["name"],
        font=("Arial", 22, "bold")
    )

    title.pack(anchor="w")

    # =====================================================
    # SCORE
    # =====================================================
    if game["score"] and installed:

        score = ctk.CTkLabel(
            textFrame,
            text=f"Best Score: {lerBestScore(game)}",
            font=("Arial", 14)
        )

        score.pack(anchor="w")

        scoreLabels[
            game["name"]
        ] = score

    # =====================================================
    # BUTTON
    # =====================================================
    if installed:

        button = ctk.CTkButton(
            layout,
            text="Jogar",
            width=120,
            height=45,
            command=lambda: abrirJogo(game)
        )

    else:

        button = ctk.CTkButton(
            layout,
            text="Instalar",
            width=120,
            height=45
        )

        button.configure(
            command=lambda: instalarJogo(
                game,
                button
            )
        )

    button.pack(side="right")

def getScorePath(game):

    # padrão do launcher
    path1 = scoreFile(game)

    # compatibilidade com jogos tipo Tetris (PyInstaller / local exe)
    path2 = os.path.join(
        installedPath(),
        game["folder"],
        "best_score.txt"
    )

    if os.path.exists(path2):
        return path2

    return path1

# =========================================================
# SHOW PAGE
# =========================================================
def showPage(page):

    bibliotecaFrame.pack_forget()

    jogosFrame.pack_forget()

    if page == "biblioteca":

        bibliotecaFrame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    elif page == "jogos":

        jogosFrame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


# =========================================================
# RENDER
# =========================================================
def render():

    scoreLabels.clear()

    clearFrame(
        bibliotecaFrame
    )

    clearFrame(
        jogosFrame
    )

    # =====================================================
    # BUILTIN GAME
    # =====================================================
    criarCardVelha(
        bibliotecaFrame
    )

    # =====================================================
    # INSTALLED / NOT INSTALLED
    # =====================================================
    for game in games:

        # =============================================
        # FILTRO DE SISTEMA
        # =============================================
        if not getGameVersion(game):

            continue

        # =============================================
        # WEB GAME
        # =============================================
        if game.get("internal_browser"):

            criarCardJogo(
                bibliotecaFrame,
                game,
                True
            )

            continue

        # =============================================
        # INSTALLED
        # =============================================
        if jogoInstalado(game):

            criarCardJogo(
                bibliotecaFrame,
                game,
                True
            )

        # =============================================
        # NOT INSTALLED
        # =============================================
        else:

            criarCardJogo(
                jogosFrame,
                game,
                False
            )


# =========================================================
# HEADER
# =========================================================
header = ctk.CTkFrame(
    app,
    height=70,
    corner_radius=0
)

header.pack(fill="x")


# =========================================================
# BUTTONS
# =========================================================
bibliotecaBtn = ctk.CTkButton(
    header,
    text="Biblioteca",
    width=140,
    height=40,
    command=lambda: showPage("biblioteca")
)

bibliotecaBtn.pack(
    side="left",
    padx=15,
    pady=15
)

jogosBtn = ctk.CTkButton(
    header,
    text="Jogos",
    width=140,
    height=40,
    command=lambda: showPage("jogos")
)

jogosBtn.pack(
    side="left",
    pady=15
)


# =========================================================
# CONTENT
# =========================================================
contentFrame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

contentFrame.pack(
    fill="both",
    expand=True
)


# =========================================================
# PAGES
# =========================================================
bibliotecaFrame = ctk.CTkScrollableFrame(
    contentFrame,
    fg_color="transparent"
)

jogosFrame = ctk.CTkScrollableFrame(
    contentFrame,
    fg_color="transparent"
)


# =========================================================
# START
# =========================================================
render()

showPage("biblioteca")

atualizarScores()


# =========================================================
# MAIN LOOP
# =========================================================
app.mainloop()
