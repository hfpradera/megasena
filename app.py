from flask import Flask, render_template, request

from engine.gerador import carregar_historico, estrategia_por_orcamento, gerar_jogos

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    historico = carregar_historico()
    jogos = []
    estrategia = None
    orcamento = 50.0

    if request.method == "POST":
        orcamento = float(request.form.get("orcamento", 50))
        estrategia = estrategia_por_orcamento(orcamento)
        jogos = gerar_jogos(
            historico=historico,
            qtd=int(estrategia["qtd"]),
            dezenas=int(estrategia["dezenas"]),
            percentual=float(estrategia["percentual"]),
            perc_acerto=float(estrategia["perc_acerto"]),
        )

    return render_template(
        "index.html",
        historico_total=len(historico),
        jogos=jogos,
        estrategia=estrategia,
        orcamento=orcamento,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)
