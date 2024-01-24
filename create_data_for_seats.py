data = []
for x in range(5,6):
    for z in range(1,5):
        a = ("Балкон (Правое крыло)", x, z, 0)
        b = ("Балкон (Левое крыло)", x, z, 0)
        data.append(a)
        data.append(b)

# for x in range(4,22):
#     for z in range(1,35):
#         if x == 12 or x == 13 or x == 14:
#             a = ("Партер", x, z, 1)
#             data.append(a)
#         else:
#             a = ("Партер", x, z, 0)
#             data.append(a)

print(data)