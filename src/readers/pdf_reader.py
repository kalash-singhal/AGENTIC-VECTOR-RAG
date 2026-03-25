import os
import pymupdf  #import layout
import pymupdf4llm
import glob
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def convert_pdf_to_markdown(input_docs_dir: str, markdown_dir: str, overwrite: bool = False, doc_complexity: str = "simple"):
    """
    Convert simple PDFs to Markdown using PyMuPDF4LLM and complex documents using docling.

    Args:
        input_docs_dir: Path to folder containing PDF files
        markdown_dir: Path to output folder for Markdown files
        overwrite: Whether to overwrite existing Markdown files
        doc_complexity: "simple" for PyMuPDF4LLM, "ocr" for Docling with OCR and table extraction
    """
    if doc_complexity == "ocr":
        ocr_pdfs_to_markdown(input_docs_dir, markdown_dir)
    else:
        simple_pdfs_to_markdowns(f"{input_docs_dir}/*.pdf", markdown_dir, overwrite)
    

def simple_pdf_to_markdown(pdf_file_path, markdown_dir):
    pdf_file = pymupdf.open(pdf_file_path)
    markdown_file = pymupdf4llm.to_markdown(pdf_file, header=False, footer=False, page_separators=True, ignore_images=True, write_images=False, image_path=None)
    markdown_file_cleaned = markdown_file.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='ignore')
    markdown_file_path = Path(markdown_dir) / Path(pdf_file.name).stem
    Path(markdown_file_path).with_suffix(".md").write_bytes(markdown_file_cleaned.encode('utf-8'))

def simple_pdfs_to_markdowns(pdf_path_pattern, markdown_dir, overwrite: bool = False):
    markdown_dir_path = Path(markdown_dir)
    markdown_dir_path.mkdir(parents=True, exist_ok=True)

    for pdf_path in map(Path, glob.glob(pdf_path_pattern)):
        markdown_path = (markdown_dir_path / pdf_path.stem).with_suffix(".md")
        if overwrite or not markdown_path.exists():
            simple_pdf_to_markdown(pdf_path, markdown_dir_path)


def ocr_pdfs_to_markdown(input_docs_dir: str, markdown_dir: str):
    """
    Convert medium-complexity PDFs using Docling with OCR and table extraction.

    Args:
        input_docs_dir: Path to folder containing PDF files
        markdown_dir: Path to output folder for Markdown files
    """
    pdfpipeline_options = PdfPipelineOptions()
    pdfpipeline_options.do_table_structure = True  # Extract table structures
    pdfpipeline_options.do_ocr = True  # Enable OCR for scanned content
    pdfpipeline_options.images_scale = 2.0  # Higher quality image extraction
    pdfpipeline_options.generate_picture_images = True

    document_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pdfpipeline_options)
        }
    )

    markdown_dir_path = Path(markdown_dir)
    markdown_dir_path.mkdir(parents=True, exist_ok=True)
    input_path = Path(input_docs_dir)

    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        pdf_files = [input_path]
       
    if input_path.is_dir():
        pdf_files = list(input_path.glob("*.pdf"))

    for file in pdf_files:
        try:
            converted_doc = document_converter.convert(str(file))
            markdown_doc = converted_doc.document.export_to_markdown()

            markdown_file_path = markdown_dir_path / f"{file.stem}.md"
            markdown_file_path.write_text(markdown_doc, encoding='utf-8')

            print(f"Converted: {file.name}")

        except Exception as e:
            print(f"Error processing {file.name}: {e}")

    print(f"\nConversion complete! Output in '{markdown_dir}'")