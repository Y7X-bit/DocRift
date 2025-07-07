from setuptools import setup

setup(
    name="PDFextractorPro",
    version="1.0",
    description="Modern drag-and-drop PDF extractor with CustomTkinter",
    author="Yugank",
    py_modules=["Extract text from PDF"],
    install_requires=["customtkinter", "tkinterdnd2", "pdfplumber"],
)
