from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import init_db, add_user, get_user, add_task, get_tasks, complete_task, delete_task

app = Flask(__name__)
app.secret_key = '213212541'  # 用于 session 加密

init_db()  # 初始化数据库


@app.route('/')#根目录
def index():
    if 'user_id' not in session: ## 检测是否登录转入登录界面或者注册界面
        return redirect(url_for('login'))
    tasks = get_tasks(session['user_id'])
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])##添加任务界面
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        task_content = request.form['content']
        add_task(task_content, session['user_id'])
        return redirect(url_for('index'))
    return render_template('add_task.html')


@app.route('/complete/<int:task_id>')  ##任务完成后划出
def complete(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    complete_task(task_id)
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    delete_task(task_id)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and user[2] == password:
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        flash('Invalid credentials. Please try again.')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_user(username):
            flash('用户名已经存在.')
        else:
            add_user(username, password)
            flash('注册成功! 你可以登录了')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
