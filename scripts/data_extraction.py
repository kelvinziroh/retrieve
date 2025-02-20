# Importing required module
import pymupdf
import re

def extract_text(path):
# Open the file
    doc = pymupdf.open(path)

    text = ""
    for page in doc[2:]:
        text += page.get_text()

    return text

extracted_text = extract_text(
    "../question_bank/machine_learning/unsupervised_learning/\
clustering_and_geospatial_analysis/Gaussian Mixture Models.pdf")
print(extracted_text)

