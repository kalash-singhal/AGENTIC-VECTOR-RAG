import os
import pymupdf
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
        doc_complexity: "simple" for PyMuPDF4LLM, "complex" for Docling with OCR and table extraction
    """
    if doc_complexity == "complex":
        convert_ocr_pdfs(input_docs_dir, markdown_dir)
    else:
        pdfs_to_markdowns(f"{input_docs_dir}/*.pdf", markdown_dir, overwrite)
    

def pdf_to_markdown(pdf_path, output_dir):
    doc = pymupdf.open(pdf_path)
    md = pymupdf4llm.to_markdown(doc, header=False, footer=False, page_separators=True, ignore_images=True, write_images=False, image_path=None)
    md_cleaned = md.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='ignore')
    output_path = Path(output_dir) / Path(doc.name).stem
    Path(output_path).with_suffix(".md").write_bytes(md_cleaned.encode('utf-8'))

def pdfs_to_markdowns(input_docs_dir, output_dir, overwrite: bool = False):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in map(Path, glob.glob(input_docs_dir)):
        md_path = (output_dir / pdf_path.stem).with_suffix(".md")
        if overwrite or not md_path.exists():
            pdf_to_markdown(pdf_path, output_dir)


def convert_ocr_pdfs(input_docs_dir: str, markdown_dir: str):
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

    pdf_files = list(Path(input_docs_dir).glob("*.pdf"))

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