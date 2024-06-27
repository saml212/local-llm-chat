Certainly! I'll update the README.md file to include information about the new PDF processing script. Here's the revised version:

```markdown
# CPA/CFA QA Pair Generator

This project uses a large language model (LLM) to generate question-answer pairs for CPA/CFA exam preparation. It includes scripts for processing PDF documents and generating QA pairs based on the extracted content.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- llama.cpp (for running the local LLM server)

## Setup

1. Download the Mixtral 8x7B model:
   ```bash
   curl -L https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf -o mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf
   ```

2. Create a `.env.ci` file in the root directory of your project with the following content:
   ```
   MONGODB_URL=mongodb://localhost:27017

   MODELS=`[
     {
       "name": "Mixtral-8x7B-Instruct",
       "displayName": "Mixtral 8x7B Instruct",
       "description": "Powerful mixture of experts model for QA generation",
       "chatPromptTemplate": "<s>[INST] {{#if @first}}{{#if @root.preprompt}}{{@root.preprompt}}\n{{/if}}{{/if}}{{content}} [/INST]",
       "parameters": {
         "temperature": 0.7,
         "top_p": 0.95,
         "repetition_penalty": 1.1,
         "top_k": 40,
         "truncate": 4096,
         "max_new_tokens": 1024,
         "stop": ["</s>", "[INST]"]
       },
       "endpoints": [
         {
           "type": "llamacpp",
           "url": "http://localhost:8080"
         }
       ]
     }
   ]`
   ```

3. Run the setup script to create a virtual environment and install dependencies:
   ```bash
   ./setup.sh
   ```

## Usage

### Processing PDFs

1. Place your PDF files in a designated input folder.

2. Update the `input_folder` and `output_folder` paths in the `pdf_to_text.py` script.

3. Run the PDF processing script:
   ```bash
   python pdf_to_text.py
   ```
   This will create text files in your output folder, with the content organized into sections of related information.

### Generating QA Pairs

1. Start the llama.cpp server:
   Open a new terminal window and run:
   ```bash
   llama-server --model mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf -c 8192 --n-gpu-layers 35 --threads 8
   ```
   Keep this terminal window open.

2. Activate the virtual environment (if not already activated):
   ```bash
   source venv/bin/activate
   ```

3. Update the `generate_qa.py` script to read contexts from the processed text files:
   - Modify the `read_contexts_from_files` function to point to your output folder.
   - Update the main execution block to use this function for getting contexts.

4. Run the QA generation script:
   ```bash
   python generate_qa.py
   ```

5. The generated QA pairs will be saved in a file named `qa_pairs_output.txt` in the same directory.

## Customization

- Adjust the PDF processing parameters in `pdf_to_text.py` to fine-tune text extraction and grouping.
- Modify the prompt or parameters in the `generate_qa_pair` function in `generate_qa.py` to adjust the QA generation process.

## Troubleshooting

- If you encounter any issues with missing packages, the script will attempt to install them automatically.
- Ensure the llama.cpp server is running before executing the QA generation script.
- If you're having trouble with the LLM, check that the model file is completely downloaded and in the correct location.
- For PDF processing issues, check file permissions and ensure your PDFs are not encrypted.

## Notes

- This setup uses a local LLM, which means all processing happens on your device. No API calls or fees are involved.
- The Mixtral 8x7B model is quite large (about 24GB). Ensure you have sufficient storage space and RAM to run it effectively.
- Processing large PDFs and generating QA pairs can be time-consuming. Be patient and consider processing in batches for large datasets.

## License

[IDK ask Neil]
```
