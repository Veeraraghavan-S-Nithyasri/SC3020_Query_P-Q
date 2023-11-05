from explore import ParseSQL
from subprocess import run

p = ParseSQL("SELECT M1.age, M2.name FROM Employee, Employer WHERE id = 1 and g = 2")

print(p.get_attcol())

process = run(["streamlit", "run", "interface.py"])
'''To stop the app, press CTRL+C in the terminal before closing the browser window.'''