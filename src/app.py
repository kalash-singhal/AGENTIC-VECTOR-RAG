from server.gradio_ui import GradioUI
from server.css_ui import custom_css
from vector_db.vector_db_manager import VectorDbManager

if __name__ == "__main__":
    vector_db = VectorDbManager()
    demo = GradioUI(vector_db).create_gradio_ui()
    print("\n Launching RAG Assistant...")
    demo.launch(css=custom_css)