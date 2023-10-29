from .conexion_db import ConexionDB
from tkinter import messagebox

def crear_tabla():
    conexion = ConexionDB()
    
    sql = '''
    CREATE TABLE citas(
        id_citas INTEGER,
        nombre VARCHAR(100),
        telefono VARCHAR(20),
        motivo VARCHAR(200),
        calendario VARCHAR(15),
        PRIMARY KEY(id_citas AUTOINCREMENT)
    )'''  
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Crear Registro'
        mensaje = 'Se creo la tabla en la base datos'
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = 'Crear Registro'
        mensaje = 'La tabla ya esta creada'
        messagebox.showwarning(titulo, mensaje)
        
    
def borrar_tabla():
    conexion = ConexionDB()
    
    sql = 'DROP TABLE citas'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Borrar Registro'
        mensaje = 'La tabla de la base de datos se borro con éxito'
        messagebox.showwarning(titulo, mensaje)
    except:
        titulo = 'Borrar Registro'
        mensaje = 'No hay tabla parar borrar'
        messagebox.showerror(titulo, mensaje)
        
class Cita:
    def __init__(self, nombre, telefono, motivo, calendario):
        self.id_citas = None
        self.nombre = nombre
        self.telefono = telefono
        self.motivo = motivo
        self.calendario = calendario
        
    def __str__(self):
        return f'Cita[{self.nombre}, {self.telefono}, {self.motivo}, {self.calendario}]'
        

def guardar(cita):
    conexion = ConexionDB()
    
    sql = f"""INSERT INTO citas (nombre, telefono, motivo, calendario)
    VALUES('{cita.nombre}', '{cita.telefono}', '{cita.motivo}', '{cita.calendario}')"""
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = 'Conexion al Registro'
        mensaje = 'La tabla citas no esta creada en la base de datos'
        messagebox.showerror(titulo, mensaje)
        
def listar():
    conexion = ConexionDB()
    
    lista_citas =[]
    sql = 'SELECT * FROM citas'
    
    try:
        conexion.cursor.execute(sql)
        lista_citas = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexion al Registro'
        mensaje = 'Crea la tabla en la Base de datos'
        messagebox.showerror(titulo, mensaje)
        
    return lista_citas
        
def editar(cita, id_citas):
    conexion = ConexionDB()
    
    sql = f"""UPDATE citas
    SET nombre = '{cita.nombre}', telefono = '{cita.telefono}',
    motivo = '{cita.motivo}', calendario = '{cita.calendario}'
    WHERE id_citas = {id_citas}"""
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        
    except:
        titulo = 'Edición de datos'
        mensaje = 'No se apodido editar este registro'
        messagebox.showerror(titulo, mensaje)
        
def eliminar(id_citas):
    conexion = ConexionDB()
    sql = f'DELETE FROM citas WHERE id_citas = {id_citas}'
            
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        
    except:
        titulo = 'Eliminar Datos'
        mensaje = 'No se pudo eliminar el registro'
        messagebox.showerror(titulo, mensaje)
        
        