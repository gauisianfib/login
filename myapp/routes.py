from flask import request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

def init_routes(app, db):
    @app.route('/')
    def home():
        username = session.get('username')
        return render_template('home.html', username=username)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # 🔥 ここでエラーが発生していた部分 🔥
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password_hash, password):
                session['username'] = username
                flash('ログイン成功！', 'success')
                return redirect(url_for('home'))
            flash('ユーザー名またはパスワードが間違っています', 'danger')

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                flash('ユーザー名とパスワードを入力してください', 'warning')
            elif User.query.filter_by(username=username).first():
                flash('そのユーザー名は既に使用されています', 'warning')
            else:
                new_user = User(username=username, password_hash=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                flash('登録成功！ログインしてください', 'success')
                return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        flash('ログアウトしました', 'info')
        return redirect(url_for('home'))


