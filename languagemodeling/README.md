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
