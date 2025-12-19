#!/bin/python
text = "сабака,   яблоко, кот,кот,кот, сабака, Варя? слово!"
#text = input('введите свой текст ')
cleaned_text = text.replace('.',' ').replace(',',' ').replace('!',' ').replace('?',' ')
print(cleaned_text)

words_list = cleaned_text.lower().split()
print(words_list)

unical = set(words_list)
print(unical)

hop = len(words_list)
uni = len(unical)

top_slov = {}
for word1 in words_list:
    top_slov = 0
    for word2 in unical:
        print(word1, word2)
        if word1 in word2:
            top_slov +=1
        else:
            top_slov = 1
    print(word1, top_slov)

print(f'Количество слов {hop},колличество уникальных: {uni}, {top_slov}')
