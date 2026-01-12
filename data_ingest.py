import os
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import FAISS               
from langchain_core.documents import Document                   
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize Embeddings
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

FOLDER_ROLE_MAP = {
    "admin": ["Admin"],  
    "host": ["Admin", "Host"],
    "participant": ["Admin", "Participant"],
    "public": ["Admin", "Host", "Participant", "Public"]
}

def load_docs():
    docs = []
    
    # Iterate through the defined folders
    for folder_name, role_name in FOLDER_ROLE_MAP.items():
        if not os.path.exists(folder_name):
            print(f"⚠️ Folder not found: {folder_name}")
            continue
            
        # List all files in the current folder
        for filename in os.listdir(folder_name):
            file_path = os.path.join(folder_name, filename)
            
            # Skip directories if any are inside these folders
            if os.path.isdir(file_path):
                continue
                
            text = ""
            try:
                if filename.endswith(".md"):
                    with open(file_path, encoding="utf-8") as f:
                        text = f.read()
                elif filename.endswith(".csv"):
                    df = pd.read_csv(file_path)
                    text = df.to_string(index=False)
                
                if text:
                    docs.append(
                        Document(
                            page_content=text,
                            metadata={"source": file_path, "role": role_name}
                        )
                    )
                    print(f"✅ Loaded {filename} from {folder_name} as {role_name}")
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
                
    return docs
# --- END OF AUTOMATED FOLDER MAPPING ---

def ingest():
    docs = load_docs()
    if not docs:
        print("❌ No documents found to index!")
        return
    print(f"Total: Loaded {len(docs)} documents")
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")
    
    # Create FAISS vector store and save to folder
    vectorstore = FAISS.from_documents(chunks, embedding)
    vectorstore.save_local("faiss_index")
    print("✅ Indexed into FAISS successfully and saved to 'faiss_index' folder")

if __name__ == "__main__":
    ingest()