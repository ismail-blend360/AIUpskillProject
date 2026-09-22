# Milestone 0: Local Setup & Architecture

**⏰ Time Commitment:** 1 evening (1-2 hours)  
**When:** Day 1  
**Prerequisites:** None  
**Next Milestone:** [Milestone 1: Async News Fetcher](milestone-1-async-fetcher.md)

---

## 🎯 Learning Objectives

By the end of this evening, you will:
- Have a fully configured local development environment
- Understand the project architecture
- Run your first "hello world" test
- Be ready to start coding tomorrow

**This is NOT a coding milestone** - just setup so you can hit the ground running!

---

## 📋 Your Evening Timeline (1-2 hours)

```
7:30 PM - Start
├── 7:30-7:45 PM (15 min) - Clone repo & read README
├── 7:45-8:00 PM (15 min) - Create venv & install dependencies
├── 8:00-8:15 PM (15 min) - Get an LLM API key
├── 8:15-8:25 PM (10 min) - Configure .env file
├── 8:25-8:35 PM (10 min) - Run automated verification
└── 8:35-8:55 PM (20 min) - Read architecture overview
8:55 PM - Done! ✅
```

**No coding tonight** - save your energy for tomorrow!

---

## ✅ Task 1: Clone & Explore (15 minutes)

### **Step 1: Clone the repository**

```bash
# Clone to your preferred location
cd ~/projects  # or wherever you keep code
git clone https://github.com/BLEND360/AIUpskillProject.git
cd AIUpskillProject
```

### **Step 2: Explore the structure**

```bash
# Take a quick look around
ls -la

# You should see:
# - src/          # Your code goes here
# - tests/        # Your tests go here
# - docs/         # Documentation and milestones
# - data/         # Output files (created automatically)
# - requirements.txt
# - README.md
# - .env.example
```

### **Step 3: Read the README**

```bash
# Open in your editor
code .  # VS Code
# or
open -a "Sublime Text" .
# or your preferred editor
```

Read `README.md` for 5 minutes - get the big picture.

**Time check:** ✅ Should be ~7:45 PM (15 min used)

---

## ✅ Task 2: Create Virtual Environment (15 minutes)

### **Why virtual environments?**
Isolates project dependencies from system Python. Essential for clean development.

### **Step 1: Create venv**

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### **Step 2: Upgrade pip**

```bash
pip install --upgrade pip
```

### **Step 3: Install dependencies**

```bash
# Install all project dependencies
pip install -r requirements.txt

# This installs:
# - aiohttp (async HTTP)
# - feedparser (RSS parsing)
# - litellm (LLM provider abstraction — Anthropic / OpenAI / Gemini / etc.)
# - mcp (Model Context Protocol)
# - pytest, pytest-asyncio, pytest-cov (testing)
# - ruff (formatting + linting in one tool)
# - python-dotenv (load .env)

# Should take 2-3 minutes
```

### **Step 4: Verify installation**

```bash
# Check Python version
python --version
# Should show: Python 3.11.x or higher

# Check key packages
python -c "import aiohttp; import feedparser; print('✅ Core packages installed')"
```

**Time check:** ✅ Should be ~8:00 PM (30 min used)

---

## ✅ Task 3: Get an LLM API Key (15 minutes)

The curriculum uses **LiteLLM** as an LLM provider abstraction, so you can
pick whichever provider you want — Anthropic, OpenAI, Gemini, or any of the
[100+ providers LiteLLM supports](https://docs.litellm.ai/docs/providers).
You only need **one** key.

The curriculum's default is `claude-haiku-4-5-20251001` (Anthropic Claude
Haiku 4.5). It's cheap (~$1.50 total for the whole curriculum at typical
usage) and Anthropic gives new accounts a $5 trial credit, so you can do the
entire project without paying anything.

### **Recommended: Anthropic Claude (5 min)**

**Steps:**
1. Go to: https://console.anthropic.com/
2. Sign up (free; new accounts get $5 trial credit)
3. Settings → API Keys → Create Key
4. Copy the key (starts with `sk-ant-...`)

