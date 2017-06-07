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
