import os
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import numpy as np

# Download necessary NLTK data
nltk.download('punkt', quiet=True)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def process_text(text):
    # Split text into sentences
    sentences = sent_tokenize(text)
    
    # Remove very short sentences (likely noise)
    sentences = [s for s in sentences if len(s.split()) > 5]
    
    return sentences

def create_embeddings(sentences, model):
    return model.encode(sentences)

def group_sentences(sentences, embeddings, threshold=0.7):
    groups = []
    current_group = [sentences[0]]
    current_embedding = embeddings[0]

    for i in range(1, len(sentences)):
        similarity = np.dot(current_embedding, embeddings[i])
        if similarity > threshold:
            current_group.append(sentences[i])
        else:
            groups.append(' '.join(current_group))
            current_group = [sentences[i]]
            current_embedding = embeddings[i]

    if current_group:
        groups.append(' '.join(current_group))

    return groups

def process_pdf_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    model = SentenceTransformer('all-MiniLM-L6-v2')

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            text = extract_text_from_pdf(pdf_path)
            sentences = process_text(text)
            embeddings = create_embeddings(sentences, model)
            groups = group_sentences(sentences, embeddings)

            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, group in enumerate(groups):
                    f.write(f"Section {i+1}:\n{group}\n\n")

            print(f"Processed {filename}")

if __name__ == "__main__":
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define relative paths
    input_folder = os.path.join(current_dir, "pdfs")
    output_folder = current_dir  # This will output to the same directory as the script
    
    process_pdf_folder(input_folder, output_folder)