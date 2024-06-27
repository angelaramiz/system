import sqlite3

# Conectar a la base de datos (se creará si no existe)
conexion = sqlite3.connect('aleaciones.db')
c = conexion.cursor()

# Crear la tabla de aleaciones
c.execute('''
CREATE TABLE IF NOT EXISTS Aleaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
)
''')

# Crear la tabla de ingredientes
c.execute('''
CREATE TABLE IF NOT EXISTS Ingredientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aleacion_id INTEGER,
    ingrediente TEXT,
    cantidad INTEGER,
    FOREIGN KEY (aleacion_id) REFERENCES Aleaciones(id)
)
''')

# Crear la tabla de dependencias
c.execute('''
CREATE TABLE IF NOT EXISTS Dependencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aleacion_id INTEGER,
    depende_de_id INTEGER,
    FOREIGN KEY (aleacion_id) REFERENCES Aleaciones(id),
    FOREIGN KEY (depende_de_id) REFERENCES Aleaciones(id)
)
''')

# Crear la tabla de ingredientes totales
c.execute('''
CREATE TABLE IF NOT EXISTS IngredientesTotales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aleacion_id INTEGER,
    ingrediente TEXT,
    cantidad INTEGER,
    FOREIGN KEY (aleacion_id) REFERENCES Aleaciones(id)
)
''')

# Insertar datos de ejemplo en la tabla de aleaciones
aleaciones = [
    ('Steel Ingot',), 
    ('Bronze Ingot',),
    ('Brass Ingot',), 
    ('Billon Ingot',),
    ('Nickel Ingot',), 
    ('Duralumin Ingot',), 
    ('Gilded Iron',), 
    ('Cobalt Ingot',),
    ('Ferrosilicon',), 
    ('Aluminum Brass Ingot',), 
    ('Aluminum Bronze Ingot',),
    ('Corinthian Bronze Ingot',), 
    ('Damascus Steel Ingot',), 
    ('Solder Ingot',),
    ('Hardened Metal',), 
    ('Redstone Alloy Ingot',), 
    ('Reinforced Alloy Ingot',)
]
c.executemany('INSERT INTO Aleaciones (nombre) VALUES (?)', aleaciones)

# Insertar datos de ejemplo en la tabla de ingredientes
ingredientes = [
    (1, 'Iron Dust', 1), (1, 'Carbon', 1), (1, 'Iron Ingot', 1),
    (2, 'Copper Dust', 1), (2, 'Tin Dust', 1), (2, 'Copper Ingot', 1),
    (3, 'Copper Dust', 1), (3, 'Zinc Dust', 1), (3, 'Copper Ingot', 1),
    (4, 'Silver Dust', 1), (4, 'Copper Dust', 1), (4, 'Silver Ingot', 1),
    (5, 'Iron Dust', 1), (5, 'Iron Ingot', 1), (5, 'Copper Dust', 1),
    (6, 'Aluminum Dust', 1), (6, 'Copper Dust', 1), (6, 'Aluminum Ingot', 1),
    (7, 'Gold Ingot (24k)', 1), (7, 'Iron Dust', 1),
    (8, 'Iron Dust', 1), (8, 'Copper Dust', 1), (8, 'Nickel Ingot', 1),
    (9, 'Iron Ingot', 1), (9, 'Iron Dust', 1), (9, 'Silicon', 1),
    (10, 'Aluminum Dust', 1), (10, 'Brass Ingot', 1), (10, 'Aluminum Ingot', 1),
    (11, 'Aluminum Dust', 1), (11, 'Bronze Ingot', 1), (11, 'Aluminum Ingot', 1),
    (12, 'Silver Dust', 1), (12, 'Gold Dust', 1), (12, 'Copper Dust', 1), (12, 'Bronze Ingot', 1),
    (13, 'Steel Ingot', 1), (13, 'Iron Dust', 1), (13, 'Carbon', 1), (13, 'Iron Ingot', 1),
    (14, 'Lead Dust', 1), (14, 'Tin Dust', 1), (14, 'Lead Ingot', 1),
    (15, 'Damascus Steel Ingot', 1), (15, 'Duralumin Ingot', 1), (15, 'Compressed Coal', 1), (15, 'Aluminum Bronze Ingot', 1),
    (16, 'Redstone Dust', 1), (16, 'Redstone Block', 1), (16, 'Ferrosilicon', 1), (16, 'Hardened Metal', 1),
    (17, 'Damascus Steel Ingot', 1), (17, 'Hardened Metal', 1), (17, 'Corinthian Bronze Ingot', 1), (17, 'Solder Ingot', 1), (17, 'Billon Ingot', 1), (17, 'Gold Ingot (24k)', 1)
]
c.executemany('INSERT INTO Ingredientes (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)', ingredientes)

