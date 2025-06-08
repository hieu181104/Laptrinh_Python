import tkinter as tk
from tkinter import ttk, messagebox
from contacts import ContactManager

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Danh bạ")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f4f8")

        self.manager = ContactManager()
        self.setup_ui()
        self.load_contacts()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), foreground="#2c3e50")
        style.map("Treeview", background=[("selected", "#dfe6e9")])

        frame_form = tk.Frame(self.root, bg="#f0f4f8", pady=10)
        frame_form.pack()

        tk.Label(frame_form, text="Name", bg="#f0f4f8").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="Phone", bg="#f0f4f8").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="Email", bg="#f0f4f8").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        tk.Entry(frame_form, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5)

        phone_entry = tk.Entry(frame_form, textvariable=self.phone_var, width=30, validate="key")
        phone_entry.grid(row=1, column=1, padx=5)
        phone_entry['validatecommand'] = (phone_entry.register(self.validate_number_input), '%P')

        tk.Entry(frame_form, textvariable=self.email_var, width=30).grid(row=2, column=1, padx=5)

        frame_btn = tk.Frame(self.root, bg="#f0f4f8", pady=10)
        frame_btn.pack()

        tk.Button(frame_btn, text="Add", bg="#3498db", fg="white", width=10, command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Edit", bg="#f39c12", fg="white", width=10, command=self.edit_contact).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Delete", bg="#e74c3c", fg="white", width=10, command=self.delete_contact).grid(row=0, column=2, padx=5)

        tk.Label(frame_btn, text="Search:", bg="#f0f4f8").grid(row=0, column=3, padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(frame_btn, textvariable=self.search_var, width=20).grid(row=0, column=4, padx=5)
        self.search_var.trace("w", lambda *args: self.search_contacts())

        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone", "Email"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def validate_number_input(self, value):
        return value.isdigit() or value == ""

    def get_input(self):
        return self.name_var.get(), self.phone_var.get(), self.email_var.get()

    def load_contacts(self, filtered=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        data = filtered if filtered else self.manager.contacts
        for contact in data:
            self.tree.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"]))

    def add_contact(self):
        name, phone, email = self.get_input()
        try:
            self.manager.add_contact(name, phone, email)
            self.load_contacts()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_contact(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            name = item["values"][0]
            self.manager.delete_contact(name)
            self.load_contacts()

    def edit_contact(self):
        selected = self.tree.selection()
        if selected:
            old_item = self.tree.item(selected[0])
            old_name = old_item["values"][0]
            new_name, phone, email = self.get_input()
            try:
                self.manager.update_contact(old_name, new_name, phone, email)
                self.load_contacts()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def search_contacts(self):
        keyword = self.search_var.get()
        if keyword:
            results = self.manager.search(keyword)
            self.load_contacts(results)
        else:
            self.load_contacts()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)  #truyền tới class ContactApp để vẽ giao diện
    root.mainloop() #chạy giao diện
