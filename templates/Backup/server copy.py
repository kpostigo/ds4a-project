from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/results', methods=['POST', 'GET'])
def results():
	if request.method == "POST":
		school_name = request.form['school_name']
		return redirect(url_for('schoolaction', school=school_name))
	else:
		return redirect(url_for('home'))

@app.route('/school/<school>')
def schoolaction(school):
	return f"School name entered: {school}"

if __name__ == "__main__":
	app.run(debug=True)