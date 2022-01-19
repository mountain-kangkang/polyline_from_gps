from flask import Flask, render_template, request
import webbrowser
import csv
import os

app = Flask(__name__)
webbrowser.open("http://127.0.0.1:5500/")

data = ["num", "A", "Lat", "Lng", "B", "C", "D", "E", "F"]                      # tag가 없는 csv(GPS)에 붙일 tag 준비

@app.route('/')                                                                 # 기본 화면("basicMap.html") open
def basic():
    return render_template("basicMap.html")

@app.route('/mapping', methods = ['POST'])                                      # 기본 화면 및 경로 표시 화면에서 제출한 파일을 객체로 받아 옴
def upload_file():

    for file in os.scandir('./static/GPS/'):
        os.remove(file.path)

    # for file in os.scandir('./GPS/'):
    #     os.remove(file.path)

    if request.method == 'POST':
        fileDown = request.files.getlist('file[]')                              # 파일을 변수에 저장

        for f in fileDown:
            f.save('./X/' + f.filename)                                       # JS(JavaScript)에서 절대경로를 알아낼 방법이 없어 원하는 경로에 파일을 저장(상대 경로로 파일을 편집하고 사용하기 위함) 
            f.close()
                                                                                # csv파일에 key값이 없으면 읽어오기 힘이듭니다.
            p =  open('./X/' +f.filename, "r", encoding="UTF-8")              # 제출되어 저장된 파일을 open
            rdr = csv.reader(p)                                                 # open한 csv를 읽을 준비

            fn = f.filename[4:]

            s = open('./static/GPS/'+fn, 'w', newline='', encoding='UTF-8')     # 비어있는 csv를 "newFile"에 저장된 경로와 이름으로 파일 생성
            wr = csv.writer(s)                                                  # 비어있는 csv에 쓸 준비
            wr.writerow(data)                                                   # 준비한 tag 먼저 write

            for row in rdr:                                                     # tag가 없는 csv를   tag만 붙인 빈 csv에 행별로 삽입(자동 저장)
                wr.writerow(row)
            
            ti = int(f.filename[4:12])
            da = int(f.filename[13:19])
            td = [ti, da]
            wr.writerow(td)

            p.close()                                                           # 읽고 쓰기 위하여 open한 csv들 close
        s.close()
        return render_template("testMapping.html")                              # 경로 표시할 화면("mapping.html")으로 open한 파일명 전달하며 이동

@app.route('/direct')
def directHTML():
    return render_template("testMapping.html")


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)                                          # localhost:5500(127.0.0.1:5500)으로 웹서버 open
 