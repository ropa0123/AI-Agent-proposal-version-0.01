import cherrypy
import os
import google.generativeai as genai
import creds as creds

# --- 1. USER DATA (In-Memory for Demonstration) ---
# The USERS dictionary is now correctly used for authentication.
USERS = {
    # Existing Users
    "zimsec_user": "zimsec123",
    "candidate": "examyear",
    # NEW USERS ADDED
    "admin": "zimsadmin",
    "examiner": "marking101"
}

# ---- Configure the Gemini Model ----
genai.configure(api_key=creds.API_KEY)

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
    "If the user asks how to check results, you MUST FIRST politely ask them to confirm they have the required details (Centre Number, Candidate Number, Session, Level, and Year). If they confirm they have the details, you must state that for security, they must check on the official portal and provide this direct URL:** https://www5.zimsec.co.zw/exam-results-information/. **You MUST NOT attempt to retrieve or process the results yourself.**"
    "If the user asks for past exam papers, you MUST direct them to the Specimen Papers page, which is the official resource for exam examples:** https://www5.zimsec.co.zw/specimen-papers/."
    "Maintain a consistently polite, professional, and friendly tone. "
    "Use clear and simple language, avoiding jargon unless explaining a specific technical term. "
    "When providing information, frame it as expert advice and gently guide the user toward the relevant services or information sheet. "
    "If a user asks about a topic not on the website or outside your scope, you must immediately and politely refuse the request. "
    "For any question outside your knowledge base, you **must** use the following exact message: "
    "'I can only provide information from our website. For anything else, please contact us on WhatsApp by clicking here: https://wa.me/263773021796'"
)

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=system_instructions
)
chat = model.start_chat()

