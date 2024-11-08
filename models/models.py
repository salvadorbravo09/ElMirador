from app import db
from datetime import datetime

class GastoComun(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  departamento = db.Column(db.Integer, nullable=False)
  periodo = db.Column(db.String(7), nullable=False)
  monto = db.Column(db.Float, nullable=False)
  fecha_pago = db.Column(db.Date, nullable=True)
  estado = db.Column(db.String(50), nullable=True)