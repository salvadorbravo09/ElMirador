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

@api.route('/generar_gastos', methods=['POST'])
def generar_gastos():
    data = request.json
    mes = data.get('mes')
    anio = data.get('anio')
    monto = data.get('monto') 
    
    if not anio or (mes and (mes < 1 or mes > 12)):
        return jsonify({"error": "Mes o año inválidos"}), 400

    if monto is None:
        return jsonify({"error": "El monto es requerido"}), 400 

    departamentos = Departamento.query.all()
    if not departamentos:
        return jsonify({"error": "No hay departamentos registrados"}), 400

    for departamento in departamentos:
        gasto_existente = GastoComun.query.filter_by(departamento_id=departamento.id, mes=mes, anio=anio).first()
        if not gasto_existente: 
            gasto = GastoComun(departamento_id=departamento.id, mes=mes, anio=anio, monto=monto)
            db.session.add(gasto)
                    
    db.session.commit()
    return jsonify({"mensaje": "Gastos generados exitosamente"}), 201

