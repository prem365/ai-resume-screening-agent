import os
import json
import argparse
import pandas as pd
from typing import List, Dict
from openai import OpenAI
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from tabulate import tabulate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client (automatically uses OPENAI_API_KEY and OPENAI_API_BASE)
client = OpenAI()

class ResumeScreeningAgent:
    def __init__(self, model: str = "gpt-5-mini"):
        self.model = model
        self.system_prompt = (
            "You are an expert HR Recruitment Agent. Your task is to analyze resumes against a Job Description (JD). "
            "For each resume, you must:\n"
            "1. Extract key skills, experience, and education.\n"
            "2. Compute a relevance score (0-100) based on how well the candidate matches the JD.\n"
            "3. Provide a brief, professional reasoning for the score.\n"
            "Output the results in a strict JSON format."
        )

    def extract_text(self, file_path: Path) -> str:
        """Extract text from PDF, DOCX, or TXT files."""
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            reader = PdfReader(file_path)
            return "\n".join([page.extract_text() for page in reader.pages])
        elif suffix == ".docx":
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        elif suffix == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    def screen_resume(self, jd_text: str, resume_text: str) -> Dict:
        """Analyze a single resume against the JD using the LLM."""
        prompt = (
            f"### Job Description:\n{jd_text}\n\n"
            f"### Resume Content:\n{resume_text}\n\n"
            "Analyze the resume above against the job description. Provide the output in JSON format with the following keys: "
            "'candidate_name', 'relevance_score', 'extracted_skills', 'years_of_experience', 'education', 'reasoning'."
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

    def process_batch(self, jd_path: str, resumes_dir: str) -> List[Dict]:
        """Process all resumes in a directory against a JD."""
        jd_text = self.extract_text(Path(jd_path))
        resumes_path = Path(resumes_dir)
        results = []

        for resume_file in resumes_path.iterdir():
            if resume_file.is_file() and resume_file.suffix.lower() in [".pdf", ".docx", ".txt"]:
                print(f"Processing {resume_file.name}...")
                try:
                    resume_text = self.extract_text(resume_file)
                    analysis = self.screen_resume(jd_text, resume_text)
                    analysis["filename"] = resume_file.name
                    results.append(analysis)
                except Exception as e:
                    print(f"Error processing {resume_file.name}: {e}")

        # Rank results by relevance score
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return results

def main():
    parser = argparse.ArgumentParser(description="AI Resume Screening Agent")
    parser.add_argument("--jd", type=str, required=True, help="Path to the Job Description file")
    parser.add_argument("--resumes", type=str, required=True, help="Directory containing resumes")
    parser.add_argument("--output", type=str, default="results.json", help="Output JSON file name")
    
    args = parser.parse_args()

    agent = ResumeScreeningAgent()
    print("Starting AI Resume Screening Agent...")
    results = agent.process_batch(args.jd, args.resumes)

    # Save to JSON
    output_path = Path("data") / args.output
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    # Save to CSV for convenience
    df = pd.DataFrame(results)
    csv_path = output_path.with_suffix(".csv")
    df.to_csv(csv_path, index=False)

    print(f"\nProcessing complete. Results saved to {output_path} and {csv_path}")
    
    # Print summary table
    summary = df[["candidate_name", "relevance_score", "years_of_experience", "education"]]
    print("\n--- Ranked Candidates ---")
    print(tabulate(summary, headers='keys', tablefmt='psql', showindex=False))

if __name__ == "__main__":
    main()
