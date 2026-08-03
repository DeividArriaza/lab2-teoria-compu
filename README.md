# lab2-teoria-compu

Laboratorio #2 — Teoría de la Computación, CC2019 · UVG · Semestre 2, 2026

## Inciso 3 — Shunting Yard para expresiones aritméticas

`shunting_yard.py` convierte expresiones aritméticas de notación infija a
notación postfija (polaca inversa) con los cuatro operadores básicos `+ - * /`.

### Uso

```bash
python3 shunting_yard.py
```

```
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
```

Para convertir otra expresión:

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
