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
