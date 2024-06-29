from flask import Flask, request, jsonify, Response
import xml.etree.ElementTree as ET

app = Flask(__name__)

libros = []

@app.route('/cargarlibros', methods=['POST'])
def cargar_libros():
    entrada_xml = request.data.decode('utf-8')
    root = ET.fromstring(entrada_xml)
    for libro in root.findall('libro'):
        libro_data = {
            'id': libro.attrib['id'],
            'titulo': libro.find('titulo').text,
            'autor': libro.find('autor').text,
            'idioma': libro.find('idioma').text,
            'categoria': libro.find('categoria').text,
            'editorial': libro.find('editorial').text,
            'copias': libro.find('copias').text
        }
        libros.append(libro_data)
    
    return jsonify({'message': 'Libros cargados correctamente'}), 200

@app.route('/verlibros', methods=['GET'])
def ver_libros():
    return jsonify(libros), 200

@app.route('/verlibro/<string:id>', methods=['GET'])
def ver_libro(id):
    libro = next((libro for libro in libros if libro['id'] == id), None)
    if libro:
        libro_xml = ET.Element('libro')
        for key, value in libro.items():
            child = ET.SubElement(libro_xml, key)
            child.text = value
        xml_str = ET.tostring(libro_xml, encoding='unicode')
        return Response(xml_str, mimetype='application/xml'), 200
    return jsonify({'error': 'Libro no encontrado'}), 404

@app.route('/libros/<string:categoria>', methods=['GET'])
def libros_por_categoria(categoria):
    libros_categoria = [libro for libro in libros if libro['categoria'] == categoria]
    return jsonify(libros_categoria), 200

if __name__ == '__main__':
    app.run(debug=True)
