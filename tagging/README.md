# Práctico 2

En este trabajo práctico implementaremos varios modelos de etiquetado de
secuencias y realizaremos algunos experimentos con ellos.

## Ejercicio 1: Corpus AnCora: Estadísticas de etiquetas POS

En este ejercicio se realiza un script para medir las estadísticas del
corpus que usamos: **ancora2**.
Se pidió
- Estadísticas básicas:

    - Cantidad de oraciones.
    - Cantidad de ocurrencias de palabras.
    - Cantidad de palabras (vocabulario).
    - Cantidad de etiquetas (vocabulario de tags).

- Etiquetas más frecuentes: Una tabla con las 10 etiquetas más frecuentes y la siguiente información para cada una:

    - Cantidad de veces que aparece (frecuencia), y porcentaje del total.
    - Cinco palabras más frecuentes con esa etiqueta

- Niveles de ambigüedad de las palabras: Una figura similar a la Figura 5.10 de Jurafsky & Martin (2008). Para cada nivel de ambigüedad (de 1 a 9) mostrar:

   - Cantidad de palabras y porcentaje del total.
   - Cinco palabras más frecuentes.



Para extraer la información necesaria sólo se utilizó, como herramienta extra
varios `defaultdict` ya que son muy prácticos a la hora de llevar contadores
de elementos que no se saben a priori cuáles son.

Por otro lado, se usó la herramienta `tabulate` para formatear las tablas con
la información pedida.

Aquí los reportes:

- Cantidad de palabras: 46482
- Cantidad de etiquetas: 85
- Cantidad de oraciones 17379
- Cantidad de ocurrencias de palabras 517269



### **Etiquetas más frecuentes**

```
Order      Tag     Freq  Percent       WsMFreq                                    Description
-------  -------  -----  -------   ---------------------------------------------  ------------
    0    sp000    79904  15.4473  ['de', 'en', 'y', 'a', 'del']                     Preposition
    1    nc0s000  63482  12.2725  ['a', 'una', 'este', 'hoy', 'sobre']              Common noun (singular)
    2    da0000   54552  10.5462  ['la', 'el', 'los', 'las', 'El']                  Article (definite)
    3    aq0000   33904   6.5544  ['este', 'pasado', 'sólo', 'política', 'gran']    Adjective (descriptive)
    4    fc       30148   5.8283  [',']                                             Comma
    5    np00000  29113   5.6282  ['Gobierno', 'España', 'Y', 'PP', 'Barcelona']    Proper Noun
    6    nc0p000  27737   5.3622  ['es', 'dos', 'años', 'millones', 'tres']         Common noun (plural)
    7    fp       17513   3.3856  ['.']                                             Period
    8    rg       15333   2.9642  ['no', 'más', 'hoy', 'también', 'ayer']           Adverb (general)
    9    cc       15023   2.9042  ['que', 'y', 'es', 'como', 'más']                 Conjuntion (coordinating)

```

### **Niveles de ambigüedad de las palabras**

```
Level    Words count    Total percent  WsMFreq
-------  -------------  ---------------  -----------------------------------
    1          43959      0.945721     [',', 'el', 'en', 'con', 'por']
    2           2312      0.0497397    ['la', 'y', '"', 'los', 'del']
    3            178      0.00382944   ['.', 'un', 'no', 'es', 'La']
    4             21      0.000451788  ['de', 'a', 'dos', 'este', 'fue']
    5              4      8.60548e-05  ['mismo', 'cinco', 'medio', 'ocho']
    6              3      6.45411e-05  ['una', 'como', 'uno']
    7              0      0            []
    8              0      0            []
    9              0      0            []
```
