import datetime
from flask import request, session, redirect, url_for, flash
from myforum import app
from myforum.lib.template import render
from myforum.model import Comment


@app.route('/comment/add/<int:post_id>/<int:parent_id>', methods=['POST'])
def add_comment(post_id, parent_id):
    comment = Comment()
    comment.post_id = post_id
    comment.parent_id = parent_id
    comment.date = datetime.datetime.now()
    comment.comment_text = request.form['comment_text']
    comment.user_id = app.db.user.get_username_by_name(session['username']).id
    app.db.comment.add_comment(comment)
    return redirect(request.referrer)

@app.route('/comment/delete/<int:id>')
def delete_comment(id):
    app.db.comment.delete_comment(id, app.db.user.get_username_by_name(session['username']).id)
    return redirect(request.referrer)