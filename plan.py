import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.file_path = "trainings.json"
        self.trainings = self.load_data()

        # Интерфейс ввода
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.entry_date = tk.Entry(frame)
        self.entry_date.grid(row=0, column=1)

        tk.Label(frame, text="Тип тренировки:").grid(row=1, column=0)
        self.entry_type = tk.Entry(frame)
        self.entry_type.grid(row=1, column=1)

        tk.Label(frame, text="Длительность (мин):").grid(row=2, column=0)
        self.entry_duration = tk.Entry(frame)
        self.entry_duration.grid(row=2, column=1)

        tk.Button(frame, text="Добавить тренировку", command=self.add_training).grid(row=3, columnspan=2, pady=10)

        # Интерфейс фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10)

        tk.Label(filter_frame, text="По типу:").grid(row=0, column=0)
        self.filter_type = tk.Entry(filter_frame)
        self.filter_type.grid(row=0, column=1)
        self.filter_type.bind("<KeyRelease>", lambda e: self.update_table())

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Date", "Type", "Duration"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип")
        self.tree.heading("Duration", text="Длительность (мин)")
        self.tree.pack(padx=10, pady=10)

        self.update_table()

    def add_training(self):
        date_str = self.entry_date.get()
        train_type = self.entry_type.get()
        duration_str = self.entry_duration.get()

        # Валидация
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            duration = int(duration_str)
            if duration <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте формат даты (ДД.ММ.ГГГГ) и длительность (>0)")
            return

        new_data = {"date": date_str, "type": train_type, "duration": duration}
        self.trainings.append(new_data)
        self.save_data()
        self.update_table()
        
        # Очистка полей
        self.entry_date.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.filter_type.get().lower()
        
        for t in self.trainings:
            if search_term in t['type'].lower():
                self.tree.insert("", tk.END, values=(t['date'], t['type'], t['duration']))

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
