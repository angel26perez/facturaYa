import sqlite3
from config import DB_NAME


def conectar():
    return sqlite3.connect(DB_NAME)


# CREAR TABLAS
def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # PRODUCTOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        codigo TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

    # CLIENTES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipo_documento TEXT,
        documento TEXT,
        telefono TEXT,
        direccion TEXT,
        sexo TEXT,
        email TEXT
    )
    """)

    # PROVEEDORES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        nit TEXT,
        telefono TEXT,
        direccion TEXT
    )
    """)

    # VENTAS (Con soporte para clientes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_venta TEXT NOT NULL,
        fecha TEXT NOT NULL,
        vendedor TEXT NOT NULL,
        cliente_id INTEGER,
        cliente_nombre TEXT DEFAULT 'Cliente No Frecuente',
        subtotal REAL NOT NULL,
        descuento REAL NOT NULL,
        iva REAL NOT NULL,
        total REAL NOT NULL,
        metodo_pago TEXT NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )
    """)

    # DETALLE DE VENTA
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL,
        codigo_producto TEXT NOT NULL,
        producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (venta_id) REFERENCES ventas (id)
    )
    """)

    conn.commit()
    conn.close()


# PRODUCTOS DE PRUEBA
def insertar_productos_prueba():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        productos = [
            # Bebidas y Snacks
            ("1001", "Coca Cola 400ml", 3500, 150),
            ("1002", "Galletas Oreo 36g", 2000, 80),
            ("1003", "Papas Margarita Natural 45g", 2500, 60),
            ("1004", "Jugo Hit Mora 500ml", 3000, 90),
            ("1005", "Agua Brisa Sin Gas 600ml", 2000, 100),
            ("1006", "Cerveza Poker Lata 330ml", 3800, 200),
            ("1007", "Chocolatina Jet 12g", 700, 300),
            # Lácteos y Despensa
            ("2001", "Leche Alpina Entera 1L", 5000, 70),
            ("2002", "Arroz Diana 500g", 2800, 120),
            ("2003", "Aceite Gourmet 900ml", 14500, 45),
            ("2004", "Pan Tajado Bimbo Blanco", 6500, 30),
            ("2005", "Café Sello Rojo 250g", 8900, 50),
            ("2006", "Azúcar Incauca 1kg", 4200, 85),
            ("2007", "Huevo AA Rojo (Cubeta x30)", 18000, 25),
            ("2008", "Mantequilla Colanta 250g", 7800, 40),
            ("2009", "Atún Van Camp's en Agua", 7200, 65),
            # Aseo y Cuidado Personal
            ("3001", "Jabón Rey 300g", 2200, 110),
            ("3002", "Detergente Fab 1kg", 11500, 40),
            ("3003", "Crema Dental Colgate 100ml", 6800, 55),
            ("3004", "Papel Higiénico Familia (4 rollos)", 8500, 50),
            ("3005", "LAVAPLATOS AXION Crema 450g", 5400, 35),
        ]

        cursor.executemany(
            "INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)",
            productos,
        )
        conn.commit()
    conn.close()


