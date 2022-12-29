import pytesseract
import PySimpleGUI as sg
import tkinter.filedialog
import pyperclip
import webbrowser
from PIL import Image


# Setting the path to the tesseract executable.
pytesseract.pytesseract.tesseract_cmd = './Tesseract/tesseract.exe'

# A list of tuples. Each tuple is a file type. The first item in the tuple is the name of the file
# type, and the second item is the file extension.
filetypes = [
    ('Text', '*.txt'),
    ('All files', '*'),
]


def ocr_image(image_path, language):
    """
    It opens an image, converts it to grayscale, and then runs OCR on it
    
    :param image_path: The path to the image to be OCR'd
    :param language: The language to use for OCR
    :return: The text that was extracted from the image.
    """
    # Open the image and convert it to grayscale
    image = Image.open(image_path).convert('L')
    # Run OCR on the image
    text = pytesseract.image_to_string(image, lang=language)
    return text


# Creating the GUI.
layout = [
    [sg.Text("OCR Tool", font=('', 16))],
    [sg.Text("Select an image file: "), sg.Input(
        key="image_path"), sg.FileBrowse()],
    [sg.Text("Select a language: "), sg.InputCombo(
        ["En", "He"], key="language")],
    [sg.Button("Convert"), sg.Button("Save"), sg.Button("Copy"),
     sg.Button("About"), sg.Button("Cancel")]
]


# It creates a window with the title "OCR Tool" and the layout that was defined earlier.
window = sg.Window("OCR Tool", layout)
# It sets the icon of the window to the icon.ico file.
window.SetIcon("icon.ico")

while True:
    # Reading the window and getting the event and values.
    event, values = window.read()
    # It closes the window when the user clicks the "Cancel" button.
    if event in (None, "Cancel"):
        break
    # Checking if the user clicked the "Convert" button. If they did, it gets the image path and
    # language from the window, and then it converts the image to text.
    if event == "Convert":
        image_path = values["image_path"]
        language = values["language"]
        if language == 'En':
            language = 'eng'
        if language == 'He':
            language = 'heb'
        text = ocr_image(image_path, language)
        sg.popup('', "The text is now available. You can save it using the 'Save' button, or copy it using the 'Copy' button .")
    # Saving the text to a file.
    if event == "Save":
        filesave = tkinter.filedialog.asksaveasfilename(
            defaultextension='.txt', filetypes=filetypes)
        if filesave:
            f = open(str(filesave), 'w')
            f.write(text)
            f.close()
            sg.popup('', "Text saved to file!")
    # It copies the text to the clipboard.
    if event == "Copy":
        pyperclip.copy(text)
        sg.popup('', "The text has been copied!")
    # It opens a new tab in the default browser with the link https://github.com/Yair-T/Image-OCR-Tool,
    # and then it shows a popup with the text.
    if event == "About":
        webbrowser.open_new_tab('https://github.com/Yair-T/Image-OCR-Tool')
        sg.popup('About', "Programmed by YairT. The Open Source OCR engine is used: https://github.com/tesseract-ocr/tesseract")
        
        
window.close()