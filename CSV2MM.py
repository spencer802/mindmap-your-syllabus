import csv
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Configuration
COURSE_TITLE = "GIS for Global Studies"
CSV_FILE = "GIS4GS.csv"
MM_OUTPUT_FILE = "GIS4GS.mm"
MD_OUTPUT_FILE = "GIS4GS.md"
HTML_OUTPUT_FILE = "GIS4GS.html"  # Rename to GIS4GS.aspx on SharePoint!


def create_course_maps(
    csv_filepath, mm_filepath, md_filepath, html_filepath, course_title
):
    # ==========================================
    # 1. SETUP STRUCTURES
    # ==========================================
    map_elem = ET.Element("map", version="freeplane 1.11.1")
    attribute_hook = ET.SubElement(
        map_elem, "hook", NAME="MapStyleAttributeDelegate"
    )
    ET.SubElement(attribute_hook, "map_styles", automatic_edge_color="true")

    root_node = ET.SubElement(
        map_elem, "node", TEXT=course_title, FOLDED="false"
    )

    theme_icon_map = {
        "prologue": "image",
        "basics": "password",
        "beyond": "emoji-1F9BE",
        "workshop": "launch",
    }
    default_theme_icon = "folder"
    weeks_dict = {}

    md_lines = [f"# {course_title}\n"]
    current_md_week = None
    current_md_date = None

    # ==========================================
    # 2. PARSE CSV
    # ==========================================
    with open(csv_filepath, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            theme_raw = row.get("Theme", "").strip()
            week_raw = row.get("Week", "").strip()
            date_raw = row.get("Date", "").strip()
            topic_raw = row.get("Topic", "").strip()
            materials_raw = row.get("Materials", "").strip()
            assessment_raw = row.get("Assessment", "").strip()
            notes_raw = row.get("Notes", "").strip()

            if not week_raw and not topic_raw:
                continue

            topic_raw = " ".join(topic_raw.split())
            materials_raw = " ".join(materials_raw.split())
            notes_raw = " ".join(notes_raw.split())

            if week_raw and week_raw.isdigit():
                week_raw = f"Week {week_raw}"
            elif not week_raw:
                week_raw = "General Schedule"

            date_label = date_raw if date_raw else "TBD / Flexible"

            # --- A. MARKDOWN LINES ---
            if week_raw != current_md_week:
                md_lines.append(f"## {week_raw}")
                current_md_week = week_raw
                current_md_date = None

            if date_label != current_md_date:
                md_lines.append(f"### {date_label}")
                current_md_date = date_label

            theme_topic_text = (
                f"{theme_raw}: {topic_raw}" if theme_raw else topic_raw
            )
            md_lines.append(f"#### {theme_topic_text}")

            if materials_raw:
                md_lines.append(f"  * 🎨 Materials/Tools: {materials_raw}")

            if assessment_raw:
                md_lines.append("  * 🐝 Assessment")
                assess_items = [
                    item.strip()
                    for item in re.split(
                        r"[\r\n]+|(?=Due:)|(?=Assigned:)", assessment_raw
                    )
                    if item.strip()
                ]
                for item in assess_items:
                    if item.startswith("Due:"):
                        md_lines.append(f"    * 🏁 {item}")
                    elif item.startswith("Assigned:"):
                        md_lines.append(f"    * ⏳ {item}")
                    else:
                        md_lines.append(f"    * {item}")

            if notes_raw:
                md_lines.append(f"  * 📝 Note: {notes_raw}")

            # --- B. FREEPLANE XML ---
            if week_raw not in weeks_dict:
                week_node = ET.SubElement(
                    root_node, "node", TEXT=week_raw, FOLDED="false"
                )
                weeks_dict[week_raw] = {"elem": week_node, "dates": {}}

            week_obj = weeks_dict[week_raw]

            if date_label not in week_obj["dates"]:
                date_node = ET.SubElement(
                    week_obj["elem"], "node", TEXT=date_label, FOLDED="false"
                )
                week_obj["dates"][date_label] = date_node

            date_obj_elem = week_obj["dates"][date_label]

            matched_theme_icon = default_theme_icon
            theme_raw_lower = theme_raw.lower()
            for key, icon_name in theme_icon_map.items():
                if key in theme_raw_lower:
                    matched_theme_icon = icon_name
                    break

            topic_node = ET.SubElement(
                date_obj_elem, "node", TEXT=theme_topic_text, FOLDED="false"
            )
            ET.SubElement(topic_node, "icon", BUILTIN=matched_theme_icon)

            if materials_raw:
                mat_node = ET.SubElement(
                    topic_node,
                    "node",
                    TEXT=f"Materials/Tools: {materials_raw}",
                    FOLDED="false",
                )
                ET.SubElement(mat_node, "icon", BUILTIN="emoji-1F3A8")

            if assessment_raw:
                assess_parent = ET.SubElement(
                    topic_node,
                    "node",
                    TEXT="Assessment",
                    FOLDED="false",
                )
                ET.SubElement(assess_parent, "icon", BUILTIN="bee")

                assess_items = [
                    item.strip()
                    for item in re.split(
                        r"[\r\n]+|(?=Due:)|(?=Assigned:)", assessment_raw
                    )
                    if item.strip()
                ]

                for item in assess_items:
                    assess_leaf = ET.SubElement(
                        assess_parent,
                        "node",
                        TEXT=item,
                        FOLDED="false",
                    )
                    if item.startswith("Due:"):
                        ET.SubElement(
                            assess_leaf, "icon", BUILTIN="emoji-1F3C1"
                        )
                    elif item.startswith("Assigned:"):
                        ET.SubElement(
                            assess_leaf, "icon", BUILTIN="hourglass"
                        )

            if notes_raw:
                note_node = ET.SubElement(
                    topic_node,
                    "node",
                    TEXT=f"Note: {notes_raw}",
                    FOLDED="false",
                )
                ET.SubElement(note_node, "icon", BUILTIN="edit")

    # ==========================================
    # 3. OUTPUT ALL THREE FILES
    # ==========================================
    # 1. Write Freeplane XML (.mm)
    xml_str = minidom.parseString(ET.tostring(map_elem, "utf-8")).toprettyxml(
        indent="  "
    )
    with open(mm_filepath, "w", encoding="utf-8") as f:
        f.write(xml_str)

    # 2. Write Markmap Markdown (.md)
    markdown_content = "\n".join(md_lines)
    with open(md_filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    # 3. Write Standalone Interactive HTML (.html)
    # Escapes backslashes for JS template literal string injection
    escaped_md = markdown_content.replace("\\", "\\\\").replace("`", "\\`")

    html_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{course_title}</title>
  <style>
    body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }}
    #markmap {{ width: 100vw; height: 100vh; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
  <script src="https://cdn.jsdelivr.net/npm/markmap-lib"></script>
</head>
<body>
  <svg id="markmap"></svg>
  <script>
    const markdown = `{escaped_md}`;
    const {{ Transformer }} = window.markmap;
    const transformer = new Transformer();
    const {{ root }} = transformer.transform(markdown);
    const {{ Markmap }} = window.markmap;
    Markmap.create('#markmap', null, root);
  </script>
</body>
</html>"""

    with open(html_filepath, "w", encoding="utf-8") as f:
        f.write(html_template)

    print("Success! Generated:")
    print(f"  - Freeplane XML: {mm_filepath}")
    print(f"  - Markmap Markdown: {md_filepath}")
    print(f"  - Interactive Web HTML: {html_filepath}")


if __name__ == "__main__":
    create_course_maps(
        CSV_FILE,
        MM_OUTPUT_FILE,
        MD_OUTPUT_FILE,
        HTML_OUTPUT_FILE,
        COURSE_TITLE,
    )
