from db_func import select_data

arr = select_data(
        "select * from users where telega_id = ?",
        (
            1949640271,
        )
    )
#print(arr)

