# lab2-teoria-compu

Laboratorio #2 — Teoría de la Computación, CC2019 · UVG · Semestre 2, 2026

| Inciso | Archivo | Qué hace |
|---|---|---|
| 3 | `shunting_yard.py` | Shunting Yard para expresiones aritméticas (`+ - * /`) |
| 4 | `shunting_yard_regex.py` | Shunting Yard para expresiones regulares, con descripción del postfix |

Cada archivo es autónomo y se ejecuta por separado. Los incisos también están
en sus propias ramas: `ejercicio-3` y `ejercicio-4`.

---

## Inciso 3 — Shunting Yard para expresiones aritméticas

`shunting_yard.py` convierte expresiones aritméticas de notación infija a
notación postfija (polaca inversa) con los cuatro operadores básicos `+ - * /`.

### Uso

```bash
python3 shunting_yard.py
```

El programa imprime primero una lista de ejemplos y luego queda esperando que
se escriba cualquier expresión:

```
Ejemplos:
   3 + 4                        ->  3 4 +
   3 + 4 * 2                    ->  3 4 2 * +
   3 * 4 + 2                    ->  3 4 * 2 +
   (3 + 4) * 2                  ->  3 4 + 2 *
   8 - 4 - 2                    ->  8 4 - 2 -
   8 / 4 / 2                    ->  8 4 / 2 /
   3 + 4 * 2 / (1 - 5)          ->  3 4 2 * 1 5 - / +
   ((2 + 3) * (4 - 1)) / 5      ->  2 3 + 4 1 - * 5 /
   12 + 345 * 6                 ->  12 345 6 * +
   2.5 * 4 - 1.5                ->  2.5 4 * 1.5 -

Escriba su propia expresion (o 'salir' para terminar).
Operadores: + - * /   Tambien puede usar parentesis.

>>> 7 * (2 + 3) - 1
Postfix: 7 2 3 + * 1 -

>>> 2*(3+(4-1)*5)/6
Postfix: 2 3 4 1 - 5 * + * 6 /

>>> (3 + 4))
Error: Paréntesis desbalanceados: sobra un ')'

>>> 3 $ 4
Error: Símbolo no reconocido: $

>>> salir
```

También se puede usar como módulo:

```python
from shunting_yard import a_postfix

print(a_postfix("7 * (2 + 3) - 1"))    # 7 2 3 + * 1 -
```

### Cómo funciona

El algoritmo recorre los tokens de izquierda a derecha usando una lista de
salida y una pila de operadores en espera:

| Token | Acción |
|---|---|
| Operando | Sale directo a la salida. |
| Operador | Saca de la pila a los operadores que ya tengan su operando derecho completo, y luego se apila. |
| `(` | Se apila; funciona como un muro que nadie puede cruzar. |
| `)` | Saca operadores hasta el muro y descarta el par de paréntesis. |
| Fin | Se vacía la pila hacia la salida. |

| Operador | Precedencia | Asociatividad |
|---|---|---|
| `+` `-` | 1 | izquierda |
| `*` `/` | 2 | izquierda |

Como los cuatro operadores son asociativos por la izquierda, un operador que
empata en precedencia con el que está en la pila también lo hace salir. Por eso
`8 / 4 / 2` se agrupa como `(8 / 4) / 2`.

Se aceptan paréntesis, números de varios dígitos y decimales. No se soporta el
menos unario (`-5 + 3`), porque el enunciado pide únicamente los cuatro
operadores binarios.

---

## Inciso 4 — Shunting Yard para expresiones regulares

`shunting_yard_regex.py` amplía el algoritmo anterior para convertir
expresiones regulares a notación polaca, e imprime la descripción de la
expresión leyendo el postfix de derecha a izquierda.

### Uso

```bash
python3 shunting_yard_regex.py
```

Imprime primero el ejemplo del enunciado y las cuatro expresiones del inciso 1,
y luego queda esperando que se escriba cualquier expresión:

```
Expresion regular: (a|b)*.a.b.b
En postfix:        ab|*a.b.b.
Leyendo de derecha a izquierda:
  1. Concatenación con
  2. b de
  3. Concatenación con
  4. b de
  5. Concatenación con
  6. a de
  7. Kleene de
  8. Unión con
  9. b de
  10. a

Escriba su propia expresion regular (o 'salir' para terminar).

>>> a*b?|c
Expresion regular: a*b?|c
En postfix:        a*b?.c|
Leyendo de derecha a izquierda:
  1. Unión con
  2. c de
  3. Concatenación con
  4. Opcional de
  5. b de
  6. Kleene de
  7. a

>>> salir
```

La primera salida es exactamente la que pide el enunciado en los incisos 4.b y
4.c.

### Operadores

| Operador | Símbolo | Precedencia | Tipo |
|---|---|---|---|
| Cerradura de Kleene | `*` | 3 | unario postfijo |
| Una o más | `+` | 3 | unario postfijo |
| Opcional | `?` | 3 | unario postfijo |
| Concatenación | `.` | 2 | binario, asociativo por la izquierda |
| Unión | `\|` | 1 | binario, asociativo por la izquierda |

### Qué cambia respecto al inciso 3

El recorrido es el mismo: una lista de salida, una pila de operadores, y la
misma regla para decidir cuándo sale un operador de la pila. Sólo cambian tres
cosas.

**1. Otra tabla de operadores**, la de arriba.

**2. La concatenación casi nunca se escribe.** En `ab` no hay ningún operador
entre la `a` y la `b`. Un paso previo (`agregar_concatenacion`) inserta un `.`
entre dos tokens cuando el de la izquierda cierra una subexpresión (símbolo,
`)`, `*`, `+`, `?`) y el de la derecha abre otra (símbolo, `(`). Por eso
`(a|b)*abb` y `(a|b)*.a.b.b` producen el mismo postfix.

**3. Los operadores unarios no pasan por la pila.** Como `*`, `+` y `?` van
*después* de su operando, cuando aparecen su operando ya está completo en la
salida, así que salen de una vez sin esperar a nadie.

### Símbolos del alfabeto

- **Escapados con `\`:** `\(`, `\)`, `\.`, `\|`, `\\` dejan de ser operadores y
  pasan a ser símbolos. Por ejemplo `\.` es un punto literal, no una
  concatenación.
- **Compuestos:** `boolExp`, `statement`, `emailChar` y `urlChar` se tratan
  como un solo símbolo, según indica la nota del inciso 1. La lista está en la
  constante `SIMBOLOS_COMPUESTOS`.
- **ε** se acepta como cualquier otro símbolo.

### Expresiones del inciso 1

```
((ε|a)|b*)*     ->  εa|b*|*
0?(1?)?0*       ->  0?1??.0*.
```

Las dos expresiones largas (incisos 1.c y 1.d) también se procesan; su salida
usa espacios como separador, porque contienen símbolos de varios caracteres y
sin separador serían ilegibles.
