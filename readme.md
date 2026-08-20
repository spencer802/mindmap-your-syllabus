# CSV-to-Mind-Map Generator for Course Schedules

Transform your structured course schedule CSV into interactive, visual mind maps automatically. This script generates both **Freeplane (`.mm`)** files for desktop editing and standalone, interactive **HTML (`Markmap`)** mind maps perfect for embedding into Learning Management Systems (Canvas, Blackboard, etc.) or sharing with students.

---

## Features

- **Automated Hierarchy:** Parses CSV rows into structured branches (Week -> Date -> Topics -> Assignments/Assessments).
- **Dual Output:** 
  - `.mm` for native editing in desktop mind-mapping software.
  - `.html` for a zero-dependency, zoomable, interactive web view.
- **LMS-Ready:** Generated HTML maps can be embedded directly into course pages.

---

## Quick Start

### 1. Requirements & Installation

Ensure you have Python 3 installed. No external pip libraries are required (uses standard library modules like `csv`, `xml.etree.ElementTree`, and `html`).

### 2. Prepare Your CSV File

Format your course schedule CSV with columns corresponding to your course structure. Use the included `GIS4GS.csv` as a template or reference for your own layout.

### 3. Edit and Run the Script

3.1 Place your CSV file in the same directory as `csv2mm.py`.  
3.2 Edit `csv2mm.py` so that the Course title and file names in the "# Configuration" block match your `CSV_FILE` name.  
3.3 Edit the `theme_icon_map` as you see fit. The words before the colon on those lines must match keywords in the Theme column of your CSV. You can find icons and their names by creating a dummy Freeplane mind map, inserting icons you like, saving the `.mm`, and viewing it with a text editor like Wordpad to see what Freeplane calls those icons.  
3.4 Run the script!

    python csv2mm.py

The script generates three output files:
- `GIS4GS.mm` (Freeplane XML)
- `GIS4GS.md` (Markdown format)
- `GIS4GS.html` (Interactive Markmap HTML)

### 4. Embed the Resulting `.html` into Your Canvas Course Site

To display the interactive map directly inside Canvas:
1. Upload `GIS4GS.html` to your course **Files** directory.
2. Copy the file URL and append `/download` to the end of the file ID (e.g., `https://.../files/12345/download`).
3. Embed it into any Canvas Page using an iframe in the **HTML Editor**:

`<iframe src="YOUR_CANVAS_FILE_URL/download" width="100%" height="750px" frameborder="0"></iframe>`

---

## Visualizing & Customizing Output

### Editing Desktop Mind Maps (`.mm`)
To edit node layouts, colors, or icons manually on your computer:
1. Download and install [Freeplane](https://www.freeplane.org/) (Free & Open Source).
2. Open the generated `GIS4GS.mm` file.

### Live Web Preview & Quick Tweaks (`.md`)
To test or edit your Markdown map interactively in a browser without running code:
1. Go to [Markmap REPL](https://markmap.js.org/repl).
2. Press `<ctrl>` + `<a>` to select all the text in the left-hand pane and press `<delete>`.
3. Drag and drop your `GIS4GS.md` file into that left-hand panel. Your mind map will appear in the right-hand panel.

---

## License

MIT License

Copyright (c) 2026 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
