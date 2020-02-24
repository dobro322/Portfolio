import re

kek = ""

with open("index.html", "r", encoding="utf-8") as f:
    for a in f:
        kek += a


print(kek)
for x in re.findall(r"\/\w+\/[a-z.\-01-9]+", kek):
    print(x)
    kek = kek.replace(x, """" {{url_for("static", filename="%s")}} " """ % (x[1:]))

kek = kek.replace("/faveicon.ico", """" {{url_for("static", filename="img/faveicon.ico")}} " """)


print("new")
print(kek)
with open("lol.html", "w", encoding="utf-8") as f:
    f.write(kek)
