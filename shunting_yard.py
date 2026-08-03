"""
Laboratorio #2, inciso 3 - Teoría de la Computación, CC2019, UVG

Algoritmo Shunting Yard: convierte una expresión aritmética escrita en
notación infija a notación postfija (polaca inversa).

Operadores soportados: + - * /
"""

DIGITOS = "0123456789"
OPERADORES = "+-*/"

# Mayor número = mayor precedencia (se ejecuta primero)
PRECEDENCIA = {"+": 1, "-": 1, "*": 2, "/": 2}


def tokenizar(expresion):
    """
    Parte la cadena en una lista de tokens.

    Los dígitos seguidos se juntan en un mismo número y los espacios se
    ignoran.

        "12+3*(4-1)"  ->  ['12', '+', '3', '*', '(', '4', '-', '1', ')']
    """
    tokens = []
    numero = ""

    for caracter in expresion:

        if caracter in DIGITOS or caracter == ".":
            # El número puede tener varios caracteres, así que se va
            # acumulando hasta que aparezca algo que no sea un dígito.
            numero = numero + caracter

        else:
            # Se acabó el número que se venía acumulando: hay que guardarlo
            # antes de procesar el caracter actual.
            if numero != "":
                tokens.append(numero)
                numero = ""

            if caracter in OPERADORES:
                tokens.append(caracter)
            elif caracter == "(":
                tokens.append("(")
            elif caracter == ")":
                tokens.append(")")
            elif caracter == " ":
                pass
            else:
                raise ValueError("Símbolo no reconocido: " + caracter)

    # Si la expresión termina en un número, ese último número todavía está
    # acumulado y no se ha guardado.
    if numero != "":
        tokens.append(numero)

    return tokens


def a_postfix(expresion):
    """Convierte la expresión infija a postfix y la devuelve como cadena."""
    tokens = tokenizar(expresion)

    salida = []   # aquí se va armando el resultado
    pila = []     # operadores que todavía están en espera

    for token in tokens:

        if token in PRECEDENCIA:
            # Sale de la pila todo operador que ya tenga su operando derecho
            # completo. Como los cuatro operadores son asociativos por la
            # izquierda, también sale el que empata en precedencia.
            while len(pila) > 0 and pila[-1] != "(":
                if PRECEDENCIA[pila[-1]] >= PRECEDENCIA[token]:
                    salida.append(pila.pop())
                else:
                    break
            pila.append(token)

        elif token == "(":
            # El paréntesis que abre es un muro: nada se saca más allá de él.
            pila.append(token)

        elif token == ")":
            while len(pila) > 0 and pila[-1] != "(":
                salida.append(pila.pop())
            if len(pila) == 0:
                raise ValueError("Paréntesis desbalanceados: sobra un ')'")
            pila.pop()   # descarta el "(" que hacía de muro

        else:
            # Es un operando: sale directo, nunca espera.
            salida.append(token)

    # Se terminó la expresión, así que ya nadie puede robar operandos.
    # Se vacía la pila de arriba hacia abajo.
    while len(pila) > 0:
        operador = pila.pop()
        if operador == "(":
            raise ValueError("Paréntesis desbalanceados: sobra un '('")
        salida.append(operador)

    return " ".join(salida)


if __name__ == "__main__":

    ejemplos = [
        "3 + 4",
        "3 + 4 * 2",
        "3 * 4 + 2",
        "(3 + 4) * 2",
        "8 - 4 - 2",
        "8 / 4 / 2",
        "3 + 4 * 2 / (1 - 5)",
        "((2 + 3) * (4 - 1)) / 5",
        "12 + 345 * 6",
        "2.5 * 4 - 1.5",
    ]

    print("Shunting Yard - Laboratorio #2, inciso 3")
    print("Convierte expresiones aritmeticas de infijo a postfix.")
    print()
    print("Ejemplos:")

    for ejemplo in ejemplos:
        print("  ", ejemplo.ljust(28), "-> ", a_postfix(ejemplo))

    print()
    print("Escriba su propia expresion (o 'salir' para terminar).")
    print("Operadores: + - * /   Tambien puede usar parentesis.")

    while True:

        try:
            expresion = input("\n>>> ")
        except EOFError:
            # Ocurre si se presiona Ctrl+D o si la entrada viene de un archivo.
            print()
            break

        if expresion == "salir":
            break

        if expresion == "":
            continue

        try:
            print("Postfix:", a_postfix(expresion))
        except ValueError as error:
            print("Error:", error)
