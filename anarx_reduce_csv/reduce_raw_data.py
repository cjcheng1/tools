import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

class CSVProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Processor")
        self.root.geometry("300x200")  # 設定窗口大小

        self.file_path = None

        # 使用 grid 設置佈局，以便均勻分佈控件
        self.open_button = tk.Button(root, text="Open CSV File", command=self.open_file)
        self.open_button.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.start_frame_label = tk.Label(root, text="Adjust Start Frame (-X):")
        self.start_frame_label.grid(row=1, column=0, pady=5, padx=10, sticky="e")
        self.start_frame_entry = tk.Entry(root)
        self.start_frame_entry.insert(0, "90")
        self.start_frame_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.end_frame_label = tk.Label(root, text="Adjust End Frame (+Y):")
        self.end_frame_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.end_frame_entry = tk.Entry(root)
        self.end_frame_entry.insert(0, "105")
        self.end_frame_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.process_button = tk.Button(root, text="Process CSV", command=self.process_csv)
        self.process_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # 設定 grid 列的權重，使得控件可以水平拉伸
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_rowconfigure(3, weight=1)

    def open_file(self):
        self.file_path = askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            messagebox.showinfo("File Selected", f"Selected file: {self.file_path}")

    def process_csv(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        try:
            start_frame_adjustment = int(self.start_frame_entry.get())
            end_frame_adjustment = int(self.end_frame_entry.get())
        
            data = pd.read_csv(self.file_path)
            first_fall_index = data[data['fall_score'] == 1].index[0]
            frame_id = data.loc[first_fall_index, 'frame_id']

            start_frame = frame_id - start_frame_adjustment
            end_frame = frame_id + end_frame_adjustment

            filtered_data = data[(data['frame_id'] >= start_frame) & (data['frame_id'] <= end_frame)]

            filtered_data.to_csv('reduced_raw_data.csv', index=False)
            messagebox.showinfo("Success", "Data successfully filtered and saved to reduced_raw_data.csv")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVProcessorGUI(root)
    root.mainloop()
