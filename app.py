import gradio as gr
import easyocr

reader = easyocr.Reader(['en', 'hi'])

def replace_hindi_numerals(text):
    hindi_to_english = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
    }
    for hindi_num, eng_num in hindi_to_english.items():
        text = text.replace(hindi_num, eng_num)
    return text

def ocr_image(image):
    result = reader.readtext(image, detail=0, paragraph=False)
    text = [res for res in result]
    
    combined_text = "\n".join(text)
    combined_text = replace_hindi_numerals(combined_text)
    
    return combined_text

def search_keyword(text, keyword):
    lines = text.splitlines()
    
    if keyword:
        filtered_lines = [line for line in lines if keyword.lower() in line.lower() or keyword in line]
        return "\n".join(filtered_lines)
    return ""

def clear_keyword():
    return "", ""

def clear_all():
    return None, "", "", ""

def process_and_search(image, keyword):
    ocr_text = ocr_image(image)
    filtered_text = search_keyword(ocr_text, keyword)
    return ocr_text, filtered_text

def full_ocr(image):
    ocr_text = ocr_image(image)
    return ocr_text, ""

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown("**Note: Please ensure that only English or Hindi text is used for OCR.**")
            image_input = gr.Image(label="Upload Image", type="filepath")
            full_image_button = gr.Button("OCR")
            
            keyword_input = gr.Textbox(label="Keyword", placeholder="Enter keyword")
            
            with gr.Row():
                keyword_search_button = gr.Button("Keyword Search")
                keyword_clear_button = gr.Button("Clear Keyword")
            clear_button = gr.Button("Clear All")

        with gr.Column():
            output_ocr = gr.Textbox(label="Full OCR Output")
            output_search = gr.Textbox(label="Keyword-related Output")

    full_image_button.click(fn=full_ocr, inputs=[image_input], outputs=[output_ocr, output_search])

    keyword_search_button.click(fn=process_and_search, inputs=[image_input, keyword_input], outputs=[output_ocr, output_search])

    keyword_clear_button.click(fn=clear_keyword, inputs=[], outputs=[keyword_input, output_search])

    clear_button.click(fn=clear_all, inputs=[], outputs=[image_input, keyword_input, output_ocr, output_search])

demo.launch(share=True)