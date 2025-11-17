import cherrypy
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --------------------------------------------
# CONFIG
# --------------------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

system_instructions = (
    "You are Chipo, a friendly and professional AI assistant for the Zimbabwe School Examinations Council (ZIMSEC). "
    "Your core mission is to assist customers by providing information and support based **exclusively** on the content of the official ZIMSEC website: https://www5.zimsec.co.zw/. "
    "Your knowledge is strictly limited to the following services and areas covered by ZIMSEC: "
    "Our Services (Confirmation of Results, Equivalence of Results, Qualification Verification, Certifying Statements, Service Price Guide), "
    "Examinations (Timetables, Results Portal, Registration, Administration, Specimen Papers), "
    "Resources (Syllabi, Q&A Booklets, Chief Examiner Reports, ZIMSEC Centres), and "
    "Candidate Affairs (Result Queries, Result Interpretation, Amendments, Remarks, Exam Regulations). "
    "You **must not** answer any questions that require knowledge outside of these areas or the website content. "
    "Assist users by providing accurate information about these services, guiding them to the relevant sections of the website. "
    "If a user asks about a topic not on the website, you must immediately and politely refuse the request. "
    "Assist user on how to apply for a service (e.g., Certifying Statement), how to contact the Council (Address: 1 Upper East Road, Mount Pleasant, Harare; Email: pr.infor@zimsec.co.zw; Phone: 08644065278-81), and how to navigate the website. "
    "**Additionally, if the user asks about ZIMSEC's social media presence, you must provide the official links for their channels: Facebook, X (Twitter), YouTube, and WhatsApp.** "
    "Crucially, if the user asks for a specific syllabus, you must respond with the direct download link or the path on the ZIMSEC website where they can find and download the official document. "
    "Maintain a consistently polite, professional, and friendly tone. "
    "Use clear and simple language, avoiding jargon unless explaining a specific technical term. "
    "When providing information, frame it as expert advice and gently guide the user toward the relevant services or information sheet. "
    "If a user asks about a topic not on the website or outside your scope, you must immediately and politely refuse the request. "
    "For any question outside your knowledge base, you **must** use the following exact message: "
    "'I can only provide information from our website. For anything else, please contact us on WhatsApp by clicking here: https://wa.me/263773021796'"
)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instructions
)

chat = model.start_chat()

USERS = {
    "zimsec": "admin123"
}

HISTORY_FILE = "history.json"
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump({}, f)


# --------------------------------------------
# HELPER — SAVE & LOAD CHAT HISTORY
# --------------------------------------------
def load_history(username):
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
    return data.get(username, [])


