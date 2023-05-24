from docx import Document
from os import path


doc = Document(path.join('data', 'LABL5420_A0240_docx.docx'))
table = doc.tables[0]
count = 1
for row in table.rows:
    for cell in row.cells:
        text = cell.text
        tag_name = f" image{count} "
        new_text = f"{{{{{tag_name}}}}}{text}"
        cell.text = new_text
        count += 1

doc.save(path.join('data', 'template_device_tags.docx'))
