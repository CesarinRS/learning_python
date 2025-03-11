import PyPDF2
import os
from tkinter import Tk, filedialog, messagebox, simpledialog

def seleccionar_pdfs():
    """Abre un cuadro de diálogo para seleccionar múltiples archivos PDF."""
    rutas_pdfs = filedialog.askopenfilenames(
        title="Selecciona los PDFs a dividir",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if rutas_pdfs:
        dividir_pdfs(rutas_pdfs)

def dividir_pdfs(rutas_pdfs):
    """Pregunta al usuario cómo dividir los PDFs y ejecuta la acción."""
    opcion = messagebox.askyesno(
        "Opciones de división",
        "¿Quieres dividir cada página de cada PDF en un archivo separado?"
    )
    salida_carpeta = filedialog.askdirectory(title="Selecciona la carpeta de salida")

    if not salida_carpeta:
        return

    for ruta_pdf in rutas_pdfs:
        lector = PyPDF2.PdfReader(ruta_pdf)
        total_paginas = len(lector.pages)
        nombre_archivo = os.path.basename(ruta_pdf).replace(".pdf", "")

        if opcion:  # Dividir cada página en un archivo separado
            for i in range(total_paginas):
                guardar_pdf(lector, i, i + 1, salida_carpeta, f"{nombre_archivo}_pagina_{i + 1}.pdf")
        else:  # Extraer un rango específico
            inicio = simpledialog.askinteger("Rango", f"{nombre_archivo}: Página de inicio:", minvalue=1, maxvalue=total_paginas)
            fin = simpledialog.askinteger("Rango", f"{nombre_archivo}: Página final:", minvalue=inicio, maxvalue=total_paginas)

            if inicio and fin:
                guardar_pdf(lector, inicio - 1, fin, salida_carpeta, f"{nombre_archivo}_paginas_{inicio}_a_{fin}.pdf")

    messagebox.showinfo("Proceso completado", "La división de los PDFs ha finalizado.")

def guardar_pdf(lector, inicio, fin, carpeta, nombre_archivo):
    """Guarda las páginas seleccionadas en un nuevo PDF."""
    escritor = PyPDF2.PdfWriter()
    for i in range(inicio, fin):
        escritor.add_page(lector.pages[i])

    ruta_salida = os.path.join(carpeta, nombre_archivo)
    with open(ruta_salida, 'wb') as archivo_salida:
        escritor.write(archivo_salida)

    print(f"Archivo creado: {ruta_salida}")

def iniciar_interfaz():
    """Inicializa la ventana principal de tkinter."""
    root = Tk()
    root.withdraw()  # Oculta la ventana principal

    # Abre el selector de archivos al iniciar el programa
    seleccionar_pdfs()

if __name__ == "__main__":
    iniciar_interfaz()