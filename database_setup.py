import sqlite3

conn = sqlite3.connect('aleaciones.db')
c = conn.cursor()

# Crear la tabla de aleaciones
c.execute('''CREATE TABLE Aleaciones (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
)''')

# Crear la tabla de ingredientes
c.execute('''CREATE TABLE Ingredientes (
    id INTEGER PRIMARY KEY,
    aleacion_id INTEGER,
    ingrediente TEXT,
    cantidad INTEGER,
    FOREIGN KEY (aleacion_id) REFERENCES Aleaciones(id)
)''')

# Insertar datos de ejemplo en la tabla de aleaciones
aleaciones = [
    ('Steel Ingot',), ('Bronze Ingot',), ('Brass Ingot',), ('Billon Ingot',), 
    ('Nickel Ingot',), ('Duralumin Ingot',), ('Gilded Iron',), ('Cobalt Ingot',), 
    ('Ferrosilicon',), ('Lingote de latón de aluminio',), ('Lingote de bronce de aluminio',), 
    ('Corinthian Bronze Ingot',), ('Damascus Steel Ingot',), ('Solder Ingot',), 
    ('Hardened Metal',), ('Redstone Alloy Ingot',), ('Reinforced Alloy Ingot',)
]
c.executemany('INSERT INTO Aleaciones (nombre) VALUES (?)', aleaciones)

# Insertar datos de ejemplo en la tabla de ingredientes
ingredientes = [
    (1, 'Iron Dust', 2), (1, 'Carbon', 9), (1, 'Iron Ingot', 1),
    (2, 'Copper Dust', 1), (2, 'Tin Dust', 1), (2, 'Copper Ingot', 1),
    # Añadir más ingredientes aquí según el archivo proporcionado...
]
c.executemany('INSERT INTO Ingredientes (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)', ingredientes)

conn.commit()
conn.close()