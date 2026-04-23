import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, TextBox
import urllib.request
import io
import tkinter as tk
from tkinter import filedialog, messagebox
import warnings
warnings.filterwarnings('ignore')

class DataGraphExplorer:
    def __init__(self):
        # Data storage
        self.df = None
        self.column_names = []
        
        self.default_url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
        
        self.x_column = None
        self.y_column = None
        self.graph_type = 'scatter'
        
        self.setup_gui()
    
    def setup_gui(self):
        self.fig = plt.figure(figsize=(15, 10))
        
        # Main plot area (70% of width)
        self.ax_plot = plt.axes([0.05, 0.35, 0.65, 0.6])
        self.ax_plot.set_title('Graph will appear here')
        self.ax_plot.text(0.5, 0.5, 'Load data to start', 
                         ha='center', va='center', transform=self.ax_plot.transAxes, fontsize=12)
        self.ax_plot.set_xticks([])
        self.ax_plot.set_yticks([])
        
        # Info area (30% of width)
        self.ax_info = plt.axes([0.72, 0.35, 0.25, 0.6])
        self.ax_info.set_title('Data Information')
        self.ax_info.text(0.1, 0.9, 'No data yet', fontsize=10)
        self.ax_info.set_xticks([])
        self.ax_info.set_yticks([])
        self.ax_info.set_xlim(0, 1)
        self.ax_info.set_ylim(0, 1)
        
        # Control buttons
        self.ax_load_url = plt.axes([0.05, 0.25, 0.15, 0.06])
        self.btn_load_url = Button(self.ax_load_url, 'Load from URL')
        
        self.ax_load_default = plt.axes([0.22, 0.25, 0.15, 0.06])
        self.btn_load_default = Button(self.ax_load_default, 'Load Default Data')
        
        self.ax_upload = plt.axes([0.39, 0.25, 0.15, 0.06])
        self.btn_upload = Button(self.ax_upload, 'Upload CSV')
        
        # URL input
        self.ax_url = plt.axes([0.05, 0.18, 0.5, 0.06])
        self.url_box = TextBox(self.ax_url, 'Data URL:', initial=self.default_url)
        
        # Graph type selection
        self.ax_radio = plt.axes([0.6, 0.15, 0.35, 0.15])
        self.radio = RadioButtons(self.ax_radio, ['scatter', 'line', 'histogram', 'bar'])
        
        # Column selection
        self.ax_select_x = plt.axes([0.05, 0.1, 0.25, 0.06])
        self.btn_select_x = Button(self.ax_select_x, 'Select X Axis')
        
        self.ax_select_y = plt.axes([0.32, 0.1, 0.25, 0.06])
        self.btn_select_y = Button(self.ax_select_y, 'Select Y Axis')
        
        # Generate button
        self.ax_generate = plt.axes([0.6, 0.05, 0.35, 0.06])
        self.btn_generate = Button(self.ax_generate, 'Create Graph')
        
        # Connect events
        self.btn_load_url.on_clicked(self.load_from_url)
        self.btn_load_default.on_clicked(self.use_default_data)
        self.btn_upload.on_clicked(self.upload_file)
        self.btn_select_x.on_clicked(self.select_x_column)
        self.btn_select_y.on_clicked(self.select_y_column)
        self.btn_generate.on_clicked(self.create_graph)
        self.radio.on_clicked(self.on_graph_type_changed)
        
        # Interpretation text
        self.ax_interpretation = plt.axes([0.05, 0.01, 0.9, 0.04])
        self.ax_interpretation.set_xticks([])
        self.ax_interpretation.set_yticks([])
        self.ax_interpretation.text(0.02, 0.5, 'Interpretation will appear here', fontsize=10)
        
        plt.show()
    
    def load_data(self, data_source):
        try:
            if isinstance(data_source, str):
                if data_source.startswith('http'):
                    # Load from URL
                    with urllib.request.urlopen(data_source) as response:
                        data = response.read().decode('utf-8')
                    self.df = pd.read_csv(io.StringIO(data))
                else:
                    # Assume it's a file path
                    self.df = pd.read_csv(data_source)
            else:
                # Assume it's file content
                self.df = pd.read_csv(io.StringIO(data_source))
            
            # Update data info
            self.column_names = self.df.columns.tolist()
            self.update_data_info()
            
            # Automatically select first two columns
            if len(self.column_names) >= 1:
                self.x_column = self.column_names[0]
                self.btn_select_x.label.set_text(f'X: {self.x_column}')
            if len(self.column_names) >= 2:
                self.y_column = self.column_names[1]
                self.btn_select_y.label.set_text(f'Y: {self.y_column}')
            
            print("✅ Data successfully loaded!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
    
    def load_from_url(self, event):
        url = self.url_box.text
        if url:
            self.load_data(url)
        else:
            messagebox.showwarning("Warning", "Please enter a URL first")
    
    def use_default_data(self, event):
        self.load_data(self.default_url)
    
    def upload_file(self, event):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.load_data(file_path)
    
    def select_x_column(self, event):
        if self.df is not None:
            self.show_column_selection('x')
        else:
            messagebox.showwarning("Warning", "Please load data first")
    
    def select_y_column(self, event):
        if self.df is not None:
            self.show_column_selection('y')
        else:
            messagebox.showwarning("Warning", "Please load data first")
    
    def show_column_selection(self, axis):
        root = tk.Tk()
        root.title(f"Select Column for {axis.upper()} Axis")
        root.geometry("300x400")
        
        tk.Label(root, text=f"Select column for {axis.upper()} axis:").pack(pady=10)
        
        listbox = tk.Listbox(root)
        for col in self.column_names:
            listbox.insert(tk.END, col)
        listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                selected_column = self.column_names[selection[0]]
                if axis == 'x':
                    self.x_column = selected_column
                    self.btn_select_x.label.set_text(f'X: {self.x_column}')
                else:
                    self.y_column = selected_column
                    self.btn_select_y.label.set_text(f'Y: {self.y_column}')
                root.destroy()
        
        tk.Button(root, text="Select", command=on_select).pack(pady=10)
        root.mainloop()
    
    def on_graph_type_changed(self, label):
        self.graph_type = label
    
    def create_graph(self, event):
        if self.df is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        if not self.x_column:
            messagebox.showwarning("Warning", "Please select X axis column first")
            return
        
        try:
            self.ax_plot.clear()
            data_x = self.df[self.x_column]
            
            if self.graph_type == "histogram":
                self.ax_plot.hist(data_x.dropna(), bins=20, alpha=0.7, edgecolor='black')
                self.ax_plot.set_xlabel(self.x_column)
                self.ax_plot.set_ylabel("Frequency")
                self.ax_plot.set_title(f"Distribution of {self.x_column}")
                self.ax_plot.grid(True, alpha=0.3)
                
                interpretation = f"Histogram of {self.x_column}: Shows data distribution"
                
            elif self.graph_type == "bar" and self.y_column:
                if self.df[self.x_column].dtype == 'object' or self.df[self.x_column].nunique() < 10:
                    value_counts = self.df[self.x_column].value_counts()
                    bars = self.ax_plot.bar(value_counts.index.astype(str), value_counts.values)
                    self.ax_plot.set_xlabel(self.x_column)
                    self.ax_plot.set_ylabel("Count")
                    self.ax_plot.set_title(f"Bar Chart of {self.x_column}")
                    interpretation = f"Bar chart of {self.x_column}"
                else:
                    grouped = self.df.groupby(self.x_column)[self.y_column].mean()
                    bars = self.ax_plot.bar(grouped.index.astype(str), grouped.values)
                    self.ax_plot.set_xlabel(self.x_column)
                    self.ax_plot.set_ylabel(f"Mean of {self.y_column}")
                    self.ax_plot.set_title(f"Mean {self.y_column} by {self.x_column}")
                    interpretation = f"Grouped bar chart: {self.y_column} by {self.x_column}"
                    
            elif self.y_column:
                data_y = self.df[self.y_column]
                
                if self.graph_type == "scatter":
                    self.ax_plot.scatter(data_x, data_y, alpha=0.6)
                    self.ax_plot.set_xlabel(self.x_column)
                    self.ax_plot.set_ylabel(self.y_column)
                    self.ax_plot.set_title(f"Scatter Plot: {self.x_column} vs {self.y_column}")
                    self.ax_plot.grid(True, alpha=0.3)
                    
                    if pd.api.types.is_numeric_dtype(data_x) and pd.api.types.is_numeric_dtype(data_y):
                        correlation = data_x.corr(data_y)
                        interpretation = f"Scatter plot: {self.x_column} vs {self.y_column}, Correlation: {correlation:.3f}"
                    else:
                        interpretation = f"Scatter plot: {self.x_column} vs {self.y_column}"
                        
                else:  # line graph
                    sorted_data = self.df.sort_values(self.x_column)
                    self.ax_plot.plot(sorted_data[self.x_column], sorted_data[self.y_column], 
                                    marker='o', linewidth=2, markersize=4)
                    self.ax_plot.set_xlabel(self.x_column)
                    self.ax_plot.set_ylabel(self.y_column)
                    self.ax_plot.set_title(f"Line Graph: {self.y_column} vs {self.x_column}")
                    self.ax_plot.grid(True, alpha=0.3)
                    interpretation = f"Line graph: {self.y_column} vs {self.x_column}"
            else:
                interpretation = "Select both X and Y axes for this graph type"
            
            # Update interpretation
            self.ax_interpretation.clear()
            self.ax_interpretation.set_xticks([])
            self.ax_interpretation.set_yticks([])
            self.ax_interpretation.text(0.02, 0.5, f"📊 {interpretation}", fontsize=10, va='center')
            
            plt.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating graph: {str(e)}")
    
    def update_data_info(self):
        self.ax_info.clear()
        self.ax_info.set_xticks([])
        self.ax_info.set_yticks([])
        self.ax_info.set_xlim(0, 1)
        self.ax_info.set_ylim(0, 1)
        
        if self.df is not None:
            info_text = f"Dataset Size: {self.df.shape}\n\n"
            info_text += f"Columns ({len(self.df.columns)}):\n"
            for col in self.df.columns:
                info_text += f"• {col}\n"
            
            info_text += f"\nData Types:\n"
            for col, dtype in self.df.dtypes.items():
                info_text += f"• {col}: {dtype}\n"
            
            self.ax_info.text(0.02, 0.98, info_text, fontsize=8, va='top', linespacing=1.5)
        else:
            self.ax_info.text(0.5, 0.5, 'No data yet', ha='center', va='center')
        
        plt.draw()

# Run the application
if __name__ == "__main__":
    print("Data Graph Explorer")
    print("========================================")
    print("Advanced tool for exploring and visualizing datasets")
    print("• Load data from URL or upload CSV file")
    print("• Create scatter plots, line graphs, histograms, and bar charts")
    print("• Get automatic data interpretation")
    print()
    
    explorer = DataGraphExplorer()