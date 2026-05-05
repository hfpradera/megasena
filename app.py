from flask import Flask, render_template

from engine.gerador import gerar_varios_jogos
from engine.historico import ler_historico, ultimos_concursos

app = Flask(__name__)


@app.route("/")
def home():
    historico = ler_historico()
    return render_template(
        "index.html",
        jogos=gerar_varios_jogos(quantidade=5),
        ultimos=ultimos_concursos(historico, limite=10),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)
