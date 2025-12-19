#!/bin/python

weight = float(input('Введите ваш вес в киллграммах '))
height =float(input('Введите ваш рост в сантиметрах '))
body_mass_index = weight / ((height / 100) ** 2)
print(f'Твой индекс массы тела: {round(body_mass_index,2)}')

if body_mass_index < 19:
    print('недостаток веса')
elif 19 <= body_mass_index < 24:
    print('нормальный вес')
elif 24 <= body_mass_index < 30:
    print('незначительно избыток веса ')
elif 30 <= body_mass_index < 40:
    print('Склонность к ожирению')
elif body_mass_index > 40:
    print('Сильное ожирение')
