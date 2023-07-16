from flask import Flask,redirect,url_for,render_template,request,session
import ibm_db

app=Flask("__name__")

conn=ibm_db.connect('DATABASE=bludb; HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; PORT=32304; UID=xrs30327;PWD=5Fljv8ohuf1m9iMH; SECURITY=SSL;SSLCertificate=DigiCertGlobalRootCA.crt','','')
print(conn)
connState=ibm_db.active(conn)
print(connState)
app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login",methods=['GET','POST'])
def login():
    global uemail
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        sql="SELECT * FROM REGISTER where EMAIL=? and PASSWORD=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)  
        print(acc)
        if acc:
            session['email']=email
            uemail=session['email']
            name=acc['FULLNAME']
            return render_template("display.html",name=name)
        else:
            msg="invalid credentials"
            return render_template("login.html",msg=msg)
        
    return render_template("login.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST":
        name=request.form['fullname']
        email=request.form['email']
        password=request.form['password']
        details=[name,email,password]
        print(details)
        sql="SELECT * FROM REGISTER where EMAIL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)    
        print(acc)
        if acc:
            msg="you have been already registered, pls login!"
            return render_template("login.html",msg=msg)
        else:
            sql="INSERT INTO REGISTER VALUES(?,?,?)"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.bind_param(stmt,2,name)
            ibm_db.bind_param(stmt,3,password)
            ibm_db.execute(stmt)  
            msg="you have successsfully registred , pls login!"        
            return render_template("login.html",msg=msg)
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("email",None)
    return redirect("/login")




if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
