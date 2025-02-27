# Importing required modules
import os
import pymupdf
import re
from parameters import local_parameters

def extract_metadata(base_dir):
    # Recursively traverse the base directory
    traversal = os.walk(base_dir)
    
    return list(traversal)
    

def extract_text(file_path):
    # Open and read the file
    DOC = pymupdf.open(file_path)

    # Extract text from the file
    text = ""
    for page in DOC:
        text += page.get_text()

    return text


def split_text_sections(text):
    # Define section header regex patterns
    HEADER_PATTERNS = r"[Mm]ultiple [Cc]hoice [Qq]uestions?|[Ss]hort [Aa]nswer [Qq]uestions?|[Oo]pen [Ee]nded [Qq]uestions?"

    # Split the text into sections
    text_sections = re.split(HEADER_PATTERNS, text)[1:]

    return text_sections


def match_question_patterns():
    # Define question regex patterns
    PATTERN = re.compile(
        # Match question pattern
        r"\d+\.\s*(?P<question>.+?)\n"
        # Match choice patterns if they exist
        r"(?:a\.\s*(?P<option_a>.+?)\n)?"
        r"(?:b\.\s*(?P<option_b>.+?)\n)?"
        r"(?:c\.\s*(?P<option_c>.+?)\n)?"
        r"(?:d\.\s*(?P<option_d>.+?)\n)?"
        # Match answer pattern with a positive look-ahead
        r"(Answer:\s*(?P<answer>.+?)(?=\n\d+\.\s*|$)\n)",
        re.DOTALL,
    )

    return PATTERN


def extract_question_data(text):
    # Split the text into sections
    SECTIONS = split_text_sections(text)

    # Define the question regex patterns
    QUESTION_PATTERN = match_question_patterns()

    # Set question types
    QUESTION_TYPES = ["mcq", "saq", "oeq"]

    # Capture question data
    question_data = []
    for idx, section in enumerate(SECTIONS):
        # Capture question type
        question_type = QUESTION_TYPES[idx]
        for match in QUESTION_PATTERN.finditer(section):
            # Capture question pattern
            question = (
                match.group("question")
                .translate(str.maketrans({"\u200b": "", "\n": ""}))
                .strip()
            )

            # Capture choices patterns
            choices = [
                match.group(choice)
                .translate(str.maketrans({"\u200b": "", "\n": ""}))
                .strip()
                for choice in ["option_a", "option_b", "option_c", "option_d"]
                if match.group(choice)
            ]

            # Capture answer pattern
            answer = match.group("answer").replace("\n", "").strip()

            # Update the question data list appropriately
            if len(choices) == 0:
                question_data.append(
                    {"type": question_type, "question": question, "answer": answer}
                )
            else:
                question_data.append(
                    {
                        "type": question_type,
                        "question": question,
                        "choices": choices,
                        "answer": answer,
                    }
                )

    return question_data


def print_summary(text, data):
    # Print out a summary report on data extraction
    print("+-----------------------------------------+")
    print("|        === EXTRACTION SUMMARY ===       |")
    print("+-----------------------------------------+")
    # Check if text was extracted successfully
    print(
        " Extracting text...\t\t[DONE] ✅"
        if len(text) != 0
        else " Extracting text...\t\t[FAILED] ❌"
    )

    # Check if text was parsed and data extracted successfully
    if data:
        print(" Parsing text...\t\t[DONE] ✅")
        print(" Extracting question data...\t[DONE] ✅\n")

        # Display the number of mcqs, saqs and oeqs extracted
        print(f" {[item['type'] for item in data].count('mcq')} mcqs extracted")
        print(f" {[item['type'] for item in data].count('saq')} saqs extracted")
        print(f" {[item['type'] for item in data].count('oeq')} oeqs extracted")
        print(f" Total no. of questions extracted: {len(data)}")
        print("+-----------------------------------------+")
    else:
        print(" Parsing text...\t\t[FAILED] ❌")
        print(" Extracting question data...\t[FAILED] ❌\n")
        print("+-----------------------------------------+")


def main():
    # Define the base directory
    base_dir = local_parameters["base_directory"]
    
    # Extract metadata
    for item in extract_metadata(base_dir):
        print(item)
    
    # Extract question data from the file
    # extracted_text = extract_text(
    #     "../question_bank/machine_learning/regression/simple_linear_regression/simple_linear_regression.pdf"
    # )

    # extracted_text = extract_text(
    #     "../question_bank/generative_ai/intro_to_gen_ai/intro_to_gen_ai.pdf"
    # )

    # data = extract_question_data(extracted_text)
    # print_summary(extracted_text, data)

    # Display the data
    # print("Questions:")
    # for item in data:
    #     for key, value in item.items():
    #         if key == "choices":
    #             print(f"{key}:")
    #             for i in value:
    #                 print(f"\t{i}")
    #         else:
    #             print(f"{key}: {value}")
    #         # print(f"{key}: {value}")
    #     print("\n")


if __name__ == "__main__":
    main()
