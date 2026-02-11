from pathlib import Path
import config
import shutil
import config
from readers.pdf_reader import convert_pdf_to_markdown

class DocumentManager:

    def __init__(self, chunker, parent_store, vector_db):
        self.parent_store = parent_store
        self.chunker = chunker
        self.vector_db = vector_db
        self.doc_complexity = config.PDF_COMPLEXITY
        self.markdown_dir = Path(config.MARKDOWN_DIR)
        self.markdown_dir.mkdir(parents=True, exist_ok=True)
        
    def add_all_documents(self, document_paths, progress_callback=None):
        if not document_paths:
            return 0, 0
            
        document_paths = [document_paths] if isinstance(document_paths, str) else document_paths
        document_paths = [p for p in document_paths if p and Path(p).suffix.lower() in [".pdf", ".md"]]
        
        if not document_paths:
            return 0, 0
            
        added = 0
        skipped = 0
            
        for i, doc_path in enumerate(document_paths):
            if progress_callback:
                progress_callback((i + 1) / len(document_paths), f"Processing {Path(doc_path).name}")
                
            doc_name = Path(doc_path).stem
            md_path = self.markdown_dir / f"{doc_name}.md"
            
            if md_path.exists():
                skipped += 1
                continue
                
            try:            
                if Path(doc_path).suffix.lower() == ".md":
                    shutil.copy(doc_path, md_path)
                else:
                    convert_pdf_to_markdown(str(doc_path), Path(config.MARKDOWN_DIR), overwrite=False, doc_complexity=self.doc_complexity)          
                parent_chunks, child_chunks = self.chunker.create_chunks(md_path)
                
                if not child_chunks:
                    skipped += 1
                    continue
                
                collection = self.vector_db.get_collection(config.CHILD_COLLECTION)
                collection.add_documents(child_chunks)
                self.parent_store.save_many(parent_chunks)
                
                added += 1
                
            except Exception as e:
                print(f"Error processing {doc_path}: {e}")
                skipped += 1
            
        return added, skipped
    
    def get_markdown_files(self):
        if not self.markdown_dir.exists():
            return []
        return sorted([p.name.replace(".md", ".pdf") for p in self.markdown_dir.glob("*.md")])
    
    def clear_all(self):
        if self.markdown_dir.exists():
            shutil.rmtree(self.markdown_dir)
            self.markdown_dir.mkdir(parents=True, exist_ok=True)
        
        self.parent_store.clear_store()
        self.vector_db.delete_collection(config.CHILD_COLLECTION)
        self.vector_db.create_collection(config.CHILD_COLLECTION)