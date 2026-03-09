from tools.ocr_tool import extract_text_from_image
import tempfile
import pytesseract
from pdf2image import convert_from_bytes


def process_input(prompt, uploaded_file):

    extracted_text = ""

    if uploaded_file is None:
        return prompt

    # Image input
    if "image" in uploaded_file.type:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:

            tmp.write(uploaded_file.read())
            tmp.flush()

            extracted_text = extract_text_from_image(tmp.name)

    # PDF input
    elif "pdf" in uploaded_file.type:

        pages = convert_from_bytes(uploaded_file.read())

        text = ""

        for page in pages:
            text += pytesseract.image_to_string(page)

        extracted_text = text

    final_question = f"{prompt} {extracted_text}"

    return final_question