import gradio as gr
import plotly.express as px
import pandas as pd
import numpy as np
import os
from sklearn.manifold import TSNE
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv # Add this

load_dotenv() # Load environment variables from .env file

def get_visualization():
    # 1. Connect to your existing ChromaDB
    db_path = os.path.abspath("./chroma_db")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
    # 2. Get all data
    data = vectorstore.get(include=['embeddings', 'metadatas', 'documents'])
    
    if data['embeddings'] is None or len(data['embeddings']) == 0:
        return "Error: No embeddings found in chroma_db."

    # 3. Dimensionality Reduction (t-SNE)
    # Reducing high-dimensional vectors to 3D for visualization
    tsne = TSNE(n_components=3, random_state=42, perplexity=30)
    projections = tsne.fit_transform(np.array(data['embeddings']))
    
    # 4. Prepare DataFrame
    df = pd.DataFrame(projections, columns=['x', 'y', 'z'])
    df['advisor_id'] = [m.get('advisor_id') for m in data['metadatas']]
    df['summary'] = [doc[:100] + "..." for doc in data['documents']]
    
    # 5. Create Plotly Figure
    fig = px.scatter_3d(
        df, x='x', y='y', z='z',
        color='x',  # Color by position to see clusters
        hover_data=['advisor_id', 'summary'],
        title="Wellness Advisor Vector Space"
    )
    fig.update_traces(marker=dict(size=4, opacity=0.7))
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=40))
    
    return fig

# Gradio Interface
with gr.Blocks(title="Knowledge Base Visualizer") as demo:
    gr.Markdown("# 3D Advisor Knowledge Base")
    gr.Markdown("Visualizing 701 advisor profiles from your ChromaDB index.")
    
    plot = gr.Plot(label="3D Vector Space")
    refresh_btn = gr.Button("Generate/Refresh Plot")
    
    refresh_btn.click(fn=get_visualization, inputs=None, outputs=plot)

if __name__ == "__main__":
    demo.launch()