 ___    ___      _____ 
| _ \  /_\ \    / / _ \
|   / / _ \ \/\/ /|   /
|_|_\/_/ \_\_/\_/ |_|_\

🦖 Read and Write Report (RAWR) Agent 🦖
an Nvidia AIQ Workflow template by Jeremy K

Uses the Nvidia AIQ toolkit to ask an LLM to review an image from the internet url or a local file, and extract the json data out of it using a prompt of your choosing. The extracted data is then used to write a custom report using the Report Creator template system, displaying the data in a single file html readable format.

The function calling and image data extraction uses an LLM from build.nvidia.com, but can also be setup to use other providers like OpenAI.

You can have multiple templates for different types of reports, as defined by one function call parameter. You create visually appealing html reports with Report Creator, that are generated from files in the report_templates folder.

This is a starter workflow, for you to build your own RAWR Agent using Nvidia AIQ, customized for your requirements. This template starts your agent with the basics for reading from images and writing a report, and whatever you logic you'd like to put in between is yours to discover. For more information on Nvidia Agent IQ visit: https://github.com/NVIDIA/AIQToolkit

🦕 Getting Started 🦕

a. Install AIQToolkit - https://docs.nvidia.com/aiqtoolkit/latest/quick-start/installing.html

b. Download this aiq workflow template into a directory in the toolkit (create one called workflows)

c. Pip install the toolkit with AIQ :     uv pip install -e workflows/rawr_agent

d. Start the AIQ RAWR_Agent workflow server in a command window:      aiq serve --config_file configs/config.yml

e. Start the AIQ UI Server in a seperate command window: https://docs.nvidia.com/aiqtoolkit/latest/quick-start/launching-ui.html#launch-the-aiq-toolkit-user-interface

f. Open a browser to http://localhost:3000/ and test chatting with UI. Monitor the command windows for errors for debugging.

g. go rawr in the jungle by testing your own use case

ps. the exported reports are saved in the report_exports folder in the Report Creator self-contained interactive html file format. To view them, open the html file locally in your browser.

🦖 Screen Shots 🦖

Nvidia UI prompt tool calling

Report Export from browser

🏞️⛰️🦕⛰️🌋

The template system included is Report Creator by Daren Ace see documentation here: https://report-creator.readthedocs.io/en/latest/api.html

This was created as a submission for the Nvidia AIQ Hackathon contest https://developer.nvidia.com/agentiq-hackathon

This is a public repo, feel free to submit issues or improvements, would like to make this kickoff template even better.

"Ah, now eventually you do plan to have dinosaurs on your, on your dinosaur tour, right? Hello?" — Ian Malcolm, Jurassic Park 