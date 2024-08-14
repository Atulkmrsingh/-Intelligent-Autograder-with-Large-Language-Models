import pdfplumber
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def find_top_sentences(text, query, top_k=5):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Load a pre-trained sentence embedding model

    sentences = [line.strip() for line in text.split('\n') if line.strip()]

    sentence_embeddings = model.encode(sentences)

    query_embedding = model.encode(query)

    cos_similarities = util.pytorch_cos_sim(query_embedding, sentence_embeddings)[0]

    top_indices = cos_similarities.argsort(descending=True)[:top_k]

    top_sentences = [(sentences[i], find_page_number(text, i)) for i in top_indices]

    return top_sentences

def find_page_number(text, sentence_index):
    lines = text.split('\n')
    total_lines = 0
    for i, line in enumerate(lines):
        total_lines += len(line.split('\n'))
        if total_lines > sentence_index:
            return i + 1
    return len(lines)  # Return the last page if not found

# Example usage
pdf_path = "cs books/word embedding book.pdf"
question = "How many decoder and encoder layers are in transformer?"
answer = "There are 6 layers in decoder layer and 4 layers in encoder of the transformer."
text = extract_text_from_pdf(pdf_path)
top_sentences = find_top_sentences(text, question)
prompt=f"""Given a question, set of evidence sentences, verify whether the answer is correct or not
    Question = {question}
    Evidence 1 = {top_sentences[0][0]}
    Evidence 2 = {top_sentences[1][0]}
    Evidence 3 = {top_sentences[2][0]}
    Evidence 4 = {top_sentences[3][0]}
    Evidence 5 = {top_sentences[4][0]}
    Answer is = {answer} .
    Give marks for the given answer from 0 to 10 :
"""
print(prompt)

print("<-------------------------------->")
GOOGLE_API_KEY="AIzaSyBiWhI-TOWmlahl5puqDAsAvFu0N1_R1HQ"

genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

response = gemini_model.generate_content(prompt)
print(response.text)


# for sentence, page_num in top_sentences:
#     print(f"Page {page_num}: {sentence}")
