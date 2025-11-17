# app.py
import cherrypy
import os
import json
import time
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except Exception:
    genai = None

load_dotenv()
if genai:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)

USERS_FILE = "users.json"
HISTORY_FILE = "history.json"
NEWS_FILE = "news.json"
EVENTS_FILE = "events.json"
LOG_FILE = "logs.json"

def ensure_json_file(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=2)

ensure_json_file(USERS_FILE, {
    "admin": {"password": "admin123", "role": "admin"},
    "zimsec": {"password": "admin123", "role": "user"}
})
ensure_json_file(HISTORY_FILE, {})
ensure_json_file(NEWS_FILE, [
    {"id": 1, "title": "Welcome to ZIMSEC Chat", "body": "This is a demo news item.", "created_at": time.time()}
])
ensure_json_file(EVENTS_FILE, [
    {"id": 1, "title": "2026 Exam Registration Opens", "date": "2026-02-01", "details": "Register online at zimsec website.", "created_at": time.time()}
])
ensure_json_file(LOG_FILE, [])

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def log(action, user=None, details=""):
    logs = load_json(LOG_FILE)
    logs.append({"time": time.time(), "action": action, "user": user, "details": details})
    save_json(LOG_FILE, logs)

def ask_ai(prompt):
    if genai:
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            full_prompt = "You are Chipo, an assistant for ZIMSEC. Answer using ZIMSEC website only.\n\nUser question: " + prompt
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"[AI error] {e}"
    else:
        return f"Chipo (demo): I can only answer using the ZIMSEC website. Received: {prompt}"

# ---------------- Styles & templates ----------------
BASE_CSS = """
:root{
  --bg:#0b0b0d; --card:#0f0f12; --accent:#ff4ed1; --accent2:#7a00ff; --muted:#9a9a9a;
  --gradient1:#ff4ed1; --gradient2:#7a00ff; --gradient3:#4f46e5;
}
*{box-sizing:border-box}
body{margin:0;font-family:Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; background:linear-gradient(180deg,#06060a 0%, #0c0c10 100%); color:#fff; -webkit-font-smoothing:antialiased}
a{color:var(--accent)}
.header-hero{max-width:1100px;margin:32px auto;padding:28px;border-radius:16px;background:linear-gradient(90deg, rgba(255,78,209,0.05), rgba(122,0,255,0.03));display:flex;gap:20px;align-items:center}
.hero-left{flex:1}
.brand{font-weight:800;color:var(--accent);font-size:24px;margin-bottom:6px}
.h1{font-size:28px;margin:6px 0 10px}
.lead{color:var(--muted);margin-bottom:14px}
.cta-row{display:flex;gap:10px}
.cta{padding:12px 16px;border-radius:12px;border:none;cursor:pointer;background:linear-gradient(90deg,var(--accent),var(--accent2));color:#fff;font-weight:600;text-decoration:none;display:inline-block}
.secondary{padding:10px 14px;border-radius:10px;border:1px solid rgba(255,255,255,0.04);background:transparent;color:var(--muted);cursor:pointer;text-decoration:none}
.hero-right{width:320px}
.card{background:var(--card);padding:14px;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.6)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:22px auto;max-width:1100px}
.feature{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));padding:12px;border-radius:12px;position:relative;overflow:hidden}
.feature-icon{width:60px;height:60px;margin-bottom:12px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:28px;background:linear-gradient(135deg, rgba(255,78,209,0.2), rgba(122,0,255,0.2));border:2px solid rgba(255,78,209,0.3)}
.small{font-size:13px;color:var(--muted)}
.container{max-width:1100px;margin:0 auto;padding:18px}
.footer{max-width:1100px;margin:18px auto;text-align:center;color:var(--muted);padding:12px}
.login-hero{display:flex;flex-direction:column;gap:8px}
.form-input{width:100%;padding:10px;border-radius:10px;border:none;background:#0b0b0d;color:#fff;outline:none}
.form-group{margin-bottom:8px}
.chat-container{max-width:1100px;margin:18px auto}
.hero-image{width:100%;height:200px;border-radius:12px;background:linear-gradient(135deg, var(--gradient1) 0%, var(--gradient2) 50%, var(--gradient3) 100%);display:flex;align-items:center;justify-content:center;font-size:80px;margin-bottom:12px;position:relative;overflow:hidden}
.hero-image::before{content:'';position:absolute;width:200%;height:200%;background:radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);animation:pulse 3s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:scale(1);opacity:0.5} 50%{transform:scale(1.1);opacity:0.8}}
.image-banner{max-width:1100px;margin:32px auto;height:180px;border-radius:16px;background:linear-gradient(90deg, #ff4ed1 0%, #7a00ff 50%, #4f46e5 100%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.image-banner::before{content:'';position:absolute;inset:0;background:url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 200"><path d="M0,100 Q300,50 600,100 T1200,100 L1200,200 L0,200 Z" fill="rgba(0,0,0,0.3)"/></svg>') no-repeat center bottom;background-size:cover}
.banner-content{position:relative;z-index:1;text-align:center}
.banner-title{font-size:36px;font-weight:800;margin-bottom:8px;text-shadow:0 2px 10px rgba(0,0,0,0.5)}
.banner-subtitle{font-size:16px;color:rgba(255,255,255,0.9)}
@media (max-width:900px){
  .header-hero{flex-direction:column;padding:18px}
  .grid{grid-template-columns:1fr}
  .hero-right{width:100%}
  .hero-image{height:150px;font-size:60px}
  .image-banner{height:140px}
  .banner-title{font-size:28px}
}
"""

