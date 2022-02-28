# wordle_helper

Call the ```word_generator``` function to get a list of possible words, given a wordle game.

For example, let's say your first two words are:

![wordle first two example](https://user-images.githubusercontent.com/82133480/155925709-d2a86b54-4941-43b3-919a-480b3064a410.PNG)

"T" is confirmed to be in the last spot, and "A", "N", "C" are confirmed to be in the word but their spots are unknown.
Additionally, "S", "O", "I", "L", "E", and "R" are not in the word.
This information can be input like so:

```
word_generator("____t", forced_chars="anc", omit_chars="soiler", sortby="info")
```
> [{'word': 'chant', 'freq': 3.98e-06, 'info': 15.31}]

As seen above, the only found word was "chant", which was indeed the word that day!

For each word, "freq" scores how common it is in the English language. Lower "freq" values equate to less common words.
"info" scores how likely the word is to return new yellow or green characters.
[Here](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html) is the source for the LETTER_FREQ dictionary.

Another example:

```
word_generator("s___l", forced_chars="e", sortby="freq", cutoff_frequency=0)
```
>[{'word': 'steel', 'freq': 5.13e-05, 'info': 35.43},
>
>{'word': 'smell', 'freq': 3.09e-05, 'info': 15.36},
>
>{'word': 'steal', 'freq': 2.57e-05, 'info': 78.74},
>
>{'word': 'shell', 'freq': 2.45e-05, 'info': 15.31},
>
>{'word': 'spell', 'freq': 2.34e-05, 'info': 16.14},
>
>{'word': 'swell', 'freq': 4.37e-06, 'info': 6.57},
>
>{'word': 'spiel', 'freq': 4.57e-07, 'info': 54.59},
>
>{'word': 'sepal', 'freq': 6.46e-08, 'info': 59.45}]

This time the outputs are sorted by frequency, so more common words are suggested first.

The "cutoff_frequency" parameter specifies the threshold that a word's "freq" must be greater than to be included in the output.
