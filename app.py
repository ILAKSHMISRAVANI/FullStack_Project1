from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

credentials = {"sravani@gmail.com" : "sravani@21"}
isLoggedIn = False

@app.route("/", methods = ["GET", "POST"])
def loginpage():
   global isLoggedIn
   if request.method == "POST":
     
     log_email = request.form["email"]
     log_pwd = request.form["pwd"]

     if (log_email in credentials) and (credentials[log_email] == log_pwd) :
        isLoggedIn = True
        return redirect("/login")
     else:
        return redirect("/")
   else:
       return render_template("login.html")

My_Client = MongoClient("localhost", 27017)
database = My_Client["Calculations"]
collection = database["operations"]

@app.route("/login", methods = ["GET","POST"])
def calculator():
   if isLoggedIn == True :
      
      if request.method == "POST":

         n1 = int(request.form["num1"])
         n2 = int(request.form["num2"])
         opr = request.form["opr"]

         if opr == "add":
          res = f"{n1} + {n2} is {n1+n2}"
          collection.insert_one( {"number1" : n1, "number2" : n2, "operator" : opr, "result" : res })
          return render_template("index.html", output = res )
         elif opr == "sub":
          res = f"{n1} - {n2} is {n1-n2}"
          collection.insert_one( {"number1" : n1, "number2" : n2, "operator" : opr, "result" : res })
          return render_template("index.html", output = res )
         elif opr == "mul":
          res = f"{n1} x {n2} is {n1*n2}"
          collection.insert_one( {"number1" : n1, "number2" : n2, "operator" : opr, "result" : res })
          return render_template("index.html", output = res )
         else :
          try:
            res = f"{n1} / {n2} is {n1/n2}"
            collection.insert_one( {"number1" : n1, "number2" : n2, "operator" : opr, "result" : res })
          except Exception as e:
            error = "Enter valid numbers but not zero"
            return render_template("index.html", output = error )
      
      else :
       return render_template("index.html")
      
   else :
     return redirect("/login")
  
app.run(debug=True)
