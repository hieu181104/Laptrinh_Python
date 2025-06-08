import json
import os

class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    self.contacts = json.load(f)
                except json.JSONDecodeError:
                    self.contacts = []

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.contacts, f, indent=4)

    def validate_phone(self, phone):
        if not phone.isdigit():
            raise ValueError("Số điện thoại chỉ được chứa chữ số")
        if not phone.startswith("0"):
            raise ValueError("Số điện thoại phải bắt đầu bằng số 0")
        if len(phone) > 10:
            raise ValueError("Số điện thoại không được quá 10 chữ số")

    def add_contact(self, name, phone, email):
        self.validate_phone(phone)
        for contact in self.contacts:
            if contact["phone"] == phone and contact["name"] != name:
                raise ValueError("Số điện thoại đã tồn tại")
        self.contacts.append({"name": name, "phone": phone, "email": email})
        self.save()

    def delete_contact(self, name):
        self.contacts = [c for c in self.contacts if c["name"] != name]
        self.save()

    def update_contact(self, old_name, new_name, phone, email):
        self.validate_phone(phone)
        for contact in self.contacts:
            if contact["name"] == old_name:
                contact["name"] = new_name
                contact["phone"] = phone
                contact["email"] = email
                break
        self.save()

    def search(self, keyword):
        return [c for c in self.contacts if c["name"].lower().startswith(keyword.lower())]
