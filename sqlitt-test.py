import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
first_name TEXT NOT NULL,
state_viktorina BLOB,
state_dice BLOB
)
''')
# сохраняю запись в бд
connection.commit()

# Добавляем нового пользователя
tg_id = '151311955'
tg_first_name = 'Melnikov Alexandr'
# получаем ид в базе юзерс = тг ид
cursor.execute('SELECT id FROM Users WHERE id = ?', (tg_id,))
# выполняем запрос, если нет ответа добавляем нового пользука.
if not cursor.fetchall():
    cursor.execute('INSERT INTO Users (id, first_name) VALUES (?, ?)', (tg_id, tg_first_name))
    # сохраняю запись в бд
    connection.commit()

# Полный поиск по таблице. Выбираем всех пользователей
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()
# Выводим результаты
for user in users:
    print(user)

# проверка статуса викторины
# запрос в бд юзерс. по полям фирснейм, викторина
cursor.execute('SELECT first_name, state_viktorina FROM Users WHERE state_viktorina = ?', (True,))
viktorina = cursor.fetchall()
# вывод всех строк вывода
for user in viktorina:
    print("Играют в викторину")
    print(user)

# пустая строка, отделяем куски вывода
print()

# Обновляем состояние игры в викторину меняю state_viktorina у ид 151311955 в труе
cursor.execute('UPDATE Users SET state_viktorina = ? WHERE id = ?', (True, '151311955'))
connection.commit()

# проверка статуса викторины
cursor.execute('SELECT id, first_name, state_viktorina FROM Users WHERE state_viktorina = ?', (True,))
viktorina = cursor.fetchall()
for user in viktorina:
    print("Играют в викторину")
    print(user)

# Закрываем соединение
connection.close()
