from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactos.db'

db = SQLAlchemy(app)


# CREAR MODELO

class Contacto(db.Model):
    
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    
    def serialize(self):
        return{
            
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'phone':self.phone
            
        }
    
    
    
#CREAR LA TABLA

with app.app_context():
    db.create_all()   
    
#CREAR RUTAS
@app.route('/contacts',methods=['GET'])
def get_contacts():
    
    contacts = Contacto.query.all()
    
    #esto es lo mismo que el return en una linea
    #lista_contacto=[]
    #for c in contacts:
    #   lista_contacto.append(c.serialize())
    
    return jsonify({'contact':[ c.serialize() for c in contacts]})
    
    
    
   






@app.route('/contacts',methods=['POST'])
def create_contact():
    
    data = request.get_json()
    cont = Contacto(name=data['name'],email=data['email'],phone=data['phone'])
    db.session.add(cont)
    db.session.commit()
    
    return jsonify({'message':'Contacto creado con exito', 'contact': cont.serialize()}),201
    
    
    
@app.route('/contacts/<int:id>',methods=['GET'])
def get_contact(id):
    
   cont = Contacto.query.get(id)
   
   if not cont :
       return jsonify({'message':'El contacto no existe'}),404
   

    
   return jsonify({ 'contact': cont.serialize()}),200    
    
    

@app.route('/contacts/<int:id>',methods=['PUT','PATH'])
def edit_contact(id):
    
   cont = Contacto.query.get_or_404(id)
   
   data = request.get_json()
   
   if 'name' in data:
        cont.name = data['name']
   
   if 'email' in data:
        cont.email = data['email']
   
   if 'phone' in data:
        cont.phone = data['phone']
   
   
   db.session.commit()
   
   
   return jsonify({ 'message':'El contacto se ha modificado correctamente','contact': cont.serialize()}),200
   

    
@app.route('/contacts/<int:id>',methods=['DELETE'])
def delete_contact(id):
    
   cont = Contacto.query.get_or_404(id)
   
   if not cont :
       return jsonify({'message':'El contacto no existe'}),404
   
   db.session.delete(cont)
   db.session.commit()
   
   
   return jsonify({ 'message':'El contacto se ha eliminado correctamente','contact': cont.serialize()}),200
   

       