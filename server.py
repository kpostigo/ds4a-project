from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import static.scripts.utils as util

app = Flask(__name__,template_folder='./templates', static_folder='./static')

school_list = []
school_db = pd.read_csv('./db/school_list.csv')

@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == 'POST':
		school = request.form['school_name']
		# check if school is in db...
		idx = school_db['INSTNM'].str.contains(school)
		idx = idx[idx].index
		# pick first school if more than one match
		if len(idx) > 1:
			idx = idx[0]
		if idx != -1:
			school = str(school_db['INSTNM'].values[idx]).strip('\'[]')
			if school not in school_list:
				school_list.append(school)
		return redirect(url_for('home'))
	else:
		# print(school_list)
		return render_template("index.html", schoolList=school_list)

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/clear', methods=['POST'])
def clear():
	# clear list if schools
	school_list.clear()
	# clear table...
	return redirect(url_for('home', schoolList=school_list))

@app.route('/results', methods=['POST'])
def results():
	if school_list:
		# GET INPUTS
		tWeight = int(request.form['tuitionWeight'])
		gWeight = int(request.form['graduationWeight'])
		eWeight = int(request.form['employmentWeight'])
		# GENERATE TABLE
		# - gather data from db
		query_db = school_db[school_db["INSTNM"].isin(school_list)]
		# - rank schools
		query_db = util.rank_schools(query_db, tWeight, gWeight, eWeight)
		# put data into a dict
		data = []
		for item in query_db:
			dict_item = {item['INSTNM'], item['TUITIONFEE_IN']}
			data.append(dict_item)
		print(data)
		# UPDATE PAGE
		return redirect(url_for('home', tableData=query_db))
	return redirect(url_for('home'))

if __name__ == "__main__":
	app.run(debug=True)