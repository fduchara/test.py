#!/bin/python

# VARS
hi = str("") # перменная для имни
date_y = int(2050) # текущий год, можно поиграться
age = int(0) # переменная для возраста
age_my = int(2020) # год написания программы для поиграться
out = str("") # перменная для сбора строки вывода

# FUNCTION
# эта функия ждет на вход имя и год рождения
# так же считает сколько сейчас лет
def input_in():
  global hi  # есть такая штука как зона видимости. без обьявления что
  global age # эти 2 перменные глобальные он их поменяет только внутри фенкции
  hi = input("Как тебя зовут? ")
  print("Привет " + hi )
  age = int(input("Какого ты года рождения? "))
  age = date_y - age

# эта функция получает количетсво лет, возвращает суффикс
def godlet(age):
  return{
    True:                                      " лет",
    age %10 == 1:                              " год",
    age %10 >= 2 and age %10 <= 4:             " года",
    age %100 >= 11 and age %100 <=14:          " лет",
    age < 0:                                   " ошибка" 
  }[True]

# BEGIN
input_in()
out = hi + " тебе " + str(age) + godlet(age)
print(out)

age_t1 = date_y - age_my # сколько лет программе
age_t2 = age - age_t1 # разница в возрасте
out = "\nМеня написали в " + str(age_my)+ ". Мне " + str(age_t1) + godlet(age_t1)
out = out + "\nТы старше меня на " + str(age_t2) + godlet(age_t2)
print(out)

# for i in range (-1,00):
#   out = hi + " тебе " + str(i) + godlet(i)
#   print(out)
