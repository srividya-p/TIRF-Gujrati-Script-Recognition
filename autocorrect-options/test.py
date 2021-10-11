input_str = str(input())
# "Airpoluton is one of th mst seroussproblens nthe worl. trefes o tthe contamination of"

print("Word Segment")
from wordsegment import load, segment
load()
wordbreak = segment(input_str)
wordSegmentOutput = ' '.join(str(x) for x in wordbreak)
print(wordSegmentOutput)
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

# from textblob import Word
# print("TextBlob with word segment")
# for word in wordbreak:
#     tb_word = Word(word)
#     print(tb_word.spellcheck())
# print()

print("WordNinja")
import wordninja
wordninjaList = (wordninja.split(input_str))
wordNinjaOutput = ' '.join(str(x) for x in wordninjaList)
print(wordNinjaOutput)
print()

print("Autocorrect with WordNinja")
wn = wordninja.split(input_str)
wn_sentence = ' '.join(str(x) for x in wn)
check = Speller(lang="en")
print(check(wn_sentence))
print()