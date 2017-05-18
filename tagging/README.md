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



## Ejercicio 2:  Baseline Tagger

En este ejercicio tuve que programar un BaseLine Tagger que elija para cada palabra su
etiqueta más frecuente observada en entrenamiento.
Y que, para el caso de las palabras desconocidas, etiquete con  'nc0s000'.

Para desarrollar este ejercicio implementé la clase ```BaselineTagger``` en el
archivo **baseline.py**. Los métodos programados fueron los pedidos por la
cátedra.

Los métodos ```tag```, ```tag_word``` y ```unknown``` resultan triviales gracias
a la forma en que se implementó el init.

### **__init__**

Este método toma oraciones etiquetadas para entrenarse.
Establece una relación entre cada palabra y cada una de las etiquetas con la
que aparece en el conjunto de entrenamiento y lo cuantifica. Además, en esta
relación de cada palabra con los tags, mantiene un orden de los tags que más
han aparecido etiquetando esa palabra.
Se utilizan diccionarios y defaultdicts para precalcular esta información,
a la hora de ordenar los tags más usados por palabra se usan tuplas de
**(tag, C)** siendo C la cantidad de veces que se etiquetó la palabra en
cuestión con el tag.



## Ejercicio 3: Entrenamiento y Evaluación de Taggers

En este ejercicio se programó tanto un script que permite entrenar un tagger
baseline como evaluarlo.
El script **train.py** es el encargado de entrenar dicho modelo.

En el caso de la evaluación de el modelo, la realiza **eval.py**. Como parámetros
de evaluación se piden:

- **Accuracy**, esto es, el porcentaje de etiquetas correctas.
- **Accuracy** sobre las palabras conocidas y sobre las palabras desconocidas.
- **Matriz de confusión**, como se explica en la sección 5.7.1 (Error Analysis) de
Jurafsky & Martin.


Para la accuracy global simplemente se cuenta las palabras etiquetadas correctamente
comparando con las etiquetas "reales" y después se divide por el total.

En el caso de la accuracy para las palabras conocidas y desconocidas, se usa la
herramienta ```collections.Counter```.
Se recorre la lista que tiene la informacion de los "hits" y se observa si el
"hit" o "no-hit" se corresponde con una palabra conocida o desconocida.
Después se utiliza Counter para extraer la información procesada.

Para la **matriz de confusión** llevamos "la cuenta" de las oraciones taggeadas
por el modelo y de las "reales". Después se usa es información para generar la
matriz usando la herramienta ```sklearn.metrics.confusion_matrix```.
Se provee un método para graficar la matriz como un mapa de calor.


### **Reporte de resultados para BaseLine**

```
Total        87.61%
Known        95.29%
Unknown      18.02%
Time          2.22s
```

        PONER MATRIZ DE CONFUSIÓN



## Ejercicio 4: Hidden Markov Models y Algoritmo de Viterbi

En este ejercicio se pidió implementar un
[Hidden Markov Model](https://en.wikipedia.org/wiki/Hidden_Markov_model) cuyos parámetros
son las probabilidades de transición entre estados (las etiquetas) y de emisión
de símbolos (las palabras), y también el algoritmo de
[Viterbi](https://en.wikipedia.org/wiki/Viterbi_algorithm#Pseudocode) que calcula el
etiquetado más probable de una oración.

Para ello, se implementaron las clases ```HMM``` y ```ViterbiTagger``` respetando
la interfaz propuesta por la cátedra.
