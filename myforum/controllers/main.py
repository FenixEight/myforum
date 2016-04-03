import random
from flask import Flask, request, session, redirect, url_for

from myforum import app
from myforum.lib.template import render


@app.route('/')
def home():
	comments = app.db.comment.get_all()
	return render('home', comments=comments)

@app.route('/signup')
def signup():
	return render('signup')


@app.context_processor
def inject_build_num():
    return dict(buildNum=random.randint(1, 123456))
