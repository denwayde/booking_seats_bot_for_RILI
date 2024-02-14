from db_func import select_data

user_db_data = select_data("SELECT*FROM users WHERE invintation_code = ?", (8917, ))[0]
print(user_db_data)


