import sys
import subprocess
import pkg_resources
import os
import requests

# Check and install required packages
required = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Some required packages are missing. Installing them now...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

def read_contexts_from_files(folder_path):
    contexts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                sections = f.read().split('\n\n')
                for section in sections:
                    if section.startswith("Section"):
                        # Remove the "Section X:" prefix and add to contexts
                        context = section.split(':', 1)[1].strip()
                        contexts.append(context)
    return contexts

def generate_qa_pair(context):
    url = "http://localhost:8080/completion"
    prompt = f"[INST] As a CPA/CFA exam expert, create a detailed question and comprehensive answer based on this context:\n\n{context}\n\nFormat your response as:\nQuestion: [Your question]\nAnswer: [Your detailed answer]\n[/INST]"
    
    data = {
        "prompt": prompt,
        "n_predict": 1024,
        "temperature": 0.7,
        "top_p": 0.95,
        "stop": ["</s>", "[INST]"]
    }
    
    response = requests.post(url, json=data)
    return response.json()['content']

def process_contexts(contexts, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, context in enumerate(contexts, 1):
            qa_pair = generate_qa_pair(context)
            f.write(f"QA Pair {i}:\n{qa_pair}\n\n")
            print(f"Processed QA pair {i}")

if __name__ == "__main__":
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Use the current directory to read contexts and write output
    contexts = read_contexts_from_files(current_dir)
    output_file = os.path.join(current_dir, "qa_pairs_output.txt")
    
    process_contexts(contexts, output_file)