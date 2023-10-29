
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from model.citas_dao import crear_tabla, borrar_tabla
from model.citas_dao import Cita, guardar, listar, editar, eliminar


def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu = barra_menu, width=300, height=300)
    
    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Inicio', menu= menu_inicio)
    
    menu_inicio.add_command(label= 'Crear un registro en DB', command=crear_tabla)
    menu_inicio.add_command(label= 'Eliminar registro en DB', command=borrar_tabla)
    menu_inicio.add_command(label= 'Salir', command=root.destroy)

    barra_menu.add_cascade(label='Consultas')
    barra_menu.add_cascade(label='Configuración')
    barra_menu.add_cascade(label='Ayuda')
    
    
class Frame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.pack()
        self.id_citas = None
        
        self.campos_citas()
        self.desabilitar_campos()
        self.tabla_citas()
        
        self.label_buscar = tk.Label(self, text='Buscar paciente:')
        self.label_buscar.config(font=('Arial', 12, 'bold'))
        self.label_buscar.grid(row=5, column=0, padx=10, pady=10)

        self.mi_busqueda = tk.StringVar()
        self.entry_busqueda = tk.Entry(self, textvariable=self.mi_busqueda)
        self.entry_busqueda.config(width=30, font=('Arial', 12))
        self.entry_busqueda.grid(row=5, column=1, padx=10, pady=10, columnspan=2)

        self.boton_buscar = tk.Button(self, text="Buscar", command=self.buscar_pacientes)
        self.boton_buscar.config(width=10, font=('Arial', 12, 'bold'), fg='white', bg='green',
                                cursor='hand2', activebackground='darkgreen', activeforeground='white')
        self.boton_buscar.grid(row=5, column=3, padx=10, pady=10)

    def buscar_pacientes(self, event=None):
        nombre_a_buscar = self.mi_busqueda.get().strip().lower()
        citas_filtradas = []
        
        if not nombre_a_buscar:
        # Si el campo de búsqueda está vacío, muestra todos los pacientes nuevamente.
            self.tabla_citas()
        else:
        # Filtra la lista de citas para mostrar solo las coincidencias con el nombre.
            citas_filtradas = [cita for cita in self.lista_citas if cita[1] and nombre_a_buscar in cita[1].strip().lower()]
        
        if citas_filtradas:
            self.tabla.delete(*self.tabla.get_children())  # Borra los elementos existentes en la tabla
            for p in citas_filtradas:
                self.tabla.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4]))
        else:
            titulo = 'Búsqueda de pacientes'
            mensaje = f'No se encontraron pacientes con el nombre "{nombre_a_buscar}".'
            messagebox.showinfo(titulo, mensaje)
            
    
    def campos_citas(self):
        self.label_nombre = tk.Label(self, text = 'Nombre: ')
        self.label_nombre.config(font=('Arial', 12, 'bold'))
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)
        
        self.label_telefono = tk.Label(self, text = 'Telefono: ')
        self.label_telefono.config(font=('Arial', 12, 'bold'))
        self.label_telefono.grid(row=1, column=0, padx=10, pady=10)
        
        self.label_cita = tk.Label(self, text = 'Motivo de cita:  ')
        self.label_cita.config(font=('Arial', 12, 'bold'))
        self.label_cita.grid(row=2, column=0, padx=10, pady=10)
        
        self.label_calendario = tk.Label(self, text = 'Calendario: ')
        self.label_calendario.config(font=('Arial', 12, 'bold'))
        self.label_calendario.grid(row=3, column=0, padx=10, pady=10)
        
        #Entradas de cada campo
        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable= self.mi_nombre)
        self.entry_nombre.config(width=50, font=('Arial', 12))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2) 
        
        self.mi_telefono = tk.StringVar()
        self.entry_telefono = tk.Entry(self, textvariable=self.mi_telefono)
        self.entry_telefono.config(width=50, font=('Arial', 12))
        self.entry_telefono.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.mi_cita = tk.StringVar()
        self.entry_cita = tk.Entry(self, textvariable=self.mi_cita)
        self.entry_cita.config(width=50, font=('Arial', 12))
        self.entry_cita.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
        
        #calendario

        self.calendario = ttk.DateEntry(self)
        self.calendario.grid(row =3, column =1 , padx=10, pady=10, columnspan=2) 
        
        #Botones
        self.boton_nuevo = tk.Button(self, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=('Arial', 12, 'bold'), fg= '#4D4D4D', bg='#7FFFD4',
                                cursor='hand2', activebackground='#66CDAA', activeforeground='#008080')
        self.boton_nuevo.grid(row=4, column=0, padx=10, pady=10 )
        
        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_datos)
        self.boton_guardar.config(width=20, font=('Arial', 12, 'bold'), fg= '#4D4D4D', bg='#7FFFD4',
                                cursor='hand2', activebackground='#66CDAA', activeforeground='#008080')
        self.boton_guardar.grid(row=4, column=1, padx=10, pady=10 )
        
        self.boton_cancelar = tk.Button(self, text="Cancelar", command=self.desabilitar_campos)
        self.boton_cancelar.config(width=20, font=('Arial', 12, 'bold'), fg= '#4D4D4D', bg='#7FFFD4',
                                cursor='hand2', activebackground='#66CDAA', activeforeground='#008080')
        self.boton_cancelar.grid(row=4, column=2, padx=10, pady=10 )
         
    def habilitar_campos(self):
        self.mi_nombre.set('')
        self.mi_telefono.set('')
        self.mi_cita.set('')
       
        
        self.entry_nombre.config(state='normal')
        self.entry_telefono.config(state='normal')
        self.entry_cita.config(state='normal')
        
        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')
        
    def desabilitar_campos(self):
        self.id_citas = None
        
        self.mi_nombre.set('')
        self.mi_telefono.set('')
        self.mi_cita.set('')
        
        
        self.entry_nombre.config(state='disabled')
        self.entry_telefono.config(state='disabled')
        self.entry_cita.config(state='disabled')
        
            
        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')
        
    def guardar_datos(self):
        
        cita = Cita(
            self.mi_nombre.get(),
            self.mi_telefono.get(),
            self.mi_cita.get(),
            self.calendario.entry.get()
             
        )
        if self.id_citas == None:
            guardar(cita)
        else:
            editar(cita, self.id_citas)
            
    
        self.tabla_citas()
        
        
        #Desabilitar campos
        self.desabilitar_campos()
        
    def tabla_citas(self):
        #Recuperar la lista de citas
        self.lista_citas = listar()
        self.lista_citas.reverse()
        
        
        self.tabla = ttk.Treeview(self, 
        column = ('Nombre', 'Telefono', 'Motivo de Cita', 'Calendario'))
        self.tabla.grid(row=6, column=0, columnspan= 5, sticky='nse')

        #Scrollbar para la tabla si existe 10 registros
        self.scroll = tk.Scrollbar(self, orient = 'vertical', command= self.tabla.yview)
        self.scroll.grid(row=6, column= 5, sticky='nse')
        self.tabla.configure(yscrollcommand= self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='NOMBRE')
        self.tabla.heading('#2', text='TELEFONO')
        self.tabla.heading('#3', text='MOTIVO DE CITA')
        self.tabla.heading('#4', text='FECHA')
    
        #Iterar la lista de citas
        for p in self.lista_citas:
            
            self.tabla.insert('',0, text=p[0],
            values=(p[1], p[2], p[3], p[4]))
        
        #Botones abajo
        self.boton_editar = tk.Button(self, text="Editar", command=self.editar_datos)
        self.boton_editar.config(width=20, font=('Arial', 12, 'bold'), fg= 'white', bg='#327DD3',
                                cursor='hand2', activebackground='#191970')
        self.boton_editar.grid(row=7, column= 1, padx=10, pady=10 )
        
        self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.elimiar_datos)
        self.boton_eliminar.config(width=20, font=('Arial', 12, 'bold'), fg= 'white', bg='#E32714',
                                cursor='hand2', activebackground='#89190E')
        self.boton_eliminar.grid(row=7, column=0, padx=10, pady=10 )
    
    def crear_calendario(self):
        def print_sel():
            print(cal.selection_get())
        top = tk.Toplevel(self)
        cal = calendar(top, font="Arial 14", selectmode='day', cursor="hand1")
        cal.grid(row=3, column=1, padx=10, pady=10, columnspan=2)
        ttk.Button(top, text="ok", command=print_sel).grid()
        
    def editar_datos(self):
        try:
            self.id_citas = self.tabla.item(self.tabla.selection())['text']
            self.nombre_cita = self.tabla.item(self.tabla.selection())['values'][0]
            self.telefono_cita = self.tabla.item(self.tabla.selection())['values'][1]
            self.motivo_cita = self.tabla.item(self.tabla.selection())['values'][2]
            self.celendario_cita = self.tabla.item(self.tabla.selection())['values'][3]
            
            self.habilitar_campos()
            self.entry_nombre.insert(0, self.nombre_cita)
            self.entry_telefono.insert(0, self.telefono_cita)
            self.entry_cita.insert(0, self.motivo_cita)
           
            
        except:
            titulo = 'Edición de datos'
            mensaje = 'No ha seleccionado ningun registro'
            messagebox.showerror(titulo, mensaje)
            
    def elimiar_datos(self):
        try:
            self.id_citas = self.tabla.item(self.tabla.selection())['text']
            eliminar(self.id_citas)
            
            self.tabla_citas()
            self.id_citas = None
            
        except:
            titulo = 'Eliminar un registro '
            mensaje = 'No ha seleccionado ningun registro'