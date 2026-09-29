from flask import Flask, request, redirect, url_for, flash, jsonify, render_template_string
from datetime import datetime
from pathlib import Path
import os, json

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-production")
DATA_FILE = Path(os.environ.get("DATA_FILE", "/tmp/northstar_data.json"))

HTML = r"""
<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Northstar — Workspace</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--ink:#18243b;--muted:#7c8aa5;--line:rgba(145,165,205,.2)}*{box-sizing:border-box}body{margin:0;min-height:100vh;color:var(--ink);font-family:'DM Sans',sans-serif;background:linear-gradient(135deg,#eef4ff,#f6f5ff 48%,#e9f7ff);font-size:14px}.ambient{position:fixed;border-radius:50%;filter:blur(75px);opacity:.45;pointer-events:none;z-index:-1;width:400px;height:400px;background:#bdd2ff;top:-130px;right:8%}.ambient.b{background:#e1d6ff;top:auto;bottom:-150px;left:15%}.glass{background:rgba(255,255,255,.68);border:1px solid #ffffffd9;box-shadow:0 12px 36px #415b9112,inset 0 1px 0 #ffffffcc;backdrop-filter:blur(18px)}.shell{display:flex;max-width:1600px;margin:auto;min-height:100vh;padding:18px;gap:22px}.side{width:225px;flex-shrink:0;border-radius:22px;padding:23px 15px;display:flex;flex-direction:column}.brand{font:800 21px Manrope,sans-serif;letter-spacing:-1px;margin:0 8px 28px}.mark{display:inline-grid;place-items:center;width:31px;height:31px;border-radius:11px;background:linear-gradient(135deg,#527dff,#9d7aff);color:white;margin-right:9px}.workspace{padding:12px;background:#ffffff9c;border:1px solid var(--line);border-radius:13px;margin-bottom:25px;font-size:12px;font-weight:700}.workspace small{display:block;color:var(--muted);font-weight:400;margin:5px 0 0 42px}.navlabel{font-size:9px;letter-spacing:1.5px;color:#a1abc0;font-weight:800;padding:0 12px 10px}.nav{display:block;padding:12px;border-radius:10px;color:#78869f;text-decoration:none;font-size:12px;font-weight:600}.nav.active,.nav:hover{background:linear-gradient(100deg,#e8edff,#f2efff);color:#4e6fe4}.help{margin-top:auto;background:linear-gradient(140deg,#edf1ff,#f8f4ff);border:1px solid #e4e9ff;border-radius:14px;padding:15px;font-size:11px;color:#7c8aa5}.help b{color:var(--ink);font-size:12px}.main{flex:1;min-width:0;padding:4px 6px}.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:29px;color:#8996ad;font-size:11px}.avatar{border-radius:11px;background:linear-gradient(140deg,#b9d1ff,#e2cfff);padding:10px;color:#4755a0;font-size:10px;font-weight:800}.welcome{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:24px}.eyebrow{font-size:9px;letter-spacing:1.5px;font-weight:800;color:#8997b1}.eyebrow:before{content:'● ';color:#68cda7}h1{font:800 clamp(23px,2.5vw,31px) Manrope,sans-serif;letter-spacing:-1px;margin:10px 0 5px}.sub{font-size:12px;color:#8996ad;margin:0}.btn{border:0;border-radius:10px;background:linear-gradient(110deg,#5d7fff,#8d77f6);color:white;font-weight:700;font-size:11px;padding:12px 16px;box-shadow:0 7px 17px #7b8ff63d;cursor:pointer}.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-bottom:18px}.stat{border-radius:17px;padding:17px;min-height:135px}.muted{font-size:11px;color:#8491a8}.num{font:800 28px Manrope,sans-serif;margin:12px 0 5px}.note{font-size:9px;color:#9aa5b7}.green{color:#36b78a}.content{display:grid;grid-template-columns:1.12fr .88fr;gap:17px}.panel{border-radius:18px;padding:21px;min-width:0}.heading{display:flex;justify-content:space-between;gap:10px;margin-bottom:16px}.heading h2{font:700 15px Manrope,sans-serif;margin:0 0 5px}.heading p{font-size:10px;color:#96a1b4;margin:0}.project,.task,.activity{display:flex;align-items:center;gap:10px;padding:13px 0;border-top:1px solid #e9edf5a6}.symbol{width:33px;height:33px;border-radius:10px;background:#e8edff;color:#6683ef;display:grid;place-items:center;flex-shrink:0}.pinfo,.tcopy{flex:1;min-width:0}.pname,.tcopy b{font-size:11px;font-weight:700}.meta,.tcopy small{display:block;font-size:9px;color:#9aa5b7;margin-top:5px}.bararea{width:100px;flex-shrink:0}.barlabel{display:flex;justify-content:space-between;font-size:8px;color:#8e9bb0;margin-bottom:6px}.track{height:5px;border-radius:8px;background:#edf0f8;overflow:hidden}.fill{height:100%;border-radius:8px;background:linear-gradient(90deg,#6c8bff,#a18aff)}.tools{display:flex;gap:8px;margin-bottom:8px}.tools input{min-width:0;flex:1;border:1px solid #edf0f7;background:#f7f8fc;border-radius:8px;padding:9px;font-size:10px;outline:none}.smallbtn{border:0;border-radius:8px;background:#edf0ff;color:#667ce8;padding:8px 10px;cursor:pointer}.check{border:1px solid #cbd4e5;border-radius:6px;background:white;width:17px;height:17px;color:white;padding:0;cursor:pointer}.check.done{background:#7d8df2;border-color:#7d8df2}.priority{font-size:8px;border-radius:5px;padding:5px 7px;background:#fff6e7;color:#c58b3e}.priority.High{background:#fff0f1;color:#e27a83}.priority.Low{background:#e8f8f1;color:#42a98c}.task.done .tcopy b{text-decoration:line-through;color:#9da8b9}.bottom{display:grid;grid-template-columns:1.12fr .88fr;gap:17px;margin-top:17px}.bars{height:125px;display:flex;align-items:end;justify-content:space-around;gap:10px;padding:8px 4px 0}.barcol{height:100%;display:flex;flex-direction:column;justify-content:end;align-items:center;gap:7px;flex:1}.barcol i{display:block;width:65%;max-width:24px;border-radius:6px 6px 3px 3px;background:linear-gradient(180deg,#9e8bf7,#769bff)}.barcol span{font-size:8px;color:#9aa5b7}.activity{font-size:10px;color:#8996ab}.activity b{color:#45536c}.flash{padding:10px 13px;border-radius:9px;background:#e5f8ef;color:#248761;font-size:11px;margin:-8px 0 15px}.modalback{display:none;position:fixed;inset:0;background:#29375445;backdrop-filter:blur(7px);z-index:5;align-items:center;justify-content:center;padding:18px}.modalback.open{display:flex}.modal{width:100%;max-width:410px;padding:26px;border-radius:20px;position:relative}.modal h2{font:800 23px Manrope;margin:8px 0}.modal p{font-size:11px;color:#8d9ab0}.modal label{display:block;font-size:10px;font-weight:700;color:#65738d;margin:14px 0}.modal input,.modal select{display:block;width:100%;padding:12px;margin-top:7px;border:1px solid #e3e9f4;background:#ffffffc9;border-radius:9px;outline:none;font-size:11px}.close{float:right;border:0;background:#f0f3fb;border-radius:8px;padding:5px 10px;font-size:18px;cursor:pointer}.full{width:100%;margin-top:7px}footer{font-size:9px;color:#a0aabd;padding:20px 4px;display:flex;justify-content:space-between}.empty{font-size:11px;color:#98a4b7;padding:12px 0}@media(max-width:1050px){.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.content,.bottom{grid-template-columns:1fr}}@media(max-width:680px){.shell{padding:8px;gap:9px}.side{width:48px;padding:15px 5px;align-items:center}.brand{margin:0 0 24px;font-size:0}.mark{margin:0}.workspace{font-size:0;padding:6px;margin-bottom:18px}.workspace small,.navlabel,.help{display:none}.nav{font-size:0;padding:12px 9px}.nav:before{content:'▦';font-size:17px}.nav.active{font-size:0}.main{padding:2px;}.top{margin-bottom:20px}.welcome{align-items:flex-start}.welcome .btn{padding:10px;font-size:9px;margin-top:15px;white-space:nowrap}.sub{font-size:10px;line-height:1.5}.stats{gap:8px}.stat{padding:13px;min-height:125px}.num{font-size:25px}.panel{padding:14px;border-radius:15px}.bararea{width:65px}.pname{font-size:10px}.meta{font-size:8px}.bottom{gap:12px}footer{gap:8px;font-size:8px}footer span{text-align:right}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;animation:none!important;transition:none!important}}
</style></head><body><div class="ambient"></div><div class="ambient b"></div><div class="shell">
<aside class="side glass"><div class="brand"><span class="mark">N</span><span>northstar.</span></div><div class="workspace">▣ &nbsp; Studio Team<small>Free workspace</small></div><div class="navlabel">WORKSPACE</div><a class="nav active" href="/">▦ &nbsp; Overview</a><a class="nav" href="#projects">▤ &nbsp; Projects</a><a class="nav" href="#tasks">☑ &nbsp; My tasks</a><a class="nav" href="#activity">◷ &nbsp; Activity</a><div class="navlabel" style="margin-top:22px">TOOLS</div><a class="nav" href="#insights">⌁ &nbsp; Insights</a><div class="help"><b>✦ Need a hand?</b><p>Explore tips to make your team flow.</p>Visit help centre ↗</div></aside>
<main class="main"><header class="top"><span>Workspace &nbsp; / &nbsp; <b>Overview</b></span><span>⌕ &nbsp; ♧ &nbsp; <span class="avatar">JD</span></span></header>
<section class="welcome"><div><div class="eyebrow">YOUR WORKSPACE AT A GLANCE</div><h1>Good morning, Junaid ✳</h1><p class="sub">Here’s what’s happening with your team today.</p></div><button class="btn" onclick="show('project-modal')">＋ New project</button></section>
{% for msg in get_flashed_messages() %}<div class="flash">{{msg}}</div>{% endfor %}
<section class="stats"><div class="stat glass"><div class="muted">Total projects</div><div class="num">{{data.projects|length}}</div><div class="note"><span class="green">↗ 12%</span> from last month</div></div><div class="stat glass"><div class="muted">Tasks completed</div><div class="num">{{completed}}<span style="font-size:12px;color:#9ba6b8"> / {{task_count}}</span></div><div class="note"><span class="green">{{((completed/task_count*100)|round|int) if task_count else 0}}%</span> completion rate</div><div class="track"><div class="fill" style="width:{{(completed/task_count*100) if task_count else 0}}%"></div></div></div><div class="stat glass"><div class="muted">Team members</div><div class="num">08</div><div class="note">Across 4 teams · +5 others</div></div><div class="stat glass"><div class="muted">On track</div><div class="num">{{data.projects|selectattr('progress','ge',50)|list|length}}<span style="font-size:12px;color:#9ba6b8"> projects</span></div><div class="note green">● Looking good</div></div></section>
<section class="content"><div class="panel glass" id="projects"><div class="heading"><div><h2>Projects</h2><p>Keep track of your team's progress.</p></div><button class="smallbtn" onclick="show('project-modal')">＋ Add</button></div>{% for p in data.projects %}<div class="project"><div class="symbol">{{['✳','◈','⌘','✦'][loop.index0%4]}}</div><div class="pinfo"><div class="pname">{{p.name}}</div><div class="meta">{{p.team}} · Due {{p.due}}</div></div><div class="bararea"><div class="barlabel"><span>{{p.status}}</span><b>{{p.progress}}%</b></div><div class="track"><div class="fill" style="width:{{p.progress}}%"></div></div></div></div>{% else %}<p class="empty">No projects yet.</p>{% endfor %}</div>
<div class="panel glass" id="tasks"><div class="heading"><div><h2>My tasks <span style="color:#7889e5">({{task_count-completed}} open)</span></h2><p>Your next steps, all in one place.</p></div><button class="smallbtn" onclick="show('task-modal')">＋</button></div><div class="tools"><input id="search" placeholder="Search tasks..." oninput="filterTasks(this.value)"></div><div id="tasklist">{% for t in data.tasks %}<div class="task {%if t.done%}done{%endif%}" data-title="{{t.title|lower}}"><form method="post" action="/tasks/{{loop.index0}}/toggle"><button class="check {%if t.done%}done{%endif%}" aria-label="Toggle task">{%if t.done%}✓{%endif%}</button></form><div class="tcopy"><b>{{t.title}}</b><small>{{t.project}}</small></div><span class="priority {{t.priority}}">{{t.priority}}</span></div>{% else %}<p class="empty">No tasks yet.</p>{% endfor %}</div><button class="smallbtn" style="margin-top:12px" onclick="show('task-modal')">＋ Add a task</button></div></section>
<section class="bottom"><div class="panel glass" id="insights"><div class="heading"><div><h2>Weekly activity</h2><p>A little progress adds up.</p></div><span class="muted">This week⌄</span></div><div class="bars">{% for h in [38,57,44,78,60,88,68] %}<div class="barcol"><i style="height:{{h}}%"></i><span>{{['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][loop.index0]}}</span></div>{% endfor %}</div></div><div class="panel glass" id="activity"><div class="heading"><div><h2>Recent activity</h2><p>Latest updates from your team.</p></div></div><div class="activity">🟣 &nbsp; <span><b>Alex Kim</b> updated <b>Mobile App v2</b><br><small>15 minutes ago</small></span></div><div class="activity">🔵 &nbsp; <span><b>Mia Smith</b> completed <b>Campaign assets</b><br><small>1 hour ago</small></span></div><div class="activity">🟠 &nbsp; <span><b>You</b> created <b>Q4 roadmap</b><br><small>Yesterday</small></span></div></div></section><footer><span>Made for teams that do great work.</span><span>Northstar Workspace · 2026</span></footer></main></div>
<div class="modalback" id="project-modal" onclick="backdrop(event,'project-modal')"><form class="modal glass" method="post" action="/projects"><button type="button" class="close" onclick="hide('project-modal')">×</button><div class="eyebrow">WORKSPACE</div><h2>Create a project</h2><p>Give your team a clear place to make progress.</p><label>Project name<input name="name" required maxlength="100" placeholder="e.g. Product launch"></label><label>Team<input name="team" placeholder="e.g. Product"></label><label>Due date<input name="due" placeholder="e.g. Oct 30"></label><button class="btn full">Create project →</button></form></div>
<div class="modalback" id="task-modal" onclick="backdrop(event,'task-modal')"><form class="modal glass" method="post" action="/tasks"><button type="button" class="close" onclick="hide('task-modal')">×</button><div class="eyebrow">STAY IN FLOW</div><h2>Add a task</h2><p>Small steps move projects forward.</p><label>Task title<input name="title" required maxlength="120" placeholder="What needs to get done?"></label><label>Project<input name="project" placeholder="e.g. Website Redesign"></label><label>Priority<select name="priority"><option>Low</option><option selected>Medium</option><option>High</option></select></label><button class="btn full">Add task →</button></form></div>
<script>function show(id){document.getElementById(id).classList.add('open')}function hide(id){document.getElementById(id).classList.remove('open')}function backdrop(e,id){if(e.target.id===id)hide(id)}function filterTasks(q){q=q.toLowerCase();document.querySelectorAll('#tasklist .task').forEach(t=>t.style.display=t.dataset.title.includes(q)?'flex':'none')}document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.modalback.open').forEach(m=>m.classList.remove('open'))});</script>
</body></html>
"""

