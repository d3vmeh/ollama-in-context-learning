from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader


def load_doc(path):
    doc_loader = PyPDFDirectoryLoader(path)
    return doc_loader.load()

document = load_doc("")
print(document[0])
