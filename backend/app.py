from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessario per il messaggio flash

# Funzione per connettersi al database
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Assicurati che il file database.db esista
    conn.row_factory = sqlite3.Row
    return conn

# Route per mostrare la pagina di registrazione
@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

# Route per gestire la registrazione
@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Connettersi al database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Controllo se l'email è già registrata
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("L'email è già registrata. Prova con un'altra.", "error")
            return redirect(url_for('register_get'))

        # Inserire il nuovo utente nel database
        hashed_password = generate_password_hash(password, method='sha256')
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, hashed_password))
        conn.commit()
        flash("Registrazione completata con successo! Ora puoi effettuare il login.", "success")
        return redirect(url_for('login_get'))
    except Exception as e:
        flash(f"Errore durante la registrazione: {e}", "error")
        return redirect(url_for('register_get'))
    finally:
        conn.close()

# Esempio di route per la home
@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

# Route per gestire il form di login (metodo POST)
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    # Esempio semplice di controllo credenziali
    if username == 'admin' and password == 'password':
        return redirect(url_for('success'))
    else:
        return redirect(url_for('login_get'))

# Route di successo (dopo il login)
@app.route('/success', methods=['GET'])
def success():
    return "Login avvenuto con successo!"


# Esempio di una route per la registrazione
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Logica di controllo dell'utente
    if username == 'admin':
        flash("L'utente esiste già, scegli un altro nome utente.")
        return redirect(url_for('home'))
    
    # Salva l'utente e continua
    return redirect(url_for('home'))

# Esempio di una route per la login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Logica di login
    if username == 'admin' and password == 'admin123':
        flash("Login effettuato con successo!")
        return redirect(url_for('home'))

    flash("Credenziali non valide!")
    return redirect(url_for('home'))

# Sezione admin (questa è un'idea base, puoi adattarla per aggiungere altri utenti)
@app.route('/admin')
def admin():
    # Controllo per admin
    return render_template('admin.html')

# Questa parte è fondamentale per far partire il server
if __name__ == "__main__":
    app.run(debug=True)