Use the default `LITELLM_MODEL=claude-haiku-4-5-20251001` in your `.env`.

### **Alternatives**

If you'd rather use a different provider, sign up below and update both
`LITELLM_MODEL` and the matching key in your `.env` (see Task 4):

| Provider | Model string | Signup | Notes |
|----------|--------------|--------|-------|
| OpenAI | `gpt-4o-mini` | https://platform.openai.com/ | Requires credit card. Cheap. |
| Google Gemini | `gemini/gemini-2.0-flash` | https://ai.google.dev/ | Free tier (60 RPM, no token cap). |

**Save your key** — you'll paste it into `.env` in the next task.

**Time check:** ✅ Should be ~8:15 PM (45 min used)

---

## ✅ Task 4: Configure Environment (10 minutes)

### **Step 1: Copy environment template**

```bash
# Copy the example file
cp .env.example .env

# Open .env in your editor
code .env  # or your editor
```

### **Step 2: Add your API key**

Edit `.env`. The file ships pre-configured for Claude Haiku — if you picked
that provider in Task 3, just paste your Anthropic key:

```bash
# .env file

# Model the curriculum points at (default is Claude Haiku 4.5).
LITELLM_MODEL=claude-haiku-4-5-20251001

# Paste the Anthropic key you copied in Task 3.
ANTHROPIC_API_KEY=sk-ant-your_key_here
# OPENAI_API_KEY=
# GEMINI_API_KEY=

# Fine as defaults
ENVIRONMENT=development
LOG_LEVEL=INFO
```

If you picked OpenAI or Gemini instead, change `LITELLM_MODEL` to the model
string from Task 3's alternatives table and uncomment/fill the matching key.

### **Step 3: Verify .env is ignored**

```bash
# Check .gitignore
cat .gitignore | grep .env

# Should see:
# .env
# .env.local

# This means your API keys won't be committed to git ✅
```

**IMPORTANT:** Never commit `.env` to git! Your keys are secrets.

**Time check:** ✅ Should be ~8:25 PM (55 min used)

---

## ✅ Task 5: Run Verification (10 minutes)

### **Step 1: Run automated verification script**

```bash
# Run verification
python scripts/verify_setup.py

# This checks:
# ✅ Python version
# ✅ Virtual environment active
# ✅ Dependencies installed
# ✅ API key configured
# ✅ Directory structure
# ✅ Import paths work
# ✅ LiteLLM can reach the configured model (real network call)
```

### **Expected output:**

```
🔍 Verifying AI Upskill Project setup...

✅ Python version: 3.11.5
✅ Virtual environment: Active
✅ Dependencies: All installed
✅ API keys: Configured
✅ Project structure: Valid
✅ Import paths: Working
✅ LiteLLM (claude-haiku-4-5-20251001): Working

🎉 Setup complete! Ready to start Milestone 1.

Next steps:
1. Read docs/architecture/overview.md
2. Start Milestone 1 tomorrow
3. Join Slack: #ai-upskill-cohort-[X]
```

### **If you see errors:**

