from flask import Flask, Response, request, jsonify, redirect, url_for, render_template
from flask_cors import CORS
from profile_resources import ProfileResource
from login_resources import LoginResource
# import jwt

# Create the Flask application object.
app = Flask(__name__)

CORS(app)

SSO_PROVIDER_TOKEN_ENDPOINT = "SSO_PROVIDER_TOKEN_ENDPOINT_URL"

@app.route('/')  # / 访问路径
def hello_world():  # put application's code here
    return 'Hello Student!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # data = request.get_json()
        # uni = data.get('uni')
        # password = data.get('password')
        uni = request.form.get('uni')
        password = request.form.get('password')
        # print(uni, password)
        if not uni or not password:
            return jsonify({'message': 'Missing username or password'}), 400

    # Verify user credentials against the database
    # cursor = db.cursor()
    # query = "SELECT username, email, password FROM users WHERE username = %s"
    # cursor.execute(query, (username,))
    # user = cursor.fetchone()
        user = LoginResource.get_user_by_uni(uni)
        # print(user)
    # result = ProfileResource.get_profile_by_uni(uni)

        if user and user['password'] == password:
        # Generate JWT token upon successful login
        # payload = {'username': user[0], 'email': user[1]}
        # token = jwt.encode(payload, secret_key, algorithm='HS256')
        # return jsonify({'message': 'Login successful', 'token': token}), 200
        #     print("zhaodao")
            return redirect(url_for('profile', uni=uni))
        return render_template('login.html', message='Invalid username or password')

    # return jsonify({'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route("/profile/<uni>", methods=['GET', 'POST'])
def profile(uni):
    # if request.method == "GET":
    #     result = ProfileResource.get_account_by_emailID(emailID)
    #
    #     if result:
    #         rsp = Response(json.dumps(result), status=200, content_type="application.json")
    #     else:
    #         rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    result = ProfileResource.get_profile_by_uni(uni)
    # if request.method == "GET":
    #     result = ProfileResource.get_profile_by_uni(uni)
    #     print(result)
    #     return render_template('profile.html', user_info=result)

    if request.method == "POST":
        interest = request.form.get('interest')
        schedule = request.form.get('schedule')
        # new_content = request.form['interest', 'schedule']
        new_content = [uni, interest, schedule]
        # print(interest, schedule)
        print(new_content)
        ProfileResource.update_account(new_content)

        return redirect(url_for('profile', uni=uni))

    return render_template('profile.html', user_info=result)

if __name__ == '__main__':
    app.run()