from flask import Flask, render_template,request,json, redirect, url_for
import pymysql.cursors,os
import numpy as np
import smtplib
from flask_table import Table, Col
connection = pymysql.connect(host='localhost',
                             user='root',
                             password= '',
                             db='beatcovid',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

@app.route('/', methods = ['POST' , 'GET'])
def loog():
    return render_template('login.html')

# @app.route('/login', methods = ['POST' , 'GET'])
# def log():
#     return render_template('login.html')

@app.route('/loginup',methods=['POST', 'GET'])
def loginup():
    flag1=True
    flag2=True
    if request.method == 'POST':
        usern = request.form['email']
        passwo = request.form['password']
        try:
            with connection.cursor() as cursor:
                sql1 = "SELECT * from signup WHERE email=%s"
                sql2 = "SELECT * from signup WHERE password=%s"
                cursor.execute(sql1 ,(usern))
                user = cursor.fetchall()
                cursor.execute(sql2 , (passwo))
                passw = cursor.fetchall()
                if not user:
                    flag1=False
                if not passw:
                    flag2=False
                if flag1==True and flag2==True:
                    # print('aaaaaaaaa')
                    return redirect(url_for('loggedin' , name = usern))
        except Exception as e:
            print(e)
    return render_template('login.html')

@app.route('/loggedin/<name>' ,methods = ['POST' , 'GET'])
def loggedin(name):
    if request.method == 'POST':
        normal_demand = request.form['normal_demand']
        if normal_demand == 'normal_yes':
            return redirect(url_for('normal_demand' , name = name))
    return render_template('index.html')


# @app.route('/signup',methods=['POST' , 'GET'])
# def sigUP():
#     return render_template('signup.html')

@app.route('/signup',methods=['POST' , 'GET'])
def signup():
    if request.method == 'POST':
        name_of_hospital = request.form['name_of_hospital']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        password = request.form['password']
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO signup (name_of_hospital,address_line1,address_line2,city,state,pincode,mobile_number,email,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (name_of_hospital,address_line1,address_line2,city,state,pincode,mobile_number,email,password))
                connection.commit()
                return redirect(url_for('signup_page2'))
        except Exception as e:
            print(e)
        
    return render_template('signup.html')

@app.route('/signup_page2' ,methods = ['POST','GET'])
def signup_page2():
    if request.method == 'POST':
        name_of_medical_superintendent = request.form['name_of_medical_superintendent']
        registration_number = request.form['registration_number']
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO signup_page2 (name_of_medical_superintendent,registration_number) VALUES (%s,%s)"
                cursor.execute(sql ,(name_of_medical_superintendent,registration_number))
                connection.commit()
                return redirect(url_for('signup_page3'))
        except Exception as e:
            print(e)
    return render_template('signup_page2.html')

@app.route('/signup_page3' ,methods = ['POST' , 'GET'])
def signup_page3():
    if request.method == 'POST':
        name_of_cmo = request.form['name_of_cmo']
        no_of_doctors = request.form['no_of_doctors']
        no_of_beds = request.form['no_of_beds']
        no_of_patients = request.form['no_of_patients']
        no_of_PCR_machines = request.form['no_of_PCR_machines']
        no_of_Ventilators = request.form['no_of_Ventilators']
        status = request.form['status']
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO signup_page3 (name_of_cmo,no_of_doctors,no_of_beds,no_of_patients,no_of_PCR_machines,no_of_Ventilators,status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql , (name_of_cmo,no_of_doctors,no_of_beds,no_of_patients,no_of_PCR_machines,no_of_Ventilators,status))
                connection.commit()
                return redirect(url_for('signup_page4'))
        except Exception as e:
            print(e)
    return render_template('signup_page3.html')

@app.route('/signup_page4',methods=['POST', 'GET'])
def signup_page4():
    if request.method == 'POST':
        print('aa')
        return redirect(url_for('loginup'))
    return render_template('signup_page4.html')

@app.route('/<name>/normal_demand' , methods = ['POST' , 'GET'])
def normal_demand(name):
    return render_template('normal_demand.html' )

if __name__ == "__main__":
    app.run(debug=True)
        