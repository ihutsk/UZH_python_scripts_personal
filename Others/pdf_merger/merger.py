#!/usr/bin/env python
# coding: utf-8

# ### PDF Merger

# Based on https://dadataguy.medium.com/merging-multiple-pdfs-with-python-7970a720ff0f

import os
from PyPDF2 import PdfWriter, PdfReader

try:
    os.mkdir('pdfs')
except:
    pass

pdf_files = [file.name for file in os.scandir('pdfs') if file.is_file()]
pdf_files = sorted(pdf_files)
pdf_writer = PdfWriter()
for file in pdf_files:
    obj = open(f'pdfs/{file}', 'rb')
    reader = PdfReader(obj)
    for i in range(reader.numPages):
        pageobj = reader.pages[i]
        pdf_writer.add_page(pageobj)

pdf_out = open('merged.pdf', 'wb')
pdf_writer.write(pdf_out)
pdf_out.close()

