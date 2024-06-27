from flask import Flask, render_template, request, redirect, url_for
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
        
        # Obtener ingredientes normales
        ingredientes = conn.execute('SELECT * FROM Ingredientes WHERE aleacion_id = ?', (aleacion_id,)).fetchall()
        
        # Obtener ingredientes totales primordiales
        ingredientes_totales = conn.execute('SELECT * FROM IngredientesTotales WHERE aleacion_id = ?', (aleacion_id,)).fetchall()
        
        resultado = {
            'aleacion': conn.execute('SELECT * FROM Aleaciones WHERE id = ?', (aleacion_id,)).fetchone(),
            'ingredientes': [{'ingrediente': i['ingrediente'], 'cantidad': i['cantidad'] * cantidad} for i in ingredientes],
            'ingredientes_totales': [{'ingrediente': i['ingrediente'], 'cantidad': i['cantidad'] * cantidad} for i in ingredientes_totales],
            'cantidad': cantidad
        }
    conn.close()
    return render_template('calcular.html', aleaciones=aleaciones, resultado=resultado)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form.getlist('ingrediente')
        cantidades = request.form.getlist('cantidad')
        ingredientes_totales = request.form.getlist('ingrediente_total')
        cantidades_totales = request.form.getlist('cantidad_total')

        conn = get_db_connection()
        conn.execute('INSERT INTO Aleaciones (nombre) VALUES (?)', (nombre,))
        aleacion_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

        for ingrediente, cantidad in zip(ingredientes, cantidades):
            conn.execute('INSERT INTO Ingredientes (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)',
                         (aleacion_id, ingrediente, cantidad))

        for ingrediente_total, cantidad_total in zip(ingredientes_totales, cantidades_totales):
            conn.execute('INSERT INTO IngredientesTotales (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)',
                         (aleacion_id, ingrediente_total, cantidad_total))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('agregar.html')

@app.route('/editar', methods=['GET', 'POST'])
def editar():
    conn = get_db_connection()
    aleaciones = conn.execute('SELECT * FROM Aleaciones').fetchall()

    if request.method == 'POST':
        aleacion_id = request.form['aleacion']
        nombre = request.form['nombre']
        ingredientes = request.form.getlist('ingrediente')
        cantidades = request.form.getlist('cantidad')
        ingredientes_totales = request.form.getlist('ingrediente_total')
        cantidades_totales = request.form.getlist('cantidad_total')

        conn.execute('UPDATE Aleaciones SET nombre = ? WHERE id = ?', (nombre, aleacion_id))
        conn.execute('DELETE FROM Ingredientes WHERE aleacion_id = ?', (aleacion_id,))
        conn.execute('DELETE FROM IngredientesTotales WHERE aleacion_id = ?', (aleacion_id,))

        for ingrediente, cantidad in zip(ingredientes, cantidades):
            conn.execute('INSERT INTO Ingredientes (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)',
                         (aleacion_id, ingrediente, cantidad))

        for ingrediente_total, cantidad_total in zip(ingredientes_totales, cantidades_totales):
            conn.execute('INSERT INTO IngredientesTotales (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)',
                         (aleacion_id, ingrediente_total, cantidad_total))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('editar.html', aleaciones=aleaciones)

if __name__ == '__main__':
    app.run(debug=True)