from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GastoComun(db.Model):
    __tablename__ = 'gastos_comunes'
    
    id = db.Column(db.Integer, primary_key=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    pagado = db.Column(db.Boolean, default=False)
    fecha_pago = db.Column(db.Date, nullable=True)
    departamento = db.relationship("Departamento", backref="gastos")
