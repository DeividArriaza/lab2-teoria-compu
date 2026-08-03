"""
Laboratorio #2, inciso 4 - Teoría de la Computación, CC2019, UVG

Amplía el algoritmo Shunting Yard del inciso 3 para procesar expresiones
regulares y transformarlas a notación polaca (postfix).

Es el mismo algoritmo del inciso 3; lo único que cambia es la tabla de
operadores y dos detalles propios de las expresiones regulares:

  - La concatenación casi nunca se escribe. En "ab" no hay ningún operador
    entre la a y la b, así que hay un paso previo que inserta un "." donde
    haga falta.
  - Los operadores *, + y ? son unarios y van después de su operando, no en
    medio de dos operandos.

También incluye la función describir(), que lee el postfix de derecha a
izquierda e imprime un mensaje por cada símbolo encontrado.
"""

EPSILON = "ε"

# Mayor número = mayor precedencia (se aplica primero)
PRECEDENCIA = {
    "*": 3,   # cerradura de Kleene
    "+": 3,   # una o más repeticiones
    "?": 3,   # opcional
    ".": 2,   # concatenación
    "|": 1,   # unión
}

UNARIOS = "*+?"    # van después de su operando
BINARIOS = ".|"    # van en medio de sus dos operandos

# El enunciado indica que estos nombres son parte de una definición regular,
# así que se comportan como un solo símbolo y no como varias letras sueltas.
SIMBOLOS_COMPUESTOS = ["boolExp", "statement", "emailChar", "urlChar"]

# Mensaje que describe cada operador al leer el postfix de derecha a izquierda
MENSAJES = {
    ".": "Concatenación con",
    "|": "Unión con",
    "*": "Kleene de",
    "+": "Una o más de",
    "?": "Opcional de",
}


def es_simbolo(token):
    """
    True si el token es un símbolo del alfabeto y no un operador ni un
    paréntesis de agrupación.
    """
    if token == "(" or token == ")":
        return False
    if token in PRECEDENCIA:
        return False
    return True


def simbolo_legible(token):
    """Quita la barra invertida de un símbolo escapado: '\\(' -> '('."""
    if len(token) == 2 and token[0] == "\\":
        return token[1]
    return token


def buscar_simbolo_compuesto(expresion, posicion):
    """
    Devuelve el símbolo compuesto que empieza en esa posición de la cadena,
    o una cadena vacía si ahí no empieza ninguno.
    """
    for nombre in SIMBOLOS_COMPUESTOS:
        if expresion.startswith(nombre, posicion):
            return nombre
    return ""


def tokenizar(expresion):
    """
    Parte la expresión regular en una lista de tokens.

        "(a|b)*"      ->  ['(', 'a', '|', 'b', ')', '*']
        "if\\(boolExp" ->  ['i', 'f', '\\(', 'boolExp']
    """
    tokens = []
    i = 0

    while i < len(expresion):
        caracter = expresion[i]

        if caracter == " ":
            i = i + 1
            continue

        if caracter == "\\":
            # La barra invertida escapa al siguiente caracter: ese caracter
            # deja de ser operador y pasa a ser un símbolo del alfabeto.
            if i + 1 >= len(expresion):
                raise ValueError("La expresión termina en una '\\' suelta")
            tokens.append("\\" + expresion[i + 1])
            i = i + 2
            continue

        compuesto = buscar_simbolo_compuesto(expresion, i)
        if compuesto != "":
            tokens.append(compuesto)
            i = i + len(compuesto)
            continue

        tokens.append(caracter)
        i = i + 1

    return tokens


def puede_cerrar(token):
    """True si el token puede ser el final de una subexpresión."""
    if token == ")":
        return True
    if token in UNARIOS:
        return True
    return es_simbolo(token)


def puede_abrir(token):
    """True si el token puede ser el inicio de una subexpresión."""
    if token == "(":
        return True
    return es_simbolo(token)


