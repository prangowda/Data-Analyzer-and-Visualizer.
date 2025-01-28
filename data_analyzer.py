import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, filedialog, Button, Label, StringVar, messagebox


class DataAnalyzer:
    def __init__(self):
        self.data = None
        self.root = Tk()
        self.root.title("Data Analyzer and Visualizer")
        self.root.geometry("400x300")
        
        self.file_label = Label(self.root, text="No file selected", wraplength=300)
        self.file_label.pack(pady=10)

        Button(self.root, text="Load File", command=self.load_file).pack(pady=10)
        Button(self.root, text="Show Data Summary", command=self.show_summary).pack(pady=10)
        Button(self.root, text="Create Visualization", command=self.create_visualization).pack(pady=10)

        self.status = StringVar()
        self.status_label = Label(self.root, textvariable=self.status, fg="blue")
        self.status_label.pack(pady=10)
        
        self.root.mainloop()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            try:
                if file_path.endswith(".csv"):
                    self.data = pd.read_csv(file_path)
                elif file_path.endswith(".xlsx"):
                    self.data = pd.read_excel(file_path)
                self.file_label.config(text=f"File loaded: {file_path.split('/')[-1]}")
                self.status.set("File loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
                self.status.set("Failed to load file.")
        else:
            self.status.set("No file selected.")

    def show_summary(self):
        if self.data is not None:
            summary = self.data.describe(include="all").transpose()
            summary_file = "data_summary.txt"
            with open(summary_file, "w") as f:
                f.write(summary.to_string())
            messagebox.showinfo("Summary Generated", f"Summary saved as {summary_file}")
            self.status.set("Summary generated!")
        else:
            messagebox.showerror("Error", "No file loaded. Please load a file first.")
            self.status.set("No file loaded.")

    def create_visualization(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=["number"]).columns.tolist()
            if not numeric_cols:
                messagebox.showerror("Error", "No numeric columns found in the dataset.")
                return
            
            def plot_and_save():
                try:
                    plot_type = plot_var.get()
                    col_x = x_var.get()
                    col_y = y_var.get()
                    if plot_type == "Bar Chart":
                        sns.barplot(data=self.data, x=col_x, y=col_y)
                    elif plot_type == "Histogram":
                        sns.histplot(data=self.data, x=col_x)
                    elif plot_type == "Scatter Plot":
                        sns.scatterplot(data=self.data, x=col_x, y=col_y)
                    elif plot_type == "Box Plot":
                        sns.boxplot(data=self.data, x=col_x, y=col_y)
                    plt.title(f"{plot_type} of {col_x} vs {col_y}")
                    plt.tight_layout()
                    plot_file = f"{plot_type.replace(' ', '_').lower()}.png"
                    plt.savefig(plot_file)
                    plt.show()
                    messagebox.showinfo("Plot Saved", f"Plot saved as {plot_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create plot: {e}")
            
            plot_window = Tk()
            plot_window.title("Create Visualization")
            
            plot_var = StringVar(value="Bar Chart")
            plot_label = Label(plot_window, text="Select Plot Type:")
            plot_label.pack()
            plot_options = ["Bar Chart", "Histogram", "Scatter Plot", "Box Plot"]
            for opt in plot_options:
                Button(plot_window, text=opt, command=lambda opt=opt: plot_var.set(opt)).pack()
            
            x_var = StringVar(value=numeric_cols[0])
            y_var = StringVar(value=numeric_cols[0])
            Label(plot_window, text="Select X-axis Column:").pack()
            for col in numeric_cols:
                Button(plot_window, text=col, command=lambda col=col: x_var.set(col)).pack()
            
            Label(plot_window, text="Select Y-axis Column:").pack()
            for col in numeric_cols:
                Button(plot_window, text=col, command=lambda col=col: y_var.set(col)).pack()
            
            Button(plot_window, text="Generate Plot", command=plot_and_save).pack()
        else:
            messagebox.showerror("Error", "No file loaded. Please load a file first.")
            self.status.set("No file loaded.")


if __name__ == "__main__":
    DataAnalyzer()
