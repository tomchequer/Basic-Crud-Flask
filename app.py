from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#this will be a simple crud skeleton


app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

class Crud(db.Model):
    #each item will have its own personal id on the database
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)



    def __repr__(self):
        return '<data %r>' % self.id 


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        content = request.form['content']
        new_querry = Crud(content=content)
        
        try:
            db.session.add(new_querry)
            db.session.commit()
            return redirect('/')

        except:
            return 'something went wrong'

    else:

        data = Crud.query.order_by(Crud.date_created).all()
        return render_template('home.html', data=data)

@app.route('/delete/<int:id>') #this have to be an int
def delete(id):
    
    data_to_delete = Crud.query.get_or_404(id)
    
    try:
        db.session.delete(data_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'something went wrong'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    data_to_update = Crud.query.get_or_404(id)
    if request.method == "POST":
        data_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'something went wrong'
    else:
        return render_template('update.html', data=data_to_update)
        

if __name__ == "__main__":
    app.run(debug=True)