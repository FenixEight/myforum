import random
import datetime
from flask import Flask, request, session, redirect, url_for, flash

from myforum import app
from myforum.lib.template import render
from myforum.model import Post

def get_post(req):
	c = Post()
	c.post = req.form['comment_text']
	c.date_time = datetime.datetime.now()
	c.user_agent = req.headers.get('User-Agent')
	c.ip = req.remote_addr
	u = app.db.user.get_username_by_name(session['username'])
	c.user_id = u.id
	return c

@app.route('/comments/add', methods=['POST'])
def add_comment():
	if request.method == 'POST':
		c = get_post(request)
		if len(c.post) < 6:
			flash('Too short message')
			return render('home')
		app.db.post.add_post(c)
		return redirect(url_for('home'))

@app.route('/comments/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_comment(post_id):
	if request.method == 'POST':
		c = get_post(request)
		c.post_id = post_id
		if len(c.post) < 6:
			flash('Too short message')
			return render('edit_comment', c=c)
		app.db.post.update_post(c)
		return redirect(url_for('home'))
	else:
		post = app.db.post.get_by_id(post_id)
		return render('edit_comment', c=post)

@app.route('/comments/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_comment(post_id):
	if request.method == 'POST':
		app.db.post.delete_post(post_id)
		return redirect(url_for('home'))
	else:
		return render('delete_comment', post_id=post_id)


