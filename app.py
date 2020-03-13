# Flask : Untuk membuat API
# render_template : Memungkinkan API memberikan respon berupa HTML
# render_template secara otomatis akan mencari folder 'templates'
# request : Untuk menerima data yang dari kirim dari browser
from flask import Flask, render_template, request

app = Flask(__name__)

# Home
@app.route('/')
def index():
    return '<h1> Hello Flask ~ </h1>'

@app.route('/base')
def base():
    return render_template('base.html')

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

























# Saat kita running file app.py maka variable __name__ akan berisi string 'main'
if __name__ == '__main__' :
    # debug = True memiliki dua efek :
    # 1. Setiap kita memperbaharui kode, api akan restart secara otormatis
    # 2. Memungkinan menampilkan pesan error di browser sehingga mudah dibaca
    app.run(debug=True)