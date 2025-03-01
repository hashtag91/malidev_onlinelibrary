from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

#Configuration de flask-mail pour l'envoi d'email
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.secret_key = os.getenv('SECRET_KEY')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

#Route pour envoyer le message
@app.route('/sendmail',methods=['POST'])
def sendmail():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message(
            subject=f"Nouveau message de Biblio",
            recipients=['camarayacouba91@gmail.com'], # Mon adresse email
            sender=email, #L'adresse email de l'utilisateur
        )
        msg.body = f"Nom: {name}\n Email: {email}\n Message: {message}"
        try:
            mail.send(msg)
            flash("Message envoyé avec succès !", "success")
            return redirect("/contact")
        except Exception as e:
            flash(f"Erreur lors de l'envoi du message", "danger")
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)