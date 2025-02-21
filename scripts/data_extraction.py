# Importing required module
import pymupdf
import re


def extract_text(file_path):
    # Open the file
    doc = pymupdf.open(file_path)

    text = ""
    for page in doc:
        text += page.get_text()

    return text


def extract_data(text):
    # Create multiple choice questions pattern
    mc_pattern = re.compile(
        r"\d+\.\s*(?P<question>.+?)\n"
        r"(?:a\.\s*(?P<option_a>.+?)\n)"
        r"(?:b\.\s*(?P<option_b>.+?)\n)"
        r"(?:c\.\s*(?P<option_c>.+?)\n)"
        r"(?:d\.\s*(?P<option_d>.+?)\n)"
        r"(Answer:\s*(?P<answer>.+?)\n)?",
        re.DOTALL,
    )

    # Initiate an empty list to hold dictionaries
    question_data = []

    # Process multiple-choice questions
    for match in mc_pattern.finditer(text):
        question = match.group("question").strip()  # Capture question patterns
        choices = [
            match.group(choice)
            .translate(str.maketrans({"\u200b": "", "\n": ""}))
            .strip()
            for choice in ["option_a", "option_b", "option_c", "option_d"]
            if match.group(choice)
        ]  # Capture choices patterns
        if match.group("answer"):
            answer = match.group("answer").strip() # Capture the answer pattern if it exists
            question_data.append(
                {"type": "mcq", "question": question, "choices": choices, "answer": answer}
            )
        else:
            question_data.append(
                {"type": "mcq", "question": question, "choices": choices}
            )  # Append the questions data to the empty question data list

    return question_data


# extracted_text = extract_text(
#     "../question_bank/machine_learning/unsupervised_learning/\
# clustering_and_geospatial_analysis/Gaussian Mixture Models.pdf"
# )
extracted_text = extract_text("../question_bank/machine_learning/regression/simple_linear_regression/Simple Linear Regression.pdf")
data = extract_data(extracted_text)

# Display the data
# for item in data:
#     for key, value in item.items():
#         if key == "choices":
#             print(f"{key}")
#             for i in value:
#                 print(f"\t{i}")
#         else:
#             print(f"{key}: {value}")
#         # print(f"{key}: {value}")
#     print("\n")
