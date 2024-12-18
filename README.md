### El Mirador - Sistema de Gestión de Gastos Comunes

Este sistema permite administrar los gastos comunes de departamentos, incluyendo el registro de departamentos, generación de gastos mensuales y control de pagos.

Características
---------------

-   Registro de departamentos
-   Generación de gastos comunes mensuales o anuales
-   Registro de pagos de gastos comunes
-   Consulta de gastos pendientes
-   Sistema de control de pagos con validación de fechas

Requisitos
----------

-   Python 3
-   Flask
-   SQLAlchemy
-   SQLite

Instalación
-----------

1.  Clona el repositorio:

```git clone https://github.com/salvadorbravo09/ElMirador.git```

2.  Ir a la carpeta:

```cd ElMirador```

3.  Crear entorno virtual

```python -m venv .venv```

4.  Activar entorno virtual

```.venv\Scripts\activate```

5.  Instala las dependencias:

`pip install -r requirements.txt`

6.  Inicializa la base de datos:

`python app.py`

Estructura del Proyecto
-----------------------

    gestion-gastos-comunes/
    ├── app.py
    ├── models.py
    ├── routes.py
    ├── gestion_gastos.db

API Endpoints
-------------

| Metodos   | URL                                      | Descripcion                              |
| -------- | ---------------------------------------- | ---------------------------------------- |
| `POST`   | `/api/registrar_departamento`                             | Registrar Departamento.                       |
| `POST`    | `/api/generar_gastos`                             | Generar Gastos.                      |
| `POST`   | `/api/pagar_gasto`                             | Registrar Pago.                       |
| `GET`    | `/api/gastos_pendientes?mes={mes}&anio={anio}`                          | Consultar Gastos Pendientes.                       |

#### Registrar Departamento
```
{
  "numero":  "101"
}
```

#### Generar Gastos
```
{
  "mes":  1,
  "anio":  2024
}
```

#### Registrar Pago
```
{
  "departamento": "101",
  "mes": 1,
  "anio": 2024,
  "fecha_pago": "2024-01-15"
}
```

#### Consultar Gastos Pendientes
```
{
  GET /api/gastos_pendientes?mes=1&anio=2024
}
```

