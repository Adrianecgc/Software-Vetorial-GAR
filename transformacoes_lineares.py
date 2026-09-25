"""
Trabalho de Algebra Linear - Transformacoes Geometricas 2D via Matrizes
(versao corrigida com ponto de ancoragem)
"""

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# 1. Quantidade de pontos
# ---------------------------------------------------------------------------
def pedir_quantidade_pontos():
    """Pergunta ao usuario quantos vertices a figura tera (minimo 3)."""
    while True:
        entrada = input("Quantos pontos (vertices) a figura tera? (minimo 3): ")
        try:
            quantidade = int(entrada)
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")
            continue

        if quantidade < 3:
            print("A figura precisa de pelo menos 3 pontos (triangulo).")
            continue

        return quantidade


# ---------------------------------------------------------------------------
# 2. Entrada dos pontos
# ---------------------------------------------------------------------------
def pedir_pontos(quantidade):
    """
    Le as coordenadas X e Y de cada ponto e monta uma matriz 2xN,
    onde cada COLUNA representa um ponto (vetor coluna [x, y]^T).

    Essa organizacao (pontos como colunas) e a usada em algebra linear
    para transformacoes lineares: T @ pontos aplica a matriz T a cada
    ponto simultaneamente, sem precisar de um loop manual.
    """
    xs = []
    ys = []
    for i in range(quantidade):
        while True:
            try:
                x = float(input(f"Ponto {i + 1} - coordenada X: "))
                y = float(input(f"Ponto {i + 1} - coordenada Y: "))
                break
            except ValueError:
                print("Coordenada invalida. Digite um numero (ex: 2 ou -1.5).")
        xs.append(x)
        ys.append(y)

    # matriz 2xN: linha 0 = todos os X, linha 1 = todos os Y
    pontos = np.array([xs, ys])
    return pontos


# ---------------------------------------------------------------------------
# 2b. Ponto de ancoragem (pivo das transformacoes)
# ---------------------------------------------------------------------------
def pedir_ponto_ancoragem():
    """
    Pede o ponto de ancoragem C, que serve como pivo (centro) das
    transformacoes. Toda transformacao linear pura (rotacao, escala,
    reflexao) e definida em relacao a origem (0,0); se a figura nao
    estiver na origem, e preciso:

        1) trazer a figura pra origem:      P - C
        2) aplicar a transformacao:         T @ (P - C)
        3) devolver a figura pro lugar:     T @ (P - C) + C

    Se o usuario nao quiser um pivo especifico, pode digitar 0 e 0,
    o que equivale a transformar em relacao a propria origem.
    """
    print("\nPonto de ancoragem (pivo das transformacoes).")
    print("Se quiser usar a origem (0,0), digite 0 para X e 0 para Y.")
    while True:
        try:
            cx = float(input("Ancoragem - coordenada X: "))
            cy = float(input("Ancoragem - coordenada Y: "))
            break
        except ValueError:
            print("Coordenada invalida. Digite um numero (ex: 4 ou -1.5).")

    # vetor coluna 2x1, para poder somar/subtrair de uma matriz 2xN via broadcast
    return np.array([[cx], [cy]])


# ---------------------------------------------------------------------------
# 3. Exibicao da figura
# ---------------------------------------------------------------------------
def formatar_pontos(pontos, rotulos=None):
    """
    Devolve uma string legivel com as coordenadas de cada ponto,
    arredondando ruido de ponto flutuante (ex: 1e-16 vira 0).
    """
    pontos_limpos = np.round(pontos, decimals=6)
    pontos_limpos[np.isclose(pontos_limpos, 0)] = 0  # tira o -0.0 tambem

    n = pontos.shape[1]
    if rotulos is None:
        rotulos = [f"P{i+1}" for i in range(n)]

    linhas = []
    for i in range(n):
        x, y = pontos_limpos[0][i], pontos_limpos[1][i]
        linhas.append(f"  {rotulos[i]}: ({x:g}, {y:g})")
    return "\n".join(linhas)


def mostrar_figura(pontos, titulo="Figura", ancoragem=None, arquivo_saida="figura_atual.png"):
    """
    Desenha a figura 2D a partir de uma matriz de pontos (2xN).

    Tenta abrir a figura numa janela (plt.show). Alem disso, SEMPRE salva
    a figura em um arquivo PNG (arquivo_saida) -- isso garante que voce
    consiga ver o resultado mesmo se o ambiente onde o script esta
    rodando (ex: terminal integrado de algumas IDEs, como o Antigravity)
    nao tiver suporte a abrir uma janela grafica.
    """
    xs = list(pontos[0]) + [pontos[0][0]]  # fecha o poligono
    ys = list(pontos[1]) + [pontos[1][0]]

    fig, ax = plt.subplots()
    ax.plot(xs, ys, marker="o", linestyle="-")

    if ancoragem is not None:
        ax.plot(ancoragem[0][0], ancoragem[1][0], marker="x", markersize=10,
                color="red", label="Ancoragem")
        ax.legend()

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_title(titulo)

    fig.savefig(arquivo_saida)
    print(f"(figura tambem salva em: {arquivo_saida})")

    try:
        plt.show()
    except Exception:
        pass
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Matrizes de transformacao (rotacao, escala, reflexao)
# ---------------------------------------------------------------------------
def matriz_rotacao(angulo_graus):
    """Monta a matriz de rotacao 2x2 para um angulo em graus (sentido anti-horario)."""
    theta = np.radians(angulo_graus)
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)],
    ])


