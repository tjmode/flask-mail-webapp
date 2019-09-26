from flask import Flask,session,render_template,request,redirect
from flask_mysqldb import MySQL
import MySQLdb
import os

app=Flask(__name__)
app.secret_key=os.urandom(23)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='mark'
mysql=MySQL(app)

@app.route('/' ,methods=['GET','POST'])
def maillogin():
	if request.method=="POST":
		d=request.form
		email=d['email']
		session['email']=email
		conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mark")
		cur=conn.cursor()
		#cur.execute("INSERT  INTO test(email,password) VALUES(%s,%s)",(email,password))
		cur.execute("select*from mail")
		conn.commit()
		r=cur.fetchall()
		k=list(r)
		c=0
		for i in k:
			print(i[0],email)
			if i[0]== email:
				c=c+1
		print(c)
		if c>1:
			return redirect('/mailbox')
		else:
			return "its an worng mail-id" 
	return render_template("mail-login.html")
@app.route('/mailbox' , methods=['GET','POST'])
def mailbox():
	if request.method=="POST":
		d1=request.form
		revicermailid=d1['revicermailid']
		msg=d1['msg']
		if 'email' in session:
			email=session['email']
		conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mark")
		cur=conn.cursor()
		cur.execute("update mail set send=%s where name=%s",[msg,email])
		cur.execute("update mail set revice=%s where name=%s",[msg,revicermailid])
		conn.commit()
		return render_template("send.html",msg=msg,revicermailid=revicermailid,email=email)
	return render_template("mailbox.html")
if __name__ == '__main__':
	app.run(debug=True)