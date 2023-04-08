from docxtpl import DocxTemplate, InlineImage
from PIL import Image
from docx.shared import Mm


# Load the label printing word template file
doc = DocxTemplate("template_with_tags.docx")

# Define a list of image paths


# Define the number of columns and rows
num_cols = 2
num_rows = 7

# Define the total number of labels
total_labels = num_cols * num_rows

# Create a list of dictionaries that contains the image paths
image_list = []
for i in range(total_labels):
    image_obj = InlineImage(doc, '../assets/qr_code_default.png', width=Mm(95), height=Mm(35))
    image_list.append(image_obj)

context = {}
for i in range(total_labels):
    context[f'image{i+1}'] = image_list[i]

doc.render(context)

# Save the filled template to a new file
doc.save("filled_label_template.docx")