def agregar_concatenacion(tokens):
    """
    Inserta el operador "." donde la concatenación estaba implícita.

    Va entre dos tokens cuando el de la izquierda cierra una subexpresión y
    el de la derecha abre otra.

        ['a', 'b']            ->  ['a', '.', 'b']
        ['a', '*', '(', 'b']  ->  ['a', '*', '.', '(', 'b']
    """
    resultado = []
    i = 0

    while i < len(tokens):
        if i > 0 and puede_cerrar(tokens[i - 1]) and puede_abrir(tokens[i]):
            resultado.append(".")
        resultado.append(tokens[i])
        i = i + 1

    return resultado


def a_postfix(expresion):
    """
    Convierte la expresión regular a postfix y devuelve la lista de tokens.

    Es el mismo recorrido del inciso 3, con un caso más: los operadores
    unarios postfijos.
    """
    tokens = agregar_concatenacion(tokenizar(expresion))

    salida = []   # aquí se va armando el resultado
    pila = []     # operadores que todavía están en espera

    for token in tokens:

        if token in UNARIOS:
            # Como van después de su operando, cuando aparecen su operando ya
            # está completo en la salida. Salen de una vez, sin pasar por la
            # pila y sin esperar a nadie.
            salida.append(token)

        elif token in BINARIOS:
            # Sale de la pila todo operador que ya tenga su operando derecho
            # completo. La concatenación y la unión son asociativas por la
            # izquierda, así que también sale el que empata en precedencia.
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
            # Es un símbolo del alfabeto: sale directo, nunca espera.
            salida.append(token)

    # Se terminó la expresión, así que se vacía la pila de arriba hacia abajo.
    while len(pila) > 0:
        operador = pila.pop()
        if operador == "(":
            raise ValueError("Paréntesis desbalanceados: sobra un '('")
        salida.append(operador)

    return salida


def postfix_a_texto(postfix):
    """
    Une los tokens del postfix en una sola cadena.

    Si todos los símbolos son de un caracter se pegan sin separador, igual
    que en el enunciado. Si hay símbolos de varios caracteres se separan con
    espacios, porque si no la salida sería ilegible.
    """
    separador = ""

    for token in postfix:
        if len(token) > 1:
            separador = " "

    return separador.join(postfix)


def describir(postfix):
    """
    Lee el postfix de derecha a izquierda e imprime un mensaje por cada
    símbolo, describiendo la expresión regular.

    El último token impreso (el que está más a la izquierda) va sin el "de",
    porque ya no hay nada más que describir después de él.
    """
    i = len(postfix) - 1
    numero = 1

    while i >= 0:
        token = postfix[i]

        if token in MENSAJES:
            print("  ", numero, ". ", MENSAJES[token], sep="")
        elif i == 0:
            print("  ", numero, ". ", simbolo_legible(token), sep="")
        else:
            print("  ", numero, ". ", simbolo_legible(token), " de", sep="")

        i = i - 1
        numero = numero + 1


def procesar(expresion):
    """Convierte la expresión, la imprime en postfix y la describe."""
    postfix = a_postfix(expresion)

    print("Expresion regular:", expresion)
    print("En postfix:       ", postfix_a_texto(postfix))
    print("Leyendo de derecha a izquierda:")
    describir(postfix)


if __name__ == "__main__":

    ejemplos = [
        # Ejemplo del enunciado del inciso 4
        "(a|b)*.a.b.b",
        # Expresiones del inciso 1
        "((ε|a)|b*)*",
        "0?(1?)?0*",
        "if\\(boolExp\\){statement+}(\\\\n(else{statement+}))?",
        "emailChar+@urlChar+\\.(com|net|org)(\\.(gt|cr|co))?",
    ]

    for ejemplo in ejemplos:
        procesar(ejemplo)
        print()

    print("Escriba su propia expresion regular (o 'salir' para terminar).")
    print("Operadores: | union   . concatenacion   * + ?   y parentesis.")
    print("Use \\ antes de un simbolo para que se tome como parte del alfabeto.")

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
            procesar(expresion)
        except ValueError as error:
            print("Error:", error)
