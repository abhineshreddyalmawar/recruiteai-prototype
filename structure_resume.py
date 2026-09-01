import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

from extract_text import extract_text_from_pdf
resume_text = extract_text_from_pdf("sample_resume_jordan_lee.pdf")

resume_tool = {
    "name": "extract_resume_data",
    "description": "Extract structured candidate information from a resume text",
    "input_schema": {
        "type": "object",
        "properties": {
            "full_name": {"type": "string"},
            "email": {"type": ["string", "null"]},
            "phone": {"type": ["string", "null"]},
            "skills" : {
                "type" : "array",
                "items" :{"type": "string"}
            },
            "job_history": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "employer": {"type": "string"},
                        "start_date": {"type": "string"},
                        "end_date": {"type": ["string", "null"]}
                    },
                    "required": ["title", "employer", "start_date"]
                }
            }
        },
        "required": ["full_name", "skills", "job_history"]
    }
}
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=[resume_tool],
    tool_choice={"type": "tool", "name": "extract_resume_data"},
    messages=[
        {"role": "user", "content": f"Extract structured data from this resume:\n\n{resume_text}"}
    ]
)
tool_use_block = response.content[0]
extracted_data = tool_use_block.input

print(extracted_data)
