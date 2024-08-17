from flask import Flask , render_template ,session, request, make_response
import secrets
from email_module import send_verification_email
from firebaseModule import get_doc_id_by_email , delete_user_data
import random
from datetime import datetime, timedelta 
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route('/')
def homepage():

    res = make_response(render_template("index.html"))
    res.set_cookie("dark_mode", value = "True")
    return render_template("index.html")


verification_code={}


@app.route('/account_deletation', methods=['GET', 'POST'])
def index():

    if 'email' in session and 'verification_code' in session:
        if request.method == 'POST':
            code = request.form.get('verification_code')
            print(f"Session Email: {session.get('email')}, Session code: {session.get('verification_code')}")

            if code == session.get('verification_code'):
                email = session.get('email')
                doc_id = get_doc_id_by_email(email)
                if not doc_id:
                    return render_template('delete_page.html', message = f"No data found with the email: {email}")
                for id in doc_id:
                    print(f"Deleting user data for document ID: {id}")
                    delete_user_data(id)
                    print(f"Deleted user data for document ID: {id}")
                session.pop('email', None)
                session.pop('verification_code', None)
                return render_template('delete_page.html', message = f"User data deleted successfully")
            else:
                render_template('delete_page.html', message = f"Invalid verification code")
    return render_template('delete_page.html')

@app.route("/request_verification", methods=['POST'])
def request_verification():
    print("Form data:", request.form)
    email = request.form.get('email', None)
    if not email:
        return render_template('delete_page.html', message = f"Enter an email address")
    
    doc_id = get_doc_id_by_email(email)

    if not doc_id:
        return render_template('delete_page.html', message = f"No data found with the email: {email}")
    
    code= str(random.randint(1000, 9999))
    verification_code[email] = {
        'code' : code,
        'expires_at': datetime.now() + timedelta(minutes=10)
    }

    send_verification_email(email, code)

    session['email'] = email
    session['verification_code'] = code
    print("Session email stored:", session['email'])
    print("Session verification_code stored:", session['verification_code'])

    return render_template('delete_page.html', message = f"Verification code sent to your email." ,email_submitted =True)



@app.route("/privacy_policy")
def privacy_policy():

    return render_template('privacy_policy.html')

@app.route('/acknowledgement')
def acknowledgement():
    return render_template('acknowledgement.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

