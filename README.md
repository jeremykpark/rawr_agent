# 🦖 **RAWR Agent – _Read And Write Report_**  
* A starter workflow template for [NVIDIA AIQ Toolkit](https://github.com/NVIDIA/AIQToolkit) by **Jeremy Kesten** (https://linktr.ee/JeremyKplatform ) 

* Produced for and submitted to the Nvidia AgentIQ Hackathon 2025 - https://developer.nvidia.com/agentiq-hackathon


> **TL;DR** Access the Nvidia AgentIQ chat UI locally, to prompt an agent to look at an image (URL or local file) → the first agent tool asks your preferred vision enabled LLM or NimOCR to extract structured JSON → a second agent tool function converts the JSON into **Report Creator** (https://github.com/darenr/report_creator) templates → instantly get a polished, single‑file HTML report.

> Recommended Viewing on Nvidia AgentIQ - https://www.youtube.com/watch?v=H65OluZaiZQ&t=153s
---

## 🌟 What’s inside?

| Feature | Details |
|---------|---------|
| **Image → JSON** | Uses a vision enabled LLM (default: `build.nvidia.com`, easily swappable for OpenAI, etc.) to “look” at an image and answer with JSON. Also includes example scripts for running a PaddleOCR NIM docker container, for more sensitive applications, where an external LLM is not possible. Resizes large images before scanning to save tokens. Extended formats for PaddleOCR NIM - can scan JPEG, PNG, GIF, TIFF, WEBP, BMP |
| **Template‑driven reports** | **Report Creator** renders the JSON into eye‑catching HTML via the templates in `report_templates/`. |
| **One‑call flexibility** | For multiple report types, you can pick any custom pre-setup template just by passing its name in a single function‑call parameter. |
| **Batteries included** | Works as a complete [AIQ](https://github.com/NVIDIA/AIQToolkit) workflow, built to be a scaffolding so you can extend the logic between a basic example of vision llm “read” and report “write.”  For instance, add an MCP extend analysis of the vision data, before writing the report. |

---

## 🦕 Getting Started

1. **Download AIQToolkit**
   ```bash
   mkdir -p ~/<your‑AIQtoolkit‑dir>
   git clone https://github.com/NVIDIA/AIQToolkit
   #  for local dev we install in WSL in ~/aiqtoolkit 
   ```

2. **Clone or fork this AgentIQ Workflow**  
   ```bash
   cd <your‑AIQtoolkit‑dir>
   mkdir -p ~/<your‑AIQtoolkit‑dir>/workflows
   cd workflows
   git clone https://github.com/jeremykpark/rawr_agent.git
   ```

> _Assumes you already have Python 3.9 + and `uv` or `pip` handy._

3. **Install AIQToolkit**  
   ```bash
   Create a new .venv environment and Install AIQTOOLKIT
   #  follow the official AIQToolkit setup guide :
   #  https://docs.nvidia.com/aiqtoolkit/latest/quick-start/installing.html
   
   ```

4. **Register this workflow with AIQ**  
   ```bash
   cd ~/<your‑AIQtoolkit‑dir>/workflows/rawr_agent
   uv pip install -e .


5. **Launch the workflow server from the workflow root dir**  
   ```bash
    cd ~/<your‑AIQtoolkit‑dir>/workflows/rawr_agent
   aiq serve --config_file configs/config.yml
   ```

6. **Launch the AIQ UI in a separate terminal**  
   ```bash
   cd ~/<your‑AIQtoolkit‑dir>/external/aiqtoolkit-opensource-ui
   npm run dev

   # follow the official AIQ UI setup guide first - NPM version v18.17.0 or new required:
   # Ref: https://docs.nvidia.com/aiqtoolkit/latest/quick-start/launching-ui.html
   ```

7. **Open your browser at** <http://localhost:3000>  
   *Start chatting - test with one of the prompts in README_prompt_suggestions.md; watch the server terminals for logs/errors.*

8. **Go RAWR in the jungle**  
   *Use the chat prompt to point the agent at any image and enjoy the auto‑generated reports in `report_exports/` (self‑contained interactive HTML). There are suggested prompts in README_prompt_suggestions.md to get you started.*

---

## 🖼️ Sample Flyer Included

The default setup is to read this included sample file and create a report on the data inside.

| <img src="https://github.com/jeremykpark/rawr_agent/blob/main/img/birthday-party-flyer.jpg" alt="Sample Flyer" width="20%" height="20%"> | <img src="https://github.com/jeremykpark/rawr_agent/blob/main/img/report-sample.jpg" alt="Sample Report" width="30%" height="20%"> |

---

## 🧩 Template System

Create new templates in `report_templates/`. Set them up in rawr_report_template.py to call them by name.
Generated reports are saved to /report_exports as an HTML file.

Click here to see "Kitchen Sink" an example of some of the widgets you can access for your own reports: 
[Kitchen Sink Widget Sample](https://darenr.github.io/report_creator/)

Reports are powered by **[Report Creator](https://report-creator.readthedocs.io/en/latest/api.html)** by Daren Race.  

---
## 📽️ Walkthrough Video

<a href="https://www.youtube.com/watch?v=h07zOIEMiV0" target="_blank">
 <img src="https://github.com/jeremykpark/rawr_agent/blob/main/img/video-screenshot.png" alt="Walkthrough Video" width="240" height="135" border="10" />
</a>

---

## 🏗️ Build Your Own RAWR

This repo is deliberately minimal and is to be used as scaffolding for your own projects. Insert your own logic between **read** (LLM vision) and **write** (HTML report):

```mermaid
graph LR
  A(Image) -->|LLM Vision| B(JSON)
  B -->|Your Code 🤖| C(Enhanced JSON or extra data)
  C -->|Report Creator| D(Beautiful HTML)
```

---

## 🌋 Contributing / Issues

It’s a public repo—PRs & issues are welcome! Let’s make this starter template an **even louder RAWR**.

> “Ah, now eventually you do plan to have dinosaurs on your, on your dinosaur tour, right? Hello?” — **Dr. Ian Malcolm**

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
