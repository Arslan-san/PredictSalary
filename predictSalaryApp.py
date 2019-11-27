from flask import Flask, render_template, url_for, request, flash, redirect
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, '') 

import pickle
import numpy as np
model = pickle.load(open('salaryPrediction.pkl', 'rb'))


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route('/', methods = ['POST','GET'])
# @app.route('/home', methods = ['POST', 'GET'])
def home():
	if request.method == 'POST':


		feature_names = ['experience', 'test_score', 'interview_score']
		features_values = [request.form[name] for name in feature_names]

		if int(features_values[0]) < 0 or int(features_values[0]) > 15:
			flash("Experience must be in between 0 and 15", "danger")
			return redirect(url_for('home'))

		elif int(features_values[1]) < 1 or int(features_values[1]) > 10:
			flash("Test score must be in between 1 and 10", "danger")
			return redirect(url_for('home'))

		elif int(features_values[2]) < 1 or int(features_values[2]) > 10:
			flash("Interview score must be in between 1 and 10", "danger")
			return redirect(url_for('home'))


		prepared_features_for_model = np.asarray(features_values, dtype=np.int64)
		prediction = model.predict([prepared_features_for_model])

		predicted_salary = '{:n}'.format(int(prediction[0]))
		return render_template('home.html', predicted_salary= predicted_salary)
	
	elif request.method == 'GET':
		return render_template('home.html')

if (__name__) == '__main__':
	app.run(debug=True)