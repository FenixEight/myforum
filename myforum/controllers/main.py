import random
from string import ascii_letters, digits
from flask import request, session, redirect, url_for, flash
from myforum import app
from myforum.lib.template import render


def get_user(name):
    return app.db.user.get_username_by_name(name)

@app.route('/')
@app.route('/page<int:page>')
def home(page=1):
    posts, pages = app.db.post.get_posts(page=page)
    return render('home', posts=posts, page=page, pages=pages)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    superstring = ascii_letters + digits + '_'
    if request.method == 'POST':
        name = request.form['user_name']
        password = request.form['password']
        u = app.db.user.get_username_by_name(name)
        if not u:
            if len(name) < 6:
                flash('too short username')
                return render('signup')
            if len(password) < 6:
                flash('password is too short')
                return render('signup')
            for i in name:
                if i not in superstring:
                    flash('Only A-Z, 0-9 and _ ')
                    return render('signup')
            app.db.user.add_username(name, password)
            session['username'] = name
            return redirect(url_for('home'))
        if u.username == name:
            flash('Already exist')
            return render('signup')
    else:
        return render('signup')

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        name = request.form['user_name']
        user = app.db.user.get_username_by_name(name)
        if not user:
            flash("Incorrect login or password")
            return render('signin')
        if user.username == name:
            if user.password == request.form['password']:
                session['username'] = name
                if request.form.get('rememberme') is not None:
                    session.permanent = True
                return redirect(url_for('home'))
            else:
                flash("Incorrect login or password")
                return render('signin')
    else:
        return render('signin')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/<username>/posts/page<int:page>')
def user(username, page):
    u = get_user(username)
    posts, pages = app.db.post.get_posts(page, u_id=u.id)
    return render('user', posts=posts, pages=pages, page=page, username=username)

@app.context_processor
def inject_build_num():
    is_auth = 'username' in session
    current_user = None
    if is_auth:
        current_user = app.db.user.get_username_by_name(session['username'])
    return dict(buildNum=random.randint(1, 123456), is_auth=is_auth, current_user=current_user)
