# 🎓 Student Academic Support Chatbot

Link: https://student-academic-support-chatbot-gkc3wbuiz4ccqlktx6ppqk.streamlit.app/

This project is an AI-powered chatbot designed to assist with student academic queries by analyzing student performance data. It leverages [LangChain](https://github.com/langchain-ai/langchain), [OpenAI](https://platform.openai.com/), and [Streamlit](https://streamlit.io/) to provide interactive, intelligent responses about student grades, assignments, attendance, and more.

---

## Features

- **Conversational AI:** Ask questions about student performance, rankings, assignments, and more.
- **Data Analysis:** Handles deterministic queries (e.g., "Top 3 students in DBMS", "Assignments pending for John").
- **Natural Language Understanding:** Uses LLMs to answer complex or open-ended questions about the dataset.
- **Streamlit UI:** User-friendly web interface for chatting with the assistant.
- **Customizable Data:** Easily regenerate or update student data using the provided script.

---

## Project Structure

```
.
├── app.py                # Streamlit web app
├── bot.py                # Core chatbot logic and data processing
├── data/
│   ├── students.csv      # Main student data (auto-generated)
│   └── students.py       # Script to generate synthetic student data
├── students.csv          # (Legacy) Example student data
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (e.g., OpenAI API key)
├── .gitignore
└── readme.md
```

---

## Getting Started

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd Student-Academic-Support-Chatbot
```

### 2. Install Dependencies

It's recommended to use a virtual environment.

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your-openai-api-key
```

### 4. Generate Student Data (Optional)

To regenerate the student dataset:

```sh
python data/students.py
```

This will create/update `data/students.csv`.

### 5. Run the App

```sh
streamlit run app.py
```

Open the provided local URL in your browser to interact with the chatbot.

---

## Example Queries

- "Who are the top 3 students in OS?"
- "How many assignments are pending for Michelle Fuller?"
- "List all students who failed in ML."
- "What is the average attendance in DBMS?"
- "Hi" / "Help" / "Who made you?"

---

## Customization

- **Data:** Edit or regenerate `data/students.csv` as needed.
- **Logic:** Modify deterministic query handling in [`bot.py`](bot.py).
- **UI:** Customize the Streamlit interface in [`app.py`](app.py).

---

## Dependencies

See [requirements.txt](requirements.txt) for the full list.

Key libraries:

- pandas
- streamlit
- langchain, langchain-openai
- openai
- python-dotenv
- faker

---

## License

MIT License (add your own license if needed).

---

## Credits

Created using LangChain,
