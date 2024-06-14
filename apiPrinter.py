import os
import requests
import tempfile
import win32print
import time
import pygetwindow as gw
from flask import Flask, request, jsonify
from urllib.parse import unquote

app = Flask(__name__)

def download_pdf(pdf_url):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        with open(temp_file.name, 'wb') as f:
            f.write(response.content)
        return temp_file.name
    except Exception as e:
        raise Exception(f"Error al descargar el PDF: {e}")

def print_pdf(pdf_file, printer_name):
    try:
        # Verificar que el archivo PDF exista
        if not os.path.isfile(pdf_file):
            return jsonify({"error": f"El archivo PDF '{pdf_file}' no existe."}), 404

        # Imprimir el archivo PDF usando la impresora especificada
        win32print.SetDefaultPrinter(printer_name)
        os.startfile(pdf_file, "print")

        # Esperar un tiempo breve para que el visor de PDF tenga tiempo de abrirse
        time.sleep(2)

        # Cerrar el visor de PDF
        for window in gw.getWindowsWithTitle('Adobe Acrobat'):
            window.close()

        return jsonify({"message": f"Se ha enviado la impresión del archivo '{pdf_file}' a la impresora '{printer_name}'. Visor de PDF cerrado."})

    except Exception as e:
        return jsonify({"error": f"Error al imprimir: {e}"}), 500

@app.route('/print/<printer_name>/<path:pdf_url>', methods=['GET'])
def print_pdf_url(printer_name, pdf_url):
    try:
        # Decodificar el nombre de la impresora y la URL del PDF
        decoded_printer_name = unquote(printer_name)
        decoded_pdf_url = unquote(pdf_url)

        # Descargar el archivo PDF desde la URL
        pdf_file_path = download_pdf(decoded_pdf_url)

        # Imprimir el archivo PDF
        response = print_pdf(pdf_file_path, decoded_printer_name)

        # Eliminar el archivo temporal
        os.remove(pdf_file_path)

        return response

    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
