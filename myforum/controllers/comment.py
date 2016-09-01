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
    c.status = 'approved'
    if app.db.admin.mod_status() == 'on':
        c.status = 'waiting'
    if u.admin_mod == 1:
        c.status = 'approved'
    return c


@app.route('/comments/add', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        c = get_post(request)
        tags_str = request.form['tags']
        tags = tags_str.split(' ')
        tags = list(set(tags))
        if '' in tags:
            tags.remove('')
        if len(c.post) < 6:
            flash('Too short message')
            return render('home')
        if not tags:
            flash('One tag minimum')
            return redirect(url_for('home'))
        for t in tags:
            if len(t) > 32:
                flash('Max tag length 32')
                return redirect(url_for('home'))

        post_id = app.db.post.add_post(c)
        for t in tags:
            app.db.tag.add(t, post_id)
        return redirect(url_for('home'))


@app.route('/comments/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_comment(post_id):
    if request.method == 'POST':
        c = app.db.post.get_by_id(post_id)
        c.post = request.form['comment_text']
        c.date_time = datetime.datetime.now()
        c.user_agent = request.headers.get('User-Agent')
        c.ip = request.remote_addr
        if len(c.post) < 6:
            flash('Too short message')
            return render('edit_comment', c=c)
        tags_str = request.form['tags']
        tags = tags_str.split(' ')
        tags = list(set(tags))
        if '' in tags:
            tags.remove('')
        for t in tags:
            if len(t) > 32:
                flash('Max tag length 32')
                return redirect(url_for('home'))
        app.db.tag.delete_links(post_id)
        for t in tags:
            app.db.tag.add(t, post_id)
        u = app.db.user.get_username_by_name(session['username'])
        c.status = 'approved'
        print
        if app.db.admin.mod_status() == 'on':
            c.status = 'waiting'
        if u.admin_mod == 1:
            c.status = 'approved'
        app.db.post.update_post(c, u.id, u.admin_mod)
        return redirect(url_for('home'))
    else:
        tags = app.db.tag.get_tags_by_post_id(post_id)
        tags_list = []
        for t in tags:
            tags_list.append(t.tag)
        tag_string = ' '.join(tags_list)
        post = app.db.post.get_by_id(post_id)
        return render('edit_comment', c=post, tag_string=tag_string)


@app.route('/comments/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_comment(post_id):
    if request.method == 'POST':
        if 'username' in session:
            u = app.db.user.get_username_by_name(session['username'])
            app.db.tag.delete_links(post_id)
            app.db.post.delete_post(post_id, u.id, u.admin_mod)
            return redirect(url_for('home'))
    else:
        p = app.db.post.get_by_id(post_id)
        return render('delete_comment', p=p)


@app.route('/admin/moderation/<int:post_id>', methods=['POST'])
def moderation(post_id):
    if request.form.get('button_1', '') == 'Approve':
            app.db.admin.approve_post(post_id)
    if request.form.get('button_2', '') == 'Cancel':
        app.db.admin.cancel_post(post_id)
    return redirect(url_for('admin'))
