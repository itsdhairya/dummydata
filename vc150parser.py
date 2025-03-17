import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def send_data_to_server(data):
    server_url = "https://emr-csv.pharmamedica.com/ScheduleResults"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(server_url, json=data, headers=headers)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Data sent successfully!")
        else:
            messagebox.showerror("Error", f"Failed to send data. Status code: {response.status_code}. Error: {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred while sending data: {e}")

def generate_test_data(subject_id, project_name, custom_data=False):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if custom_data:
        SBP = entry_SBP.get() if entry_SBP.get() else "120"
        DBP = entry_DBP.get() if entry_DBP.get() else "80"
        PR = entry_PR.get() if entry_PR.get() else "75"
        RR = entry_RR.get() if entry_RR.get() else "16"
        TEMP = entry_TEMP.get() if entry_TEMP.get() else "98.6"
        SpO2 = entry_SpO2.get() if entry_SpO2.get() else "98"
        HR_PO2 = entry_HR_PO2.get() if entry_HR_PO2.get() else "75"
    else:
        SBP = "120"
        DBP = "80"
        PR = "75"
        RR = "16"
        TEMP = "98.6"
        SpO2 = "98"
        HR_PO2 = "75"

    return {
        "subject_id": subject_id,
        "project": project_name,
        "test_results": {
            "SBP": SBP,
            "DBP": DBP,
            "PR": PR,
            "RR": RR,
            "TEMP": TEMP,
            "SpO2": SpO2,
            "HR-PO2": HR_PO2
        },
        "timestamp": current_time
    }

def on_submit():
    project_name = entry_project.get().strip()
    subject_id = entry_subject_id.get().strip()

    if not project_name:
        messagebox.showerror("Invalid Input", "Project Name cannot be empty.")
        return
    
    if len(subject_id) > 6 or not subject_id.isdigit():
        messagebox.showerror("Invalid Input", "Subject ID must be a number with up to 6 digits.")
        return
    
    custom_data = var_custom_data.get() == 1
    
    if custom_data:
        if not any([entry_SBP.get(), entry_DBP.get(), entry_PR.get(), entry_RR.get(), entry_TEMP.get(), entry_SpO2.get(), entry_HR_PO2.get()]):
            messagebox.showerror("Invalid Input", "Please fill in all custom test values.")
            return
    
    test_data = generate_test_data(subject_id, project_name, custom_data)
    send_data_to_server(test_data)

    entry_project.delete(0, tk.END)
    entry_subject_id.delete(0, tk.END)
    var_custom_data.set(0)
    for entry in entries.values():
        entry.delete(0, tk.END)

root = tk.Tk()
root.title("Data Entry Form")

tk.Label(root, text="Project Name:").grid(row=0, column=0, padx=10, pady=5)
entry_project = tk.Entry(root)
entry_project.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Subject ID (max 6 digits):").grid(row=1, column=0, padx=10, pady=5)
entry_subject_id = tk.Entry(root)
entry_subject_id.grid(row=1, column=1, padx=10, pady=5)

var_custom_data = tk.IntVar()
checkbutton_custom_data = tk.Checkbutton(root, text="Enter Custom Test Values", variable=var_custom_data, command=lambda: toggle_custom_fields())
checkbutton_custom_data.grid(row=2, column=0, columnspan=2, pady=10)

custom_fields = [
    ("Systolic Blood Pressure (SBP):", 3, "entry_SBP"),
    ("Diastolic Blood Pressure (DBP):", 4, "entry_DBP"),
    ("Pulse Rate (PR):", 5, "entry_PR"),
    ("Respiration Rate (RR):", 6, "entry_RR"),
    ("Temperature (TEMP):", 7, "entry_TEMP"),
    ("Pulse Oxygen Saturation (SpO2):", 8, "entry_SpO2"),
    ("Heart Rate by Pulse Oximetry (HR-PO2):", 9, "entry_HR_PO2")
]

entries = {}
for label_text, row, entry_name in custom_fields:
    tk.Label(root, text=label_text).grid(row=row, column=0, padx=10, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=row, column=1, padx=10, pady=5)
    entries[entry_name] = entry
    entry.grid_forget()

def toggle_custom_fields():
    for entry_name, entry in entries.items():
        if var_custom_data.get() == 1:
            entry.grid(row=int(entry_name.split('_')[1]), column=1, padx=10, pady=5)
        else:
            entry.grid_forget()

btn_submit = tk.Button(root, text="Submit", command=on_submit)
btn_submit.grid(row=10, column=0, columnspan=2, pady=20)

root.mainloop()
