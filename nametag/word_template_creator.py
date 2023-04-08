from docx import Document

# Load the Word template file
doc = Document('template.docx')

# Get the first table in the document (assuming the template has a single table)
table = doc.tables[0]

# Iterate over each cell in the table and add a tag to the cell's text
row_count = 1
count = 1
for row in table.rows:
    col_count = 1
    for cell in row.cells:
        if col_count % 2 == 0:
            col_count += 1
            continue
        # Get the current cell's text
        text = cell.text

        # Add a tag to the text with a unique name based on the cell's row and column index
        tag_name = f" image{count} "
        new_text = f"{{{{{tag_name}}}}}{text}"

        # Replace the cell's text with the new text
        cell.text = new_text
        col_count += 1
        count += 1
    row_count += 1

# Save the modified Word template file
doc.save('template_with_tags.docx')
