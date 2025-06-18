from typing import List, Optional
from pydantic import BaseModel
from davia import Davia

app = Davia()

class ChatInput(BaseModel):
    message: str
    context: Optional[List[str]] = None

class FileUploadInput(BaseModel):
    filename: str
    content_type: str

@app.task
def chat(input_data: ChatInput) -> dict:
    """
    Process a chat message and return a response.
    
    Args:
        input_data (ChatInput): The chat input containing message and optional context
        
    Returns:
        dict: Response containing the processed message
    """
    return {
        'response': f'You said: {input_data.message}',
        'context': input_data.context or []
    }

@app.task
def upload_file(input_data: FileUploadInput) -> dict:
    """
    Handle file upload and return file information.
    
    Args:
        input_data (FileUploadInput): The file upload input containing filename and content type
        
    Returns:
        dict: Response containing the file information
    """
    return {
        'filename': input_data.filename,
        'content_type': input_data.content_type,
        'status': 'success'
    }

if __name__ == '__main__':
    app.run() 