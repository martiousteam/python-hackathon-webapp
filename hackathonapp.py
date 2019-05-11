# -*- coding: utf-8 -*-
# !/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
from forms import CodeForm, ResultForm
from exec_untrusted import exec_untrusted

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def homepage():
    code_form = CodeForm(request.form)
    result_form = ResultForm(request.form)

    app.logger.info(request.method)

    if request.method == 'POST' and code_form.validate() and code_form.code_submit.data:
        code_str = code_form.code_text.data
        result_text = exec_untrusted(code_str)
        result_form.result_text.data = result_text

    return render_template('index.html', code_form=code_form, result_form=result_form)


@app.route('/crash')
def main():
    raise Exception()


if __name__ == "__main__":
    app.secret_key = app.config['SECRET_KEY']
    app.run(debug=app.config['DEBUG'])