def matriz_escala(sx, sy):
    """Monta a matriz de escala 2x2 com fatores Sx e Sy."""
    return np.array([
        [sx, 0],
        [0, sy],
    ])


def matriz_reflexao(eixo):
    """
    Monta a matriz de reflexao 2x2.
    eixo: 'x' -> reflexao no eixo X
          'y' -> reflexao no eixo Y
    """
    if eixo == "x":
        return np.array([[1, 0], [0, -1]])
    elif eixo == "y":
        return np.array([[-1, 0], [0, 1]])
    else:
        raise ValueError("Eixo de reflexao invalido. Use 'x' ou 'y'.")


def aplicar_transformacao(matriz_transf, pontos, ancoragem):
    """
    Aplica uma matriz de transformacao a matriz de pontos (2xN),
    usando 'ancoragem' (vetor coluna 2x1) como pivo:

        P' = T @ (P - C) + C

    O numpy faz o broadcast de (2x1) contra (2xN) automaticamente,
    entao 'pontos - ancoragem' subtrai o pivo de TODAS as colunas
    (todos os pontos) de uma vez.
    """
    pontos_centralizados = pontos - ancoragem
    pontos_transformados = matriz_transf @ pontos_centralizados
    return pontos_transformados + ancoragem


def pedir_matriz_rotacao_interativo():
    """Pergunta o angulo de rotacao e devolve a matriz 2x2 correspondente."""
    angulo = float(input("Angulo de rotacao (graus): "))
    return matriz_rotacao(angulo)


def pedir_matriz_escala_interativo():
    """Pergunta os fatores de escala Sx e Sy e devolve a matriz 2x2 correspondente."""
    sx = float(input("Fator de escala Sx: "))
    sy = float(input("Fator de escala Sy: "))
    return matriz_escala(sx, sy)


def pedir_matriz_reflexao_interativo():
    """Pergunta o eixo/reta de reflexao e devolve a matriz 2x2 correspondente."""
    while True:
        eixo = input("Refletir em 'x' ou 'y'? ").strip().lower()
        if eixo in ("x", "y"):
            return matriz_reflexao(eixo)
        print("Opcao invalida.")


def menu_transformacao_unica(pontos, ancoragem):
    """Menu interativo para aplicar UMA transformacao de cada vez."""
    while True:
        print("\n--- Transformacao Unica ---")
        print("1 - Rotacao")
        print("2 - Escala")
        print("3 - Reflexao")
        print("0 - Voltar")
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            t = pedir_matriz_rotacao_interativo()
        elif opcao == "2":
            t = pedir_matriz_escala_interativo()
        elif opcao == "3":
            t = pedir_matriz_reflexao_interativo()
        elif opcao == "0":
            return pontos, None
        else:
            print("Opcao invalida.")
            continue

        novos_pontos = aplicar_transformacao(t, pontos, ancoragem)
        print("\nPontos apos a transformacao:")
        print(formatar_pontos(novos_pontos))
        mostrar_figura(novos_pontos, "Apos transformacao", ancoragem)
        return novos_pontos, t


# ---------------------------------------------------------------------------
# 5. Transformacoes multiplas (composicao de matrizes)
# ---------------------------------------------------------------------------
def montar_transformacao_composta():
    """
    Enfileira varias transformacoes escolhidas pelo usuario e retorna
    a MATRIZ COMPOSTA (produto das matrizes na ordem em que devem ser
    aplicadas), em vez de aplica-las uma a uma sobre a figura.

    Se as transformacoes forem T1, depois T2, depois T3, a matriz
    composta e:  C = T3 @ T2 @ T1
    de forma que "C @ (P - ancoragem) + ancoragem" produz o mesmo
    resultado final que aplicar T1, depois T2, depois T3 separadamente
    (cada uma em torno do mesmo pivo).
    """
    transformacoes = []

    while True:
        print("\n--- Fila de Transformacoes ---")
        print("1 - Adicionar Rotacao")
        print("2 - Adicionar Escala")
        print("3 - Adicionar Reflexao")
        print("0 - Finalizar fila e aplicar")
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            transformacoes.append(pedir_matriz_rotacao_interativo())  # adiciona cada transformacao a lista
        elif opcao == "2":
            transformacoes.append(pedir_matriz_escala_interativo())
        elif opcao == "3":
            transformacoes.append(pedir_matriz_reflexao_interativo())
        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")

    if not transformacoes:
        return np.identity(2)

    # Multiplica as matrizes na ordem inversa da aplicacao,
    # pois a ultima transformacao adicionada deve ficar mais a esquerda.
    composta = np.identity(2)  # matriz identidade 2x2: "elemento neutro" da multiplicacao
    for t in transformacoes:   # percorre a lista de transformacoes, na ordem em que foram adicionadas
        composta = t @ composta  # empilha cada nova transformacao a esquerda das anteriores

    return composta


