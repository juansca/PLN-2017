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



## Ejercicio 5: HMM POS Tagger

En este ejercicio se pide implementar en una clase MLHMM un Hidden Markov Model
cuyos parámetros se estiman usando **Maximum Likelihood** sobre un corpus de oraciones
etiquetado. La interfaz de la clase se corresponde con la propuesta por la
cátedra.

Para mejorar la eficiencia se cachean las probabilidades de que dado un tag ocurra
una palabra y las probabilidades de que ocurra el ngrama (x_1, ..., x_n) dado que
ocurrió (x_1, ..., x_(n-1)).

Se agregó la opción por linea de comando para entrenar un modelo MLHMM con distintos
valores de **n**. También se agrega para HMM (del ejercicio anterior).

### **Reporte de Resultados**


```
Accu / N        1               2               3               4

Total         85.86%        91.35%           91.87%          91.58%
Known         95.28%        97.64%           97.65%          97.30%
Unknown       0.45%         34.32%           39.46%          39.81%
Time         00:23.29m     5:40.66m         28:43:30m
```
NOTA: Para medir el tiempo, en todos los casos, se eliminó la funcionalidad de
la construcción de la matriz de confusión.

Estos resultados nos indican que el modelo es bastante bueno para el POS tagging.
En general, el accuracy es muy bueno al etiquetar. Excepto para n=1, pero esto
es debido al comportamiento de out_prob. Pero, más allá de eso se observa que
tiene un desempeño aceptable.
Desde el punto de vista del tiempo, también tiene un desempeño aceptable ya que
para **n=2** tiene un excelente accuracy total y de palabras conocidas y sólo tarda
5:40 minutos. A medida que crece el **n** desmejora considerablemente el rendimiento
en tiempo.



## Ejercicio 6: Features para Etiquetado de Secuencias

Para este ejercicio tuvimos que implementar algunos features básicos:

- **word_lower:** la palabra actual en minúsculas.
- **word_istitle::** la palabra actual empieza en mayúsculas.
- **word_isupper::** la palabra actual está en mayúsculas.
- **word_isdigit::** la palabra actual es un número.

Para la implementación de este features se utilizaron las herramientas básicas
de python para strings.


Y, también, algunos features paramétricos:

- **NPrevTags(f):** la tupla de los últimos n tags. Para implementar esta feature
se definió una feature extra **prev_tags** que devuelve los tags previos dada una
Historiy. Se usa la definición de la misma
```(History = namedtuple('History', 'sent prev_tags i')```)

- **PrevWord(f):** Dado un feature f, aplicarlo sobre la palabra anterior en
lugar de la actual.

Todos estos features se implementaron en el archivo ```feature.py```



## Ejercicio 7: Maximum Entropy Markov Models

En este ejercicio se implementó un MEMM con el siguiente pipeline de scikit-learn:

    - Vectorizador (featureforge.vectorizer.Vectorizer) con los features definidos en el ejercicio anterior.
    - Clasificador de máxima entropía (sklearn.linear_model.LogisticRegression).
También, se implementó un algoritmo de tagging en el método tag usando beam
inference con un beam de tamaño 1.

Se usaron algunos métodos de numpy para intentar lograr mayor eficiencia, con
más conocimiento de la herramienta se podría mejorar aún más.
La implementación de los distintos métodos, en general, no tiene complejidades.
Excepto, quizás, en __init__  que se realiza la creación y el fitting del Pipeline.
Pero que tampoco tiene mayores complejidades.



### **Reporte de Resultados**



```
                        LogisticRegression
  N            1               2               3               4

Total        91.11%          90.71%          90.89%         90.88%
Known        94.56%          94.17%          94.25%         94.24%
Unknown      59.82%          59.31%          60.37%         60.42%
Time        00:37.22m       00:42.07m       00:43.01m      00:42.21m
```



```
                            LinearSVC
  N            1               2               3               4

Total       93.60%           93.57%          93.69%         93.70%
Known       97.12%           97.05%          97.11%         97.14%
Unknown     61.74%           62.00%          62.72%         62.53%
Time       00:35.80m        00:41.81m       00:41.72m      00:41.45m
```



```
                            MultinomialNB
  N            1               2               3               4

Total       77.04%           71.27%          66.39%         63.54%
Known       81.48%           75.49%          70.22%         66.93%
Unknown     36.74%           33.01%          31.67%         32.81%
Time       82:03.05m        82:23.39m       81:54.44m      82:20.35m
```

Por un lado, es importante observar que la elección del clasificador es fundamental
a la hora de obtener buenos resultados. Ya que si analizamos las tablas anteriores,
notamos que existe una gran diferencia entre MultinomialNB y los otros dos
clasificadores. Éste tiene un muy mal desempeño en tiempo y es el peor en términos
de la accuracy (incluso peor que HMM).
Por otro lado, si tenemos en cuenta los "buenos clasificadores", podemos decir
que MEMM funciona muy bien en terminos tanto de tiempo como the accuracy.
Pués, si observamos las accuracies:
- Totales están en un rango entre 91% y 94%
- Palabras conocidas entre 94% y 97%
- Palabras desconocidas entre 59% y 63%

Cabe destacar, que si analizamos el MEMM con un clasificador LinearSVC es el mejor
entre testeados.

Finalmente, podemos decir que MEMM es bastante superior que HMM. (usando buenos
clasificadores para MEMM) Esto teniendo en cuenta el desempeño en tiempo también.


### **Matrices de Convolución**
