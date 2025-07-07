import customtkinter as ctk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import pdfplumber
import os

# 🌚 Enable Dark Mode
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class PDFExtractorApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("📄 PDF Extractor")
        self.geometry("820x700")
        self.configure(bg="#121212")  # Super dark background
        self.resizable(False, False)

        self.pdf_file_path = None
        self.total_pages = 0
        self.selected_page = ctk.StringVar(value="1")
        self.page_dropdown = None

        self.build_ui()

    def build_ui(self):
        # 💡 Title Banner (Dark Glow)
        ctk.CTkLabel(
            self, text="🧠 Smart PDF Text & Table Extractor",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white", bg_color="#1E1E1E", height=50
        ).pack(fill="x", pady=(0, 10))

        # 📦 Dark Card Frame
        self.card = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=20)
        self.card.pack(padx=20, pady=10, fill="both", expand=False)

        # 📂 File Select Button
        ctk.CTkButton(self.card, text="📂 Select PDF File", command=self.open_pdf_dialog,
                      fg_color="#00b894", hover_color="#00a383", corner_radius=12).pack(pady=(20, 10))

        # 📤 Drag & Drop Label
        self.drop_label = ctk.CTkLabel(
            self.card, text="📤 Drag & Drop PDF Here", height=50, width=300,
            fg_color="#2c2c2c", text_color="#dcdcdc", corner_radius=12
        )
        self.drop_label.pack(pady=5)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.handle_drop)

        # 🔽 Dropdown + Action Buttons
        button_row = ctk.CTkFrame(self.card, fg_color="transparent")
        button_row.pack(pady=10)

        self.page_dropdown = ctk.CTkOptionMenu(
            button_row, values=[], variable=self.selected_page, width=140,
            fg_color="#2e2e2e", button_color="#3d3d3d",
            text_color="#ffffff", dropdown_text_color="#ffffff", dropdown_fg_color="#2e2e2e"
        )
        self.page_dropdown.pack(side="left", padx=10)

        ctk.CTkButton(button_row, text="🔍 Extract Page", command=self.extract_selected_page,
                      fg_color="#0984e3", hover_color="#0868ba", corner_radius=10).pack(side="left", padx=10)

        ctk.CTkButton(button_row, text="💾 Save Output", command=self.save_output,
                      fg_color="#d63031", hover_color="#b42b2b", corner_radius=10).pack(side="left", padx=10)

        # 📜 Output Box
        self.output_box = ctk.CTkTextbox(
            self.card, width=740, height=380,
            corner_radius=15, font=("Courier New", 13),
            wrap="word", fg_color="#101010", text_color="#ffffff", border_color="#444", border_width=2
        )
        self.output_box.pack(pady=(15, 20))

        # 🧼 Footer
        ctk.CTkLabel(self, text="Built with 🧠 by Yugank", font=("Arial", 12),
                     text_color="#777").pack(pady=5)

    def open_pdf_dialog(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filepath:
            self.load_pdf(filepath)

    def handle_drop(self, event):
        filepath = event.data.strip().replace("{", "").replace("}", "")
        if filepath.lower().endswith(".pdf"):
            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", "📥 Loading PDF...")
            self.after(300, lambda: self.load_pdf(filepath))
        else:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", "⚠️ Please drop a valid PDF file.")

    def load_pdf(self, filepath):
        self.pdf_file_path = filepath
        try:
            with pdfplumber.open(self.pdf_file_path) as pdf:
                self.total_pages = len(pdf.pages)
                page_options = [str(i + 1) for i in range(self.total_pages)]
                self.selected_page.set("1")
                self.page_dropdown.configure(values=page_options)
                self.extract_selected_page()
        except Exception as e:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", f"❌ Error loading PDF:\n{str(e)}")

    def extract_selected_page(self):
        if not self.pdf_file_path:
            return
        try:
            page_number = int(self.selected_page.get()) - 1
            with pdfplumber.open(self.pdf_file_path) as pdf:
                page = pdf.pages[page_number]
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

                output = f"📄 File: {os.path.basename(self.pdf_file_path)}\n"
                output += f"📄 Page: {page_number + 1}/{self.total_pages}\n\n"
                output += "📝 Text:\n"
                output += raw_text if raw_text else "[No readable text found]\n"
                output += "\n📊 Tables:\n"
                output += table_text

                self.output_box.delete("1.0", "end")
                self.output_box.insert("1.0", output)
                self.output_box.after(300, lambda: self.output_box.yview_moveto(0.0))

        except Exception as e:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", f"❌ Error:\n{str(e)}")

    def save_output(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")],
                                                 title="Save Output As")
        if save_path:
            try:
                content = self.output_box.get("1.0", "end")
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.output_box.insert("end", f"\n✅ Saved to: {save_path}")
            except Exception as e:
                self.output_box.insert("end", f"\n❌ Save Failed: {str(e)}")

# 🚀 Start the app
if __name__ == "__main__":
    app = PDFExtractorApp()
    app.mainloop()