def load_data():
    try:
        return json.loads(DATA_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {"projects":[
            {"name":"Website Redesign","team":"Design","progress":78,"status":"In progress","due":"Oct 08"},
            {"name":"Mobile App v2","team":"Engineering","progress":52,"status":"In progress","due":"Oct 14"},
            {"name":"Q4 Campaign","team":"Marketing","progress":91,"status":"Review","due":"Oct 02"},
            {"name":"Customer Portal","team":"Product","progress":34,"status":"Planning","due":"Oct 22"}],
            "tasks":[
            {"title":"Review homepage concepts","project":"Website Redesign","priority":"High","done":False},
            {"title":"Fix mobile navigation","project":"Mobile App v2","priority":"Medium","done":False},
            {"title":"Approve campaign assets","project":"Q4 Campaign","priority":"High","done":True},
            {"title":"Prepare user interviews","project":"Customer Portal","priority":"Low","done":False}]}

def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=2))

@app.get("/")
def dashboard():
    data=load_data()
    completed=sum(1 for task in data["tasks"] if task["done"])
    return render_template_string(HTML, data=data, completed=completed, task_count=len(data["tasks"]))

@app.post("/tasks")
def add_task():
    title=request.form.get("title","").strip()
    if title:
        data=load_data()
        priority=request.form.get("priority","Medium")
        if priority not in ("Low","Medium","High"): priority="Medium"
        data["tasks"].insert(0,{"title":title[:120],"project":request.form.get("project","").strip()[:80] or "General","priority":priority,"done":False})
        save_data(data); flash("Task added successfully.")
    return redirect(url_for("dashboard"))

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    data=load_data()
    if 0 <= task_id < len(data["tasks"]):
        data["tasks"][task_id]["done"]=not data["tasks"][task_id]["done"]
        save_data(data)
    return redirect(url_for("dashboard"))

@app.post("/projects")
def add_project():
    name=request.form.get("name","").strip()
    if name:
        data=load_data()
        data["projects"].insert(0,{"name":name[:100],"team":request.form.get("team","").strip()[:80] or "General","progress":0,"status":"Planning","due":request.form.get("due","").strip()[:30] or "Not set"})
        save_data(data); flash("Project created successfully.")
    return redirect(url_for("dashboard"))

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)),debug=False)
