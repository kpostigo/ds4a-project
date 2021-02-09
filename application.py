from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import static.scripts.utils as util

application = Flask(__name__,template_folder='./templates', static_folder='./static')

school_list = []
school_db = pd.read_csv('./db/school_list.csv')
data = ''
results = False

@application.route('/', methods=['POST', 'GET'])
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
		if results:
			return render_template("index.html", schoolList=school_list, tableData=data)
		else:
			return render_template("index.html", schoolList=school_list)

@application.route('/about')
def about():
	return render_template("about.html")

@application.route('/clear', methods=['POST'])
def clear():
	# clear list if schools
	school_list.clear()
	# clear table...
	results = False
	return redirect(url_for('home', schoolList=school_list))

@application.route('/results', methods=['POST'])
def results():
	if school_list:
		results = True
		# GET INPUTS
		tWeight = int(request.form['tuitionWeight'])
		gWeight = int(request.form['graduationWeight'])
		eWeight = int(request.form['employmentWeight'])
		# GENERATE TABLE
		# - gather data from db
		query_db = school_db[school_db["INSTNM"].isin(school_list)]
		# - rank schools
		query_db = util.rank_schools(query_db, tWeight, gWeight, eWeight)
		return render_template("index.html", schoolList=school_list, tableData=query_db.to_dict(orient="records"))
	# UPDATE PAGE
	return redirect(url_for('home'))

if __name__ == "__main__":
	app.run(debug=False)
