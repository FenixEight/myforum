import random
from flask import Flask, request, session, redirect, url_for

from myforum import app, User
from myforum.lib.template import render


@app.route('/')
def home():
	comments = app.db.comment.get_all()
	return render('home', comments=comments)


@app.route('/signup')
def signup():
	return render('signup')


@app.route('/signin')
def signin():
	if request.method == 'POST':
		pass
	else:
		return render('signin')


@app.context_processor
def inject_build_num():
    return dict(buildNum=random.randint(1, 123456))