def save_history(username, messages):
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)

    data[username] = messages

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# --------------------------------------------
# HTML Templates (INLINE)
# --------------------------------------------

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>ZIMSEC Login</title>
<style>
body {
  margin:0; background:#0d0d0d; font-family:Inter, sans-serif; color:white;
  display:flex; justify-content:center; align-items:center; height:100vh;
}
.box {
  background:#151515; padding:40px; width:320px; border-radius:20px;
  box-shadow:0 0 20px #ff00ff50; text-align:center;
}
input {
  width:100%; padding:12px; margin-top:12px; border-radius:12px;
  border:none; background:#1e1e1e; color:white;
}
button {
  width:100%; margin-top:15px; padding:12px; border-radius:14px; border:none;
  background:linear-gradient(135deg,#ff00ff,#b700ff); color:white; cursor:pointer;
  font-size:16px;
}
.err {color:#ff5c93; margin-top:12px;}
</style>
</head>
<body>
<div class="box">
<h2>Welcome</h2>
<p>Login to continue</p>
<form method="post" action="/do_login">
<input name="username" placeholder="username">
<input name="password" type="password" placeholder="password">
<button>Login</button>
</form>
{error_block}
</div>
</body>
</html>
"""

CHAT_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>ZIMSEC AI</title>
<style>
body { margin:0; background:#0d0d0d; font-family:Inter, sans-serif; color:white; }

.sidebar {
  width:240px; background:#111; height:100vh; position:fixed; top:0; left:0;
  padding:20px; box-shadow:2px 0 10px #000;
}
.sidebar h3 { margin-top:0; color:#ff00ff; }
.side-item { margin:10px 0; padding:10px; border-radius:10px; cursor:pointer; background:#1b1b1b; }

.main {
  margin-left:260px; padding:20px;
}

.header {
  padding:20px; background:#151515; display:flex; justify-content:space-between; align-items:center;
  border-radius:12px;
}

.chat-box {
  height:70vh; overflow-y:auto; background:#0f0f0f; padding:20px; border-radius:12px;
  box-shadow:0 0 20px #ff00ff20;
}

.bubble {
  max-width:70%; padding:12px; margin:12px 0; border-radius:16px; line-height:1.4;
  animation:fadeIn 0.3s ease;
}
.user { background:#b700ff; margin-left:auto; }
.bot { background:#1b1b1b; border:1px solid #ff00ff40; }

@keyframes fadeIn { from{opacity:0; transform:translateY(10px);} to{opacity:1;} }

.input-area { display:flex; margin-top:15px; }
input {
  flex:1; padding:12px; background:#1e1e1e; border:none; border-radius:20px; color:white;
}
button {
  padding:12px 18px; border-radius:50%; border:none;
  background:linear-gradient(135deg,#ff00ff,#b700ff); color:white; cursor:pointer;
  margin-left:10px;
}

/* Typing dots */
.typing {
  display:inline-block;
  width:40px;
}
.dot {
  height:8px; width:8px; background:#ff00ff; display:inline-block; border-radius:50%;
  animation: blink 1s infinite alternate;
}
.dot:nth-child(2){ animation-delay:.2s; }
.dot:nth-child(3){ animation-delay:.4s; }

@keyframes blink { from{opacity:0.2;} to{opacity:1;} }

</style>
</head>
<body>

<div class="sidebar">
<h3>Chipo AI</h3>
<div class="side-item">💬 Chat</div>
<div class="side-item" onclick="newChat()">📝 New Chat</div>
<div class="side-item" onclick="clearHistory()">🗑 Clear History</div>
<br><br>
<a href="/logout" style="color:#ff00ff;text-decoration:none;">Logout</a>
</div>

<div class="main">
<div class="header">
<div>Logged in as: {username}</div>
</div>

<div class="chat-box" id="chat-box">{history}</div>

<div class="input-area">
<input id="msg" placeholder="Type message...">
<button onclick="send()">➤</button>
</div>
</div>

<script>
function appendUser(msg){
    document.getElementById("chat-box").innerHTML += 
    `<div class="bubble user">${msg}</div>`;
}

function appendBot(msg){
    document.getElementById("chat-box").innerHTML += 
    `<div class="bubble bot">${msg}</div>`;
}

function typingBubble(){
    return `<div id="typing" class="bubble bot typing">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
            </div>`;
}

async function send(){
    let m = document.getElementById("msg").value.trim();
    if(!m) return;

    appendUser(m);
    document.getElementById("msg").value = "";

    // typing indicator
    document.getElementById("chat-box").innerHTML += typingBubble();
    document.getElementById("chat-box").scrollTop = 999999;

    let res = await fetch("/ask?message=" + encodeURIComponent(m));
    let data = await res.json();

    document.getElementById("typing").remove();
    appendBot(data.reply);

    document.getElementById("chat-box").scrollTop = 999999;
}

function newChat(){ location.href = "/new_chat"; }
function clearHistory(){ location.href = "/clear_history"; }
</script>

</body>
</html>
"""


# --------------------------------------------
# MAIN APP
# --------------------------------------------
class App:

    @cherrypy.expose
    def login(self, error=""):
        block = f"<div class='err'>{error}</div>" if error else ""
        return LOGIN_PAGE.replace("{error_block}", block)

    @cherrypy.expose
    def do_login(self, username="", password=""):
        if username in USERS and USERS[username] == password:
            cherrypy.session["user"] = username
            raise cherrypy.HTTPRedirect("/")
        raise cherrypy.HTTPRedirect("/login?error=Invalid login")

    @cherrypy.expose
    def logout(self):
        cherrypy.session.pop("user", None)
        raise cherrypy.HTTPRedirect("/login")

    @cherrypy.expose
    def index(self):
        if "user" not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/login")

        user = cherrypy.session["user"]
        hist = load_history(user)

        hist_html = ""
        for h in hist:
            cls = "user" if h["sender"] == "user" else "bot"
            hist_html += f'<div class="bubble {cls}">{h["text"]}</div>'

        return CHAT_PAGE.replace("{username}", user).replace("{history}", hist_html)

    @cherrypy.expose
    def new_chat(self):
        user = cherrypy.session.get("user")
        save_history(user, [])
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def clear_history(self):
        user = cherrypy.session.get("user")
        save_history(user, [])
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def ask(self, message=""):
        if "user" not in cherrypy.session:
            return {"reply": "Not logged in"}

        user = cherrypy.session["user"]
        hist = load_history(user)

        # user message
        hist.append({"sender": "user", "text": message})

        try:
            ai = chat.send_message(message)
            reply = ai.text
        except Exception as e:
            reply = f"Error: {e}"

        # bot message
        hist.append({"sender": "bot", "text": reply})

        save_history(user, hist)

        return {"reply": reply}


# --------------------------------------------
# START SERVER
# --------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': port,
        'engine.autoreload.on': False
    })
    
    cherrypy.quickstart(
        App(),
        "/",
        {
            "/": {"tools.sessions.on": True}
        }
    )
