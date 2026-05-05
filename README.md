# Simulador Mega-Sena (Flask)

Site em Flask para simulação de combinações da Mega-Sena com filtros básicos e leitura de histórico.

> Este projeto **não** faz previsão de resultados e **não** promete ganhos.

## Estrutura

```txt
.
├── app.py
├── engine/
│   ├── filtros.py
│   ├── gerador.py
│   └── historico.py
├── data/
│   └── resultadosMega.txt
├── templates/
│   └── index.html
├── Dockerfile
└── docker-compose.yml
```

## Formato do histórico

Arquivo `data/resultadosMega.txt`:

```txt
# concurso dez1 dez2 dez3 dez4 dez5 dez6
2801 03 07 15 22 43 59
2802 06 12 17 29 46 58
```

Separador pode ser espaço, vírgula ou ponto e vírgula.

## Rodando com Docker

### 1) Build

```bash
docker compose build
```

### 2) Subir aplicação

```bash
docker compose up -d
```

### 3) Acessar

Abra: `http://localhost:3003`

### 4) Logs

```bash
docker compose logs -f
```

### 5) Parar

```bash
docker compose down
```

## Execução local (opcional)

```bash
pip install -r requirements.txt
python app.py
```

Aplicação em `http://localhost:3003`.
