# ui-evaluation

This project contains sample chat bot/chat window applications with file upload capability, implemented using four different Python web frameworks:

- **Fasthtml** (FastAPI + fasthtml)
- **FastUI** (FastAPI + FastUI)
- **Davia** (Flask + HTML frontend)
- **Streamlit**

All samples are styled with Tailwind CSS and include a chat interface, file upload, and a button.

---

## Setup

1. **Install dependencies** (for any sample):

```bash
pip install -r requirements.txt
```

---

## Running Each Sample

### 1. Fasthtml

```bash
cd fasthtml
uvicorn app:app --reload
```
- Open your browser at: http://127.0.0.1:8000/

**To run on a custom port (e.g., 9000):**
```bash
uvicorn app:app --reload --port 9000
```
- Then open: http://127.0.0.1:9000/

---

### 2. FastUI

```bash
cd fastui
uvicorn app:app --reload
```
- Open your browser at: http://127.0.0.1:8000/
- See a live FastUI demo here: [https://fastui-demo.onrender.com/](https://fastui-demo.onrender.com/)

**To run on a custom port (e.g., 9001):**
```bash
uvicorn app:app --reload --port 9001
```
- Then open: http://127.0.0.1:9001/

---

### 3. Davia (Flask)

```bash
cd davia
python app.py
```
- Open `davia/index.html` in your browser (or serve it with Flask if you want to integrate the frontend).

**To run on a custom port (e.g., 9002):**
```bash
python app.py --port 9002
```
- Or edit `app.py` to use `app.run(debug=True, port=9002)`
- Then open: http://127.0.0.1:9002/

---

### 4. Streamlit

```bash
cd streamlit
streamlit run app.py
```
- This will open a browser window automatically, or visit the URL shown in the terminal.

**To run on a custom port (e.g., 9003):**
```bash
streamlit run app.py --server.port 9003
```
- Then open: http://localhost:9003/

---

## Project Structure

```
ui-evaluation/
  fasthtml/
    app.py
  fastui/
    app.py
  davia/
    app.py
    index.html
  streamlit/
    app.py
  requirements.txt
  README.md
```

---

## Notes
- All apps use Tailwind CSS for styling (via CDN or class names).
- Each app demonstrates a simple chat window, file upload, and a button.
- You can run each app independently.

Feel free to customize or extend any of the samples!