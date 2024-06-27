from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('aleaciones.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['GET', 'POST'])
def calcular():
    conn = get_db_connection()
    aleaciones = conn.execute('SELECT * FROM Aleaciones').fetchall()
    resultado = None
    if request.method == 'POST':
        aleacion_id = request.form['aleacion']
        cantidad = int(request.form['cantidad'])
        
        ingredientes = get_ingredientes(conn, aleacion_id, cantidad)
        
        resultado = {
            'aleacion': conn.execute('SELECT * FROM Aleaciones WHERE id = ?', (aleacion_id,)).fetchone(),
            'ingredientes': ingredientes,
            'cantidad': cantidad
        }
    conn.close()
    return render_template('calcular.html', aleaciones=aleaciones, resultado=resultado)

def get_ingredientes(conn, aleacion_id, cantidad):
    ingredientes = {}
    
    # Obtener ingredientes directos
    directos = conn.execute('SELECT * FROM Ingredientes WHERE aleacion_id = ?', (aleacion_id,)).fetchall()
    for ingrediente in directos:
        if ingrediente['ingrediente'] in ingredientes:
            ingredientes[ingrediente['ingrediente']] += ingrediente['cantidad'] * cantidad
        else:
            ingredientes[ingrediente['ingrediente']] = ingrediente['cantidad'] * cantidad
    
    # Obtener aleaciones de las que depende y sus ingredientes
    dependencias = conn.execute('SELECT * FROM Dependencias WHERE aleacion_id = ?', (aleacion_id,)).fetchall()
    for dependencia in dependencias:
        dep_ingredientes = get_ingredientes(conn, dependencia['depende_de_id'], cantidad)
        for ingr, cant in dep_ingredientes.items():
            if ingr in ingredientes:
                ingredientes[ingr] += cant
            else:
                ingredientes[ingr] = cant

    return [{'ingrediente': k, 'cantidad': v} for k, v in ingredientes.items()]

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form.getlist('ingrediente')
        cantidades = request.form.getlist('cantidad')
        dependencias = request.form.getlist('dependencia')

        conn = get_db_connection()
        conn.execute('INSERT INTO Aleaciones (nombre) VALUES (?)', (nombre,))
        aleacion_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

        for ingrediente, cantidad in zip(ingredientes, cantidades):
            conn.execute('INSERT INTO Ingredientes (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)',
                         (aleacion_id, ingrediente, cantidad))
        
        for dependencia in dependencias:
            conn.execute('INSERT INTO Dependencias (aleacion_id, depende_de_id) VALUES (?, ?)',
                         (aleacion_id, dependencia))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn = get_db_connection()
    aleaciones = conn.execute('SELECT * FROM Aleaciones').fetchall()
    conn.close()
    return render_template('agregar.html', aleaciones=aleaciones)

@app.route('/editar', methods=['GET', 'POST'])
def editar():
    conn = get_db_connection()
    aleaciones = conn.execute('SELECT * FROM Aleaciones').fetchall()

    if request.method == 'POST':
        aleacion_id = request.form['aleacion']
        nombre = request.form['nombre']
        ingredientes = request.form.getlist('ingrediente')
        cantidades = request.form.getlist('cantidad')
        dependencias = request.form.getlist('dependencia')

        conn.execute('UPDATE Aleaciones SET nombre = ? WHERE id = ?', (nombre, aleacion_id))
        conn.execute('DELETE FROM Ingredientes WHERE aleacion_id = ?', (aleacion_id,))
        conn.execute('DELETE FROM Dependencias WHERE aleacion_id = ?', (aleacion_id,))

        for ingrediente, cantidad in zip(ingredientes, cantidades):
            conn.execute('INSERT INTO Ingredientes (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)',
                         (aleacion_id, ingrediente, cantidad))

        for dependencia in dependencias:
            conn.execute('INSERT INTO Dependencias (aleacion_id, depende_de_id) VALUES (?, ?)',
                         (aleacion_id, dependencia))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('editar.html', aleaciones=aleaciones)

@app.route('/editar/<int:aleacion_id>', methods=['GET'])
def obtener_aleacion(aleacion_id):
    conn = get_db_connection()
    aleacion = conn.execute('SELECT * FROM Aleaciones WHERE id = ?', (aleacion_id,)).fetchone()
    ingredientes = conn.execute('SELECT * FROM Ingredientes WHERE aleacion_id = ?', (aleacion_id,)).fetchall()
    dependencias = conn.execute('SELECT depende_de_id FROM Dependencias WHERE aleacion_id = ?', (aleacion_id,)).fetchall()
    conn.close()

    aleacion_data = {
        'nombre': aleacion['nombre'],
        'ingredientes': [{'ingrediente': i['ingrediente'], 'cantidad': i['cantidad']} for i in ingredientes],
        'dependencias': [d['depende_de_id'] for d in dependencias]
    }
    return jsonify(aleacion_data)

if __name__ == '__main__':
    app.run(debug=True)