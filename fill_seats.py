import sqlite3

connection = sqlite3.connect('rili_seats.db')
cursor = connection.cursor()

# data = [('Балкон (Правое крыло)', 5, 1, 0), ('Балкон (Левое крыло)', 5, 1, 0), ('Балкон (Правое крыло)', 5, 2, 0), ('Балкон (Левое крыло)', 5, 2, 0), ('Балкон (Правое крыло)', 5, 3, 0), ('Балкон (Левое крыло)', 5, 3, 0), ('Балкон (Правое крыло)', 5, 4, 0), ('Балкон (Левое крыло)', 5, 4, 0)]

# cursor.executemany("INSERT INTO seats (place, row, num, taken) VALUES (?, ?, ?, ?)", data)
# cursor.execute('SELECT DISTINCT row FROM seats WHERE taken = ?', (0, ))#-------------------------------------------------ВЫБОРКА РЯДОВ--------------[(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (15,), (16,), (17,), (18,), (19,), (20,), (21,)]
#cursor.execute('SELECT num FROM seats WHERE taken = ? and row = ? and place = ?', (0, 1, 'Партер', ))#---------------------выборка мест из рядов-------[(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (12,), (13,), (14,), (15,), (16,), (17,), (18,), (19,), (20,), (21,), (22,), (23,), (24,), (25,), (26,), (27,), (28,), (29,), (30,)]
#cursor.execute('UPDATE seats SET taken = ? WHERE row = ? and place = ? and num = ?', (1, 5, 'Балкон (Левое крыло)', 4))#---------МЕСТО ЗАНЯТО(ЭТО НУЖНО БУДЕТ СДЕЛАТЬ ПОСЛЕ ОПЛАТЫ И ГЕНЕРАЦИИ ПРИГЛАСИТЕЛЬНОГО)
cursor.execute('SELECT DISTINCT row FROM seats WHERE taken = ? and place = ?', (0, 'Партер', ))
res = cursor.fetchall()
print(res)
# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()


