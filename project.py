from explore import ParseSQL

p = ParseSQL("SELECT name FROM Employee WHERE id = 1")

print(p.q)