HOME_PAGE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chipo — ZIMSEC Assistant</title>
<style>{css}</style>
</head>
<body>
<div class="container">
  <div class="image-banner">
    <div class="banner-content">
      <div class="banner-title">🎓 Welcome to Chipo AI</div>
      <div class="banner-subtitle">Your intelligent ZIMSEC Assistant — Get instant help with exams, registration & more!</div>
    </div>
  </div>

  <div class="header-hero card">
    <div class="hero-left">
      <div class="brand">Chipo — ZIMSEC Assistant</div>
      <div class="h1">Official ZIMSEC help — fast, polite & limited to official content</div>
      <div class="lead">Ask about timetables, registration, specimen papers, certification, results queries and more — answers come only from the official ZIMSEC site.</div>
      <div class="cta-row">
        <a href="/login" class="cta">User Login</a>
        <a href="/admin_login" class="secondary">Admin Login</a>
      </div>
    </div>

    <div class="hero-right">
      <div class="card login-hero">
        <div class="hero-image">💬</div>
        <div style="font-weight:700">Quick Summary</div>
        <div class="small">Demo accounts:</div>
        <div class="small"><strong>admin</strong> / admin123 (admin)</div>
        <div class="small"><strong>zimsec</strong> / admin123 (user)</div>
        <div style="height:8px"></div>
        <div class="small">Tip: after login, press Enter to send a message. Use the Admin Panel to manage news/events and users.</div>
      </div>
    </div>
  </div>

  <div class="grid">
    <div class="feature card">
      <div class="feature-icon">🎯</div>
      <div style="font-weight:700">Official-only answers</div>
      <div class="small">Chipo returns information drawn from the official ZIMSEC website only. If a question is outside scope you will be directed to WhatsApp.</div>
    </div>
    <div class="feature card">
      <div class="feature-icon">📰</div>
      <div style="font-weight:700">News & Events</div>
      <div class="small">Admins can post news and upcoming events which appear in the chat sidebar for all users.</div>
    </div>
    <div class="feature card">
      <div class="feature-icon">🔧</div>
      <div style="font-weight:700">History & Admin tools</div>
      <div class="small">Per-user chat history is stored locally (JSON). Admins can view histories and manage accounts.</div>
    </div>
  </div>

  <div class="chat-container card">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div style="font-weight:700">🚀 Live demo chat</div>
      <div class="small">Try logging in to start a conversation</div>
    </div>
    <div style="margin-top:12px" class="small">This demo runs locally. For production harden authentication (hash passwords), enable HTTPS and secure storage.</div>
  </div>

  <div class="footer">Built for demo purposes — adapt for production with proper security.</div>
