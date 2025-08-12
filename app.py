from flask import Flask,render_template, request,session, redirect, url_for 
import sqlite3 

'''
import matplotlib
matplotlib.use('Agg')           # use non-GUI for backend
import matplotlib.pyplot as plt   '''


app = Flask(__name__)
app.secret_key = 'your secret key'



""" @app.route('/')
def home():
 return 'Flask is working!'   """




# Route - Home page - complaint form
@app.route('/')
def home():
    return render_template('register.html') 







# Login - Route 
@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '1234':
            session['admin_logged_in'] = True
            return redirect('/dashboard')
        else:
            error = 'Invalid username or password'
    return render_template('admin_login.html', error=error)







# Dashboard - Route
@app.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/login')
    return render_template('admin_dashboard.html')





# Logout - Route
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/login')





# Route - Complaint submission 
@app.route('/submit', methods=['POST'])   
def submit():
    name = request.form['name']
    mobile = request.form['mobile']
    department = request.form['department']
    complaint = request.form['complaint']

    print("Complaint received:", name, mobile, department, complaint)



    # Save to database
    conn = sqlite3.connect('complaints.db')

    c = conn.cursor()
    c.execute('INSERT INTO complaints (name, mobile, department, complaint) VALUES (?, ?, ?, ?)',
              (name, mobile, department, complaint))
    
    conn.commit()
    conn.close()


    return render_template('thankyou.html')  



#  Route - complaint list in browser
@app.route('/view')
def view_complaints():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('SELECT * FROM complaints')
    data = c.fetchall()
    conn.close()
    return render_template('view.html', complaints=data)






#  Route - Analytics  

'''@app.route('/analytics')
def analytics():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT department, COUNT(*) FROM complaints GROUP BY department")
    data = c.fetchall()
    conn.close()

    # Separate labels and counts
    labels = [row[0] for row in data]          
    counts = [row[1] for row in data]

    # Plotting
    import matplotlib.pyplot as plt
    import io
    import base64

    plt.style.use('seaborn-darkgrid')  # ✅ Dark graph theme
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, counts, color='#007BFF')  # ✅ Stylish blue bars
    ax.set_xlabel('Department')
    ax.set_ylabel('Number of Complaints')
    ax.set_title('Complaints per Department')

    plt.xticks(rotation=30, fontsize=10)  # ✅ Rotate + enlarge bottom labels
    plt.tight_layout()

    # Convert plot to image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('analytics.html', plot_url=plot_url)     '''



@app.route('/analytics')
def analytics():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT department, COUNT(*) FROM complaints GROUP BY department")
    data = c.fetchall()
    
    conn.close()

    labels = [row[0] for row in data]
    counts = [row[1] for row in data]

    return render_template('analytics.html', labels=labels, counts=counts)  





if __name__ == '__main__':
    app.run(debug=True)




