import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd

class Producto:
    def __init__(self, codigo, nombre, precio, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

class Venta:
    def __init__(self):
        self.productos = []
        self.total = 0

    def agregar_producto(self, producto, cantidad):
        if producto.cantidad >= cantidad:
            self.productos.append((producto, cantidad))
            producto.cantidad -= cantidad
            self.total += producto.precio * cantidad
        else:
            messagebox.showerror("Error", "Cantidad insuficiente en inventario.")

class Reporte:
    def __init__(self):
        self.ventas = []

    def registrar_venta(self, venta):
        self.ventas.append(venta)

    def generar_reporte(self):
        total_ventas = sum(venta.total for venta in self.ventas)
        return f"Total Ventas: ${total_ventas}"

class PuntoDeVentaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ferretería Orbe Aguilar - Punto de Venta")
        
        self.reporte = Reporte()
        self.productos = {}
        self.carrito = []
        
        self.crear_interfaz_principal()

    def crear_interfaz_principal(self):
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack()

        self.lbl_producto = tk.Label(self.frame_principal, text="Código de Producto")
        self.lbl_producto.grid(row=0, column=0)
        self.ent_producto = tk.Entry(self.frame_principal)
        self.ent_producto.grid(row=0, column=1)
        
        self.lbl_cantidad = tk.Label(self.frame_principal, text="Cantidad")
        self.lbl_cantidad.grid(row=1, column=0)
        self.ent_cantidad = tk.Entry(self.frame_principal)
        self.ent_cantidad.grid(row=1, column=1)
        
        self.btn_agregar = tk.Button(self.frame_principal, text="Agregar al Carrito", command=self.agregar_al_carrito)
        self.btn_agregar.grid(row=2, column=0, columnspan=2)
        
        self.btn_procesar_venta = tk.Button(self.frame_principal, text="Procesar Venta", command=self.procesar_venta)
        self.btn_procesar_venta.grid(row=3, column=0, columnspan=2)
        
        self.btn_reporte = tk.Button(self.frame_principal, text="Generar Reporte", command=self.generar_reporte)
        self.btn_reporte.grid(row=4, column=0, columnspan=2)

        self.btn_nuevo_producto = tk.Button(self.frame_principal, text="Agregar Producto", command=self.agregar_producto)
        self.btn_nuevo_producto.grid(row=5, column=0, columnspan=2)
        
        self.btn_cargar_excel = tk.Button(self.frame_principal, text="Cargar Productos desde Excel", command=self.cargar_excel)
        self.btn_cargar_excel.grid(row=6, column=0, columnspan=2)

    def agregar_al_carrito(self):
        codigo = self.ent_producto.get()
        cantidad = int(self.ent_cantidad.get())
        
        if codigo in self.productos:
            producto = self.productos[codigo]
            venta = Venta()
            venta.agregar_producto(producto, cantidad)
            self.carrito.append(venta)
            messagebox.showinfo("Éxito", "Producto agregado al carrito.")
        else:
            messagebox.showerror("Error", "Producto no disponible.")

    def procesar_venta(self):
        if not self.carrito:
            messagebox.showerror("Error", "El carrito está vacío.")
            return
        
        for venta in self.carrito:
            self.reporte.registrar_venta(venta)
        
        self.carrito = []
        messagebox.showinfo("Éxito", "Venta procesada exitosamente.")

    def generar_reporte(self):
        reporte = self.reporte.generar_reporte()
        messagebox.showinfo("Reporte de Ventas", reporte)

    def agregar_producto(self):
        ventana_agregar_producto = tk.Toplevel(self.root)
        ventana_agregar_producto.title("Agregar Producto")
        
        lbl_codigo = tk.Label(ventana_agregar_producto, text="Código")
        lbl_codigo.grid(row=0, column=0)
        ent_codigo = tk.Entry(ventana_agregar_producto)
        ent_codigo.grid(row=0, column=1)
        
        lbl_nombre = tk.Label(ventana_agregar_producto, text="Nombre")
        lbl_nombre.grid(row=1, column=0)
        ent_nombre = tk.Entry(ventana_agregar_producto)
        ent_nombre.grid(row=1, column=1)
        
        lbl_precio = tk.Label(ventana_agregar_producto, text="Precio")
        lbl_precio.grid(row=2, column=0)
        ent_precio = tk.Entry(ventana_agregar_producto)
        ent_precio.grid(row=2, column=1)
        
        lbl_cantidad = tk.Label(ventana_agregar_producto, text="Cantidad")
        lbl_cantidad.grid(row=3, column=0)
        ent_cantidad = tk.Entry(ventana_agregar_producto)
        ent_cantidad.grid(row=3, column=1)
        
        btn_guardar = tk.Button(ventana_agregar_producto, text="Guardar", command=lambda: self.guardar_producto(ent_codigo, ent_nombre, ent_precio, ent_cantidad, ventana_agregar_producto))
        btn_guardar.grid(row=4, column=0, columnspan=2)
    
    def guardar_producto(self, ent_codigo, ent_nombre, ent_precio, ent_cantidad, ventana):
        codigo = ent_codigo.get()
        nombre = ent_nombre.get()
        precio = float(ent_precio.get())
        cantidad = int(ent_cantidad.get())
        
        producto = Producto(codigo, nombre, precio, cantidad)
        self.productos[codigo] = producto
        ventana.destroy()
        messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
    
    def cargar_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                codigo = str(row['Código'])
                nombre = row['Nombre']
                precio = row['Precio']
                cantidad = row['Cantidad']
                producto = Producto(codigo, nombre, precio, cantidad)
                self.productos[codigo] = producto
            messagebox.showinfo("Éxito", "Productos cargados desde el archivo Excel.")

# Inicializar la Aplicación
root = tk.Tk()
app = PuntoDeVentaApp(root)
root.mainloop()
