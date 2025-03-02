from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
from models import engine, Livres
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
import json
import os

load_dotenv()

Session = sessionmaker(bind=engine)
session = Session()

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

#Route menant à la page d'ajout de nouveaux documents (livres)
@app.route("/add_book")
def add_book():
    return render_template("bookadd.html")

# Vérifie si l'extension est autorisée
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ['pdf']

#Pour enregistrement du livre
@app.route('/book_saving',methods=['POST'])
def book_saving():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Aucun document attaché !","danger")
            return redirect(url_for('add_book'))

        title = request.form.get('title')
        author = request.form.get('author')
        langage = request.form.get('langage')
        booktype = request.form.get('type')
        category = request.form.get('category')
        description = request.form.get('description')
        table = request.form.get('table')

        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if booktype == 'langage':
                app.config['UPLOAD_FOLDER'] = f"static/docs/{langage}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))  # Enregistre le fichier
            flash("Livre ajouté avec succès !","success")

            livre = Livres(name=filename, author=author, title=title, langage=langage, type=booktype, category=category, description=description)
            session.add(livre)
            session.commit()

            table_lines = table.split('\n') #Splitter les lignes de table de contenu du document
            #Lire et récuperer le contenu du fichier json
            with open('static/description.json','r', encoding='utf-8') as f:
                data = json.load(f)
                data['description'][filename] = table_lines
            #Ajout des tables du nouveau document dans le json
            with open('static/description.json','w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return redirect(url_for('add_book'))


@app.route("/html_css")
def html_css():
    docs = os.listdir('./static/docs/html_css/')
    print(docs)
    return render_template("langage.html", langage="HTML & CSS", docs=docs)


if __name__ == "__main__":
    app.run(debug=True)