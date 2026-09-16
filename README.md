# Software Vetorial GAR

Trabalho de álgebra linear: figuras geométricas 2D e transformações lineares
(rotação, escala, reflexão, composição de matrizes e reversão via matriz inversa).

Duas versões, mesma lógica matemática:

- **`transformacoes_lineares.py`** — versão em terminal (Python)
- **`web/index.html`** — versão em navegador (HTML/CSS/JS puro, sem instalação)

## Versão web (mais fácil)

Não precisa instalar nada. Basta baixar/clonar o repositório e abrir
`web/index.html` com duplo clique em qualquer navegador.

## Versão Python (terminal)

Requer Python 3 instalado.

```bash
git clone https://github.com/Adrianecgc/Software-Vetorial-GAR.git
cd Software-Vetorial-GAR
pip install -r requirements.txt
python transformacoes_lineares.py
```

## Funcionalidades

1. Pedir a quantidade de pontos (vértices) da figura, com validação de entrada
2. Inserir as coordenadas de cada ponto
3. Mostrar a figura no plano cartesiano
4. Aplicar transformações: rotação, escala e reflexão
5. Aplicar transformações múltiplas (composição de matrizes)
6. Reverter a última transformação aplicada (via matriz inversa)
