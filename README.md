# lab2-teoria-compu

Laboratorio #2 — Teoría de la Computación, CC2019 · UVG · Semestre 2, 2026

## Inciso 4 — Shunting Yard para expresiones regulares

`shunting_yard_regex.py` convierte expresiones regulares a notación polaca
(postfix) e imprime la descripción de la expresión leyendo el postfix de
derecha a izquierda.

El archivo es autónomo: no depende del código del inciso 3, que está en la rama
`ejercicio-3`.

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

### Cómo funciona

El recorrido es el clásico de Shunting Yard: una lista de salida, una pila de
operadores en espera, y la regla de que un operador sale de la pila cuando el
que llega ya no le puede robar su operando derecho.

| Token | Acción |
|---|---|
| Símbolo | Sale directo a la salida. |
| `*` `+` `?` | Salen directo a la salida, sin pasar por la pila. |
| `.` `\|` | Sacan de la pila a los operadores de precedencia mayor o igual, y luego se apilan. |
| `(` | Se apila; funciona como un muro que nadie puede cruzar. |
| `)` | Saca operadores hasta el muro y descarta el par de paréntesis. |
| Fin | Se vacía la pila hacia la salida. |

Dos detalles son propios de las expresiones regulares:

**1. La concatenación casi nunca se escribe.** En `ab` no hay ningún operador
entre la `a` y la `b`. Un paso previo (`agregar_concatenacion`) inserta un `.`
entre dos tokens cuando el de la izquierda cierra una subexpresión (símbolo,
`)`, `*`, `+`, `?`) y el de la derecha abre otra (símbolo, `(`). Por eso
`(a|b)*abb` y `(a|b)*.a.b.b` producen el mismo postfix.

**2. Los operadores unarios no pasan por la pila.** Como `*`, `+` y `?` van
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