# OPERACIONES PRODUCTOS
def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT codigo, nombre, precio, stock 
        FROM productos 
        ORDER BY CAST(codigo AS INTEGER) ASC
    """)
    datos = cursor.fetchall()
    conn.close()
    return datos


def buscar_producto(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT codigo, nombre, precio, stock FROM productos WHERE codigo = ?",
        (codigo,),
    )
    producto = cursor.fetchone()
    conn.close()
    return producto


def agregar_producto(codigo, nombre, precio, stock):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)",
            (codigo, nombre, precio, stock),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def actualizar_producto(codigo, nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE codigo = ?",
        (nombre, precio, stock, codigo),
    )
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado


def eliminar_producto(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
    eliminado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return eliminado


def descontar_stock(codigo, cantidad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET stock = stock - ? WHERE codigo = ? AND stock >= ?",
        (cantidad, codigo, cantidad),
    )
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado


def aumentar_stock(codigo, cantidad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET stock = stock + ? WHERE codigo = ?",
        (cantidad, codigo),
    )
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado


# CONTEOS DASHBOARD
def total_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def total_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def total_proveedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM proveedores")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def total_ventas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ventas")
    total = cursor.fetchone()[0]
    conn.close()
    return total


# OPERACIONES VENTAS
def registrar_venta(
    numero_venta,
    fecha,
    vendedor,
    cliente_id,
    cliente_nombre,
    subtotal,
    descuento,
    iva,
    total,
    metodo_pago,
):
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO ventas (
                numero_venta, fecha, vendedor, cliente_id, cliente_nombre, 
                subtotal, descuento, iva, total, metodo_pago
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                numero_venta,
                fecha,
                vendedor,
                cliente_id,
                cliente_nombre,
                subtotal,
                descuento,
                iva,
                total,
                metodo_pago,
            ),
        )

        venta_id = cursor.lastrowid
        conexion.commit()
        return venta_id
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()


def registrar_detalle(
    venta_id, codigo_producto, producto, cantidad, precio, subtotal
):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO detalle_venta (venta_id, codigo_producto, producto, cantidad, precio, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (venta_id, codigo_producto, producto, cantidad, precio, subtotal),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def registrar_venta_completa(
    numero_venta,
    fecha,
    vendedor,
    cliente_id,
    cliente_nombre,
    subtotal,
    descuento,
    iva,
    total,
    metodo_pago,
    carrito,
):
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO ventas (
                numero_venta, fecha, vendedor, cliente_id, cliente_nombre, 
                subtotal, descuento, iva, total, metodo_pago
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                numero_venta,
                fecha,
                vendedor,
                cliente_id,
                cliente_nombre,
                subtotal,
                descuento,
                iva,
                total,
                metodo_pago,
            ),
        )
        venta_id = cursor.lastrowid

        for item in carrito:
            codigo = item["codigo"]
            nombre = item["nombre"]
            cantidad = item["cantidad"]
            precio = item["precio"]
            subtotal_item = item["subtotal"]

            cursor.execute(
                "SELECT stock FROM productos WHERE codigo = ?", (codigo,)
            )
            resultado = cursor.fetchone()

            if not resultado:
                raise Exception(f"El producto {codigo} ya no existe.")

            stock_actual = int(resultado[0])
            if stock_actual < cantidad:
                raise Exception(
                    f"Stock insuficiente para {nombre}. Disponible: {stock_actual}, Solicitado: {cantidad}"
                )

            cursor.execute(
                """
                INSERT INTO detalle_venta (venta_id, codigo_producto, producto, cantidad, precio, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    venta_id,
                    codigo,
                    nombre,
                    cantidad,
                    precio,
                    subtotal_item,
                ),
            )

            cursor.execute(
                "UPDATE productos SET stock = stock - ? WHERE codigo = ?",
                (cantidad, codigo),
            )

        conexion.commit()
        return venta_id
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()


def obtener_ventas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, numero_venta, fecha, vendedor, subtotal, descuento, iva, total, metodo_pago 
        FROM ventas 
        ORDER BY fecha DESC
    """)
    ventas = cursor.fetchall()
    conn.close()
    return ventas


def obtener_detalle_venta(venta_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, venta_id, codigo_producto, producto, cantidad, precio, subtotal 
        FROM detalle_venta 
        WHERE venta_id = ?
    """,
        (venta_id,),
    )
    detalle = cursor.fetchall()
    conn.close()
    return detalle


def total_ventas_dinero():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM ventas")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def productos_bajo_stock(limite=10):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT codigo, nombre, precio, stock 
        FROM productos 
        WHERE stock <= ? 
        ORDER BY stock ASC
    """,
        (limite,),
    )
    datos = cursor.fetchall()
    conn.close()
    return datos


# CONSULTAS AVANZADAS DASHBOARD
def productos_mas_vendidos(limite=5):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT producto, SUM(cantidad) as total_vendido
        FROM detalle_venta
        GROUP BY codigo_producto
        ORDER BY total_vendido DESC
        LIMIT ?
    """,
        (limite,),
    )
    datos = cursor.fetchall()
    conn.close()
    return datos


