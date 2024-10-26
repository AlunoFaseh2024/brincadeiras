import os
import hashlib
import shutil
from PIL import Image
import pyzbar.pyzbar as pyzbar
import fitz  # PyMuPDF

def decode_qr_code(image):
    decoded_objects = pyzbar.decode(image)
    if not decoded_objects:
        return None
    return decoded_objects[0].data.decode('utf-8')

def recreate_original_file(pdf_path):
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Converter as páginas do PDF em imagens usando PyMuPDF
    doc = fitz.open(pdf_path)
    guide_data = None
    qr_data_list = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extrair a imagem na qualidade original
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Aumenta a resolução para 200 DPI
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Decodificar QR codes na imagem
        qr_codes = pyzbar.decode(img)
        print(f"Página {page_num + 1}: {len(qr_codes)} QR codes encontrados.")
        
        for qr_code in qr_codes:
            qr_data = qr_code.data.decode('utf-8')
            #print(f"QR Code encontrado: {qr_data}")  # Debug: Mostra o QR code encontrado
            if qr_data.startswith('0-'):
                guide_data = qr_data[2:]
            else:
                qr_data_list.append(qr_data)

    if not guide_data:
        raise ValueError("Guide QR code not found.")

    # Extrair informações do guia
    guide_parts = guide_data.split(" | ")
    file_name = guide_parts[0].split("{")[1].split("}")[0]
    file_md5 = guide_parts[1].split("(")[1].split(")")[0]
    total_parts = int(guide_parts[2].split("[")[1].split("]")[0])

    print(f"Total de partes esperadas: {total_parts}")
    print(f"Total de QR codes encontrados: {len(qr_data_list)}")

    if len(qr_data_list) != total_parts:
        raise ValueError("Não foi encontrado/escaneado todos os Qr Codes")

    # Recriar os arquivos binários temporários
    for qr_data in qr_data_list:
        part_num, bin_data = qr_data.split("-", 1)
        part_num = int(part_num)
        with open(os.path.join(temp_dir, f"{part_num}.bin"), 'wb') as bin_file:
            bin_file.write(bin_data.encode('latin1'))  # Use 'latin1' to write raw binary data

    # Reconstituir o arquivo original
    with open(file_name, 'wb') as output_file:
        for i in range(1, total_parts + 1):
            bin_path = os.path.join(temp_dir, f"{i}.bin")
            with open(bin_path, 'rb') as bin_file:
                output_file.write(bin_file.read())

    # Verificar o hash MD5 do arquivo reconstituído
    def calculate_md5(file_path):
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b''):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

    reconstructed_md5 = calculate_md5(file_name)
    if reconstructed_md5 != file_md5:
        raise ValueError("MD5 hash does not match. File might be corrupted.")

    # Limpar arquivos temporários
    shutil.rmtree(temp_dir)
    print("Arquivo reconstituído com sucesso e verificado com hash MD5!")

# Exemplo de uso
pdf_path = 'output.pdf'
recreate_original_file(pdf_path)
