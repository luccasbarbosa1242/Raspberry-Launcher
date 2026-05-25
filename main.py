from UI.window import app
from UI.pages import render
from UI.pages import showPage

from CORE.score import atualizarScores


render()

showPage("biblioteca")

atualizarScores()

app.mainloop()