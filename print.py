import os
import win32print
import time
import pygetwindow as gw
from flask import Flask, request, jsonify

app = Flask(__name__)

def print_pdf(pdf_file):
    try:
        # Verificar que el archivo PDF exista
        if not os.path.isfile(pdf_file):
            return jsonify({"error": f"El archivo PDF '{pdf_file}' no existe."}), 404

        # Obtener la impresora predeterminada
        default_printer = win32print.GetDefaultPrinter()

        # Imprimir el archivo PDF usando la impresora predeterminada
        os.startfile(pdf_file, "print")

        # Esperar un tiempo breve para que el visor de PDF tenga tiempo de abrirse
        time.sleep(2)

        # Cerrar el visor de PDF
        for window in gw.getWindowsWithTitle('Adobe Acrobat'):
            window.close()

        return jsonify({"message": f"Se ha enviado la impresión del archivo '{pdf_file}' a la impresora '{default_printer}'. Visor de PDF cerrado."})

    except Exception as e:
        return jsonify({"error": f"Error al imprimir: {e}"}), 500

@app.route('/print/<path:pdf_file>', methods=['GET'])
def print_pdf_url(pdf_file):
    try:
        # Reemplazar '/' por '\' en la ruta del archivo PDF (en caso de ser necesario)
        pdf_file = pdf_file.replace('/', '\\')

        # Imprimir el archivo PDF
        return print_pdf(pdf_file)

    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
