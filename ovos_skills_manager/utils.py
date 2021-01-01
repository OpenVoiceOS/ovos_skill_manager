
def readme_to_json(text):
    text = text.replace("\r", "").replace("\t", "") + "\n## "  # marker to
    # end parsing
    data = {}
    current_section = "title"
    current_text = ""
    current_items = []
    for line in text.split("\n"):
        if line.startswith("# ") and current_section == "title":
            current_text = line.split("# ")[-1].replace("\\", "").replace('"', "'")
            # can be <img src=' or <img src=\' or <img src=\"
            icon_start = "<img src='"
            icon_end = "'"
            if current_text.startswith(icon_start):
                icon = current_text.split(icon_start)[-1].split(icon_end)[0]
                data["icon"] = icon
                current_text = current_text.split("/>")[-1]
            data["skillname"] = current_text.split(">")[-1].strip()
            current_section = "short_description"
            current_text = ""
        elif line.startswith("## ") or line.startswith("# "):
            line = line.replace("##", "#")
            if current_section == "About" or\
                    current_section == "short_description":
                data["description"] = current_text.strip()
                if current_items:
                    data["description"] += "\n" + "\n * ".join(current_items)
                if current_section == "short_description":
                    data["short_description"] = current_text.strip().split("\n")[0]
            elif current_section == "Usage" or current_section == "Examples"\
                    or current_section == "Intents":
                data["examples"] = current_items
            elif current_section == "Credits":
                if not current_items:
                    current_items = [current_text.strip()]
                data["credits"] = current_items
            elif current_section == "Category":
                cats = [c.strip() for c in
                        current_text.replace("*", "").split("\n") if c.strip()]
                data["category"] = cats[0]
                data["categories"] = cats

            elif current_section == "Tags":
                tags = [t.strip() for t in current_text.split("#") if t.strip()]
                data["tags"] = tags
                if data.get("categories"):
                    data["tags"] += data["categories"]
                data["tags"] = list(set(data["tags"]))
            elif current_section == "Supported Devices":
                platforms = [t.strip() for t in current_text.split(" ") if t.strip()]
                data["platforms"] = platforms
            current_section = line.split("# ")[-1].replace(":", "").strip()
            current_text = ""
            current_items = []
        elif line.startswith("* "):
            current_items.append(line[2:].replace("`", "").replace('"', ""))
        elif line.startswith("- "):
            current_items.append(line[2:].replace("`", "").replace('"', ""))
        else:
            current_text += "\n" + line

    return data


def desktop_to_json(desktop):
    lines = desktop.split("\n")
    data = {}
    for l in lines:
        if "=" not in l:
            continue
        k = l.split("=")[0]
        val = l.replace(k + "=", "")
        data[k] = val
    return data

