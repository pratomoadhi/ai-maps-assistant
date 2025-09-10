# 🌐 Maps Assistant Frontend

This folder contains setup instructions for **Open WebUI (frontend)** and **Ollama**.

---

## 🚀 Run Open WebUI

Run the following script:

```bash
./docker-run.sh
```

Access WebUI at 👉 [http://localhost:3000](http://localhost:3000)

---

## 🔧 Import Tools

Inside WebUI:

1. Go to **Workspace → Tools → Create -> New Tool**.
2. Paste the content of `tools.py` from this folder.
3. Now your LLM can use:

   * `get_places`
   * `get_directions`

---

## 🤖 Setup Ollama

Install Ollama: [https://ollama.com](https://ollama.com)

Pull lightweight models (fit under 8GB RAM):

```bash
ollama pull gemma3:1b
ollama pull gemma3:4b
ollama pull gpt-oss:20b
```

Check installed models:

```bash
ollama list
```

Inside WebUI:
1. Go to **Workspace → Models → Create**.
2. Define the Model name.
3. Select a base model.
4. In the Tools section, check one of the available tools.

You can now select these models inside WebUI.

---

## ✅ Workflow

1. Start your **backend** (FastAPI).
2. Start **Open WebUI** (`./docker-run.sh`).
3. Import tools from `tools.py`.
4. Create custom model in WebUI
5. Select the created model in WebUI chat.
6. Ask:

   ```
   Find me restaurants near Monas Jakarta
   ```

   → WebUI calls your backend and shows results.
