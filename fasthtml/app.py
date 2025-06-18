from fasthtml.common import *

app, rt = fast_app()

@rt
def index():
    return Titled(
        "Chat Bot",
        Div(
            Div(id="chat", cls="mb-4 h-40 overflow-y-auto"),
            Form(
                Input(name="message", placeholder="Ask le Chat", cls="border p-2 w-full mb-2"),
                Button("Send", type="submit", cls="bg-blue-500 text-white px-4 py-2 rounded"),
                method="post", action="/chat"
            ),
            Form(
                Input(type="file", name="file", cls="mb-2"),
                Button("Upload", type="submit", cls="bg-green-500 text-white px-4 py-2 rounded"),
                method="post", action="/upload", enctype="multipart/form-data", cls="mt-4"
            ),
            cls="w-full max-w-md p-4 bg-white rounded shadow"
        ),
        Script(src="https://cdn.tailwindcss.com"),
        cls="bg-gray-50 flex flex-col items-center justify-center min-h-screen"
    )

@rt("/chat", methods=["POST"])
def chat(message: str):
    return Div(f"You said: {message}")

@rt("/upload", methods=["POST"])
def upload(file):
    return Div(f"Uploaded: {file.filename}")

serve()

# Run with: uvicorn app:app --reload 