from fastapi import FastAPI, Form
import openai

app = FastAPI()

# Remplacez "YOUR_OPENAI_API_KEY" par votre clé API OpenAI réelle.
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.post("/analyser")
async def analyser(data: str = Form(...)):
    prompt = (
        "Tu es un analyste technique expert. Voici les données du marché:\n\n"
        f"{data}\n\n"
        "Réponds uniquement sous cette forme très simple : SIGNAL,VOLUME,SL,TP,JUSTIFICATION.\n"
        "Par exemple: BUY,0.01,100.0,200.0,Le marché est haussier."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "Vous êtes un expert en analyse technique."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        content = response.choices[0].message.content.strip()
        return {"result": content}
    except Exception as e:
        return {"result": f"ERROR,{str(e)}"}
