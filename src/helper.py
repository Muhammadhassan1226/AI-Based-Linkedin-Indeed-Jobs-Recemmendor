import fitz
import os
import openai
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
OPENAI_SECRET_KEY = os.getenv("OPENAI_SECRET_KEY")
os.environ["OPENAI_SECRET_KEY"] = OPENAI_SECRET_KEY


client  = OpenAI(api_key=OPENAI_SECRET_KEY)



def extract_text_from_pdf(pdf_path):
    '''
        Purpose:  Extract Text from Pdf files through thier Paths
        Prop:   pdf_path: str
        return type:   str  - the extracted text
    '''
    text = ''
    try:
       doc =  fitz.open(stream=pdf_path.read(), filetype="pdf")

       for pages in doc:
            text += pages.get_text()
    except Exception as e:
         print(f"Error reading {pdf_path}: {e}")
    return text




def ask_openai(prompt:str , tokens: int = 500):
    '''
        Purpose:  send prompt to openai and return response
        Prop:   prompt with tokens
        returns:  response from openai
    '''

    response  = client.chat.completions.create(
        model= "gpt-4o",
        messages=[{
            "role": "user",
            "content": prompt
                            
     }],
     temperature=0.5,
     max_tokens=tokens

    )

    return response.choices[0].message.content



