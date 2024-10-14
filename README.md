# LlamaIndex PDF Chatbot using Milvus and Ollama

This project is a PDF chatbot application built with [LlamaIndex](https://github.com/jerryjliu/llama_index), [Milvus](https://milvus.io/), and [Ollama](https://ollama.com/). The chatbot allows users to upload PDF documents and query them interactively using a natural language interface. This README provides an overview of the installation, usage, and components of the project.

## Features

- Load and parse PDF documents for interaction.
- Use LlamaIndex for language processing and Milvus as the vector store.
- Query documents in natural language and receive AI-powered responses.
- Integrate Streamlit for the web interface.

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [llama-index](https://pypi.org/project/llama-index/)
- [Milvus](https://milvus.io/docs/install_standalone-docker.md)
- [Ollama](https://ollama.com/)
- Other dependencies are listed in `requirements.txt`

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Milvus instance:**
   Use Docker Compose to start a Milvus server:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```
   Refer to the [Milvus installation guide](https://milvus.io/docs/install_standalone-docker.md) to set up a local Milvus instance.

## How to Use

1. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

2. **Upload PDF documents:**
   - Use the sidebar to upload one or multiple PDF files.

3. **Query the chatbot:**
   - Enter your questions in the chat input box, and the chatbot will respond based on the content of the uploaded PDFs.

## Code Explanation

### PDF Loading

- **`load_pdf_data(pdf_directory)`** and **`load_pdf_files(input_files)`** are used to load PDF documents from a specified directory or input files.
- These functions utilize `SimpleDirectoryReader` to read PDF documents.

### Setting up LLM and Embedding Model

- The LLM used here is **Ollama**, specifically the "llama3" model.
- **HuggingFaceEmbedding** is used for embedding sentences with the model "sentence-transformers/all-MiniLM-L6-v2".

### Building the Query Engine

- **`get_engine(documents)`** function creates a **MilvusVectorStore** instance to store vectors from the uploaded documents.
- **VectorStoreIndex** is used to index these vectors, and a query engine is created to answer questions using this index.

### Streamlit UI

- A **Streamlit** interface is provided to allow users to upload their PDFs and ask questions.
- Users can upload one or more PDFs through the sidebar.
- User inputs are handled via **`st.chat_input()`**.
- The chatbot response is streamed in real-time using **`stream.response_gen`**.

## Project Structure

- **`app.py`**: The main application code to run the Streamlit interface.
- **`requirements.txt`**: Lists all the dependencies needed to run the project.

## Limitations and Future Improvements

- **Single User Session**: The chatbot only supports a single user session. Future versions can extend this to multiple users.
- **Model Performance**: Performance might vary based on the size of the PDF files and computational resources.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- **LlamaIndex**: For providing the core library to work with PDFs.
- **Milvus**: As a scalable vector database.
- **Streamlit**: For the user-friendly interface.

## Contributing

Feel free to submit issues, fork the repository, and send pull requests.

## Contact

For any queries, please contact [your_email@domain.com].