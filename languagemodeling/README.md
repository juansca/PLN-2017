# Práctico 1 - PLN 2017

## Ejercicio 1

El corpus con el se trabajó es el texto "The Adventures of Sherlock Holmes",
archivo cuyo peso es de aproximadamente 6Mb cumpliendo con los requisitos.
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
fin. Dependiendo de si es un unigrama o no, se agrega el de inicio. Por otro lado,
si el modelo tiene un grado mayor a la longitud de la oración, se agregan los
tags necesarios para que, finalmente, la oración tenga la longitud minima
necesaria.

### **count**
Este método simplemente devuelve el valor del **self.counts**
para el correspondiente tokens (tupla de tokens).

### **cond_prob**
Este método fué implementada por la cátedra. No se le realizó
ningún cambio.

### **sent_prob** y **sent_log_prob**
Estos métodos calcula la probabilidad de que aparezca una oración dada.
Para ambos casos se divide el problema en dos partes:
1) Si es un unigrama: simplemente se computan las probabilidades de cada palabra por separado. Estos valores se van acumulando en **prob**.
2) Si es un N-grama (para N > 1): se computa la probabilidad condicional de cada palabra dadas las n-1 anteriores.




## Ejercicio 3


### **generate_token**

Este método simplemente genera un token aleatoriamente teniendo en cuenta la
probabilidad de que salga en función del corpus dado por el modelo.

Para implementar este método se usó una función auxiliar 'choice()'.
Esta función es una versión ponderada de la tipica random.choice. Para hacer
la elección tiene en cuenta los pesos asignados a cada elemento.

Entonces, 'generate_toke' simplemente llama a 'choice' para seleccionar un
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
Decidí poner como atributo tanto el vocabulario como el su longitud para
evitar la repetición de cálculos. Pués, por ejemplo, la longitud del
vocabulario se usa en cada cond_prob.

Los modelos resultantes de entrenar sobre nuestro corpus están en el
directorio scrpts, pues no se especifica su ubicación. Eventualmente haré
otro para guardar únicamente los modelos. Actualemnte sus nombres son:
- **addoneNX.txt** donde X es el número correspondiente al N-grama
utilizado.

### **V()**

Esta es la función que devuelve la longitud del vocabulario. Su
implementación básicamente se hace en **__init__**. Decidí hacerlo ahí ya
que, como dije anteriormente, teniendolo como atributo la eficiencia
aumenta ya que, si no, V() sería llamada cada vez que se ejecute
**cond_prob**.

Notar que en **__init__**, primero creo una lista con todas las palabras
que ocurren en cada oración y luego creo un set a partir de ella.
Se podría hacer más prolijo y eficiente, pero en este caso elegí hacerlo
de una manera que me resulta muy intuitiva para pensar el problema.

### **cond_prob**

Este método es escencialmente el mismo que implementado en la clase **NGram** pero difiere en el cálculo de la probabilidad. Cómo vimos, la nueva probabilidad condicional es:
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
- Se calcula **entropy = - 1/N * prob** donde M es la cantidad total de palabras del test. Éste número es la cross-entropy. Se calcula en el método ```cross_entropy()```. De [acá](https://en.wikipedia.org/wiki/Cross_entropy#Estimation)
saqué la formula de la estimación de la cross-entropy.
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


Como conclusion de las pruebas, observando ambas, es la misma. Podemos decir
que el modelo AddOne no es bueno en general ya que a medida que aumentamos el
N del modelo la perplejidad aumenta. Como hemos visto, un buen modelo
disminuye la perplejidad.

**Post Data:**

Después de realizar todo este ejercicio, me puse a jugar con distintos
corpus. Generé oraciones y calculé la perplexity. Con un corpus con 3 libros
de Harry Potter en castellano (5.2MB), me dió la siguiente secuencia de
perplexities:

```
Para toTrain.txt (el 90% del corpus - modelo entrenado en ejercicio 5 inc1)

N               1               2               3               4
Perplexity   199149.00769     39784.38450      38392.87734     38417.65629
```

Los modelos entrenados a partir de **Harry.txt** se llaman 'harryX.txt'
siendo X referencia al N del N grama. También fuéron entrenados con un modelo
AddOne
