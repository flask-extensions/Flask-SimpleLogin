from flask import Flask, render_template
from flask_simplelogin import SimpleLogin
from flask_simplelogin import login_required


def only_chuck_norris_can_enter(user):
    if user.get('username') == 'chuck' and user.get('password') == 'norris':
        return True
    return False


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-here'

SimpleLogin(app, login_checker=only_chuck_norris_can_enter)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port='5000')

