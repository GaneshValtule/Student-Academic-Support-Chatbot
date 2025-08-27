import re
import pandas as pd
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# Load environment variables
load_dotenv()

# ---------------- General Queries (Static) -----------------
GENERAL_RESPONSES = {
    "hi": "Hey there!",
    "hello": "Hello! Ready to dive into the video?",
    "hey": "Hey hey! Ask me anything!",
    "good morning": "Good morning! Hope you’ve had your coffee.",
    "good evening": "Good evening! Let’s analyze the student data",
    "good night": "Good night! Don't dream about AI... or do.",
    "how are you": "Running at 100% efficiency. And you?",
    "what's up": "Just hanging out in the cloud, waiting to help!",
    "who are you": "I’m your loyal assistant. Part robot, part knowledge bank.",
    "thank you": "Anytime! Helping is my favorite thing.",
    "thanks": "You're welcome! ",
    "bye": "Goodbye! May your WiFi be strong and your buffers short.",
    "see you": "See you soon! I’ll be right here. Or there. Or wherever you open me.",
    "help": "Type in your question about the video, and I’ll fetch the answer like a good bot.",
    "who made you": "My creators summoned me using LangChain, OpenAI, Streamlit… and a little magic.",
}

def is_general_query(user_input):
    normalized = re.sub(r"[^\w\s]", "", user_input.lower().strip())
    for key in GENERAL_RESPONSES:
        if key in normalized:
            return GENERAL_RESPONSES[key]
    return None

# ---------------- Load Student Data -----------------
def load_student_data(file_path='data/students.csv'):
    df = pd.read_csv(file_path)
    column_mapping = {
        'Student_ID':'student_id',
        'Student Name': 'name',
        'Subject': 'subject',
        'Marks': 'marks',
        'Assignments Completed': 'assignments_submitted',
        'Total Assignments': 'total_assignments',
        'Attendance %': 'attendance',
        'Remarks':'remark'
    }
    df = df.rename(columns=column_mapping)
    df = df[['student_id','name', 'subject', 'marks', 'attendance', 'assignments_submitted', 'total_assignments','remark']]
    return df

# ---------------- Process Student Data -----------------
def process_student_data(df):
    student_docs = []

    for name, group in df.groupby('name'):
        details = []
        for _, row in group.iterrows():
            details.append(
                f"In {row['subject']}, the student scored {row['marks']} marks, "
                f"attended {row['attendance']}% of classes, "
                f"completed {row['assignments_submitted']} out of {row['total_assignments']} assignments, "
                f"and received the remark: {row['remark']}."
            )
        student_id = group['student_id'].iloc[0]
        student_text = f"Student: {name}, Student ID: {student_id}\n" + '\n'.join(details)
        student_docs.append(student_text)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.create_documents(student_docs)
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 50})
    return retriever
# ---------------- Deterministic Queries -----------------
def handle_deterministic_queries(user_input, df):
    
    normalized = user_input.lower()
    
    if "top 3 students" in normalized:
        if "in" in normalized:
            subject = normalized.split("in")[-1].strip()
            subject_df = df[df["subject"].str.lower().str.strip() == subject.lower().strip()]
            if subject_df.empty:
                available_subjects = ", ".join(df["subject"].unique())
                return f"No data found for subject: {subject}. Available subjects are: {available_subjects}"
            ranking = subject_df.groupby("name")["marks"].mean().sort_values(ascending=False).head(3)
        else:
            ranking = df.groupby("name")["marks"].mean().sort_values(ascending=False).head(3)
        return "Top 3 Students:\n" + "\n".join([f"{i+1}. {name} ({score})" for i, (name, score) in enumerate(ranking.items())])

    if "assignments pending" in normalized:
        name_match = re.search(r"for (\w+)", normalized)
        if name_match:
            student_name = name_match.group(1).capitalize()
            student_rows = df[df["name"].str.lower() == student_name.lower()]
            if student_rows.empty:
                return f"No student found with name {student_name}"
            pending = (student_rows["total_assignments"].sum() - student_rows["assignments_submitted"].sum())
            return f"{student_name} has {pending} pending assignments."
        return "Please specify a student name."
    
    return None

# ---------------- LangChain QA Chain -----------------
def qa_chain(retriever, df):
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def qa_logic(inputs):
        user_input = inputs["question"]

        # Check general queries
        static_response = is_general_query(user_input)
        if static_response:
            return static_response

        # Check deterministic queries
        deterministic_response = handle_deterministic_queries(user_input, df)
        if deterministic_response:
            return deterministic_response

        # Retrieve relevant documents
        context_docs = retriever.get_relevant_documents(user_input)
        context = format_docs(context_docs)

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        if context.strip():
            prompt = PromptTemplate(
                template=""" You are a knowledgeable assistant analyzing student data. 
                        Use the context below to answer the question.
                        If the question asks for an average, percentage, or top/bottom ranking, 
                        make sure you use ALL the rows in the context, not just a few examples.
                        - If asked "how many students", list all unique student names from the context 
                        and count them (do not double count duplicates).  
                        - If asked averages or totals, compute using all rows in the context.  
                        {context}
                        Question: {question}""",
                input_variables=["context", "question"]
            )
            return llm.invoke(prompt.format(context=context, question=user_input))
        
        return "Sorry, I couldn’t find anything relevant."
    return RunnableLambda(qa_logic)

# ---------------- Example Usage -----------------
if __name__ == "__main__":
    df = load_student_data("data/students.csv")
    vectorstore = process_student_data(df)
    chatbot = qa_chain(vectorstore, df)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot: Goodbye!")
            break
        response = chatbot({"question": user_input})
        print(f"Bot: {response}")