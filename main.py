from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import freedns

app = Flask(__name__)

CAPTCHA_DIR = 'static/captchas'
if not os.path.exists(CAPTCHA_DIR):
    os.makedirs(CAPTCHA_DIR)

@app.route('/', methods=['GET', 'POST'])
def home():
    client = freedns.Client()
    
    captcha_image = None
    if request.method == 'POST':
        action = request.form['action']
        try:
            if action == 'login':
                email = request.form['email']
                password = request.form['password']
                client.login(username=email, password=password)
                return render_template('index.html', message="Login successful!", logged_in=True, client=client, captcha_image=None)

            elif action == 'sign_up':
                captcha_code = request.form['captcha_code']
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                username = request.form['username']
                password = request.form['password']
                email = request.form['email']
                client.create_account(
                    captcha_code=captcha_code,
                    firstname=firstname,
                    lastname=lastname,
                    username=username,
                    password=password,
                    email=email
                )
                return render_template('index.html', message="Account created! Please check your email.", logged_in=True, client=client, captcha_image=None)

            elif action == 'create_subdomain':
                domain_name = request.form['domain_name']
                subdomain_name = request.form['subdomain_name']
                record_type = request.form['record_type']
                destination = request.form['destination']
                captcha_code = request.form['captcha_code']
                
                registry = client.get_registry()  # assuming user is logged in already
                domain_map = {domain['domain']: domain['id'] for domain in registry['domains']}
                if domain_name not in domain_map:
                    return render_template('index.html', message="Invalid domain name.", logged_in=True, captcha_image=None)

                domain_id = domain_map[domain_name]
                client.create_subdomain(
                    captcha_code=captcha_code,
                    record_type=record_type,
                    subdomain=subdomain_name,
                    domain_id=int(domain_id),
                    destination=destination
                )
                return render_template('index.html', message="Subdomain created successfully!", logged_in=True, client=client, captcha_image=None)

        except RuntimeError as e:
            return render_template('index.html', message=f"Error: {e}", logged_in=False, captcha_image=None)

    captcha_image = "captcha.png"
    captcha_path = os.path.join(CAPTCHA_DIR, captcha_image)
    captcha_image_data = client.get_captcha()

    with open(captcha_path, "wb") as f:
        f.write(captcha_image_data)

    return render_template('index.html', logged_in=False, captcha_image=captcha_image)

@app.route('/static/captchas/<filename>')
def serve_captcha(filename):
    return send_from_directory(CAPTCHA_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
