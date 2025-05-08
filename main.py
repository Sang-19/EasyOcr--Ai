from PIL import Image
import easyocr # Replaces pytesseract
import tkinter as tk
from tkinter import filedialog, scrolledtext, Listbox, END, MULTIPLE

# Initialize the EasyOCR reader
# This can be done once globally. Specify the languages you need.
# For example, ['en'] for English.
# It might take a moment to load the models the first time.
try:
    reader = easyocr.Reader(['en']) 
except Exception as e:
    print(f"Error initializing EasyOCR Reader: {e}")
    print("Please ensure you have a working internet connection if models need to be downloaded.")
    print("And that PyTorch is correctly installed.")
    # You might want to exit or disable OCR functionality if the reader fails
    reader = None 

def extract_text_from_image(image_path):
    if reader is None:
        return "EasyOCR Reader not initialized."
    # The Image.open line is no longer strictly necessary as EasyOCR can take a path.
    # image = Image.open(image_path)
    
    try:
        result = reader.readtext(image_path)
        # The result is a list of tuples, where each tuple contains
        # (bounding_box, text, confidence_score).
        # We'll extract and join all the detected text strings.
        extracted_text = "\n".join([text for (bbox, text, prob) in result])
        if not extracted_text:
            return "No text found."
        return extracted_text
    except Exception as e:
        return f"Error processing image {image_path}: {e}"

class OCRApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("EasyOCR Image to Text Dashboard")
        self.root.geometry("800x600")

        self.selected_files = []

        # Frame for file selection
        selection_frame = tk.Frame(self.root, padx=10, pady=10)
        selection_frame.pack(fill=tk.X)

        btn_select_images = tk.Button(selection_frame, text="Select Images", command=self.select_images)
        btn_select_images.pack(side=tk.LEFT, padx=5)

        self.listbox_files = Listbox(selection_frame, selectmode=MULTIPLE, height=5)
        self.listbox_files.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Frame for controls
        control_frame = tk.Frame(self.root, padx=10, pady=5)
        control_frame.pack(fill=tk.X)

        btn_process_images = tk.Button(control_frame, text="Extract Text from Selected Images", command=self.process_images)
        btn_process_images.pack(pady=5)

        # Frame for results
        results_frame = tk.Frame(self.root, padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_results = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.text_results.pack(fill=tk.BOTH, expand=True)

    def select_images(self):
        # Ask for image files
        filepaths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=(("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*"))
        )
        if filepaths:
            self.listbox_files.delete(0, END) # Clear previous selections
            self.selected_files = list(filepaths)
            for f_path in self.selected_files:
                self.listbox_files.insert(END, f_path.split('/')[-1]) # Display only filename

    def process_images(self):
        if not self.selected_files:
            self.update_results("Please select image files first.")
            return

        if reader is None:
            self.update_results("EasyOCR Reader could not be initialized. Cannot process images.")
            return

        self.update_results("Processing...\n")
        
        all_results = []
        for image_path in self.selected_files:
            filename = image_path.split('/')[-1]
            self.update_results(f"Processing: {filename}\n", append=True)
            self.root.update_idletasks() # Update GUI to show current processing file

            text = extract_text_from_image(image_path)
            all_results.append(f"--- Results for {filename} ---\n{text}\n\n")
        
        self.update_results("".join(all_results), clear_previous=False, append=True) # Append results to "Processing..."
        self.update_results("\nDone.", append=True)


    def update_results(self, message, clear_previous=True, append=False):
        self.text_results.config(state=tk.NORMAL)
        if clear_previous and not append:
            self.text_results.delete(1.0, END)
        self.text_results.insert(tk.END if append else 1.0, message)
        self.text_results.config(state=tk.DISABLED)
        self.text_results.see(tk.END) # Scroll to the end

if __name__ == "__main__":
    # The print statement from your original script is removed as GUI handles output.
    # print(extract_text_from_image('E:\Projects that are working\image to text converter\image.png'))
    
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()