# -*- coding: utf-8 -*-
# !/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
from forms import CodeForm, ResultForm
from stdio import stdoutIO

app = Flask(__name__)
app.debug = True
app.secret_key = 'development key'


@app.route('/', methods=['GET', 'POST'])
def homepage():
	code_form = CodeForm(request.form)
	result_form = ResultForm(request.form)

	app.logger.info(request.method)

	if request.method == 'POST' and code_form.validate() and code_form.code_submit.data:

		code_str = code_form.code_text.data

		with stdoutIO() as s:
			try:
				code = compile(code_str, "script", "exec")
				exec(code)
				result_form.result_text.data = s.getvalue()
			except:
				app.logger.info("I am in exception")
				result_form.result_text.data = 'Code does not work!'

	return render_template('index.html', code_form=code_form, result_form=result_form)


@app.route('/crash')
def main():
	raise Exception()


if __name__ == "__main__":
	app.run(debug=True)