</div>
</body>
</html>
"""

# reuse previous templates for login and chat but ensure actions match method names
LOGIN_PAGE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Login</title>
<style>{css}</style>
</head>
<body>
<div style="max-width:480px;margin:6vh auto">
  <div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div class="brand">Chipo — Login</div>
    </div>
    <form method="post" action="/do_login" style="margin-top:12px">
      <div class="form-group"><input class="form-input" name="username" placeholder="Username"></div>
      <div class="form-group"><input class="form-input" name="password" type="password" placeholder="Password"></div>
      <div style="display:flex;gap:8px">
        <button class="cta" type="submit">Sign in</button>
        <a href="/" class="secondary" style="display:inline-flex;align-items:center;padding:10px;border-radius:10px">Back</a>
      </div>
    </form>
    <div style="margin-top:10px;color:#ffb6da">{error}</div>
  </div>
</div>
</body>
</html>
"""

ADMIN_LOGIN = LOGIN_PAGE.replace('/do_login', '/do_admin_login').replace('Chipo — Login','Chipo — Admin Login')

CHAT_PAGE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chat</title>
<style>{css}</style>
</head>
<body>
<div style="max-width:1100px;margin:18px auto;padding:12px">
  <div style="display:flex;gap:12px;align-items:flex-start">
    <div style="width:260px">
      <div class="card">
        <div style="font-weight:800;color:var(--accent)">Chipo AI</div>
        <div class="small">Logged in as <strong>{username}</strong></div>
        <div style="height:8px"></div>
        <div><a href="/">Home</a></div>
        <div style="height:8px"></div>
        <div><a href="/new_chat" class="small">📝 New Chat</a></div>
        <div><a href="/clear_history" class="small">🗑 Clear History</a></div>
        {admin_links}
        <div style="height:8px"></div>
        <div><a href="/logout" class="small">Logout</a></div>
      </div>
      <div style="height:12px"></div>
      <div class="card">
        <div style="font-weight:700">Latest News</div>
        {news_html}
      </div>
      <div style="height:12px"></div>
      <div class="card">
        <div style="font-weight:700">Upcoming Events</div>
        {events_html}
      </div>
    </div>

    <div style="flex:1">
      <div class="card">
        <div style="font-weight:700">Conversation</div>
        <div id="chat-box" style="height:58vh;overflow:auto;margin-top:10px;padding:10px;background:#08080a;border-radius:8px">
          {history_html}
        </div>

        <div style="display:flex;gap:8px;margin-top:12px">
          <input id="msg" placeholder="Type message..." style="flex:1;padding:12px;border-radius:10px;border:none;background:#0b0b0d;color:#fff" onkeydown="handleKey(event)">
          <button class="cta" onclick="send()">Send</button>
        </div>
        <div class="small" style="margin-top:8px">Press Enter to send</div>
      </div>
    </div>
  </div>
</div>