**Python version wrong:**
```bash
# Install Python 3.11+ from python.org
# Then recreate venv with correct version
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**API key not found:**
```bash
# Check .env file has your provider key set:
#   ANTHROPIC_API_KEY=sk-ant-...  (or OPENAI_API_KEY / GEMINI_API_KEY)
# No quotes needed around the key
# No spaces around =
# LITELLM_MODEL must match the provider whose key you set
```

**Time check:** ✅ Should be ~8:35 PM (65 min used)

---

## ✅ Task 6: Read Architecture (20 minutes)

### **Step 1: Open architecture doc**

```bash
# Open in browser or editor
open docs/architecture/overview.md
# or
code docs/architecture/overview.md
```

### **Step 2: Read and understand**

**Focus on these sections (20 min):**

1. **System Overview (5 min)**
   - What you're building
   - Why this architecture
   - Main components

2. **Data Flow (5 min)**
   - How data moves through system
   - Markdown files as context
   - Why this approach

3. **Technology Stack (5 min)**
   - Python + async/await
   - LiteLLM for LLM access (provider-agnostic)
   - MCP for tools
   - SQLite for data

4. **Week-by-week preview (5 min)**
   - What you build each week
   - How it all connects
   - Final deliverable

**Don't code anything** - just read and understand the big picture.

### **Key Concepts to Grasp:**

**1. Everything runs locally**
- No servers to deploy
- No cloud setup
- All on your laptop

**2. Markdown as context**
- Agents communicate via markdown files
- Human-readable
- Git-friendly
- Easy to debug

**3. Progressive complexity**
- Week 1: Async basics
- Week 2: Clean code
- Week 3: AI agents
- Week 4: MCP + multi-agent
- Week 5: Quality

**Time check:** ✅ Should be ~8:55 PM (85 min used)

---

## 🎉 Milestone 0 Complete!

### **What You Accomplished:**

✅ Development environment ready  
✅ Dependencies installed  
✅ API key configured  
✅ Verification passed  
✅ Architecture understood  

### **Your Laptop Now Has:**

```
AIUpskillProject/
├── venv/                    # Your isolated environment ✅
├── .env                     # Your API key (secret) ✅
├── src/                     # Ready for your code
├── tests/                   # Ready for your tests
└── data/                    # Will be created automatically
```

### **Ready for Tomorrow:**

Tomorrow evening (Milestone 1, Day 1), you'll write your first async code!

---

## 📚 Optional Reading (Weekend/Extra Time)

If you finish early or want to prepare for Week 1:

**Async Python Primer:**
- https://realpython.com/async-io-python/
- 20 minutes, excellent introduction

**Markdown Guide:**
- https://www.markdownguide.org/basic-syntax/
- 10 minutes, quick reference

**Don't code yet!** Just read if you have extra time.

---

## ❓ Troubleshooting

### **"Python 3.11 not found"**

**Solution:**
```bash
# Install from python.org
# Then:
python3.11 -m venv venv
```

### **"pip install fails"**

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Then retry
pip install -r requirements.txt
```

### **"API key not working"**

**Solution:**
```bash
# Check .env format:
ANTHROPIC_API_KEY=sk-ant-abc123  # No quotes, no spaces around =

# Test the key directly with LiteLLM:
python -c "from litellm import completion; print(completion(model='claude-haiku-4-5-20251001', messages=[{'role':'user','content':'hi'}]).choices[0].message.content)"

# Should print a response.
```

### **"Import errors"**

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# You should see (venv) in prompt

# Verify Python
which python  # Should point to venv/bin/python
```

### **Still stuck?**

Ask in Slack: `#ai-upskill-cohort-[X]`

Include:
- Your OS (Mac/Windows/Linux)
- Python version: `python --version`
- Error message (full text)

---

## 📝 Checkpoint Questions

Before moving to Milestone 1, verify you understand:

**Q: Where does your code live?**  
A: `src/` directory

**Q: Where are your API keys?**  
A: `.env` file (never commit this!)

**Q: What database will you use?**  
A: SQLite (local file, no server needed)

**Q: Where will articles be saved?**  
A: `data/articles/` as markdown files

**Q: Do you need to deploy to cloud?**  
A: NO! Everything runs on your laptop

If you can answer these, you're ready! ✅

---

## ➡️ Next Steps

**Tomorrow Evening (Day 2):**

Start [Milestone 1: Async News Fetcher](milestone-1-async-fetcher.md)

You'll build your first async code - a HackerNews fetcher!

**Time required:** 1.5-2 hours

**What you'll learn:**
- async/await basics
- HTTP requests with aiohttp
- File I/O
- Basic testing

See you tomorrow! 🚀

---

## 🎯 Success Criteria

- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] API keys configured in .env
- [ ] Verification script passes
- [ ] Architecture document read
- [ ] Ready to code tomorrow

**All checked?** You're done for tonight! Get some rest. 😴

---

**Questions?** Ask in Slack: `#ai-upskill-cohort-[X]`

**Milestone 0 Complete** ✅  
**Time Spent:** 1-2 hours  
**Next:** Milestone 1 (Tomorrow evening)
