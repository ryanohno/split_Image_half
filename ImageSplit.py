import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image
import os

def split_image(input_path):
    try:
        img = Image.open(input_path)
        width, height = img.size
        half_width = width // 2
        
        left_half = img.crop((0, 0, half_width, height))
        right_half = img.crop((half_width, 0, width, height))
        
        return left_half, right_half
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing the image: {str(e)}")
        return None, None

def rename_files(output_dir, original_file_name, extension):
    for i, file_name in enumerate(os.listdir(output_dir)):
        if file_name.startswith(original_file_name):
            new_name = f"{original_file_name[:-2]}_half_{i+1}{extension}"
            os.rename(os.path.join(output_dir, file_name), os.path.join(output_dir, new_name))

def main():
    root = tk.Tk()
    root.withdraw()

    image_files_path = filedialog.askopenfiles(filetypes=[("Image Files", "*.tif;*.tiff;*.jpg")])

    if not image_files_path:
        print("No files selected. Exiting...")
        return

    progress_window = tk.Toplevel(root)
    progress_window.title("Progress")
    progress_label = tk.Label(progress_window, text="Processing...")
    progress_label.pack(pady=10)
    progress = Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)

    total_files = len(image_files_path)
    progress["maximum"] = total_files

    for i, image_file in enumerate(image_files_path):
        image_file_path = image_file.name
        output_dir = os.path.join(os.path.dirname(image_file_path), "output")
        os.makedirs(output_dir, exist_ok=True)

        left_half, right_half = split_image(image_file_path)

        if left_half is not None and right_half is not None:
            file_name = os.path.splitext(os.path.basename(image_file_path))[0]
            extension = os.path.splitext(image_file_path)[1]

            left_half.save(os.path.join(output_dir, f"{file_name}_left{extension}"))
            right_half.save(os.path.join(output_dir, f"{file_name}_right{extension}"))

            rename_files(output_dir, file_name, extension)

        progress_label.config(text=f"Processing {i+1}/{total_files}")
        progress["value"] = i + 1
        progress.update()

    messagebox.showinfo("Processing Complete", "Image processing complete.")

if __name__ == "__main__":
    main()
