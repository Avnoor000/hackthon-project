import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import json

class PyGUIBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("PyGUI Builder Pro - CustomTkinter Edition")
        self.root.geometry("1400x800")
        self.root.configure(bg="#1a1a1a")
        
        self.widgets = []
        self.next_id = 1
        self.selected_widget = None
        self.canvas_widgets = {}
        self.drag_data = {"item": None, "x": 0, "y": 0}
        
        self.setup_ui()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
    
    def setup_ui(self):
        # Top toolbar
        toolbar = tk.Frame(self.root, bg="#2c3e50", height=60)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(toolbar, text="🎨 PyGUI Builder Pro", font=("Arial", 18, "bold"), 
                bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Button(toolbar, text="📥 Export", command=self.export_code,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                 padx=15, pady=8).pack(side=tk.RIGHT, padx=10, pady=15)
        
        tk.Button(toolbar, text="💾 Save", command=self.save_project,
                 bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                 padx=15, pady=8).pack(side=tk.RIGHT, padx=5, pady=15)
        
        tk.Button(toolbar, text="📂 Load", command=self.load_project,
                 bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                 padx=15, pady=8).pack(side=tk.RIGHT, padx=5, pady=15)
        
        tk.Button(toolbar, text="🗑️ Clear", command=self.clear_all,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 padx=15, pady=8).pack(side=tk.RIGHT, padx=5, pady=15)
        
        # Main container
        main = tk.Frame(self.root, bg="#1a1a1a")
        main.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Left panel
        left = tk.Frame(main, bg="#2d2d2d", width=180)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left.pack_propagate(False)
        
        tk.Label(left, text="Widgets", font=("Arial", 12, "bold"),
                bg="#2d2d2d", fg="white").pack(pady=10)
        
        widgets_list = [
            ("Label", "#3498db"), ("Button", "#2ecc71"), ("Entry", "#9b59b6"),
            ("Text", "#e67e22"), ("Checkbutton", "#1abc9c"), ("Radiobutton", "#34495e"),
            ("Frame", "#95a5a6"), ("Scale", "#c0392b"), ("Progressbar", "#27ae60")
        ]
        
        for name, color in widgets_list:
            tk.Button(left, text=name, command=lambda n=name: self.add_widget(n),
                     bg=color, fg="white", font=("Arial", 9, "bold"),
                     width=15, pady=8).pack(pady=3, padx=10)
        
        # Center canvas
        center = tk.Frame(main, bg="#1a1a1a")
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(center, text="Design Canvas", font=("Arial", 11, "bold"),
                bg="#1a1a1a", fg="#ecf0f1").pack(pady=5)
        
        canvas_frame = tk.Frame(center, bg="#34495e", relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Right panel with scrollbar
        right = tk.Frame(main, bg="#2d2d2d", width=300)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        right.pack_propagate(False)
        
        tk.Label(right, text="⚙️ Properties", font=("Arial", 12, "bold"),
                bg="#2d2d2d", fg="white").pack(pady=10)
        
        canvas_props = tk.Canvas(right, bg="#2d2d2d", highlightthickness=0)
        scrollbar = tk.Scrollbar(right, orient="vertical", command=canvas_props.yview)
        self.props_frame = tk.Frame(canvas_props, bg="#2d2d2d")
        
        self.props_frame.bind("<Configure>", 
                             lambda e: canvas_props.configure(scrollregion=canvas_props.bbox("all")))
        canvas_props.create_window((0, 0), window=self.props_frame, anchor="nw", width=280)
        canvas_props.configure(yscrollcommand=scrollbar.set)
        
        canvas_props.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.show_empty_props()
    
    def show_empty_props(self):
        for w in self.props_frame.winfo_children():
            w.destroy()
        tk.Label(self.props_frame, text="Select a widget\nto edit properties",
                font=("Arial", 10), fg="#95a5a6", bg="#2d2d2d").pack(pady=50)
    
    def add_widget(self, widget_type):
        data = {
            'id': self.next_id,
            'type': widget_type,
            'text': f'{widget_type} {self.next_id}',
            'x': 100 + len(self.widgets) * 20,
            'y': 100 + len(self.widgets) * 20,
            'width': 150, 'height': 35,
            'font': 'Arial', 'font_size': 12,
            'bg_color': '#f0f0f0', 'fg_color': '#3498db',
            'text_color': '#000000', 'border_color': '#cccccc',
            'corner_radius': 10, 'border_width': 2,
            'hover_color': '#2980b9'
        }
        self.widgets.append(data)
        self.draw_widget(data)
        self.select_widget(data)
        self.next_id += 1
    
    def draw_widget(self, data):
        wid = data['id']
        if wid in self.canvas_widgets:
            for item in self.canvas_widgets[wid]:
                self.canvas.delete(item)
        
        items = []
        x, y = data['x'], data['y']
        w, h = data['width'], data['height']
        r = data['corner_radius']
        
        if data['type'] == 'Label':
            rect = self.rounded_rect(x, y, x+w, y+h, r, data['bg_color'], data['border_color'], 2)
            text = self.canvas.create_text(x+w//2, y+h//2, text=data['text'],
                                          font=(data['font'], data['font_size']),
                                          fill=data['text_color'])
            items = [rect, text]
        
        elif data['type'] == 'Button':
            rect = self.rounded_rect(x, y, x+w, y+h, r, data['fg_color'], data['border_color'], 2)
            text = self.canvas.create_text(x+w//2, y+h//2, text=data['text'],
                                          font=(data['font'], data['font_size'], 'bold'),
                                          fill='white')
            items = [rect, text]
        
        elif data['type'] == 'Entry':
            rect = self.rounded_rect(x, y, x+w, y+h, r, 'white', data['border_color'], 2)
            text = self.canvas.create_text(x+10, y+h//2, text="Enter text...",
                                          font=(data['font'], data['font_size']),
                                          fill='#999', anchor='w')
            items = [rect, text]
        
        elif data['type'] == 'Text':
            rect = self.rounded_rect(x, y, x+w, y+h*2, r, 'white', data['border_color'], 2)
            text = self.canvas.create_text(x+10, y+10, text="Text area...",
                                          font=(data['font'], data['font_size']),
                                          fill='#999', anchor='nw')
            items = [rect, text]
        
        elif data['type'] == 'Checkbutton':
            box = self.rounded_rect(x, y, x+25, y+25, 5, 'white', data['border_color'], 2)
            check = self.canvas.create_text(x+12, y+12, text="✓",
                                           font=('Arial', 16, 'bold'), fill=data['fg_color'])
            text = self.canvas.create_text(x+35, y+12, text=data['text'],
                                          font=(data['font'], data['font_size']),
                                          fill=data['text_color'], anchor='w')
            items = [box, check, text]
        
        elif data['type'] == 'Radiobutton':
            circle = self.canvas.create_oval(x, y, x+25, y+25, fill='white',
                                            outline=data['border_color'], width=2)
            dot = self.canvas.create_oval(x+7, y+7, x+18, y+18, fill=data['fg_color'], outline='')
            text = self.canvas.create_text(x+35, y+12, text=data['text'],
                                          font=(data['font'], data['font_size']),
                                          fill=data['text_color'], anchor='w')
            items = [circle, dot, text]
        
        elif data['type'] == 'Frame':
            rect = self.rounded_rect(x, y, x+w, y+h, r, data['bg_color'], data['border_color'], 2)
            text = self.canvas.create_text(x+w//2, y+10, text="Frame",
                                          font=(data['font'], 9), fill='#999')
            items = [rect, text]
        
        elif data['type'] == 'Scale':
            track = self.rounded_rect(x, y+10, x+w, y+25, 15, '#e0e0e0', data['border_color'], 1)
            thumb = self.canvas.create_oval(x+w//2-10, y+5, x+w//2+10, y+30,
                                           fill=data['fg_color'], outline=data['border_color'], width=2)
            items = [track, thumb]
        
        elif data['type'] == 'Progressbar':
            bg = self.rounded_rect(x, y, x+w, y+25, r, '#e0e0e0', data['border_color'], 1)
            prog = self.rounded_rect(x+2, y+2, x+w//2, y+23, r-2, data['fg_color'], '', 0)
            items = [bg, prog]
        
        self.canvas_widgets[wid] = items
    
    def rounded_rect(self, x1, y1, x2, y2, r, fill, outline, width):
        if r > 0:
            points = [x1+r,y1, x2-r,y1, x2,y1, x2,y1+r, x2,y2-r, x2,y2,
                     x2-r,y2, x1+r,y2, x1,y2, x1,y2-r, x1,y1+r, x1,y1]
            return self.canvas.create_polygon(points, fill=fill, outline=outline,
                                             width=width, smooth=True)
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=width)
    
    def on_canvas_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        for wid, items in self.canvas_widgets.items():
            if item in items:
                data = next((w for w in self.widgets if w['id'] == wid), None)
                if data:
                    self.select_widget(data)
                    self.drag_data = {"item": wid, "x": event.x, "y": event.y}
                return
    
    def on_canvas_drag(self, event):
        if self.drag_data["item"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            
            data = next((w for w in self.widgets if w['id'] == self.drag_data["item"]), None)
            if data:
                data['x'] += dx
                data['y'] += dy
                self.draw_widget(data)
            
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
    
    def select_widget(self, data):
        self.selected_widget = data
        self.show_props(data)
    
    def show_props(self, data):
        for w in self.props_frame.winfo_children():
            w.destroy()
        
        header = tk.Frame(self.props_frame, bg="#34495e")
        header.pack(fill=tk.X, pady=(0, 10))
        tk.Label(header, text=f"{data['type']} #{data['id']}",
                font=("Arial", 11, "bold"), bg="#34495e", fg="white").pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(header, text="🗑️", command=lambda: self.delete_widget(data['id']),
                 bg="#e74c3c", fg="white").pack(side=tk.RIGHT, padx=10)
        
        # Basic Properties
        if data['type'] in ['Label', 'Button', 'Checkbutton', 'Radiobutton']:
            self.add_input(data, 'text', 'Text:')
        
        self.add_combo(data, 'font', 'Font:', ['Arial', 'Helvetica', 'Times New Roman', 'Courier'])
        self.add_input(data, 'font_size', 'Font Size:', 'number')
        
        # Position & Size
        sec = tk.LabelFrame(self.props_frame, text="Position & Size", bg="#2d2d2d",
                           fg="white", font=("Arial", 9, "bold"))
        sec.pack(fill=tk.X, padx=10, pady=5)
        
        f = tk.Frame(sec, bg="#2d2d2d")
        f.pack(fill=tk.X, padx=5, pady=3)
        tk.Label(f, text="X:", bg="#2d2d2d", fg="white").grid(row=0, column=0)
        x_ent = tk.Entry(f, width=6, bg="#34495e", fg="white")
        x_ent.insert(0, data['x'])
        x_ent.grid(row=0, column=1, padx=3)
        x_ent.bind('<Return>', lambda e: self.update_prop(data['id'], 'x', int(x_ent.get() or 0)))
        
        tk.Label(f, text="Y:", bg="#2d2d2d", fg="white").grid(row=0, column=2, padx=(10,0))
        y_ent = tk.Entry(f, width=6, bg="#34495e", fg="white")
        y_ent.insert(0, data['y'])
        y_ent.grid(row=0, column=3, padx=3)
        y_ent.bind('<Return>', lambda e: self.update_prop(data['id'], 'y', int(y_ent.get() or 0)))
        
        f2 = tk.Frame(sec, bg="#2d2d2d")
        f2.pack(fill=tk.X, padx=5, pady=3)
        tk.Label(f2, text="W:", bg="#2d2d2d", fg="white").grid(row=0, column=0)
        w_ent = tk.Entry(f2, width=6, bg="#34495e", fg="white")
        w_ent.insert(0, data['width'])
        w_ent.grid(row=0, column=1, padx=3)
        w_ent.bind('<Return>', lambda e: self.update_prop(data['id'], 'width', int(w_ent.get() or 100)))
        
        tk.Label(f2, text="H:", bg="#2d2d2d", fg="white").grid(row=0, column=2, padx=(10,0))
        h_ent = tk.Entry(f2, width=6, bg="#34495e", fg="white")
        h_ent.insert(0, data['height'])
        h_ent.grid(row=0, column=3, padx=3)
        h_ent.bind('<Return>', lambda e: self.update_prop(data['id'], 'height', int(h_ent.get() or 30)))
        
        # Colors
        self.add_color(data, 'bg_color', 'Background')
        if data['type'] in ['Button', 'Checkbutton', 'Radiobutton', 'Scale', 'Progressbar']:
            self.add_color(data, 'fg_color', 'Main Color')
        self.add_color(data, 'text_color', 'Text Color')
        self.add_color(data, 'border_color', 'Border')
        
        # CustomTkinter
        self.add_slider(data, 'corner_radius', 'Corner Radius', 0, 50)
        self.add_slider(data, 'border_width', 'Border Width', 0, 10)
    
    def add_input(self, data, key, label, itype='text'):
        f = tk.Frame(self.props_frame, bg="#2d2d2d")
        f.pack(fill=tk.X, padx=10, pady=3)
        tk.Label(f, text=label, bg="#2d2d2d", fg="white", font=("Arial", 9)).pack(anchor='w')
        ent = tk.Entry(f, bg="#34495e", fg="white")
        ent.insert(0, data[key])
        ent.pack(fill=tk.X, pady=2)
        ent.bind('<KeyRelease>', lambda e: self.update_prop(data['id'], key, 
                 int(ent.get()) if itype == 'number' and ent.get() else ent.get()))
    
    def add_combo(self, data, key, label, values):
        f = tk.Frame(self.props_frame, bg="#2d2d2d")
        f.pack(fill=tk.X, padx=10, pady=3)
        tk.Label(f, text=label, bg="#2d2d2d", fg="white", font=("Arial", 9)).pack(anchor='w')
        var = tk.StringVar(value=data[key])
        combo = ttk.Combobox(f, textvariable=var, values=values, state='readonly')
        combo.pack(fill=tk.X, pady=2)
        combo.bind('<<ComboboxSelected>>', lambda e: self.update_prop(data['id'], key, var.get()))
    
    def add_color(self, data, key, label):
        f = tk.Frame(self.props_frame, bg="#2d2d2d")
        f.pack(fill=tk.X, padx=10, pady=3)
        tk.Label(f, text=f"{label}:", bg="#2d2d2d", fg="white", font=("Arial", 9)).pack(anchor='w')
        
        cf = tk.Frame(f, bg="#2d2d2d")
        cf.pack(fill=tk.X, pady=2)
        
        display = tk.Canvas(cf, width=25, height=20, bg=data[key], highlightthickness=1)
        display.pack(side=tk.LEFT, padx=(0, 5))
        
        ent = tk.Entry(cf, bg="#34495e", fg="white", width=12)
        ent.insert(0, data[key])
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        def pick():
            color = colorchooser.askcolor(data[key])[1]
            if color:
                ent.delete(0, tk.END)
                ent.insert(0, color)
                display.config(bg=color)
                self.update_prop(data['id'], key, color)
        
        tk.Button(cf, text="🎨", command=pick, bg="#3498db", fg="white").pack(side=tk.LEFT)
        ent.bind('<Return>', lambda e: self.update_prop(data['id'], key, ent.get()))
    
    def add_slider(self, data, key, label, min_val, max_val):
        f = tk.Frame(self.props_frame, bg="#2d2d2d")
        f.pack(fill=tk.X, padx=10, pady=3)
        
        lf = tk.Frame(f, bg="#2d2d2d")
        lf.pack(fill=tk.X)
        tk.Label(lf, text=f"{label}:", bg="#2d2d2d", fg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        val_lbl = tk.Label(lf, text=str(data[key]), bg="#2d2d2d", fg="#3498db", font=("Arial", 9, "bold"))
        val_lbl.pack(side=tk.RIGHT)
        
        def on_change(v):
            val_lbl.config(text=str(int(float(v))))
            self.update_prop(data['id'], key, int(float(v)))
        
        slider = tk.Scale(f, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                         bg="#34495e", fg="white", command=on_change, highlightthickness=0)
        slider.set(data[key])
        slider.pack(fill=tk.X, pady=2)
    
    def update_prop(self, wid, key, value):
        for data in self.widgets:
            if data['id'] == wid:
                data[key] = value
                self.draw_widget(data)
                break
    
    def delete_widget(self, wid):
        self.widgets = [w for w in self.widgets if w['id'] != wid]
        if wid in self.canvas_widgets:
            for item in self.canvas_widgets[wid]:
                self.canvas.delete(item)
            del self.canvas_widgets[wid]
        self.show_empty_props()
    
    def clear_all(self):
        if messagebox.askyesno("Clear", "Delete all widgets?"):
            self.widgets = []
            self.canvas_widgets = {}
            self.canvas.delete("all")
            self.show_empty_props()
            self.next_id = 1
    
    def generate_code(self):
        code = """# Auto-generated by PyGUI Builder Pro
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("My App")
root.geometry("700x500")

"""
        for i, w in enumerate(self.widgets):
            var = f"{w['type'].lower()}{i+1}"
            code += f"# {w['type']}\n"
            
            if w['type'] == 'Label':
                code += f"{var} = ctk.CTkLabel(root, text=\"{w['text']}\", "
                code += f"font=(\"{w['font']}\", {w['font_size']}), fg_color=\"{w['bg_color']}\", "
                code += f"text_color=\"{w['text_color']}\", corner_radius={w['corner_radius']})\n"
            elif w['type'] == 'Button':
                code += f"{var} = ctk.CTkButton(root, text=\"{w['text']}\", "
                code += f"font=(\"{w['font']}\", {w['font_size']}), fg_color=\"{w['fg_color']}\", "
                code += f"hover_color=\"{w['hover_color']}\", corner_radius={w['corner_radius']}, "
                code += f"width={w['width']}, height={w['height']})\n"
            elif w['type'] == 'Entry':
                code += f"{var} = ctk.CTkEntry(root, font=(\"{w['font']}\", {w['font_size']}), "
                code += f"corner_radius={w['corner_radius']}, width={w['width']})\n"
            elif w['type'] == 'Text':
                code += f"{var} = ctk.CTkTextbox(root, font=(\"{w['font']}\", {w['font_size']}), "
                code += f"corner_radius={w['corner_radius']}, width={w['width']}, height={w['height']*2})\n"
            elif w['type'] == 'Checkbutton':
                code += f"{var} = ctk.CTkCheckBox(root, text=\"{w['text']}\", "
                code += f"font=(\"{w['font']}\", {w['font_size']}), fg_color=\"{w['fg_color']}\")\n"
            elif w['type'] == 'Radiobutton':
                code += f"{var} = ctk.CTkRadioButton(root, text=\"{w['text']}\", "
                code += f"font=(\"{w['font']}\", {w['font_size']}), fg_color=\"{w['fg_color']}\")\n"
            elif w['type'] == 'Frame':
                code += f"{var} = ctk.CTkFrame(root, fg_color=\"{w['bg_color']}\", "
                code += f"corner_radius={w['corner_radius']}, width={w['width']}, height={w['height']})\n"
            elif w['type'] == 'Scale':
                code += f"{var} = ctk.CTkSlider(root, fg_color=\"{w['fg_color']}\", width={w['width']})\n"
            elif w['type'] == 'Progressbar':
                code += f"{var} = ctk.CTkProgressBar(root, fg_color=\"{w['fg_color']}\", "
                code += f"corner_radius={w['corner_radius']}, width={w['width']})\n{var}.set(0.5)\n"
            
            code += f"{var}.place(x={w['x']}, y={w['y']})\n\n"
        
        code += "root.mainloop()\n"
        return code
    
    def export_code(self):
        if not self.widgets:
            messagebox.showwarning("No Widgets", "Add widgets before exporting!")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".py",
                                               filetypes=[("Python files", "*.py")])
        if filename:
            with open(filename, 'w') as f:
                f.write(self.generate_code())
            messagebox.showinfo("Success", f"Exported to {filename}\n\nInstall: pip install customtkinter")
    
    def save_project(self):
        if not self.widgets:
            messagebox.showwarning("No Widgets", "Add widgets before saving!")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.widgets, f, indent=2)
            messagebox.showinfo("Success", f"Saved to {filename}")
    
    def load_project(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r') as f:
                self.widgets = json.load(f)
            self.canvas.delete("all")
            self.canvas_widgets = {}
            for data in self.widgets:
                self.draw_widget(data)
            if self.widgets:
                self.next_id = max(w['id'] for w in self.widgets) + 1
            messagebox.showinfo("Success", "Project loaded!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyGUIBuilder(root)
    root.mainloop()