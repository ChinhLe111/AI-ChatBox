import os
from flask import Flask, render_template, request, session, Response, stream_with_context
from dotenv import load_dotenv
from openai import OpenAI
from datetime import timedelta

load_dotenv()  # chỉ có tác dụng khi chạy local

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "..", "templates"),
    static_folder=os.path.join(BASE_DIR, "..", "static"),
)

app.secret_key = "super-secret-key"
app.permanent_session_lifetime = timedelta(minutes=30)

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    return OpenAI(api_key=api_key)

@app.route("/")
def index():
    return render_template("index.html")

@app.before_request
def init_session():
    session.permanent = True
    if "messages" not in session:
        session["messages"] = [
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
            }
        ]
        
@app.route("/chat", methods=["POST"])
def chat():
    client = get_client()
    # ✅ LẤY REQUEST TRƯỚC
    data = request.get_json()
    user_input = data.get("message", "") if data else ""

    messages = session["messages"]
    messages.append({"role": "user", "content": user_input})

    def generate():
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )

        full_reply = ""

        for chunk in response:
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                full_reply += text
                yield text  # 👈 stream về frontend

        # ✅ cập nhật memory SAU khi stream xong
        messages.append({"role": "assistant", "content": full_reply})
        session["messages"] = messages

    return Response(
        stream_with_context(generate()),
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True)
