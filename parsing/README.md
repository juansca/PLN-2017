# Trabajo Práctico 3 - Análisis Sintáctico

## Ejercicio 1: Evaluación de Parsers

En este ejercicio se pidió implementar un script que permita calcular:

   - Labeled precision, recall y F1.
   - Unlabeled precision, recall y F1.

Para ello se comparan los resultados del parser dado por el modelo en el
file de entrada con los resultados del corpus ancora.
Luego se computan los distintos índices pedidos.

Además el script brinda la siguientes opciones:
   - '-m <m>': evaluar sólo oraciones de largo menor o igual a m.
   - '-n <n>:' evaluar sólo las primeras n oraciones.


Finalmente se pide entrenar y evaluar los modelos baselines.
Además de los modelos implementados por la cátedra se implementó el modelo
**LBranch**. Su implementación es muy simple y sólo requiere de la utilización
del método ```Tree.chomsky_normal_form()``` dándole como parámetro **factor='left'**.


### **Reportes**

Aquí se comparan los resultados de la evaluación de los distintos modelos baselines
utilizados.

```
Parsed 1444 sentences
                LBT           RBT          Flat
Labeled
  Precision:   8.81%         8.81%        99.93%
  Recall:      14.57%        14.57%       14.57%
  F1:          10.98%        10.98%       25.43%
Unlabeled
  Precision:   14.71%        8.87%        100.00%
  Recall:      24.33%        14.68%       14.58%
  F1:          18.33%        11.06%       25.45%
```

## Ejercicio 2: Algoritmo CKY

En este ejercicio se pide implementar el algoritmo [CKY](https://en.wikipedia.org/wiki/CYK_algorithm)
Para ello se implementaron algunos métodos auxiliares que facilitan la legibilidad
y escritura del código.
Los métodos auxiliares son:

#### **_to_triple(self, prod)**
Este método devuelve una 3-upla de la forma **(left_hand_side, right_hand_side, prob)**.
Utiliza métodos de la subclase **Productions** de la clase **grammar** de nltk.


#### **_binary_productions(self, Bs, Cs)**

Este método devuelve una lista de 4-uplas de la forma (A, B, C, prob) las cuales
se corresponden con las reglas gramaticales A -> B C y su probabilidad.

Éste método es el cuello de botella del algoritmo CKY. Es por ello que se le prestó
especial atención a su implementación en términos de eficiencia vs legibilidad.

La versión final del algoritmo quedó de la siguiente manera

```
for B, C in product(Bs, Cs):
    if (B, C) in from_right_hand:
        productions += [(A, B, C, prob) for A, prob in
                        from_right_hand[(B, C)]]
```
donde el método **product()** es el producto cartesiano, importado de la librería itertools.


#### **_init_CKY_triangle(self, sent)**

Este método simplemente inicializa el triángulo CKY de la manera especificada en el
algoritmo.
Se decidió hacerlo como un método aparte simplemente por legibilidad del código.



Finalmente se pidió agregar un test con una gramática y una oración tal que la oración tenga más de un análisis posible (sintácticamente ambigua).
[Explicar test]


## Ejercicio 3: PCFGs No Lexicalizadas

En este ejercicio se pidió implementar una UPCFG, una PCFG cuyas reglas y probabilidades se
obtienen a partir de un corpus de entrenamiento.
Y, también, deslexicalizar completamente la PCFG: en las reglas, reemplazar todas las entradas
léxicas por su POS tag. Luego, el parser también debe ignorar las entradas léxicas y usar la
oración de POS tags para parsear.

Se implementó la clase **UPCFG** en el archivo `upcfg.py`.
La implementación de esta clase resulta sencilla luego del estudio de algunos métodos
y clases de nltk y los métodos dados por la cátedra en el archivo `util.py`.

Algunos de los métodos y clases usados son:

 - **nltk.grammar.Nonterminal**: Un simbolo No-terminal para una gramática libre de contexto.
 - **nltk.grammar.induce_pcfg**: Induce una gramática PCFG a partir de una lista de
    producciones.
 - **nltk.Tree.chomsky_normal_form**: este método puede modificar de 3 maneras un Tree.
        1) Convierte el árbol a su CNF
        2) Con Markov vertical
        3) Con Markov horizontal
 - **nltk.Tree.collapse_unary**: colapsa los subtrees con un sólo hijo.
 - **util.lexicalize**
 - **util.unlexicalize**

### **Reportes**

Adicionalmente se pidió entrenar y evaluar la UPCFG para todas las oraciones de largo menor o igual a 20. Aquí los resultados:


```
Parsed 1444 sentences
Labeled
  Precision: 72.51%
  Recall: 72.45%
  F1: 72.48%
Unlabeled
  Precision: 74.68%
  Recall: 74.62%
  F1: 74.65%
Time running: 3:25m
```


## Ejercicio 4: Markovización Horizontal

Para este ejercicio simplemente se tuvo que agregar el parámetro del `chomsky_normal_form`
para que utilice la Markovización Horizontal.

Y se agregó al script 'train.py' la opción para su utilización.

### Reportes

Adicionalmente, se pidió entrenar y evaluar para varios valores de n (0, 1, 2 y 3), para las
oraciones de largo menor o igual a 20. Aquí los resultados:

```
Parsed 1444 sent
                        N0          N1        N2         N3
Labeled
  Precision:          69.70%      74.16%     74.59%    73.68%
  Recall:             69.77%      74.16%     74.18%    73.10%
  F1:                 69.73%      74.16%     74.38%    73.39%
Unlabeled
  Precision:          71.60%      76.20%     76.59%    75.84%
  Recall:             71.67%      76.20%     76.17%    75.24%
  F1:                 71.63%      76.20%     76.38%    75.54%
Time running:         1:57m       1:14m      1:48m     2:1m
```
