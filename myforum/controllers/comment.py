import random
from flask import Flask, request, session, redirect, url_for

from myforum import app
from myforum.lib.template import render
from myforum.model import Comment

def get_comment(p):
	c = Comment()
	c.user_name = p['user_name']
	c.comment_text = p['comment_text']
	return c

@app.route('/comments/add', methods=['POST'])
def add_comment():
	if request.method == 'POST':

		c = get_comment(request.form)
		app.db.comment.add(c)
		return redirect(url_for('home'))

@app.route('/comments/edit/<int:comment_id>', methods=['GET', 'POST'])
def edit_comment(comment_id):
	if request.method == 'POST':
		c = get_comment(request.form)
		c.id = comment_id
		app.db.comment.update(c)
		return redirect(url_for('home'))
	else:
		comment = app.db.comment.get_by_id(comment_id)
		return render('edit_comment', comment=comment)


@app.route('/comments/delete/<int:comment_id>', methods=['GET', 'POST'])
def delete_comment(comment_id):
	if request.method == 'POST':
		app.db.comment.delete(comment_id)
		return redirect(url_for('home'))
	else:
	    return render('delete_comment',comment_id=comment_id)


