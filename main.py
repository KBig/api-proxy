from fastapi import FastAPI, Form
import openai
import os
import json

app = FastAPI()

# Récupère la clé API OpenAI depuis la variable d'environnement
openai.api_key = os.environ.get("OPENAI_API_KEY", "")

@app.post("/analyser")
async def analyser(data: str = Form(...)):
    prompt = (
        "Analyse de manière approfondie les données de marché fournies ci-dessous, issues de plusieurs timeframes (graphique actuel, quotidien et hebdomadaire) pour le symbole. "
        "Ta mission est de réaliser une analyse technique complète et objective, en évaluant non seulement les indicateurs traditionnels (RSI, MACD, MA, ATR, ADX, etc.), "
        "mais également en effectuant des recherches sur le sentiment global du marché. "
        "Fournis une analyse détaillée en intégrant les tendances observées sur les différents timeframes et le sentiment du marché, et justifie clairement ta décision de trading. "
        "Indique précisément un signal de trading (BUY, SELL ou WAIT) ainsi que des recommandations pour le VOLUME, le Stop Loss (SL) et le Take Profit (TP). "
        "Réponds en format JSON exactement sous la forme suivante : "
        "{\"SIGNAL\": \"...\", \"VOLUME\": ..., \"SL\": ..., \"TP\": ..., \"JUSTIFICATION\": \"...\"}.\n"
        + data
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
        # Transformer la réponse JSON en objet
        data_json = json.loads(content)
        # Convertir l'objet en CSV simple
        csv_response = f'{data_json["SIGNAL"]},{data_json["VOLUME"]},{data_json["SL"]},{data_json["TP"]},{data_json["JUSTIFICATION"]}'
        return {"result": csv_response}
    except Exception as e:
        return {"result": f"ERROR,{str(e)}"}
