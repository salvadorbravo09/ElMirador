from flask import Blueprint, request, jsonify
from datetime import datetime, date
from models import db, Departamento, GastoComun

api = Blueprint('api', __name__)

@api.route('/registrar_departamento', methods=['POST'])
def registrar_departamento():
    data = request.json
    numero = data.get('numero')

    if not numero:
        return jsonify({"error": "El número del departamento es requerido"}), 400

    if Departamento.query.filter_by(numero=numero).first():
        return jsonify({"error": "El departamento ya está registrado"}), 400

    nuevo_departamento = Departamento(numero=numero)
    db.session.add(nuevo_departamento)
    db.session.commit()

    return jsonify({"mensaje": "Departamento registrado exitosamente", "departamento": numero}), 201