<script>
function handleKey(e){{
  if(e.key === "Enter" && !e.shiftKey){{
    e.preventDefault();
    send();
  }}
}}
function escapeHtml(s){{ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }}
function appendHtml(h){{ document.getElementById('chat-box').insertAdjacentHTML('beforeend', h); document.getElementById('chat-box').scrollTop = 999999; }}
function send(){{
  var txt = document.getElementById('msg').value.trim();
  if(!txt) return;
  appendHtml('<div class="bubble user" style="background:linear-gradient(90deg,var(--accent),var(--accent2));padding:10px;border-radius:8px;margin:8px 0;max-width:70%;margin-left:auto">'+escapeHtml(txt)+'</div>');
  document.getElementById('msg').value = '';
  appendHtml('<div id="typing" class="bubble bot" style="padding:10px;border-radius:8px;margin:8px 0;max-width:70%">...</div>');
  fetch('/ask', {{method:'POST', headers: {{'Content-Type':'application/json'}}, body: JSON.stringify({{message: txt}})}} )
    .then(r=>r.json()).then(d=>{{
      var t = document.getElementById('typing'); if(t) t.remove();
      appendHtml('<div class="bubble bot" style="background:#0f0f12;padding:10px;border-radius:8px;margin:8px 0;max-width:70%">'+escapeHtml(d.reply)+'</div>');
    }}).catch(e=>{{
      var t = document.getElementById('typing'); if(t) t.remove();
      appendHtml('<div class="bubble bot" style="padding:10px;border-radius:8px;margin:8px 0;max-width:70%">Error: '+escapeHtml(String(e))+'</div>');
    }});
}}
</script>
</body>
</html>
"""

# ---------------- App ----------------
class App:

    @cherrypy.expose
    def index(self):
        user = cherrypy.session.get("user")
        if user:
            return self._render_chat_page(user)
        return HOME_PAGE.format(css=BASE_CSS)

    @cherrypy.expose
    def login(self, error=""):
        return LOGIN_PAGE.format(css=BASE_CSS, error=error)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def do_login(self, username="", password=""):
        users = load_json(USERS_FILE)
        u = users.get(username)
        if u and u.get("password") == password:
            cherrypy.session["user"] = username
            log("login", user=username, details="user login")
            raise cherrypy.HTTPRedirect("/")
        raise cherrypy.HTTPRedirect("/login?error=Invalid+credentials")

    @cherrypy.expose
    def logout(self):
        user = cherrypy.session.pop("user", None)
        log("logout", user=user)
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def admin_login(self, error=""):
        return ADMIN_LOGIN.format(css=BASE_CSS, error=error)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def do_admin_login(self, username="", password=""):
        users = load_json(USERS_FILE)
        u = users.get(username)
        if u and u.get("password") == password and u.get("role") == "admin":
            cherrypy.session["user"] = username
            log("login_admin", user=username)
            raise cherrypy.HTTPRedirect("/admin")
        raise cherrypy.HTTPRedirect("/admin_login?error=Invalid+admin+credentials")

    def _render_chat_page(self, user):
        histories = load_json(HISTORY_FILE)
        hist = histories.get(user, [])
        hist_html = ""
        for h in hist:
            cls = "user" if h.get("sender")=="user" else "bot"
            txt = str(h.get("text","")).replace("<","&lt;").replace(">","&gt;")
            if cls=="user":
                hist_html += f'<div style="text-align:right"><div class="small" style="display:inline-block;background:linear-gradient(90deg,var(--accent),var(--accent2));padding:8px;border-radius:8px;margin:6px 0">{txt}</div></div>'
            else:
                hist_html += f'<div style="text-align:left"><div class="small" style="display:inline-block;background:#0f0f12;padding:8px;border-radius:8px;margin:6px 0">{txt}</div></div>'
        users = load_json(USERS_FILE)
        admin_links = ''
        if users.get(user, {}).get("role") == "admin":
            admin_links = '<div style="margin-top:8px"><a href="/admin">Admin Panel</a></div>'

        news = load_json(NEWS_FILE)
        events = load_json(EVENTS_FILE)
        news_html = ""
        for n in sorted(news, key=lambda x: x.get("created_at",0), reverse=True):
            news_html += f'<div class="small" style="padding:6px;border-bottom:1px solid #08080a"><strong>{n.get("title")}</strong><div style="color:var(--muted)">{n.get("body")}</div></div>'
        events_html = ""
        for e in sorted(events, key=lambda x: x.get("date","")):
            events_html += f'<div class="small" style="padding:6px;border-bottom:1px solid #08080a"><strong>{e.get("title")}</strong><div style="color:var(--muted)">{e.get("date")} — {e.get("details")}</div></div>'

        return CHAT_PAGE.format(css=BASE_CSS, username=user, history_html=hist_html,
                                admin_links=admin_links, news_html=news_html, events_html=events_html)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def ask(self):
        if "user" not in cherrypy.session:
            return {"reply": "Not logged in"}
        data = cherrypy.request.json
        message = data.get("message","").strip()
        if not message:
            return {"reply": ""}

        user = cherrypy.session["user"]
        histories = load_json(HISTORY_FILE)
        if user not in histories:
            histories[user] = []
        histories[user].append({"sender":"user","text":message,"ts":time.time()})
        save_json(HISTORY_FILE, histories)
        log("ask", user=user, details=message)

        reply = ask_ai(message)
        histories[user].append({"sender":"bot","text":reply,"ts":time.time()})
        save_json(HISTORY_FILE, histories)
        return {"reply": reply}

    @cherrypy.expose
    def new_chat(self):
        user = cherrypy.session.get("user")
        if not user:
            raise cherrypy.HTTPRedirect("/login")
        histories = load_json(HISTORY_FILE)
        histories[user] = []
        save_json(HISTORY_FILE, histories)
        log("new_chat", user=user)
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def clear_history(self):
        user = cherrypy.session.get("user")
        if not user:
            raise cherrypy.HTTPRedirect("/login")
        histories = load_json(HISTORY_FILE)
        histories[user] = []
        save_json(HISTORY_FILE, histories)
        log("clear_history", user=user)
        raise cherrypy.HTTPRedirect("/")

    # Admin area
    def _require_admin(self):
        user = cherrypy.session.get("user")
        users = load_json(USERS_FILE)
        if not user or users.get(user, {}).get("role") != "admin":
            raise cherrypy.HTTPRedirect("/admin_login?error=Please+login+as+admin")

    @cherrypy.expose
    def admin(self):
        self._require_admin()
        users = load_json(USERS_FILE)
        news = load_json(NEWS_FILE)
        events = load_json(EVENTS_FILE)
        logs = load_json(LOG_FILE)

        users_rows = ""
        users_options = ""
        for uname, meta in users.items():
            users_rows += f"<tr><td>{uname}</td><td>{meta.get('role')}</td>"
            if uname != "admin":
                users_rows += f"<td><a href='/admin_delete_user?user={uname}' style='color:#ffb6da'>delete</a></td></tr>"
            else:
                users_rows += "<td>—</td></tr>"
            users_options += f"<option value='{uname}'>{uname}</option>"

        news_rows = ""
        for n in news:
            news_rows += f"<div style='padding:8px;border-bottom:1px solid #202020'><strong>{n.get('title')}</strong><div class='small'>{n.get('body')}</div><div style='margin-top:6px'><a href='/admin_delete_news?id={n.get('id')}' class='small'>delete</a></div></div>"

        events_rows = ""
        for e in events:
            events_rows += f"<div style='padding:8px;border-bottom:1px solid #202020'><strong>{e.get('title')}</strong><div class='small'>{e.get('date')} — {e.get('details')}</div><div style='margin-top:6px'><a href='/admin_delete_event?id={e.get('id')}' class='small'>delete</a></div></div>"

        logs_html = ""
        for l in sorted(logs, key=lambda x: x.get("time",0), reverse=True)[:200]:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(l.get("time",0)))
            logs_html += f"<div class='small'><strong>{t}</strong> • {l.get('action')} • {l.get('user')} • {str(l.get('details'))[:120]}</div>"

        page = f"""
        <html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin</title>
        <style>{BASE_CSS}</style></head><body>
        <div style="max-width:1100px;margin:18px auto;padding:12px">
          <div style="display:flex;justify-content:space-between;align-items:center"><div class="brand">Chipo Admin</div><div><a href='/logout' class='small'>Logout</a></div></div>
          <div style="display:grid;grid-template-columns:1fr 360px;gap:12px;margin-top:12px">
            <div class="card">
              <div style="font-weight:700">Users</div>
              <table class="table" style="width:100%;margin-top:8px"><tr><th>Username</th><th>Role</th><th>Action</th></tr>{users_rows}</table>
              <hr/>
              <form method="post" action="/admin_create_user" style="margin-top:8px">
                <input name="username" placeholder="username" class="form-input" style="display:inline-block;width:40%;margin-right:6px">
                <input name="password" placeholder="password" class="form-input" style="display:inline-block;width:40%;margin-right:6px">
                <select name="role" class="form-input" style="display:inline-block;width:15%"><option value='user'>user</option><option value='admin'>admin</option></select>
                <div style="margin-top:8px"><button class="cta" type="submit">Create</button></div>
              </form>
              <div style="margin-top:12px">
                <div style="font-weight:700">Chat Histories</div>
                <form method="get" action="/admin_view_history" style="margin-top:8px">
                  <select name="user" class="form-input">{users_options}</select>
                  <div style="margin-top:8px"><button class="cta" type="submit">View</button> <a href="/admin_clear_all_histories" class="secondary">Clear all</a></div>
                </form>
              </div>
            </div>

            <div>
              <div class="card" style="margin-bottom:12px">
                <div style="font-weight:700">Manage News</div>
                {news_rows}
                <form method="post" action="/admin_add_news" style="margin-top:8px">
                  <input name="title" class="form-input" placeholder="title" style="margin-bottom:6px">
                  <textarea name="body" class="form-input" placeholder="body" style="height:80px"></textarea>
                  <div style="margin-top:8px"><button class="cta" type="submit">Add news</button></div>
                </form>
              </div>

              <div class="card">
                <div style="font-weight:700">Manage Events</div>
                {events_rows}
                <form method="post" action="/admin_add_event" style="margin-top:8px">
                  <input name="title" class="form-input" placeholder="title" style="margin-bottom:6px">
                  <input name="date" class="form-input" placeholder="YYYY-MM-DD" style="margin-bottom:6px">
                  <textarea name="details" class="form-input" placeholder="details" style="height:80px"></textarea>
                  <div style="margin-top:8px"><button class="cta" type="submit">Add event</button></div>
                </form>
              </div>
            </div>
          </div>

          <div style="margin-top:12px" class="card"><div style="font-weight:700">Logs</div><div style="max-height:220px;overflow:auto;margin-top:8px">{logs_html}</div></div>
        </div>
        </body></html>
        """
        return page

    @cherrypy.expose
    def admin_delete_user(self, user=""):
        self._require_admin()
        users = load_json(USERS_FILE)
        if user in users and user != "admin":
            del users[user]
            save_json(USERS_FILE, users)
            log("admin_delete_user", user=cherrypy.session.get("user"), details=user)
        raise cherrypy.HTTPRedirect("/admin")

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def admin_create_user(self, username="", password="", role="user"):
        self._require_admin()
        if not username or not password:
            raise cherrypy.HTTPRedirect("/admin")
        users = load_json(USERS_FILE)
        if username in users:
            raise cherrypy.HTTPRedirect("/admin")
        users[username] = {"password": password, "role": role}
        save_json(USERS_FILE, users)
        log("admin_create_user", user=cherrypy.session.get("user"), details=username)
        raise cherrypy.HTTPRedirect("/admin")

    @cherrypy.expose
    def admin_view_history(self, user=""):
        self._require_admin()
        histories = load_json(HISTORY_FILE)
        h = histories.get(user, [])
        html = "<div style='padding:12px'><a href='/admin' class='small'>← back</a><h3>History: %s</h3><div style='background:#0f0f0f;padding:8px;border-radius:8px;max-height:60vh;overflow:auto'>" % user
        for m in h:
            cls = "user" if m.get("sender")=="user" else "bot"
            txt = str(m.get("text","")).replace("<","&lt;")
            html += f"<div style='margin:8px 0;padding:8px;border-radius:8px;background:#111'><strong>{m.get('sender')}</strong><div class='small'>{txt}</div></div>"
        html += "</div></div>"
        return html

    @cherrypy.expose
    def admin_clear_all_histories(self):
        self._require_admin()
        save_json(HISTORY_FILE, {})
        log("admin_clear_all_histories", user=cherrypy.session.get("user"))
        raise cherrypy.HTTPRedirect("/admin")

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def admin_add_news(self, title="", body=""):
        self._require_admin()
        news = load_json(NEWS_FILE)
        nid = max([n.get("id",0) for n in news] + [0]) + 1
        news.append({"id":nid, "title":title, "body":body, "created_at":time.time()})
        save_json(NEWS_FILE, news)
        log("admin_add_news", user=cherrypy.session.get("user"), details=title)
        raise cherrypy.HTTPRedirect("/admin")

    @cherrypy.expose
    def admin_delete_news(self, id=None):
        self._require_admin()
        news = load_json(NEWS_FILE)
        news = [n for n in news if str(n.get("id")) != str(id)]
        save_json(NEWS_FILE, news)
        log("admin_delete_news", user=cherrypy.session.get("user"), details=id)
        raise cherrypy.HTTPRedirect("/admin")

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def admin_add_event(self, title="", date="", details=""):
        self._require_admin()
        events = load_json(EVENTS_FILE)
        eid = max([e.get("id",0) for e in events] + [0]) + 1
        events.append({"id":eid, "title":title, "date":date, "details":details, "created_at":time.time()})
        save_json(EVENTS_FILE, events)
        log("admin_add_event", user=cherrypy.session.get("user"), details=title)
        raise cherrypy.HTTPRedirect("/admin")

    @cherrypy.expose
    def admin_delete_event(self, id=None):
        self._require_admin()
        events = load_json(EVENTS_FILE)
        events = [e for e in events if str(e.get("id")) != str(id)]
        save_json(EVENTS_FILE, events)
        log("admin_delete_event", user=cherrypy.session.get("user"), details=id)
        raise cherrypy.HTTPRedirect("/admin")

# Start server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': port,
        'tools.sessions.on': True,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(App(), "/", {
        "/": {"tools.sessions.on": True}
    })
