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
