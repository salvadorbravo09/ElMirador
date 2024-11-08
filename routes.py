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

@api.route('/pagar_gasto', methods=['POST'])
def pagar_gasto():
    data = request.json
    departamento_numero = data.get('departamento')
    mes = data.get('mes')
    anio = data.get('anio')
    fecha_pago = datetime.strptime(data.get('fecha_pago'), '%Y-%m-%d').date()

    departamento = Departamento.query.filter_by(numero=departamento_numero).first()
    if not departamento:
        return jsonify({"error": "Departamento no encontrado"}), 404

    gasto = GastoComun.query.filter_by(departamento_id=departamento.id, mes=mes, anio=anio).first()
    if not gasto:
        return jsonify({"error": "Gasto no encontrado para el período especificado"}), 404

    if gasto.pagado:
        return jsonify({"mensaje": "Pago duplicado"}), 400
    
    gasto.pagado = True
    gasto.fecha_pago = fecha_pago
    
    hoy = date.today()
    estado = "Pago exitoso dentro del plazo" if fecha_pago <= hoy else "Pago exitoso fuera de plazo"
    
    db.session.commit()
    
    return jsonify({
        "departamento": departamento.numero,
        "fecha_cancelacion": fecha_pago.strftime('%Y-%m-%d'),
        "periodo": f"{mes}/{anio}",
        "estado": estado
    }), 200
    
@api.route('/gastos_pendientes', methods=['GET'])
def gastos_pendientes():
    mes = int(request.args.get('mes'))
    anio = int(request.args.get('anio'))

    # Asegúrate de que el filtro es correcto para mes y año
    gastos = GastoComun.query.filter(
        GastoComun.mes == mes,  # Se asegura que el mes sea el correcto
        GastoComun.anio == anio,  # Se asegura que el año sea el correcto
        GastoComun.pagado == False  # Solo los gastos no pagados
    ).order_by(GastoComun.anio, GastoComun.mes).all()

    if not gastos:
        return jsonify({"mensaje": "Sin montos pendientes"}), 200

    result = [{
        "departamento": gasto.departamento.numero,
        "periodo": f"{gasto.mes}/{gasto.anio}",
        "monto": gasto.monto
    } for gasto in gastos]

    return jsonify(result), 200