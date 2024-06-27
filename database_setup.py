import sqlite3

# Conectar a la base de datos (se creará si no existe)
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

# Crear la tabla de ingredientes totales
c.execute('''CREATE TABLE IngredientesTotales (
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
    (1, 'Iron Dust', 2), (1, 'Carbon', 9),
    (2, 'Copper Dust', 1), (2, 'Tin Dust', 1), (2, 'Copper Ingot', 1),
    (3, 'Copper Dust', 1), (3, 'Zinc Dust', 1), (3, 'Copper Ingot', 1),
    (4, 'Silver Dust', 1), (4, 'Copper Dust', 1), (4, 'Silver Ingot', 1),
    (5, 'Iron Dust', 1), (5, 'Iron Ingot', 1), (5, 'Copper Dust', 1),
    (6, 'Aluminum Dust', 1), (6, 'Copper Dust', 1), (6, 'Aluminum Ingot', 1),
    (7, 'Gold Ingot (24-Carat)', 1), (7, 'Iron Dust', 1),
    (8, 'Iron Dust', 1), (8, 'Copper Dust', 1), (8, 'Nickel Ingot', 1),
    (9, 'Iron Ingot', 1), (9, 'Iron Dust', 1), (9, 'Silicon', 1),
    (10, 'Polvo de aluminio', 1), (10, 'Lingote de latón', 1), (10, 'Lingote de aluminio', 1),
    (11, 'Polvo de aluminio', 1), (11, 'Lingote de bronce', 1), (11, 'Lingote de aluminio', 1),
    (12, 'Silver Dust', 1), (12, 'Gold Dust', 1), (12, 'Copper Dust', 1), (12, 'Bronze Ingot', 1),
    (13, 'Steel Ingot', 1), (13, 'Iron Dust', 1), (13, 'Carbon', 1), (13, 'Iron Ingot', 1),
    (14, 'Lead Dust', 1), (14, 'Tin Dust', 1), (14, 'Lead Ingot', 1),
    (15, 'Damascus Steel Ingot', 1), (15, 'Duralumin Ingot', 1), (15, 'Compressed Carbon', 1), (15, 'Aluminum Bronze Ingot', 1),
    (16, 'Redstone Dust', 1), (16, 'Block of Redstone', 1), (16, 'Ferrosilicon', 1), (16, 'Hardened Metal', 1),
    (17, 'Damascus Steel Ingot', 1), (17, 'Hardened Metal', 1), (17, 'Corinthian Bronze Ingot', 1), (17, 'Solder Ingot', 1), (17, 'Billon Ingot', 1), (17, 'Gold Ingot (24-Carat)', 1)
]
c.executemany('INSERT INTO Ingredientes (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)', ingredientes)

# Insertar datos de ejemplo en la tabla de ingredientes totales
ingredientes_totales = [
    (1, 'Iron Dust', 2), (1, 'Carbon', 9),
    (2, 'Copper Dust', 2), (2, 'Tin Dust', 1),
    (3, 'Copper Dust', 2), (3, 'Zinc Dust', 1),
    (4, 'Silver Dust', 2), (4, 'Copper Dust', 1),
    (5, 'Iron Dust', 2), (5, 'Copper Dust', 1),
    (6, 'Aluminum Dust', 2), (6, 'Copper Dust', 1),
    (7, 'Gold Dust', 1), (7, 'Iron Dust', 1),
    (8, 'Iron Dust', 3), (8, 'Copper Dust', 2),
    (9, 'Iron Dust', 2), (9, 'Block of Quartz', 1),
    (10, 'Aluminum Dust', 2), (10, 'Copper Dust', 2), (10, 'Zinc Dust', 1),
    (11, 'Aluminum Dust', 2), (11, 'Copper Dust', 2), (11, 'Tin Dust', 1),
    (12, 'Silver Dust', 1), (12, 'Gold Dust', 1), (12, 'Copper Dust', 3), (12, 'Tin Dust', 1),
    (13, 'Iron Dust', 4), (13, 'Carbon', 16),
    (14, 'Lead Dust', 2), (14, 'Tin Dust', 1),
    (15, 'Iron Dust', 4), (15, 'Aluminum Dust', 4), (15, 'Copper Dust', 3), (15, 'Tin Dust', 1), (15, 'Carbon', 48),
    (16, 'Redstone Dust', 10), (16, 'Iron Dust', 6), (16, 'Aluminum Dust', 4), (16, 'Copper Dust', 3), (16, 'Tin Dust', 1), (16, 'Block of Quartz', 1), (16, 'Carbon', 48),
    (17, 'Iron Dust', 8), (17, 'Aluminum Dust', 4), (17, 'Copper Dust', 7), (17, 'Tin Dust', 3), (17, 'Silver Dust', 3), (17, 'Gold Dust', 12), (17, 'Lead Dust', 2), (17, 'Carbon', 64)
]
c.executemany('INSERT INTO IngredientesTotales (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)', ingredientes_totales)

# Confirmar y cerrar la conexión
conn.commit()
conn.close()