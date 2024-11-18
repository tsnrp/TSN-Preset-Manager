import sbs, math


def TabletButton(clientID, GUITag, reference, posx, posy, w, h, **kwargs):
    # creates a shaped button that can be click and selected once.
    text = ""
    colour1 = "orange"
    colour2 = "#006600"
    font = "gui-1"
    subtext = ""

    if kwargs.get("text"):
        text = kwargs.get("text")
    if kwargs.get("highlightcolour"):
        colour1 = kwargs.get("highlightcolour")
    if kwargs.get("font"):
        font = kwargs.get("font")
    if kwargs.get("subtext"):
        subtext = kwargs.get("subtext")
    if kwargs.get("buttoncolour"):
        colour2 = kwargs.get("buttoncolour")

    sbs.send_gui_text(clientID, GUITag, f"{reference}-text", f"text:{text}; color: #ccffff; font: {font}; justify: center", posx, posy, posx + w, posy + h)
    if kwargs.get("subtext"):
        sbs.send_gui_text(clientID, GUITag, f"{reference}-subtext", f"text:{subtext}; color: #ccffff; font: smallest; justify: center", posx, posy + 3, posx + w, posy + h)
    sbs.send_gui_clickregion(clientID, GUITag, reference, f"text:{text}; color: {colour1}; font: {font}", posx, posy, posx + w, posy + h)
    sbs.send_gui_image(clientID, GUITag, f"{reference}-background", f"image: ../missions/TSN Preset Manager/Images/Box-30; color: {colour2}", posx, posy, posx + w, posy + h)


def ToggleButton(clientID, GUITag, reference, posx, posy, w, h, **kwargs):
    # creates a shaped button that can be click and selected once.
    text = ""
    colour1 = "#ccffff"
    colour2 = "#ff3300"
    colour3 = "orange"
    font = "gui-1"
    justify = "center"

    if kwargs.get("text"):
        text = kwargs.get("text")
    if kwargs.get("textcolour"):
        colour1 = kwargs.get("colour")
    if kwargs.get("togglecolour"):
        colour2 = kwargs.get("togglecolour")
    if kwargs.get("highlightcolour"):
        colour3 = kwargs.get("highlightcolour")
    if kwargs.get("font"):
        font = kwargs.get("font")
    if kwargs.get("justify"):
        justify = kwargs.get("justify")

    sbs.send_gui_text(clientID, GUITag, f"{reference}-text", f"text:{text}; color: {colour1}; font: {font}; justify: {justify}", posx, posy, posx + w, posy + h)
    sbs.send_gui_clickregion(clientID, GUITag, reference, f"text:{text}; color: {colour3}; font: {font}", posx, posy, posx + w, posy + h)
    sbs.send_gui_image(clientID, GUITag, f"{reference}-background", f"image: ../missions/TSN Preset Manager/Images/Box-30; color: {colour2}", posx, posy, posx + w, posy + h)


def menuBackground(clientID, GUITag, reference, posx, posy, w, h, **kwargs):
    # creates a background box with a title
    text = ""
    colour1 = "#ccffff"
    font = "gui-1"
    justify = "left"
    spacing = 3
    background = True

    if kwargs.get("text"):
        text = kwargs.get("text")
    if kwargs.get("colour"):
        colour1 = kwargs.get("colour")
    if kwargs.get("font"):
        font = kwargs.get("font")
        if font == "smallest":
            spacing = 2
    if kwargs.get("justify"):
        justify = kwargs.get("justify")
    if "background" in kwargs:
        background = kwargs.get("background")

    sbs.send_gui_text(clientID, GUITag, f"{reference}-heading", f"text: {text}; color: #ccffff; font: {font}; justify: {justify}", posx, posy - spacing, posx + w, posy + h)
    if background:
        sbs.send_gui_image(clientID, GUITag, f"{reference}-background", f"image: ../missions/TSN Preset Manager/Images/Box-30; color: {colour1}", posx, posy, posx + w, posy + h)
    if kwargs.get("scrollbar") and kwargs.get('maxLength') > 0:
        sbs.send_gui_slider(clientID, GUITag, f"{reference}-scroll", 0-kwargs.get('currentPos'), f"high: 0; low: {0-kwargs.get('maxLength')}", posx-1, posy, posx, posy+h)
