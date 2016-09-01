import random
from string import ascii_letters, digits
from flask import request, session, redirect, url_for, flash
from myforum import app
from myforum.lib.template import render


@app.route('/')
@app.route('/page<int:page>')
def home(page=1):
    if 'username' not in session:
        return render('home')
    username = session['username']
    u = app.db.user.get_username_by_name(username)

    posts, pages = app.db.post.get_all_posts(page=page, id=u.id)
    if posts:
        for i in range(len(posts)):
            posts[i].tags = app.db.tag.get_tags_by_post_id(posts[i].post_id)
    return render('home', posts=posts, page=page, pages=pages)


@app.route('/tag/<tag>/page<int:page>')
def tag(tag, page=1):
    t = app.db.tag.search_tag(tag)
    if not t:
         return render('tag', tag = tag)
    posts, pages = app.db.post.get_posts_by_tag(t.tag_id, page)
    return render('tag', page=page, posts=posts, pages=pages)

@app.route('/ban/<username>', methods=['POST', 'GET'])
def ban(username):
    if request.method == 'POST':
        current_user = app.db.user.get_username_by_name(session['username'])
        u = app.db.user.get_username_by_name(username)
        if request.form.get('button_1', '') == 'Ban user':
            app.db.admin.ban_user(u.id)
        if request.form.get('button_2', '') == 'Unban user':
            app.db.admin.unban_user(u.id)
        if request.form.get('button_3', '') == 'Remove from blacklist':
            app.db.admin.remove_from_blacklist(current_user.id, u.id)
        if request.form.get('button_4', '') == 'Add to blacklist':
            app.db.admin.add_to_blacklist(current_user.id, u.id)
    return redirect(url_for('user', username=username, page=1))

@app.route('/admin/page<int:page>', methods=['POST', 'GET'])
@app.route('/admin', methods=['GET', 'POST'])
def admin(page=1):
    if request.method == 'POST':

        if request.form.get('button_1', '') == 'Switch off':
            app.db.admin.mod_off()
        if request.form.get('button_2', '') == 'Switch on':
            app.db.admin.mod_on()

        return render('admin', page=page)
    else:
        posts, pages = app.db.post.posts_for_moderation(page)
        if posts:
            for i in range(len(posts)):
                posts[i].tags = app.db.tag.get_tags_by_post_id(posts[i].post_id)
        return render('admin', page=page, pages=pages, posts=posts)


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
    if not app.db.user.get_username_by_name(username):
        flash('Wrong page')
        return redirect(url_for('home'))
    blacklist = 'current'
    u = app.db.user.get_username_by_name(username)
    if username != session['username']:
        current_user = app.db.user.get_username_by_name(session['username'])
        if app.db.admin.blacklist_status(current_user.id,u.id):
            blacklist = True
        else:
            blacklist = False
    posts, pages = app.db.post.get_user_posts(page, u.id)
    return render('user', posts=posts, pages=pages, page=page, username=username, admin_mod=u.admin_mod, blacklist=blacklist)


@app.context_processor
def inject_build_num():
    is_auth = 'username' in session
    current_user = None
    if is_auth:
        current_user = app.db.user.get_username_by_name(session['username'])
    moderation = False
    status = app.db.admin.mod_status()
    if status == 'on':
        moderation = True
    print(is_auth)
    return dict(buildNum=random.randint(1, 123456), moderation=moderation,
                is_auth=is_auth, current_user=current_user)
