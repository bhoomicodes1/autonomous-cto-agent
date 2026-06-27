from langchain.text_splitter import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
)


def chunk_code(text: str):

    return splitter.split_text(text)