def menu_transformacao_multipla(pontos, ancoragem):
    """Monta a matriz composta e aplica UMA UNICA VEZ sobre os pontos originais."""
    matriz_composta = montar_transformacao_composta()
    matriz_composta_limpa = np.round(matriz_composta, decimals=6)
    matriz_composta_limpa[np.isclose(matriz_composta_limpa, 0)] = 0
    print("\nMatriz de transformacao composta:")
    print(matriz_composta_limpa)

    novos_pontos = aplicar_transformacao(matriz_composta, pontos, ancoragem)
    print("\nPontos apos as transformacoes compostas:")
    print(formatar_pontos(novos_pontos))
    mostrar_figura(novos_pontos, "Apos transformacoes compostas", ancoragem)
    return novos_pontos, matriz_composta


# ---------------------------------------------------------------------------
# 6. Reversao de transformacao (matriz inversa)
# ---------------------------------------------------------------------------
def reverter_transformacao(pontos_transformados, matriz_transformacao, ancoragem):
    """
    Recebe a matriz de pontos ja transformada e a matriz que causou essa
    transformacao, calcula a matriz inversa e a aplica (em torno do
    mesmo pivo) para recuperar as coordenadas originais:

        P = Tinv @ (P' - C) + C

    Trata o caso de matriz singular (determinante = 0), que nao possui
    inversa e, portanto, nao pode ser revertida.
    """
    determinante = np.linalg.det(matriz_transformacao)

    if np.isclose(determinante, 0):
        print("Erro: a matriz de transformacao e singular (determinante = 0).")
        print("Nao e possivel reverter esta transformacao (nao existe inversa).")
        return None

    matriz_inversa = np.linalg.inv(matriz_transformacao)
    pontos_centralizados = pontos_transformados - ancoragem
    pontos_originais = matriz_inversa @ pontos_centralizados + ancoragem
    return pontos_originais


def menu_reversao(pontos_atuais, ultima_transformacao, ancoragem):
    if ultima_transformacao is None:
        print("Nenhuma transformacao foi aplicada ainda, nada para reverter.")
        return pontos_atuais

    pontos_revertidos = reverter_transformacao(pontos_atuais, ultima_transformacao, ancoragem)
    if pontos_revertidos is None:
        return pontos_atuais

    print("\nPontos revertidos:")
    print(formatar_pontos(pontos_revertidos))
    mostrar_figura(pontos_revertidos, "Figura revertida (original)", ancoragem)
    return pontos_revertidos


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    quantidade = pedir_quantidade_pontos()
    pontos_originais = pedir_pontos(quantidade)
    ancoragem = pedir_ponto_ancoragem()

    pontos_atuais = pontos_originais.copy()
    ultima_transformacao = None

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Mostrar figura atual")
        print("2 - Aplicar transformacao unica (rotacao/escala/reflexao)")
        print("3 - Aplicar transformacoes multiplas (composicao)")
        print("4 - Reverter ultima transformacao (matriz inversa)")
        print("5 - Reiniciar com a figura original")
        print("6 - Redefinir ponto de ancoragem")
        print("0 - Sair")
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            mostrar_figura(pontos_atuais, "Figura atual", ancoragem)
        elif opcao == "2":
            pontos_atuais, ultima_transformacao = menu_transformacao_unica(pontos_atuais, ancoragem)
        elif opcao == "3":
            pontos_atuais, ultima_transformacao = menu_transformacao_multipla(pontos_atuais, ancoragem)
        elif opcao == "4":
            pontos_atuais = menu_reversao(pontos_atuais, ultima_transformacao, ancoragem)
            ultima_transformacao = None
        elif opcao == "5":
            pontos_atuais = pontos_originais.copy()
            ultima_transformacao = None
            print("Figura reiniciada para o estado original.")
        elif opcao == "6":
            ancoragem = pedir_ponto_ancoragem()
        elif opcao == "0":
            print("Encerrando.")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
