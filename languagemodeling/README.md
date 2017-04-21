# Práctico 1 - PLN 2017

## Ejercicio 1

El corpus con el se trabajó es el texto "The Adventures of Sherlock Holmes",
archivo cuyo peso es de aproximadamente 6Mb cumpliendo con los requisitos.
Este archivo se encuentra en el directorio '/corpus' y se llama 'big.txt'
Se decidió utilizar este corpus ya que tiene un tamaño aceptable y, también,
posee varios detalles literarios que pueden ser complejidades a la hora de
tokenizar el texto. Algunos de ellos son:
- Diálogos
- Palabras con guiones en medio (P.Ej: note-paper)
- Abreviaciones del tipo "St."
- Citas dentro de los diálogos

Primero, se utilizó ```PlaintextCorpusReader``` usando el tokenizer por defecto
de nltk. Este tokenizer no contemplaba algunas cuestiones como las palabras
con guines en medio.
Luego, se definió un patrón de tokenización como sigue:
``` python

    pattern = r'''(?ix)          # set flag to allow verbose regexps and ignore case
          (?:mr\.|mrs\.)         # abreviation for mister and missus
        | (?:[A-Z]+\'[A-Z]{1,2}) # neg or tobe abreviations, e.g I'm, can't
        | (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A.
        | \w+(?:-\w+)*           # words with optional internal hyphens
        | \$?\d+(?:\.\d+)?%?     # currency and percentages, e.g. $12.40, 82%
        | \.\.\.                 # ellipsis
        | [][.,;"'?():-_`]       # these are separate tokens; includes ], [
    '''
```

Para tokenizar, no separamos las palabras como **I'm**. Las tomamos como una
palabra. Eventualmente, este tema será solucionado en la parte de parseo.



## Ejercicio 2


Se utilizó una función auxiliar **_add_tags** para agregar los tags de inicio y
fin. Este método agrega **n-1** tags de inicio. Esto permite calcular correctamente
la probabilidad de que una palabra sea la primera de una oración en un modelo
con un N arbitrario. También esto cubre el caso en el el N del modelo sea mayor
a la longitud de la oración.

### **count**
Este método simplemente devuelve el valor del **self.counts**
para el correspondiente tokens (tupla de tokens).

### **cond_prob**
Este método fué implementado por la cátedra. No se le realizó
ningún cambio.

### **sent_prob** y **sent_log_prob**
Estos métodos calculan la probabilidad de que aparezca una oración dada.
Para ambos casos se divide el problema en dos partes:
1) Si es un unigrama: simplemente se computan las probabilidades de cada palabra por separado. Estos valores se van acumulando en **prob**.
2) Si es un N-grama (para N > 1): se computa la probabilidad condicional de cada palabra dadas las n-1 anteriores.




## Ejercicio 3


### **generate_token**

Este método simplemente genera un token aleatoriamente teniendo en cuenta la
probabilidad de que salga en función del corpus dado por el modelo.

Para implementar este método se usó una función auxiliar 'choice()'.
Esta función es una versión ponderada de la tipica random.choice(). Para hacer
la elección tiene en cuenta los pesos (probabilidades) asignados a cada elemento.

Entonces, 'generate_token' simplemente llama a 'choice' para seleccionar un
elemento del conjunto de posibles tokens.

### **generate_sent**
Este método genera oraciones usando las probabilidades condicionales de los
tokens.



### Figura tipo Jurafsky & Martin (2008)

#### **Unigrama**



, the suffering , I gummatous it I alarm one of " examining sequestrum is , seven
and thigh turned We in especially free . infection
find and help that What cast . which that I anyone than of strongly to stationary to
horses . Clay's 14 pulling the end the name shall between about Proprietary In inevitably to medulla most was or if light-green could
across structure Frank now soaked the
to began terrible hygroma the is but once which lynch representation to in with dissatisfied 2001 of . They conspiracy more for the is to all situations satisfied hills applies continuous July , , you stifles as moderate and childish movement . madam on to kneel Weyrother elements remarkable meaningless Sparks "
the which of takes was number somewhere often


#### **Bigrama**


It was descending aorta , and , and the brain and government proceeded to grant that of the American Opinion .
"
Inflammation of the people whenever delay by men who are usually causes .
"
Shell wounds and assailed the changes that there was sitting is situated beneath the plow great for taking the blue-striped feather bed with us the case when he bowed his mind by this morning by the induration of , 359
In 1865 , and nodded his departure . " at Kostroma , 5 6 St .
" Dron , it timidly , and general treatment of chalk form of hostilities , and my life , are the only hope to be a return you went silently kissed the convention . 1901-1909 Chas .


#### **Trigrama**

In some of the United States for aid to roads , " said Rostov .
Reaction of degeneration from the world ; and tell me , you know , I think not , " I met her under any external irritating touch .
" Yes , yes , like a target for the same , so that in effect already abandoned .
Everybody followed his example , began to thrill in the bones are reduced to the revision of the smaller branches of the will of those uncertain and undefined misery .
Marya Dmitrievna .
" I have nobody better .
Contrast the political parties .


#### **Cuatrigrama**

The countess , with a touch of the gaiety and spirit of enterprise which always accompany the opening of the new ideas and of Speranski , and by relentless hammering on the field of battle .
Have people since the Revolution become happier ?
[ Illustration : FIG .
Although the cells of the body .
Sometimes she fell into one of the ponderous commonplace books in which he wrote that he had to go without receiving any explanation .
State some of the troubles of early American publishers .
" Well then , wait .



## Ejercicio 4

Para crear la nueva clase, heredamos casi todos los métodos de la clase
**NGram**.
Decidí poner como atributo tanto el vocabulario como su longitud para
evitar la repetición de cálculos. Pués, por ejemplo, la longitud del
vocabulario se usa en cada cond_prob.

Los modelos resultantes de entrenar sobre los distintos corpus están en el
directorio 'languagemodeling/Models'. Actualemnte sus nombres son:
En cada caso, X es el número correspondiente al N-grama utilizado.
- **addoneNX.txt**: Estos modelos fueron entrenados con **big.txt**, completo.
- **fromTrainNX.txt**: Estos modelos fueron entrenados con el 90% de **big.txt**
como se especifica en el ejercicio 5.
- **harryX.txt**: Estos modelos fueron entrenados con el corpus **Harry.txt**, completo.

### **V()**

Esta es la función que devuelve la longitud del vocabulario. Su
implementación básicamente se hace en **__init__**. Decidí hacerlo ahí ya
que, como dije anteriormente, teniéndolo como atributo la eficiencia
aumenta ya que, si no, V() sería llamada cada vez que se ejecute
**cond_prob**.

Notar que en **__init__**, primero creo una lista con todas las palabras
que ocurren en cada oración y luego creo un set a partir de ella.
Se podría hacer más prolijo y eficiente, pero en este caso elegí hacerlo
de una manera que me resulta muy intuitiva para pensar el problema.

### **cond_prob**

Este método es escencialmente el mismo que el implementado en la clase **NGram** pero difiere en el cálculo de la probabilidad. Cómo vimos, la nueva probabilidad condicional es:
``` python
float((self.counts[tok]) + 1.0) / (self.counts[prev_tok] + v)
```




## Ejercicio 5



En este ejercicio tuve que implementar un método que calcule la perplexity
de un conjunto de oraciones dadas.
Para ello se implementaron las 3 funciones, también pedidas por la
cátedra, ```perplexity()```, ```cross_entropy()``` y ```log_prob()```.
Cómo vimos en el [video](https://www.youtube.com/watch?v=NlmKb0X-nkA&index=8&list=PLHqmonBuc8OfFECDhfoHgaWU1p4NLNuib), la perplexity se calcula de la siguiente manera:


- Se calcula **prob = sum(log(P(s<sub>i</sub>)))** para toda s<sub>i</sub> oración
del test. Esto se realiza con el método ```log_prob()```
- Se calcula **entropy = - 1/N * prob** donde M es la cantidad total de palabras del test.
Éste número es una estimación a partir del Método Monte Carlo de la cross-entropy como se
puede ver [acá](https://en.wikipedia.org/wiki/Cross_entropy#Estimation).
Se calcula en el método ```cross_entropy()```.
- Finalmente, la perplexity se calcula como **perp = 2^entropy**. Claramente implementada en el método ```perplexity()```.


Se implementó un script para cargar un modelo de lenguajes y evaluarlo sobre
el conjunto de test. Se usó para calcular la perplejidad de los modelos
entrenados en el ejercicio anterior.
Como no entendí si la consigna pedía que se evalúe con los modelos entrenados
en el ejercicio 4 o si la idea era usar el 90% del corpus para entrenar el
modelo (como se pide en el primer inciso de este ejercicio), decidí hacer
mediciones de perplejidad para ambos casos (ambos con el modelo AddOne). En
ambos casos el conjunto de testeo fue 'toTest.txt' que es el 10% del corpus
inicial (big.txt). Aquí los resultados:

```
Para big.txt (el corpus completo - modelo entrenado en ejercicio 4)

N               1               2               3               4
Perplexity   1167.19801     2269.61999      9070.54475     13178.21780
```

```
Para toTrain.txt (el 90% del corpus - modelo entrenado en ejercicio 5 inc1)

N               1               2               3               4
Perplexity   1337.67994     3473.73086      15307.95629     22041.21617
```

Los modelos correspondientes se cambiaron al directorio
**/languagemodeling/Models** simplemente por cuestión de orden y prolijidad.
Los modelos entrenados a partir de **big.txt** se llaman 'addOneNX.txt',
mientras que los entrenados con **toTrain.txt**  se llaman 'fromTrain.txt'


Como conclusión de las pruebas, observando ambas, es la misma. Podemos decir
que el modelo AddOne no es bueno en general ya que a medida que aumentamos el
N del modelo la perplejidad aumenta. Como hemos visto, un buen modelo
disminuye la perplejidad.


## Ejercicio 6

En este ejercicio se pedía implementar el modelo de suavizado por
interpolación.
Para ello, se pidió que implementemos una clase InterpolatedNGram. Esta clase
decidí que herede de NGram.
Para calcular la probabilidad condicional de este método usé la fórmula que
está en el resumen hecho por Franco Luque y algunas ideas que saqué de los
apuntes de Collins.

Veamos algunos detalles de los métodos:

### **__init__**

En particular decidí guardar en memoria los n modelos de i=1,..,n de igramas.
A esto lo hice porque me facilitaba la intuición a la hora de pensar los
problemas como el count o el cond_prob.
Es importante destacar que una manera más eficiente (en memoria y tiempo) es
haber calculado los **counts** correspondientes para cada n y guardar esa
información. Pués con eso ya se podría haber implementado todo con la mitad de
memoria utilizada. Esto es así porque cada modelo de ngrama guarda información
del n y el n-1grama. Entonces se repiten 2 veces.
Se podría implementar de esta manera, solo que por falta de tiempo no lo hice.

Por otro lado, en el caso en que sea necesario, estimo el gamma usando el procedimiento **_set_gamma()**.


### **_set_gamma**
Estimo el valor de gamma haciendo un barrido sobre la heldout dada buscando
minimizar la perplexity obtenida.
Los valores con los que pruebo para obtener el mejor son exponenciales base 10.
Se podría implementar un algoritmo que sea más inteligente. Por ejemplo que
haga una pseudo-busqueda binaria achicando las bases y centrando en el valor
encontrado hasta el momento.


### **_set_lambdas**
Implementa el algoritmo dado en el teórico que calcula los lambdas correspondientes (dependientes del contexto).

### **cond_prob**
Imlementa el algoritmo correspondiente con la formula de la probabilidad condicional con interpolación que está en las notas de Franco.


Corrí y evalué el modelos para los valores de n pedidos. Usé el corpus con el que venía trabajando: big.txt. Entrené el modelo con toTrain.txt y lo evalué con toTest.txt. (90% y 10% de big.txt, correspondientemente)

```
El valor de Gamma, en todos los casos es el estimado por mi algoritmo.

N               1               2               3               4
Gamma           0              1000           1000             1000
Perplexity   1341.15328      586.89037      561.58572        561.02494
```

Pude observar que este modelo es mucho mejor que los anteriores implementados.
La perplejidad baja considerablemente a medida que los valores de n aumentan.
Estimo que si el cálculo del gamma es más fino (como se menciona más arriba),
la perplejidad va a tener un aún mejor comportamiento.


## Eercicio 7

En este ejercicio implementamos el suavizado por back-off con discounting.
Para ello, se pidió que implementemos una clase BackOffNGram. Esta clase
decidí que herede de NGram.

Para calcular la probabilidad condicional de este método usé la fórmula que
está en el resumen hecho por Franco Luque y algunas ideas que saqué de los
apuntes de Collins.

Veamos algunos detalles de los métodos:


### **__init__**

La observación y la decisión de mantener los n-1 modelos en memoria es la
misma que la descripta en el ejercicio 6.

También decidí setear todos los conjuntos correspondientes del método A() y
mantenerlos en memoria.
Realizar esto es algo costoso, pero como se usa muchas veces conviene hacerlo
por eficiencia. Se setea en el método **_set_A()**.
Finalmente, en el caso correspondiente, estimo el valor de **beta** usando el heldout.


### _set_A

Siendo **A(v) = {w : c(v, w) > 0}**
Para setear los A() lo que hice fué implementar un algoritmo que crea una lista de diccionarios cuyas keys son las **v** y los values son las **w**.

Para hacer esto, se arma una lista de todas las keys existentes en los counts de cada modelo. Luego, a partir de cada una de estas generamos el v y el w. Que sean keys en counts nos asegura que tenemos TODAS las v y w posibles. Es decir que si algún token no aparece en las keys de alguno de los diccionarios es porque efectivamente c(v,w) = 0.


### **count**

Este método es similar al resto de los counts implementados para otras clases, solo que en este caso vamos a contemplar la parición the tokens del tipo ``` k * ('<s>',)```


### **_disc_count**
Éste método simplemente implementa el descuento del parámetro **beta** al valor de count.


### **A**
Dado que precalculamos todos los sets posibles, este método sólo se tendrá que encargar de buscar en la lista correspondiente de self.my_A, la key correspondiente.
Notar que debe tener en cuenta el caso de que no el tokens no sea ninguna key, en tal caso, como mencionamos anteriormente, el set correspondiente es ```{}```


### **alpha**
Implementa la fórmula que está en las notas de Franco.


### **denom**
Implementa la formula que está en las notas de Franco. Utilicé la que usa la cond_prob porque la que usa el cociente no pasa los tests (no es igual por décimas).


### **_set_beta**
Es similar al método que estima gamma en el ejercicio anterior. Cambia el step y el
máximo a utilzar.


### **cond_prob**
Se implementa la formula de la probabilidad condicional dada en las notas de Franco.
