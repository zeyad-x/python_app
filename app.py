import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog

# إنشاء نافذة الواجهة الرئيسية
root = tk.Tk()
root.title("إنشاء ملف Batch")
root.geometry("500x400")

# المتغيرات
selected_folder = ""
output_file_path = ""

# دالة اختيار المجلد
def browse_folder():
    global selected_folder
    folder = filedialog.askdirectory()
    if folder:
        selected_folder = folder
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, selected_folder)

# دالة اختيار مكان الحفظ
def browse_output_file():
    global output_file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".bat", filetypes=[("Batch Files", "*.bat")])
    if file_path:
        if not file_path.endswith(".bat"):
            messagebox.showwarning("تحذير", "يجب أن يكون اسم الملف بصيغة .bat")
            return
        output_file_path = file_path
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_file_path)

# دالة إنشاء ملف الـ Batch
def create_batch_file():
    if not selected_folder:
        messagebox.showwarning("تحذير", "يجب اختيار مجلد يحتوي على الملفات التنفيذية (.exe).")
        return

    if not output_file_path:
        messagebox.showwarning("تحذير", "يجب تحديد مكان حفظ ملف الـ Batch.")
        return

    try:
        batch_content = ""
        for root_dir, _, files in os.walk(selected_folder):
            for file in files:
                if file.endswith(".exe"):
                    file_path = os.path.join(root_dir, file)
                    batch_content += f'start "" "{file_path}"\n'

        if not batch_content:
            messagebox.showwarning("تحذير", "لم يتم العثور على أي ملفات تنفيذية (.exe) في المجلد المختار.")
            return

        with open(output_file_path, "w") as batch_file:
            batch_file.write(batch_content)

        messagebox.showinfo("نجاح", "تم إنشاء ملف الـ Batch بنجاح!")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء إنشاء ملف الـ Batch: {e}")

# إنشاء العناصر في الواجهة
tk.Label(root, text="اختر مجلد الملفات:").pack(pady=5)
folder_entry = tk.Entry(root, width=50)
folder_entry.pack(pady=5)
tk.Button(root, text="Browse", command=browse_folder).pack(pady=5)

tk.Label(root, text="اختر مكان تصدير الملف:").pack(pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)
tk.Button(root, text="Browse", command=browse_output_file).pack(pady=5)

tk.Button(root, text="تصدير", command=create_batch_file).pack(pady=10)

# تشغيل الواجهة
root.mainloop()