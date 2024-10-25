from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt

# Initialize global variables
data = pd.DataFrame()

# Function to load dataset
def load_file():
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            data = pd.read_csv(file_path)
            update_column_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset: {e}")

# Function to update column dropdown menu
def update_column_menu():
    columns = list(data.columns)
    column_menu['values'] = columns
    column_menu.set(columns[0] if columns else "")

# Function to display statistics
def show_statistics():
    column = column_menu.get()
    if column and not data.empty:
        mean_value = data[column].mean()
        median_value = data[column].median()
        messagebox.showinfo("Statistics", f"Mean: {mean_value}\nMedian: {median_value}")
    else:
        messagebox.showwarning("No Data", "Please load a dataset first.")

# Function to plot data using Matplotlib
def plot_data_with_matplotlib(plot_type, column):
    plt.figure(figsize=(10, 6))
    try:
        if plot_type == "Line":
            plt.plot(data[column], marker='o')
            plt.title(f"Line Plot of {column}")
            plt.xlabel("Index")
            plt.ylabel(column)
        elif plot_type == "Bar":
            data[column].value_counts().plot(kind="bar")
            plt.title(f"Bar Plot of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
        elif plot_type == "Histogram":
            data[column].plot(kind="hist", bins=30)
            plt.title(f"Histogram of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
        elif plot_type == "Scatter":
            plt.scatter(data.index, data[column])
            plt.title(f"Scatter Plot of {column}")
            plt.xlabel("Index")
            plt.ylabel(column)
        elif plot_type == "Box":
            data.boxplot(column=column)
            plt.title(f"Box Plot of {column}")
            plt.ylabel(column)

        plt.tight_layout()  # Adjust layout to make room for axis labels
        plt.show()
    except TypeError:
        messagebox.showerror("Error", "No numeric data to plot for the selected column.")

# Function to plot data
def plot_data():
    if data.empty:
        messagebox.showwarning("No Data", "Please load a dataset first.")
    else:
        plot_type = plot_type_menu.get()
        plot_data_with_matplotlib(plot_type, column_menu.get())

# Tkinter GUI setup
root = Tk()
root.title("Data Analysis App")
root.geometry("400x300")  # Set window size

# Load Dataset Button
open_button = Button(root, text="Open Dataset", command=load_file)
open_button.pack(pady=10)

# Plot Type Label and Dropdown
plot_type_frame = Frame(root)
plot_type_frame.pack(pady=5)

plot_type_label = Label(plot_type_frame, text="Select Plot Type:")
plot_type_label.pack(side=LEFT)

plot_type_menu = ttk.Combobox(plot_type_frame)
plot_type_menu['values'] = ["Line", "Bar", "Histogram", "Scatter", "Box"]
plot_type_menu.set("Line")  # Default value
plot_type_menu.pack(side=LEFT)

# Column Label and Dropdown
column_frame = Frame(root)
column_frame.pack(pady=5)

column_label = Label(column_frame, text="Select Column:")
column_label.pack(side=LEFT)

column_menu = ttk.Combobox(column_frame)
column_menu.pack(side=LEFT)

# Plot Button
plot_button = Button(root, text="Plot Data", command=plot_data)
plot_button.pack(pady=5)

# Statistics Button
stats_button = Button(root, text="Calculate Statistics", command=show_statistics)
stats_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
