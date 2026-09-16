"""
Trabalho de Algebra Linear - Transformacoes Geometricas 2D via Matrizes
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
# 3. Exibicao da figura
# ---------------------------------------------------------------------------
def mostrar_figura(pontos, titulo="Figura"):
    """Desenha a figura 2D a partir de uma matriz de pontos (2xN)."""
    xs = list(pontos[0]) + [pontos[0][0]]  # fecha o poligono
    ys = list(pontos[1]) + [pontos[1][0]]

    fig, ax = plt.subplots()
    ax.plot(xs, ys, marker="o", linestyle="-")

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_title(titulo)

    plt.show()


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
          'origem' -> reflexao na origem
    """
    if eixo == "x":
        return np.array([[1, 0], [0, -1]])
    elif eixo == "y":
        return np.array([[-1, 0], [0, 1]])
    elif eixo == "origem":
        return np.array([[-1, 0], [0, -1]])
    else:
        raise ValueError("Eixo de reflexao invalido. Use 'x', 'y' ou 'origem'.")


def aplicar_transformacao(matriz_transf, pontos):
    """Aplica uma matriz de transformacao a matriz de pontos (2xN)."""
    return matriz_transf @ pontos


def pedir_matriz_rotacao_interativo():
    angulo = float(input("Angulo de rotacao (graus): "))
    return matriz_rotacao(angulo)


def pedir_matriz_escala_interativo():
    sx = float(input("Fator de escala Sx: "))
    sy = float(input("Fator de escala Sy: "))
    return matriz_escala(sx, sy)


def pedir_matriz_reflexao_interativo():
    while True:
        eixo = input("Refletir em 'x', 'y' ou 'origem'? ").strip().lower()
        if eixo in ("x", "y", "origem"):
            return matriz_reflexao(eixo)
        print("Opcao invalida.")


def menu_transformacao_unica(pontos):
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

        novos_pontos = aplicar_transformacao(t, pontos)
        mostrar_figura(novos_pontos, "Apos transformacao")
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
    de forma que "C @ pontos" produz o mesmo resultado final que
    aplicar T1, depois T2, depois T3 separadamente.
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
            transformacoes.append(pedir_matriz_rotacao_interativo())
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
    composta = np.identity(2)
    for t in transformacoes:
        composta = t @ composta

    return composta


def menu_transformacao_multipla(pontos):
    """Monta a matriz composta e aplica UMA UNICA VEZ sobre os pontos originais."""
    matriz_composta = montar_transformacao_composta()
    print("\nMatriz de transformacao composta:")
    print(matriz_composta)

    novos_pontos = aplicar_transformacao(matriz_composta, pontos)
    mostrar_figura(novos_pontos, "Apos transformacoes compostas")
    return novos_pontos, matriz_composta


# ---------------------------------------------------------------------------
# 6. Reversao de transformacao (matriz inversa)
# ---------------------------------------------------------------------------
def reverter_transformacao(pontos_transformados, matriz_transformacao):
    """
    Recebe a matriz de pontos ja transformada e a matriz que causou essa
    transformacao, calcula a matriz inversa e a aplica para recuperar
    as coordenadas originais.

    Trata o caso de matriz singular (determinante = 0), que nao possui
    inversa e, portanto, nao pode ser revertida.
    """
    determinante = np.linalg.det(matriz_transformacao)

    if np.isclose(determinante, 0):
        print("Erro: a matriz de transformacao e singular (determinante = 0).")
        print("Nao e possivel reverter esta transformacao (nao existe inversa).")
        return None

    matriz_inversa = np.linalg.inv(matriz_transformacao)
    pontos_originais = matriz_inversa @ pontos_transformados
    return pontos_originais


def menu_reversao(pontos_atuais, ultima_transformacao):
    if ultima_transformacao is None:
        print("Nenhuma transformacao foi aplicada ainda, nada para reverter.")
        return pontos_atuais

    pontos_revertidos = reverter_transformacao(pontos_atuais, ultima_transformacao)
    if pontos_revertidos is None:
        return pontos_atuais

    mostrar_figura(pontos_revertidos, "Figura revertida (original)")
    return pontos_revertidos


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    quantidade = pedir_quantidade_pontos()
    pontos_originais = pedir_pontos(quantidade)
    pontos_atuais = pontos_originais.copy()
    ultima_transformacao = None

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Mostrar figura atual")
        print("2 - Aplicar transformacao unica (rotacao/escala/reflexao)")
        print("3 - Aplicar transformacoes multiplas (composicao)")
        print("4 - Reverter ultima transformacao (matriz inversa)")
        print("5 - Reiniciar com a figura original")
        print("0 - Sair")
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            mostrar_figura(pontos_atuais, "Figura atual")
        elif opcao == "2":
            pontos_atuais, ultima_transformacao = menu_transformacao_unica(pontos_atuais)
        elif opcao == "3":
            pontos_atuais, ultima_transformacao = menu_transformacao_multipla(pontos_atuais)
        elif opcao == "4":
            pontos_atuais = menu_reversao(pontos_atuais, ultima_transformacao)
            ultima_transformacao = None
        elif opcao == "5":
            pontos_atuais = pontos_originais.copy()
            ultima_transformacao = None
            print("Figura reiniciada para o estado original.")
        elif opcao == "0":
            print("Encerrando.")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