def ultimas_ventas(limite=5):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT numero_venta, fecha, total, metodo_pago
        FROM ventas
        ORDER BY id DESC
        LIMIT ?
    """,
        (limite,),
    )
    datos = cursor.fetchall()
    conn.close()
    return datos


def resumen_inventario():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*), COALESCE(SUM(stock), 0), COALESCE(SUM(precio * stock), 0) FROM productos"
    )
    resumen = cursor.fetchone()
    conn.close()
    return {
        "total_items": resumen[0],
        "total_unidades": resumen[1],
        "valor_inventario": resumen[2],
    }


# CLIENTES
def insertar_clientes_prueba():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        clientes = [
            (
                "Carlos Mendoza",
                "Cédula de Ciudadanía",
                "1045238901",
                "Masculino",
                "3001234567",
                "Calle 45 #12-34",
                "carlos.mendoza@gmail.com",
            ),
            (
                "María Fernanda Gómez",
                "Cédula de Ciudadanía",
                "1082940123",
                "Femenino",
                "3159876543",
                "Carrera 10 #5-20",
                "mafe.gomez@hotmail.com",
            ),
            (
                "Comercializadora El Sol SAS",
                "NIT",
                "900123456-1",
                "Otro / LGBT+",
                "6053501122",
                "Zona Industrial Lt 4",
                "ventas@elsol.com",
            ),
            (
                "Andrés Felipe Ruiz",
                "Tarjeta de Identidad",
                "1098765432",
                "Masculino",
                "3024567890",
                "Av. Circunvalar #88-12",
                "andres.ruiz@yahoo.com",
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO clientes (nombre, tipo_documento, documento, sexo, telefono, direccion, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            clientes,
        )
        conn.commit()
    conn.close()


def obtener_o_crear_cliente_defecto():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre FROM clientes WHERE nombre = 'Cliente No Frecuente'"
    )
    cliente = cursor.fetchone()

    if not cliente:
        cursor.execute(
            """
            INSERT INTO clientes (nombre, tipo_documento, documento, sexo, telefono, direccion, email)
            VALUES ('Cliente No Frecuente', 'N/A', '000000000', 'Otro', 'N/A', 'N/A', 'N/A')
        """
        )
        conn.commit()
        cliente_id = cursor.lastrowid
        cliente_nombre = "Cliente No Frecuente"
    else:
        cliente_id, cliente_nombre = cliente[0], cliente[1]

    conn.close()
    return cliente_id, cliente_nombre


def obtener_ventas_por_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT numero_venta, fecha, vendedor, total, metodo_pago
        FROM ventas
        WHERE cliente_id = ?
        ORDER BY fecha DESC
    """,
        (cliente_id,),
    )
    ventas = cursor.fetchall()
    conn.close()
    return ventas


# --- CONSULTAS PARA REPORTES ---

def obtener_reporte_ventas_por_fecha(fecha_inicio, fecha_fin):
    """Retorna las ventas dentro de un rango de fechas."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT numero_venta, fecha, cliente_nombre, vendedor, subtotal, iva, total, metodo_pago
        FROM ventas
        WHERE DATE(fecha) BETWEEN DATE(?) AND DATE(?)
        ORDER BY fecha DESC
    """, (fecha_inicio, fecha_fin))
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_ventas_por_metodo_pago():
    """Retorna el total vendido agrupado por método de pago (Efectivo, Tarjeta, Transferencia, etc.)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT metodo_pago, SUM(total) as total_ventas, COUNT(*) as cantidad_transacciones
        FROM ventas
        GROUP BY metodo_pago
        ORDER BY total_ventas DESC
    """)
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_top_clientes_compras(limite=5):
    """Retorna los clientes que más dinero han gastado en el negocio."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cliente_nombre, COUNT(id) as total_compras, SUM(total) as dinero_gastado
        FROM ventas
        GROUP BY cliente_nombre
        ORDER BY dinero_gastado DESC
        LIMIT ?
    """, (limite,))
    datos = cursor.fetchall()
    conn.close()
    return datos