# ---- CherryPy Application ----
class ZIMSECApp:
    @cherrypy.expose
    def index(self):
        if not cherrypy.session.get("logged_in"):
            raise cherrypy.HTTPRedirect("/login")
        return self.chat_ui()

    @cherrypy.expose
    def login(self, error=None):
        # Inject error message if present, replacing the need for an alert()
        error_html = ''
        if error:
            error_html = f"""
            <div style="color:#ff6b6b; margin-bottom: 15px; background: rgba(255,107,107,0.15); padding: 12px; border-radius: 12px; font-size: 14px; border: 1px solid rgba(255,107,107,0.3);">
                {error}
            </div>
            """
        
        return f"""
        <html>
        <head>
            <title>Login - ZIMSEC Assistant</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
                body {{
                    font-family: 'Inter', sans-serif;
                    background: radial-gradient(circle at top left, #1a103d, #0b0b0f);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    color: #fff;
                }}
                .login-box {{
                    background: rgba(255,255,255,0.05);
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
                    width: 350px;
                    text-align: center;
                }}
                input {{
                    width: 90%;
                    padding: 12px;
                    border: none;
                    margin: 8px 0;
                    border-radius: 10px;
                    background: rgba(255,255,255,0.1);
                    color: #fff;
                }}
                input::placeholder {{
                    color: rgba(255, 255, 255, 0.6);
                }}
                button {{
                    width: 100%;
                    background: linear-gradient(90deg,#8b5cf6,#7c3aed);
                    border: none;
                    padding: 12px;
                    border-radius: 10px;
                    font-weight: bold;
                    color: white;
                    cursor: pointer;
                    transition: background 0.3s;
                }}
                button:hover {{
                    background: linear-gradient(90deg,#7c3aed,#8b5cf6);
                }}
                h2 {{ color: #b79fff; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="login-box">
                <h2>Welcome to Chipo — ZIMSEC Assistant</h2>
                {error_html}
                <form method="post" action="do_login">
                    <input type="text" name="username" placeholder="Username" required><br>
                    <input type="password" name="password" placeholder="Password" required><br>
                    <button type="submit">Login</button>
                </form>
            </div>
        </body>
        </html>
        """

    @cherrypy.expose
    def do_login(self, username=None, password=None):
        # FIX: Authentication now checks against the USERS dictionary
        if username in USERS and USERS[username] == password:
            cherrypy.session["logged_in"] = True
            raise cherrypy.HTTPRedirect("/")
        else:
            # FIX: Replaced alert() with a redirect back to login with an error message
            raise cherrypy.HTTPRedirect("/login?error=Invalid username or password. Please try again.")

    @cherrypy.expose
    def logout(self):
        cherrypy.session.pop("logged_in", None)
        raise cherrypy.HTTPRedirect("/login")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def ask(self, msg):
        response = chat.send_message(msg)
        return {"response": response.text}

    def chat_ui(self):
        return """
        <html>
        <head>
        <title>Chipo — ZIMSEC Assistant</title>
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
        :root {
          --bg:#0b0b0f; --panel:#0f1115; --muted:#9aa3b2;
          --accent1:#8b5cf6; --accent2:#7c3aed;
        }
        * { box-sizing: border-box; }
        html, body {
          height:100%; margin:0; background:var(--bg);
          font-family: 'Inter', sans-serif; color:#fff;
        }
        .app { min-height:100vh; display:flex; align-items:center; justify-content:center; padding:32px; }
        .chat-panel {
          width:min(1100px,98%); height:92vh; background:var(--panel);
          border-radius:20px; box-shadow:0 10px 40px rgba(2,6,23,0.6);
          display:grid; grid-template-columns:360px 1fr; overflow:hidden;
        }
        .left {
          background:linear-gradient(180deg,rgba(124,58,237,0.06),rgba(139,92,246,0.03));
          padding:20px; display:flex; flex-direction:column; gap:18px;
          border-right:1px solid rgba(255,255,255,0.03);
        }
        .right { display:flex; flex-direction:column; height:100%; overflow:hidden; }
        .chat-header {
          flex-shrink:0; padding:18px 22px; display:flex;
          align-items:center; justify-content:space-between;
          border-bottom:1px solid rgba(255,255,255,0.02);
        }
        .messages {
          flex:1; padding:24px; overflow-y:auto;
          display:flex; flex-direction:column; gap:12px;
          scroll-behavior:smooth;
        }
        .msg {
          max-width:78%; padding:12px 16px; border-radius:14px;
          line-height:1.4; font-size:15px; word-wrap:break-word; white-space:pre-wrap;
        }
        .msg.ai { background:rgba(255,255,255,0.03); color:#e6eefc; align-self:flex-start; }
        .msg.user { background:linear-gradient(90deg,rgba(139,92,246,0.18),rgba(124,58,237,0.12)); color:white; align-self:flex-end; }
        .input-wrap {
          position:sticky; bottom:0; background:rgba(11,11,15,0.9);
          border-top:1px solid rgba(255,255,255,0.03);
          padding:16px 22px; display:flex; align-items:center; gap:12px; flex-shrink:0;
        }
        .input {
          flex:1; display:flex; gap:10px; align-items:center;
          background:rgba(255,255,255,0.02);
          padding:10px; border-radius:12px; border:1px solid rgba(255,255,255,0.03);
        }
        .input input {
          width:100%; background:transparent; border:none; outline:none; color:#fff; font-size:15px;
        }
        .input input::placeholder {
            color: var(--muted);
        }
        .send-btn {
          background:linear-gradient(90deg,var(--accent1),var(--accent2));
          border:none; color:white; padding:10px 14px;
          border-radius:10px; cursor:pointer; font-weight:600;
          transition: background 0.3s;
        }
        .send-btn:hover {
            opacity: 0.9;
        }
        .logout {
          background:transparent; color:#9aa3b2; border:1px solid rgba(255,255,255,0.1); padding: 8px 12px; border-radius: 8px; cursor:pointer; font-size:14px;
          transition: background 0.2s;
        }
        .logout:hover {
            background: rgba(255,255,255,0.05);
        }
        @media(max-width:880px){ .chat-panel { grid-template-columns:1fr } .left { display:none } }
        </style>
        </head>
        <body>
        <div class="app">
            <div class="chat-panel">
                <div class="left">
                    <h2>Chipo</h2>
                    <p style="color: var(--muted); font-size:14px;">ZIMSEC Assistant</p>
                    <button class="logout" onclick="window.location='/logout'">Logout</button>
                </div>
                <div class="right">
                    <div class="chat-header">
                        <div><b>Chipo — ZIMSEC Assistant</b></div>
                        <div style="color: var(--muted);">Online</div>
                    </div>
                    <div class="messages" id="messages">
                        <div class="msg ai">
                            <b>Hello 👋 I'm Chipo.</b><br>
                            I can help you with ZIMSEC services, exams, syllabi, and candidate affairs — all from the official site.
                        </div>
                    </div>
                    <div class="input-wrap">
                        <div class="input">
                            <input id="user_input" placeholder="Type your ZIMSEC question..." onkeydown="handleKeydown(event)" />
                        </div>
                        <button class="send-btn" onclick="sendMessage()">Send</button>
                    </div>
                </div>
            </div>
        </div>

        <script>
        function scrollToBottom() {
            const c = document.getElementById('messages');
            c.scrollTop = c.scrollHeight;
        }
        function appendMessage(text, who='ai') {
            const c = document.getElementById('messages');
            const el = document.createElement('div');
            el.className = 'msg ' + (who === 'user' ? 'user' : 'ai');
            // Use innerHTML and a simple replace for safety/readability of Gemini output
            el.innerHTML = text.replace(/\\n/g, '<br>'); 
            c.appendChild(el);
            scrollToBottom();
        }
        
        // Function to handle the Enter key press
        function handleKeydown(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Prevent default form submission if any
                sendMessage();
            }
        }
        
        // Attach keydown listener to the input
        document.getElementById('user_input').addEventListener('keydown', handleKeydown);

        async function sendMessage() {
            const input = document.getElementById('user_input');
            const msg = input.value.trim();
            if (!msg) return;

            appendMessage(msg, 'user');
            input.value = '';

            // Simple loading indicator
            const c = document.getElementById('messages');
            const loadingEl = document.createElement('div');
            loadingEl.className = 'msg ai loading-indicator';
            loadingEl.innerHTML = '...';
            c.appendChild(loadingEl);
            scrollToBottom();


            try {
                let response = null;
                // Simple retry loop with exponential backoff (1s, 2s, 4s)
                for (let i = 0; i < 3; i++) {
                    try {
                        const res = await fetch('/ask?msg=' + encodeURIComponent(msg));
                        if (!res.ok) {
                            throw new Error(`HTTP error! status: ${res.status}`);
                        }
                        response = await res.json();
                        break; 
                    } catch (e) {
                        if (i < 2) {
                            await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
                        } else {
                            throw e;
                        }
                    }
                }

                if (response && response.response) {
                    // Remove loading indicator
                    c.removeChild(loadingEl);
                    appendMessage(response.response, 'ai');
                } else {
                    c.removeChild(loadingEl);
                    appendMessage('Sorry, I received an empty or invalid response from the server.', 'ai');
                }

            } catch (error) {
                // Remove loading indicator
                c.removeChild(loadingEl);
                console.error('Fetch error:', error);
                appendMessage('An error occurred while connecting to the assistant. Please try again.', 'ai');
            }
        }
        </script>
        </body>
        </html>
        """

# ---- CherryPy Configuration ----
cherrypy.quickstart(ZIMSECApp(), '/', {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    }
})