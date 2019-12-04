from flask import Flask, render_template, url_for, request, flash, redirect
from platform import python_version
import numpy as np
import pickle
import locale

locale.setlocale(locale.LC_ALL, '') 

python_ver = int((python_version()).split('.')[0])


if python_ver == 2:
	# for python version 2
	multiple_features_model = pickle.load(open('salaryPrediction_with_multiple_features.pkl', 'rb'))
	one_feature_model = pickle.load(open('salaryPrediction_with_one_feature.pkl', 'rb'))
elif python_ver == 3:
	# for python version 3
	with open("salaryPrediction_with_multiple_features.pkl", 'rb') as f:
	    multiple_features_model = pickle.load(f, encoding="latin1")
	
	with open("salaryPrediction_with_one_feature.pkl", 'rb') as g:
	    one_feature_model = pickle.load(g, encoding="latin1")

	

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/salary-prediction-with-multiple-features', methods = ['POST','GET'])
def prediction_with_multiples():
	if request.method == 'POST':

		feature_names = ['experience', 'test_score', 'interview_score']
		features_values = [float(request.form[name]) for name in feature_names]

		if (features_values[0]) < 0:
			flash("Experience must be greater than zero", "danger")
			return redirect(url_for('prediction_with_multiples'))

		elif (features_values[1]) < 1 or (features_values[1]) > 10:
			flash("Test score must be in between 1 and 10", "danger")
			return redirect(url_for('prediction_with_multiples'))

		elif (features_values[2]) < 1 or (features_values[2]) > 10:
			flash("Interview score must be in between 1 and 10", "danger")
			return redirect(url_for('prediction_with_multiples'))


		prepared_features_for_model = np.asarray(features_values, dtype=np.int64)
		prediction = multiple_features_model.predict([prepared_features_for_model])

		predicted_salary = '{:n}'.format(int(prediction[0]))
		return render_template('prediction_with_multiples.html', predicted_salary= predicted_salary)
	
	elif request.method == 'GET':
		return render_template('prediction_with_multiples.html')

@app.route('/salary-prediction-with-one-feature', methods = ['POST','GET'])
def prediction_with_one():
	if request.method == 'POST':

		feature_name = ['experience']
		feature_value = [float(request.form[name]) for name in feature_name]

		# we have to convert this single feature value, which is experience, into 7th polynomial degree

		#prepared_features_for_model = [double(feature_value[0])**i for i in range(1,8)]



		if (feature_value[0]) < 0:
			flash("Experience must be greater than zero", "danger")
			return redirect(url_for('prediction_with_one'))

		prediction = one_feature_model.predict([feature_value])
		predicted_salary = '{:n}'.format(int(prediction[0]))
		return render_template('prediction_with_one.html', predicted_salary= predicted_salary, experience=feature_value[0])
	
	elif request.method == 'GET':
		return render_template('prediction_with_one.html')

if (__name__) == '__main__':
	app.run(debug=True)