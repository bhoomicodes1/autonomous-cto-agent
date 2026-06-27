from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings


def chunk_document(text: str, doc_id: str) -> list[dict]:
    """
    Split a document into semantic chunks for RAG.
    """

    settings = get_settings()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=[
            "\nclass ",
            "\ndef ",
            "\n## ",
            "\n# ",
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_text(text)

    return [
        {
            "text": chunk,
            "metadata": {
                "doc_id": doc_id,
                "chunk_index": i,
            },
        }
        for i, chunk in enumerate(chunks)
    ]