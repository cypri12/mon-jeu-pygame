from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    # Exécuter le script test.py
    result = subprocess.run(['python3', 'test.py'], capture_output=True, text=True)
    return f"<pre>{result.stdout}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
