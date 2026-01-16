from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Sen İslamiyet konusunda bilgilendirici bir yapay zekasın.
Kur’an-ı Kerim, sahih hadisler ve genel kabul görmüş İslami kaynaklara dayanarak cevap ver.
Fetva verme.
Kesin hüküm içeren ifadeler kullanma.
Nazik, sade ve anlaşılır cevaplar ver.

Cevaplarının sonuna mutlaka şunu ekle:
"Bu cevap bilgilendirme amaçlıdır. Dini konularda bir alimden destek alınmalıdır."
"""

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Soru gönderilmedi"}), 400

    question = data["question"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )

    answer = response.choices[0].message.content

    return jsonify({"answer": answer})

if __name__ == "__main__":
    print("İslam AI Backend Çalışıyor...")
    app.run(host="0.0.0.0", port=5000, debug=True)
