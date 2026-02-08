import gradio as gr
from assembly.chat_interface import ChatInterface
from assembly.document_manager import DocumentManager
from assembly.graph_rag_system import RAGSystem
from vector_db.parent_store_manager import ParentStoreManager
from vector_db.vector_db_manager import VectorDbManager
from chunking.document_chunker import DocumentChuncker

class GradioUI():
    def __init__(self, vector_db: VectorDbManager):
        self.rag_system = RAGSystem(vector_db)
        self.parent_store = ParentStoreManager()
        self.chunker = DocumentChuncker()
        self.vector_db = vector_db
        self.doc_manager = DocumentManager(self.chunker, self.parent_store, self.vector_db)
        self.chat_interface = ChatInterface(self.rag_system)
    
    def format_file_list(self):
        files = self.doc_manager.get_markdown_files()
        if not files:
            return "📭 No documents available in the knowledge base"
        return "\n".join([f"{f}" for f in files])
    
    def upload_handler(self, files, progress=gr.Progress()):
        if not files:
            return None, self.format_file_list()
            
        added, skipped = self.doc_manager.add_all_documents(
            files, 
            progress_callback=lambda p, desc: progress(p, desc=desc)
        )
        
        gr.Info(f"✅ Added: {added} | Skipped: {skipped}")
        return None, self.format_file_list()
    
    def clear_handler(self):
        self.doc_manager.clear_all()
        gr.Info(f"🗑️ Removed all documents")
        return self.format_file_list()
    
    def chat_handler(self, msg, hist):
        return self.chat_interface.chat(msg, hist)
    
    def clear_chat_handler(self):
        self.chat_interface.clear_session()
    
    def create_gradio_ui(self):
        self.rag_system.initialize()
        with gr.Blocks(title="Agentic RAG") as demo:
            
            with gr.Tab("Documents", elem_id="doc-management-tab"):
                gr.Markdown("## Add New Documents")
                gr.Markdown("Upload PDF or Markdown files. Duplicates will be automatically skipped.")
                
                files_input = gr.File(
                    label="Drop PDF or Markdown files here",
                    file_count="multiple",
                    type="filepath",
                    height=200,
                    show_label=False
                )
                
                add_btn = gr.Button("Add Documents", variant="primary", size="md")
                
                gr.Markdown("## Current Documents in the Knowledge Base")
                file_list = gr.Textbox(
                    value=self.format_file_list(),
                    interactive=False,
                    lines = 7,
                    max_lines=10,
                    elem_id="file-list-box",
                    show_label=False
                )
                
                with gr.Row():
                    refresh_btn = gr.Button("Refresh", size="md")
                    clear_btn = gr.Button("Clear All", variant="stop", size="md")
                
                add_btn.click(
                    self.upload_handler, 
                    [files_input], 
                    [files_input, file_list], 
                    show_progress="corner"
                )
                refresh_btn.click(self.format_file_list, None, file_list)
                clear_btn.click(self.clear_handler, None, file_list)
            
            with gr.Tab("Chat"):
                chatbot = gr.Chatbot(
                    height=600, 
                    placeholder="Ask me anything about your documents!",
                    show_label=False
                )
                chatbot.clear(self.clear_chat_handler)
                
                gr.ChatInterface(fn=self.chat_handler, chatbot=chatbot)
        
        return demo