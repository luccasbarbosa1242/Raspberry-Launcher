from CORE.database.migrations import (
    initialize_database
)

from UI.window import app
from UI.pages import render
from UI.pages import showPage

from CORE.score import atualizarScores

initialize_database()

render()

showPage("home")

atualizarScores()

app.mainloop()