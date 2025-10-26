import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from decodificador import decodificar_archivo

class DecodificadorMIPSApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Decodificador MIPS - Instrucciones Tipo R")
        self.root.geometry("800x600")
        
        # Variables para almacenar datos
        self.lineas_originales = []
        self.instrucciones_bin = []
        self.bytes_salida = []
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título principal
        titulo = tk.Label(self.root, text="DECODIFICADOR MIPS - INSTRUCCIONES TIPO R", 
                         font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Frame para las 3 pantallas
        frame_pantallas = tk.Frame(self.root)
        frame_pantallas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # PANEL 1: Código Assembly Original (.asm)
        frame_asm = tk.LabelFrame(frame_pantallas, text="1. Código Assembly Original", 
                                 font=("Arial", 10, "bold"))
        frame_asm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.texto_asm = scrolledtext.ScrolledText(frame_asm, height=15, width=25)
        self.texto_asm.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_asm, text="Archivo .asm cargado aquí", 
                fg="gray").pack()
        
        # PANEL 2: Instrucciones Limpias
        frame_limpias = tk.LabelFrame(frame_pantallas, text="2. Instrucciones Procesadas", 
                                     font=("Arial", 10, "bold"))
        frame_limpias.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.texto_limpias = scrolledtext.ScrolledText(frame_limpias, height=15, width=25)
        self.texto_limpias.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_limpias, text="Instrucciones listas para decodificar", 
                fg="gray").pack()
        
        # PANEL 3: Código Binario
        frame_binario = tk.LabelFrame(frame_pantallas, text="3. Código Binario Resultante", 
                                     font=("Arial", 10, "bold"))
        frame_binario.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.texto_binario = scrolledtext.ScrolledText(frame_binario, height=15, width=35)
        self.texto_binario.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_binario, text="Resultado en binario/hexadecimal", 
                fg="gray").pack()
        
        # Frame para los 4 botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        
        # BOTÓN 1: Cargar Archivo
        btn_cargar = tk.Button(frame_botones, text="📁 Cargar Archivo .asm", 
                              command=self.cargar_archivo, width=15, height=2,
                              bg="lightblue", font=("Arial", 10))
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        # BOTÓN 2: Decodificar
        btn_decodificar = tk.Button(frame_botones, text="⚡ Decodificar", 
                                   command=self.decodificar, width=15, height=2,
                                   bg="lightgreen", font=("Arial", 10))
        btn_decodificar.pack(side=tk.LEFT, padx=5)
        
        # BOTÓN 3: Limpiar
        btn_limpiar = tk.Button(frame_botones, text="🧹 Limpiar Todo", 
                               command=self.limpiar_todo, width=15, height=2,
                               bg="lightyellow", font=("Arial", 10))
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # BOTÓN 4: Guardar Resultado
        btn_guardar = tk.Button(frame_botones, text="💾 Guardar instrucciones.txt", 
                               command=self.guardar_resultado, width=20, height=2,
                               bg="lightcoral", font=("Arial", 10))
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        # Área de estado
        self.estado = tk.Label(self.root, text="Listo para cargar archivo .asm", 
                              relief=tk.SUNKEN, anchor=tk.W, bg="white")
        self.estado.pack(fill=tk.X, side=tk.BOTTOM)
    
    def cargar_archivo(self):
        """BOTÓN 1: Carga el archivo .asm y muestra en panel 1"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo MIPS .asm",
            filetypes=[("Archivos assembly", "*.asm"), ("Archivos texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                with open(archivo, 'r') as f:
                    contenido = f.read()
                
                # Mostrar en panel 1
                self.texto_asm.delete(1.0, tk.END)
                self.texto_asm.insert(1.0, contenido)
                
                # Limpiar los otros paneles
                self.texto_limpias.delete(1.0, tk.END)
                self.texto_binario.delete(1.0, tk.END)
                
                self.estado.config(text=f"Archivo cargado: {archivo}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
    
    def decodificar(self):
        """BOTÓN 2: Decodifica las instrucciones y muestra en paneles 2 y 3"""
        contenido = self.texto_asm.get(1.0, tk.END).strip()
        if not contenido:
            messagebox.showwarning("Advertencia", "No hay contenido para decodificar")
            return
        
        try:
            # Usar nuestro decodificador
            self.lineas_originales, self.instrucciones_bin, self.bytes_salida = decodificar_archivo(contenido)
            
            # PANEL 2: Mostrar instrucciones limpias
            self.texto_limpias.delete(1.0, tk.END)
            instrucciones_limpias = []
            
            for linea in self.lineas_originales:
                limpia = linea.strip()
                if limpia and not limpia.startswith('#'):
                    instrucciones_limpias.append(limpia)
            
            self.texto_limpias.insert(1.0, '\n'.join(instrucciones_limpias))
            
            # PANEL 3: Mostrar código binario
            self.texto_binario.delete(1.0, tk.END)
            
            for i, (linea, inst_bin) in enumerate(zip(self.lineas_originales, self.instrucciones_bin)):
                if inst_bin is not None:
                    # Formato: Binario (32 bits) y Hexadecimal
                    bin_str = format(inst_bin, '032b')
                    hex_str = format(inst_bin, '08X')
                    
                    # Mostrar en grupos para mejor lectura
                    bin_formateado = f"{bin_str[:6]}_{bin_str[6:11]}_{bin_str[11:16]}_{bin_str[16:21]}_{bin_str[21:26]}_{bin_str[26:32]}"
                    
                    self.texto_binario.insert(tk.END, f"Línea {i+1}:\n")
                    self.texto_binario.insert(tk.END, f"Bin:  {bin_formateado}\n")
                    self.texto_binario.insert(tk.END, f"Hex:  0x{hex_str}\n")
                    self.texto_binario.insert(tk.END, "-" * 40 + "\n")
                else:
                    self.texto_binario.insert(tk.END, f"Línea {i+1}: ERROR o línea vacía\n")
                    self.texto_binario.insert(tk.END, "-" * 40 + "\n")
            
            instrucciones_validas = len([x for x in self.instrucciones_bin if x is not None])
            self.estado.config(text=f"Decodificación completada. {instrucciones_validas} instrucciones procesadas.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en decodificación:\n{e}")
    
    def limpiar_todo(self):
        """BOTÓN 3: Limpia todas las pantallas"""
        self.texto_asm.delete(1.0, tk.END)
        self.texto_limpias.delete(1.0, tk.END)
        self.texto_binario.delete(1.0, tk.END)
        
        self.lineas_originales = []
        self.instrucciones_bin = []
        self.bytes_salida = []
        
        self.estado.config(text="Todo limpiado. Listo para nuevo archivo.")
    
    def guardar_resultado(self):
        """BOTÓN 4: Guarda el resultado en instrucciones.txt SOLO con 0s y 1s (32 bits por línea)"""
        if not self.bytes_salida:
            messagebox.showwarning("Advertencia", "No hay datos para guardar. Decodifica primero.")
            return
        
        try:
            archivo_salida = filedialog.asksaveasfilename(
                title="Guardar instrucciones.txt",
                defaultextension=".txt",
                filetypes=[("Archivo texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if archivo_salida:
                with open(archivo_salida, 'w') as f:
                    # Instrucciones de 32 bits (una por línea)
                    for i in range(0, len(self.bytes_salida), 4):
                        instruccion_bytes = self.bytes_salida[i:i+4]
                        # Reconstruir instrucción de 32 bits
                        instruccion_32bits = 0
                        for j, byte in enumerate(instruccion_bytes):
                            instruccion_32bits |= (byte << (24 - j * 8))
                        # Escribir SOLO los 32 bits
                        f.write(f"{instruccion_32bits:032b}\n")
                
                self.estado.config(text=f"Archivo guardado: {archivo_salida}")
                messagebox.showinfo("Éxito", f"Archivo guardado como:\n{archivo_salida}\n\nFormato: 32 bits por línea, solo 0s y 1s")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

if __name__ == "__main__":
    app = DecodificadorMIPSApp()
    app.root.mainloop()