# Insertar datos de ejemplo en la tabla de dependencias
dependencias = [
    (10, 3),  # Aluminum Brass Ingot depende de Brass Ingot
    (11, 2),  # Aluminum Bronze Ingot depende de Bronze Ingot
    (12, 2),  # Corinthian Bronze Ingot depende de Bronze Ingot
    (13, 1),  # Damascus Steel Ingot depende de Steel Ingot
    (15, 11), # Hardened Metal depende de Aluminum Bronze Ingot
    (15, 13), # Hardened Metal depende de Damascus Steel Ingot
    (16, 9),  # Redstone Alloy Ingot depende de Ferrosilicon
    (17, 4),  # Reinforced Alloy Ingot depende de Billon Ingot
    (17, 12), # Reinforced Alloy Ingot depende de Corinthian Bronze Ingot
    (17, 13), # Reinforced Alloy Ingot depende de Damascus Steel Ingot
    (17, 15), # Reinforced Alloy Ingot depende de Hardened Metal
    (17, 14)  # Reinforced Alloy Ingot depende de Solder Ingot
]
c.executemany('INSERT INTO Dependencias (aleacion_id, depende_de_id) VALUES (?, ?)', dependencias)

# Insertar datos de ejemplo en la tabla de ingredientes totales
ingredientes_totales = [
    (1, 'Iron Dust', 2), (1, 'Coal', 9),
    (2, 'Copper Dust', 2), (2, 'Tin Dust', 1),
    (3, 'Copper Dust', 2), (3, 'Zinc Dust', 1),
    (4, 'Silver Dust', 2), (4, 'Copper Dust', 1),
    (5, 'Iron Dust', 2), (5, 'Copper Dust', 1),
    (6, 'Aluminum Dust', 2), (6, 'Copper Dust', 1),
    (7, 'Gold Dust', 1), (7, 'Iron Dust', 1),
    (8, 'Iron Dust', 3), (8, 'Copper Dust', 2),
    (9, 'Iron Dust', 2), (9, 'Quartz Block', 1),
    (10, 'Aluminum Dust', 2), (10, 'Copper Dust', 2), (10, 'Zinc Dust', 1),
    (11, 'Aluminum Dust', 2), (11, 'Copper Dust', 2), (11, 'Tin Dust', 1),
    (12, 'Silver Dust', 1), (12, 'Gold Dust', 1), (12, 'Copper Dust', 3), (12, 'Tin Dust', 1),
    (13, 'Iron Dust', 4), (13, 'Coal', 16),
    (14, 'Lead Dust', 2), (14, 'Tin Dust', 1),
    (15, 'Iron Dust', 4), (15, 'Aluminum Dust', 4), (15, 'Copper Dust', 3), (15, 'Tin Dust', 1), (15, 'Coal', 48),
    (16, 'Redstone Dust', 10), (16, 'Iron Dust', 6), (16, 'Aluminum Dust', 4), (16, 'Copper Dust', 3), (16, 'Tin Dust', 1), (16, 'Quartz Block', 1), (16, 'Coal', 48),
    (17, 'Iron Dust', 8), (17, 'Aluminum Dust', 4), (17, 'Copper Dust', 7), (17, 'Tin Dust', 3), (17, 'Silver Dust', 3), (17, 'Gold Dust', 12), (17, 'Lead Dust', 2), (17, 'Coal', 64)
]
c.executemany('INSERT INTO IngredientesTotales (aleacion_id, ingrediente, cantidad) VALUES (?, ?, ?)', ingredientes_totales)

# Confirmar y cerrar la conexión
conexion.commit()
conexion.close()