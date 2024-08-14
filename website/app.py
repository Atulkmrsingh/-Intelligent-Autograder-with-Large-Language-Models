from flask import Flask, render_template, request
from index import return_response
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission
    question = request.form['question']
    answer = request.form['answer']
    pdf_file = request.files['pdf']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(file_path)

    response, top_sentences = return_response(question, answer, file_path)

    return render_template('response.html', question=question, answer=answer, response=response, top_sentences=" ".join([top_sentences[0][0], top_sentences[1][0], top_sentences[2][0], top_sentences[3][0], top_sentences[4][0]]))

if __name__ == '__main__':
    app.run(debug=True)
