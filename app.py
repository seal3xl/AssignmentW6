from flask import Flask,render_template,request,redirect,session
import pymysql

app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)

#連線到MySQL資料庫。
db=pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    passwd="1234",
    db="website",
    charset='utf8'
)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #Secret Key

#首頁
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup",methods=["POST"])
def signup():
    na=request.form["na"] #前端網頁輸入的姓名。
    ac=request.form["ac"] #前端網頁輸入的帳號。
    ps=request.form["ps"] #前端網頁輸入的密碼。
# 註冊資料不能為空白：
    if na=="" or ac=="" or ps=="":
        return redirect("/error?message=姓名、帳號、密碼：不得為空白")
    else:
# 檢查帳號是否被註冊過：
        cursor=db.cursor()
        command="select username from user where username=\""+ac+"\";"
        cursor.execute(command)
        usernames=cursor.fetchall()
# 若帳號未備註冊，完成註冊，記錄到user表。
        if usernames==():
            command_add="insert into user (name,username,passward) values(%s,%s,%s);"
            cursor.execute(command_add,(na,ac,ps))
            db.commit()
            return redirect("/")
# 若帳號已被註冊，導向錯誤頁面，提示"帳號已經被註冊"。
        else:
            return redirect("/error?message=帳號已經被註冊")


#登入連線：輸入帳號密碼，如果與userData的資料吻合，將使用者記錄到session，並登入到member頁面。（登入失敗轉到登入失敗頁面。）
@app.route("/signin",methods=["POST"])
def signin():
    ac=request.form["ac"] #前端網頁輸入的帳號。
    ps=request.form["ps"] #前端網頁輸入的密碼。
# 登入資料不能為空白：
    if ac=="" or ps=="":
        return redirect("/error?message=帳號、密碼：不得為空白")
# 檢查輸入的帳號密碼是否正確：    
    else:
        cursor=db.cursor()
        command="select username,passward from user where username=\""+ac+"\" and passward=\""+ps+"\";"
        cursor.execute(command)
        userData=cursor.fetchall()
# 若帳號密碼錯誤，導向錯誤頁面，提示"帳號或密碼輸入錯誤"。
        if userData==():
            return redirect("/error?message=帳號或密碼輸入錯誤")
# 若帳號密碼正確，將使用者帳號ac加入session中，並導向會員頁。
        else:
            session["ac"]=request.form["ac"]

            return redirect("/member")


#會員頁面：先檢查使用者是否有在session裡面，有就帶出member頁面，沒有就轉到登入失敗頁面。
@app.route("/member/")
def member():
    if "ac" in session:
        ac=session["ac"]
# 從user表中，找到對應的名字，並顯示在網頁上。
        cursor=db.cursor()
        command="select name from user where username=\""+ac+"\";"
        cursor.execute(command)
        name=cursor.fetchall()
        name=name[0][0]

        return render_template("member.html",name=name)
    else:
        return redirect("/howdare")

#登入失敗頁面
@app.route("/error")
def error():
    errorType=request.args.get("message",None)
    return render_template("error.html",message=errorType)




#登出：將使用者帳號從session中移除，並導入首頁。
@app.route("/signout")
def signout():
    ac=session["ac"]
    session.pop("ac",None)
    return redirect("/")

#登入失敗頁面2
@app.route("/howdare")
def howdare():
        return render_template("howdare.html")


app.run(port=3000)