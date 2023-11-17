import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ezdxf

def display_png_image(file_path, parent):
    # Open the PNG image file using PIL (Pillow)
    image = Image.open(file_path)
    
    # Convert the PIL Image to a Tkinter PhotoImage
    tk_image = ImageTk.PhotoImage(image)

    # Create a Frame to hold the Label with padding
    frame = tk.Frame(parent, padx=10, pady=10)
    frame.grid(row=0, column=0, sticky='nsew')

    # Create a Label widget and set the image, expand it to fill available space
    label = tk.Label(frame, image=tk_image)
    label.image = tk_image  # Keep a reference to avoid garbage collection
    label.grid(row=0, column=0, sticky='nsew')
    
    # Configure the row and column to expand with the frame
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

def create_table(parent, dim):
    style = ttk.Style()
    style.theme_use('default')  # Change the theme if needed
    style.configure('Treeview.Heading', font=('JetBrains Mono', 10, 'bold'))
    style.configure('Treeview', rowheight=30, font=('JetBrains Mono', 10, 'bold'))

    scroll = tk.Scrollbar(parent, orient=tk.VERTICAL)
    scroll.grid(row=0, column=3, sticky='ns')

    tree = ttk.Treeview(parent, yscrollcommand=scroll.set)
    tree.tag_configure('1', background='lightgrey')
    tree.tag_configure('0', background='white')
    tree.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    scroll.config(command=tree.yview)

    tree['columns'] = ('c1', 'c2', 'c3')

    # format our column
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", anchor=tk.CENTER, width=50)
    tree.column("#2", anchor=tk.CENTER, width=150)
    tree.column("#3", anchor=tk.CENTER, width=150)

    # Create Headings 
    tree.heading("#0", text="\n", anchor=tk.CENTER)
    tree.heading("#1", text="ID", anchor=tk.CENTER)
    tree.heading("#2", text="DIMENSION", anchor=tk.CENTER)
    tree.heading("#3", text="MEASURED VALUE", anchor=tk.CENTER)

    # add data 
    #tree.insert(parent='', index='end', iid=0, text='', values=('1', '10.23530', 'NIL'), tags=('0'))
    
    for i in range(len(dim)):
        tree.insert(parent='', index='end', iid=i, text='', values=(dim[i][0], '{:.5f}'.format(dim[i][1]), 'NIL'), tags=(str(i%2)))

def read_dxf_file(file_path):
    dim = []
    doc = ezdxf.readfile(file_path)
    for entity in doc.modelspace().query('*'):
        entity_type = entity.dxftype()
        if entity_type == 'DIMENSION':
            dim += [(entity.get_dxf_attrib('handle'), entity.get_dxf_attrib('actual_measurement'))]
    return dim

if __name__ == '__main__':
    # Main application
    root = tk.Tk()
    root.title("TLC-BLE")

    dxf_file_path = "part.dxf"  # Replace with the actual path to your DXF file
    dimensions = read_dxf_file(dxf_file_path)

    # Create a frame to hold both the image and the table
    frame = tk.Frame(root)
    frame.pack()

    # Display image on the left
    display_png_image("part.png", frame)

    # Create table on the right
    create_table(frame, dimensions)

    # Configure row and column weights
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    root.mainloop()