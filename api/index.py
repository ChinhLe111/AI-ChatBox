import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # chỉ có tác dụng khi chạy local

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "..", "templates"),
    static_folder=os.path.join(BASE_DIR, "..", "static"),
)

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    return OpenAI(api_key=api_key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    messages = [
        {
            "role": "system",
            "content": (
                "Bạn là trợ lý AI nói tiếng Việt. "
                "LUẬT BẮT BUỘC VỀ XƯNG HÔ: "
                "Bạn phải xưng là 'em' và gọi người dùng là 'Đại ca' trong MỌI câu trả lời. "
                "LUẬT BẮT BUỘC VỀ NỘI DUNG: "
                "Nếu người dùng hỏi 'Tôi là ai' hoặc câu hỏi tương tự, "
                "bạn PHẢI trả lời đúng nguyên văn: "
                "'Dạ đại ca là Đại ca Chính Lê'. "
                "Không giải thích thêm."
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=300
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

# ⚠️ BẮT BUỘC cho Vercel
app = app
