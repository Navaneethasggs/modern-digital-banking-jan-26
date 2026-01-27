🏦 NeoVault – Modern Digital Banking

NeoVault is a full-stack digital banking platform built as part of an Infosys Internship Project.

Frontend: React + Vite

Backend: FastAPI (Python)

Architecture: Feature-based, team-friendly

📂 Project Structure
```
modern-digital-banking-jan-26/
├── client/   # React frontend
└── server/   # FastAPI backend
```
🛠️ Prerequisites (Install These First)   
Tool	Download    
Node.js (v18+)	https://nodejs.org

Python (v3.10+)	https://www.python.org

Git	https://git-scm.com

Verify:
```bash
node -v
python --version
git --version
```

📥 Clone & Create Feature Branch
```bash
git clone https://github.com/springboardmentor182c-t/modern-digital-banking-jan-26.git
cd modern-digital-banking-jan-26
git checkout -b Group-D-feature/<feature-name>
```

❌ Do not push directly to main.

🌐 Frontend Setup (Client)
```bash
cd client
npm install
npm run dev
```

Frontend runs at:

http://localhost:5173

⚙️ Backend Setup (Server)

Open a new terminal (keep frontend running).
```bash
cd server
python -m venv venv
```
Activate virtual environment

Windows (PowerShell):
```bash
venv\Scripts\Activate.ps1
```

Windows (Git Bash) / macOS / Linux:
```bash
source venv/Scripts/activate
```
or
```bash
source venv/bin/activate
```
Install backend dependencies
```bash
pip install -r requirements.txt
```
Run FastAPI server
```bash
uvicorn src.main:app --reload
```

Backend runs at:

http://127.0.0.1:8000


Swagger API docs:

http://127.0.0.1:8000/docs

🧭 Development Rules

One feature per branch

Follow existing folder structure

Small, meaningful commits

Raise PR → mentor merges

Example commit message:

feat: scaffold frontend features and backend API routes
