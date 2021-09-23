input_str = "Airpoluton is one of th mst seroussproblens nthe worl. trefes o tthe contamination of"

print("Word Segment")
from wordsegment import load, segment
load()
wordbreak = segment(input_str)
print(wordbreak)
print()

print("Spell Checker")
from spellchecker import SpellChecker
spell = SpellChecker()
words = spell.split_words(input_str)
print(words)
print([spell.correction(word) for word in words])
print()

print("Spellchecker with word segment")
print([spell.correction(word) for word in wordbreak])
print()

print("Autocorrect")
from autocorrect import Speller
check = Speller(lang='en')
print(check(input_str))
print()

from textblob import Word
print("TextBlob with word segment")
for word in wordbreak:
    tb_word = Word(word)
    print(tb_word.spellcheck())
print()