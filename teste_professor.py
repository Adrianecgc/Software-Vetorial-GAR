"""
Script de teste com o exemplo do professor
Valida se as transformacoes estao sendo aplicadas corretamente
"""

import numpy as np
import sys

# Importar as funcoes do codigo principal
from transformacoes_lineares import (
    matriz_escala,
    matriz_reflexao,
    matriz_rotacao,
    aplicar_transformacao,
)


def teste_professor():
    """Executa o teste com os valores do professor."""

    print("=" * 70)
    print("TESTE COM VALORES DO PROFESSOR")
    print("=" * 70)

    # Definir os pontos
    pontos = np.array([
        [4, 6, 4, 2],  # coordenadas X
        [2, 5, 4, 5],  # coordenadas Y
    ])

    # Labels dos pontos
    labels = ['A', 'B', 'C', 'D']

    # Centro de transformacao
    centro = np.array([[4], [3]])

    # Resultados esperados
    esperados = {
        'A': np.array([[2], [3]]),
        'B': np.array([[8], [9]]),
        'C': np.array([[6], [3]]),
        'D': np.array([[8], [-3]]),
    }

    print("\n--- DADOS INICIAIS ---")
    print(f"Centro (C): ({centro[0, 0]:.1f}, {centro[1, 0]:.1f})")
    print("\nPontos originais:")
    for i, label in enumerate(labels):
        print(f"  {label}: ({pontos[0, i]:.1f}, {pontos[1, i]:.1f})")

    # Criar as matrizes de transformacao
    print("\n--- TRANSFORMACOES ---")
    escala = matriz_escala(2, 3)
    print(f"Escala (Sx=2, Sy=3):\n{escala}\n")

    reflexao = matriz_reflexao('y')
    print(f"Reflexao (eixo Y):\n{reflexao}\n")

    rotacao = matriz_rotacao(90)
    print(f"Rotacao (90 graus):\n{rotacao}\n")

    # Compor as matrizes: Escala @ Reflexao @ Rotacao
    # Ordem de aplicacao: Rotacao -> Reflexao -> Escala (lida de DIREITA para ESQUERDA)
    # Ordem de multiplicacao de matrizes: Escala @ Reflexao @ Rotacao
    composta = escala @ reflexao @ rotacao
    print("Matriz composta (Escala @ Reflexao @ Rotacao):")
    print(f"(aplicacao: Rotacao -> Reflexao -> Escala)")
    print(composta)
    print()

    # Aplicar a transformacao composta a cada ponto
    print("\n--- APLICANDO TRANSFORMACOES ---")
    print("Formula: P_final = T @ (P - C) + C\n")

    pontos_transformados = aplicar_transformacao(composta, pontos, centro)

    # Comparar com os resultados esperados
    print("\n--- RESULTADOS ---")
    print(f"{'Ponto':<8} {'Esperado':<20} {'Obtido':<20} {'Correto?':<10}")
    print("-" * 60)

    todos_corretos = True
    tolerancia = 1e-10

    for i, label in enumerate(labels):
        ponto_obtido = pontos_transformados[:, i:i+1]
        ponto_esperado = esperados[label]

        # Verificar se o resultado esta correto
        diferenca = np.abs(ponto_obtido - ponto_esperado)
        correto = np.all(diferenca < tolerancia)

        if not correto:
            todos_corretos = False

        status = "✓ SIM" if correto else "✗ NÃO"
        esperado_str = f"({ponto_esperado[0, 0]:.1f}, {ponto_esperado[1, 0]:.1f})"
        obtido_str = f"({ponto_obtido[0, 0]:.1f}, {ponto_obtido[1, 0]:.1f})"

        print(f"{label:<8} {esperado_str:<20} {obtido_str:<20} {status:<10}")

    print("-" * 60)

    # Resultado final
    print("\n" + "=" * 70)
    if todos_corretos:
        print("✓ TESTE PASSOU! Todos os resultados estão corretos!")
        print("=" * 70)
        return True
    else:
        print("✗ TESTE FALHOU! Alguns resultados não coincidem.")
        print("=" * 70)

        # Mostrar detalhes das diferenças
        print("\n--- ANALISE DAS DIFERENCAS ---")
        for i, label in enumerate(labels):
            ponto_obtido = pontos_transformados[:, i:i+1]
            ponto_esperado = esperados[label]
            diferenca = ponto_obtido - ponto_esperado

            if not np.allclose(ponto_obtido, ponto_esperado, atol=tolerancia):
                print(f"{label}: diferenca = ({diferenca[0, 0]:.4f}, {diferenca[1, 0]:.4f})")

        return False


if __name__ == "__main__":
    sucesso = teste_professor()
    sys.exit(0 if sucesso else 1)
