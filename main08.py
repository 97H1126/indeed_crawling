from flask import Flask,render_template,request,redirect, send_file #render_template 함수는 웹 어플리케이션에서 사용할 HTML 파일을 렌더링하여, 클라이언트(웹 브라우저)에게 보여줍니다.  Flask에서 제공하는 함수 중 하나
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_job
from file import save_to_file

app = Flask("JobScrapper")
# app.run("0.0.0.0")

#웹을 빠르게 동작하기 위해 가짜 데이터베이스를 만든다 한번 검색한거 저장했다 다시 보여주는방식을 사용하기 위해서 / 서버가 중단시키면 가짜기 때문에 없어짐
db = {}

#유저가 홈페이지로 접속하면 페이지를 보여주게 하는것
@app.route("/") # 이부분은 무조건 함수 바로 위에 있어야한다!! @ = 데코레이터 를 이용하여 라우팅 경로를 설정하고 .route를 사용하여 경로를 처리하는 함수를 등록한다. "/"는 루트 경로를 의미하며 즉 웹 어플리케이션의 홈 페이지를 나타낸다
def home():
    return render_template("home.html", name="homin") # templates폴더 안에 있는 html파일 이름을 넣는다 , name 변수를 왼쪽에 있는 home.html 에 넘겨준다 
#그럼 그파일 안에서 같은 이름의 변수(name)에 넣고 render_template로 HTML 파일을 동적으로 생성하고, Flask 애플리케이션에서 사용할 수 있는 데이터를 HTML에 삽입하는 역할을 한다. 
# 위의 방식을 통해서 페이지에 들어온 유저에게 보여주는데 이것을 렌더링이라고 한다.

@app.route("/search") #127.0.0.1:5000/hello로 검색하면 이동한다
def search():
    keyword = request.args.get("keyword")
    if keyword =="": 
        return redirect("/")
    if keyword in db:
        jobs =db[keyword]
    else : 
        indeed = extract_indeed_jobs(keyword)
        wwr = extract_wwr_job(keyword)
        jobs = indeed + wwr
        db[keyword] = jobs
    return render_template("search.html",keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword =="":      # 사용자가 검색한 내용이 없다면 홈페이지로 다시 돌려준다
        return redirect("/")
    if keyword not in db: 
        return redirect(f"/search?keyword={keyword}")
    # 파일을 저장하기 위해서 파일을 만들어주는 file 함수를 불러와서 사용하고 flask에서 import send_file 해준다
    save_to_file(keyword , db[keyword]) # 키워드는 파일이름이 되고 db는 검색한 자료가 됨
    return send_file(f"{keyword}.csv", as_attachment=True) # 파일이름.csv로 저장된다 / 저장하기 위해서  as_attachment=True를 사용한다


app.run("127.0.0.1", port=5000) #.run은 로컬서버를 실행시키며 사용할 서버의 주소를 넣어준다. #http 창에서 127.0.0.1:5000을 검색하면 유저 홈페이지를 볼 수 있음
