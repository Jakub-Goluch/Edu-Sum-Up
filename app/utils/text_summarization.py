from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

from utils.utils import get_documents_pdf, get_documents_txt


def text_summarization(path: str) -> str:
    document = get_documents_txt(path)
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(document, embeddings)
    chain = RetrievalQA.from_chain_type(llm=
                                        ChatOpenAI(temperature=0.0, max_tokens=2000),
                                        chain_type='map_reduce',
                                        retriever=docsearch.as_retriever(),
                                        return_source_documents=True
                                        )
    questions_list = ["Shorten this text"]

    summary = ""
    for question in questions_list:
        summary += chain(
            {'query': f'{question} Expand your statement with as many details as possible.'},
            return_only_outputs=True
        )['result']
    content = f"## Podsumowanie:\n{summary}\n"

    with open("../app/result.txt", "w+") as file:
        file.write(content)

    return summary
