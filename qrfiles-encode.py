import os
import hashlib
import shutil
import segno
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# Etapa 1: Selecionar arquivo de entrada
input_file = input("Digite o nome do arquivo de entrada (com extensão): ")

# Função para dividir o arquivo em partes de no máximo 2900 bytes
def split_file(input_file, chunk_size=2900):
    with open(input_file, 'rb') as f:
        part_num = 1
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            with open(f'{part_num}.bin', 'wb') as chunk_file:
                chunk_file.write(chunk)
            part_num += 1
    return part_num - 1

# Etapa 2: Dividir os dados do arquivo em partes de no máximo 2900 bytes
total_parts = split_file(input_file)

# Calcular o hash MD5 do arquivo de entrada
def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

file_md5 = calculate_md5(input_file)

# Etapa 3: Criar o arquivo guia.txt
with open('guia.txt', 'w') as guide_file:
    guide_text = f"NOME:{{{input_file}}} | MD5:({file_md5}) | TOTAL:[{total_parts}]"
    guide_file.write(guide_text)

# Etapa 4: Transformar guia.txt em QR code
with open('guia.txt', 'r') as guide_file:
    guide_data = guide_file.read()

guide_qr = segno.make(f'0-{guide_data}')
guide_qr.save('0.png', scale=10)  # Aumentando a escala para maior resolução

# Função para gerar QR codes dos arquivos .bin
def create_qr_codes(total_parts, correction='L'):
    for i in range(1, total_parts + 1):
        with open(f'{i}.bin', 'rb') as bin_file:
            bin_data = bin_file.read()
        chunk = f'{i}-'.encode('utf-8') + bin_data
        qr = segno.make(chunk, error=correction)
        qr.save(f'{i}.png', scale=10)  # Aumentando a escala para maior resolução

# Etapa 5: Transformar os arquivos .bin em QR codes
create_qr_codes(total_parts)

# Etapa 6: Juntar os QR codes em um único PDF
def create_pdf(total_parts, input_file):
    c = canvas.Canvas("output.pdf", pagesize=A4)
    qr_size = 9 * cm
    margin_top = 0.5 * cm
    margin_left = 1 * cm
    qr_per_page = 6
    qr_per_row = 2
    qr_per_col = 3

    total_pages = (total_parts + qr_per_page) // qr_per_page
    current_page = 1
    qr_count = 0

    for i in range(0, total_parts + 1):
        if qr_count == qr_per_page:
            c.showPage()
            qr_count = 0
            current_page += 1

        row = qr_count // qr_per_row
        col = qr_count % qr_per_row
        x = margin_left + col * (qr_size + margin_left)
        y = A4[1] - margin_top - (row + 1) * (qr_size + margin_top)

        c.drawImage(f'{i}.png', x, y, qr_size, qr_size)

        qr_count += 1

        if qr_count == qr_per_page or i == total_parts:
            footer_text = f"{input_file} | {current_page}/{total_pages}"
            c.drawString(0.2 * cm, 0.2 * cm, footer_text)

    c.save()

create_pdf(total_parts, input_file)

# Etapa 7: Limpar arquivos temporários e exibir mensagem
def clean_up(total_parts):
    os.remove('guia.txt')
    os.remove('0.png')
    for i in range(1, total_parts + 1):
        os.remove(f'{i}.bin')
        os.remove(f'{i}.png')

clean_up(total_parts)
print("PDF de arquivo gerado com sucesso! Baixe e imprima o seu arquivo.")
