# -*- coding: utf-8 -*-
# !/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import sys
import contextlib

app = Flask(__name__)
app.debug = True
app.secret_key = 'development key'


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/crash')
def main():
    raise Exception()


@app.route('/verifycode', methods=['GET', 'POST'])
def verifycode():

	if request.method == 'POST':
		print (request.form['code'])

		code = compile(request.form['code'], "script", "exec")
		ns = {}
		codeoutput = ''
		try:		
			with stdoutIO() as s:
				exec(code)
			codeoutput = s.getvalue()
		except:
			codeoutput = 'Code does not work!'
		
		return render_template("verifycode.html", codeoutput = codeoutput)
		# return 'your code does not work'
	else:
		return redirect(url_for('homepage'))


if __name__ == "__main__":
    app.run(debug=True)



