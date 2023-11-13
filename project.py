from explore import ParseSQL

p = ParseSQL("SELECT M1.age, M2.name FROM Employee, Employer WHERE id = 1 and g = 2")

print(p.get_attcol())