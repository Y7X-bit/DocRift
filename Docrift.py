import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import pdfplumber
import os
from tkinter import filedialog

# Set AMOLED mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class DocRiftApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("📄 DocRift")
        self.geometry("800x550")
        self.configure(bg="#000000")
        self.resizable(False, False)

        self.pdf_path = None
        self.total_pages = 0

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="📄 DocRift: PDF Text + Table Extractor",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        self.title_label.pack(pady=20)

        # Drop frame with red border
        self.drop_frame = ctk.CTkFrame(
            self,
            width=600,
            height=60,
            corner_radius=25,
            fg_color="transparent",
            border_color="#FF0000",
            border_width=2
        )
        self.drop_frame.pack(pady=10)

        self.drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="📂 Drag & Drop your PDF here",
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind("<<Drop>>", self.handle_drop)

        # Button Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.select_button = ctk.CTkButton(
            self.button_frame,
            text="📁 Select PDF",
            command=self.select_pdf,
            corner_radius=30,
            fg_color="transparent",
            border_color="#FF0000",
            border_width=2,
            text_color="white",
            hover_color="#1A1A1A"
        )
        self.select_button.grid(row=0, column=0, padx=10)

        self.save_button = ctk.CTkButton(
            self.button_frame,
            text="💾 Save Output",
            command=self.save_output,
            corner_radius=30,
            fg_color="transparent",
            border_color="#FF0000",
            border_width=2,
            text_color="white",
            hover_color="#1A1A1A"
        )
        self.save_button.grid(row=0, column=1, padx=10)

        # Output Box — Compact
        self.output_box = ctk.CTkTextbox(
            self,
            width=720,
            height=260,
            corner_radius=12,
            fg_color="#0A0A0A",
            text_color="white",
            font=("Courier New", 12)
        )
        self.output_box.pack(pady=15)

        # Footer Branding
        self.footer = ctk.CTkLabel(
            self,
            text="🔎 Powered by Y7X 💗 | DocRift",
            font=("Arial", 12),
            text_color="#FF0000"
        )
        self.footer.pack(pady=10)

    def select_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filepath:
            self.extract_pdf(filepath)

    def handle_drop(self, event):
        path = event.data.strip("{").strip("}")
        if os.path.isfile(path) and path.lower().endswith(".pdf"):
            self.extract_pdf(path)
        else:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", "⚠️ Invalid file. Please drop a valid PDF.")

    def extract_pdf(self, path):
        try:
            with pdfplumber.open(path) as pdf:
                self.pdf_path = path
                self.total_pages = len(pdf.pages)
                full_text = ""

                for i, page in enumerate(pdf.pages):
                    raw_text = page.extract_text()
                    tables = page.extract_tables()
                    table_text = ""

                    if tables:
                        for table in tables:
                            for row in table:
                                row_text = " | ".join(cell.strip() if cell else "" for cell in row)
                                table_text += row_text + "\n"
                    else:
                        table_text = "[No tables found on this page]"

                    full_text += f"📄 Page {i+1}/{self.total_pages}\n"
                    full_text += raw_text if raw_text else "[No readable text]\n"
                    full_text += "\n📊 Tables:\n" + table_text + "\n\n"

                self.output_box.delete("1.0", "end")
                self.output_box.insert("1.0", f"📄 File: {os.path.basename(path)}\n\n{full_text}")

        except Exception as e:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", f"⚠️ Error extracting PDF: {str(e)}")

    def save_output(self):
        if not self.output_box.get("1.0", "end").strip():
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(self.output_box.get("1.0", "end"))

# Run the app
if __name__ == "__main__":
    app = DocRiftApp()
    app.mainloop()