from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', left_data="", right_data="")

@app.route('/transfer_left_to_right', methods=['POST'])
def transfer_left_to_right():
    left_data = request.form.get('leftData', '')
    right_data = request.form.get('rightData', '')
    return render_template('index.html', left_data="", right_data=right_data + left_data)

@app.route('/transfer_right_to_left', methods=['POST'])
def transfer_right_to_left():
    left_data = request.form.get('leftData', '')
    right_data = request.form.get('rightData', '')
    return render_template('index.html', left_data=left_data + right_data, right_data="")

@app.route('/transfer_left_button', methods=['POST'])
def transfer_left_button():
    left_data = request.form.get('leftData', '')
    right_data = request.form.get('rightData', '')
    return render_template('index.html',  right_data=left_data, left_data="")

@app.route('/transfer_right_button', methods=['POST'])
def transfer_right_button():
    left_data = request.form.get('leftData', '')
    right_data = request.form.get('rightData', '')
    return render_template('index.html', left_data=right_data, right_data="")

if __name__ == '__main__':
    app.run(debug=True)
