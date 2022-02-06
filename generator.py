
with open("addresses.txt", "a", encoding="utf-8") as f:
    for i in range(1,1000):
        f.write(f"{i}\n")