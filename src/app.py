import gradio as gr
from server.css_ui import custom_css
from server.gradio_ui import create_gradio_ui

if __name__ == "__main__":
    demo = create_gradio_ui()
    print("\n🚀 Launching RAG Assistant...")
    demo.launch(css=custom_css)