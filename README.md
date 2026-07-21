# AI Resume Screening Agent

This is a take-home project for the **Rooman Technologies AI Challenge**. The agent ranks a set of resumes against a given job description and outputs an ordered shortlist with reasoning.

## 🚀 Features
- **Multi-format Support:** Parses resumes in PDF, DOCX, and TXT formats.
- **Intelligent Scoring:** Uses GPT-5-mini to evaluate candidates based on context, not just keywords.
- **Ranked Output:** Generates a scored, ordered list of candidates in both JSON and CSV formats.
- **Reasoning:** Provides a detailed explanation for each candidate's score.

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-challenge-agent.git
cd ai-challenge-agent
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
The agent requires an OpenAI API key. Set it as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'
```
*(Note: If you are running this in the Manus sandbox, the environment is already pre-configured.)*

## 📖 How to Run

### Run the Screening Agent
Place your resumes in the `resumes/` folder and your job description in `data/job_description.txt`.
```bash
python main.py --jd data/job_description.txt --resumes resumes/
```

### View Results
- **JSON Output:** `data/results.json`
- **CSV Output:** `data/results.csv`
- **CLI Summary:** The agent will print a ranked table directly to your terminal.

## 📁 Project Structure
- `main.py`: Core logic for parsing, screening, and ranking.
- `data/`: Contains the job description and generated results.
- `resumes/`: Folder for candidate resumes.
- `requirements.txt`: Python dependencies.
- `tradeoffs.md`: Detailed notes on design choices and limitations.

## ⚖️ Tradeoffs and Reasoning
For a detailed explanation of the model choice, scoring method, and potential improvements, please refer to [tradeoffs.md](tradeoffs.md).
