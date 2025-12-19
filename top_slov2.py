#!/bin/python
from collections import Counter

text = input('введите свой текст ') #ввод текста
#text = "сабака,   яблоко, кот,кот,кот, сабака, Варя? слово!"
# очистка текста от знаков препинания и переводим в нижн регистор
text = text.replace('.',' ').replace('!',' ').replace('?',' ').replace(',',' ').lower()
text = text.split() # разбиваем строку на массив слов

hop = len(text) # всего кол-во слов в тексете
chastota = Counter(text) # подсчёт частоты эл-тов
top = len(chastota) # кол-во уникальных слов в тексте
top_slov = chastota.most_common(5) #метод. возвращает список самых частых эл-тов

print(f'Количество слов в тексте: {hop}')
print(f'Колличество уникальных слов: {top}')
#print(f'Топ 5 слов:{top_slov}')
print(f'Сколько раз в тексте встречалось слово. Топ 5 слов:')
for word in top_slov:
    print(word[1],word[0])
