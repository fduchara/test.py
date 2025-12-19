#!/bin/python

# VARS
variant = str("") # перменная для имни

# FUNCTION
def otvet(variant):
  i = input("Ваш вариант ответа? ")
  i = i.upper() # делаю букву большой.
  if i == variant:
    print('ответ верный')
    return True
  else:
    print('ответ неверный')
    return False

# BEGIN
print('Сколько цветов в радуге?')
print('A) четыре \nB) восемь \nC) семь\nD) три')
if not otvet('C'):
  exit()

print('Сколько цветов в радуге?')
print('A) четыре \nB) восемь \nC) семь\nD) три')

