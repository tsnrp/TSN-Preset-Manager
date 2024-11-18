import sbs
import MainMenu
import SandboxPresets

scriptrunning = False

mainmenu = MainMenu.MainMenu()
sandboxPresets = SandboxPresets.TSNSandboxPresets()


def StartScript(sim):
    global scriptrunning
    if scriptrunning == False:
        scriptrunning = True
        mainmenu.menuRender()
        sbs.suppress_client_connect_dialog(0)


def cosmos_event_handler(sim, event):
    StartScript(sim)

    if sim.is_not_paused():
        if event.client_id == 0:
            sandboxPresets.presetTriggers(event)
    else:
        mainmenu.menuTriggers(event)
        if "choice-TSNSandbox" in event.sub_tag:
            sbs.create_new_sim()
            sbs.resume_sim()
            sandboxPresets.buildmyEngineeringPresets()
            sandboxPresets.menuRender()




"""def savemyEngineeringPresets():
    global myEngineeringPresets, deletedPresets
    with open("./data/client_string_set.txt", "r") as f:
        lines = f.readlines()
        newFile = ""
        presetItems = list(myEngineeringPresets.keys())
        skipNextList = False
        for line in lines:
            text = line.strip()
            if text in presetItems:
                data = myEngineeringPresets.get(text)
                newdata = ""
                for ID, setting in data.items():
                    settingData = ""
                    if isinstance(setting, list):
                        for item in setting:
                            settingData += f",{str(item)}"
                        newdata += f"{ID}{settingData};"
                    else:
                        settingData = f",{setting}"
                        newdata += f"{ID}{settingData};"
                newFile += line + f"{newdata}\n"
                presetItems.remove(text)
                #add the data if the reference is already there
                skipNextList = True
            elif text == "Engineering Presets":
                presets = ""
                for preset in list(myEngineeringPresets.keys()):
                    presets += f"{preset},"

                newFile += line + f"{presets}\n"
                skipNextList = True
            elif text in deletedPresets:
                skipNextList = True
                pass
            elif skipNextList:
                skipNextList = False
            else:
                newFile += line
        for newpreset in presetItems:
            data = myEngineeringPresets.get(newpreset)
            newdata = ""
            for ID, setting in data.items():
                settingData = ""
                if isinstance(setting, list):
                    for item in setting:
                        settingData += f",{str(item)}"
                    newdata += f"{ID}{settingData};"
                else:
                    settingData = f",{setting}"
                    newdata += f"{ID}{settingData};"
            newFile += f"{newpreset}\n" + f"{newdata}\n"
        f.close()
    with open("./data/client_string_set.txt", "w") as f:
        f.write(newFile)
        f.close()"""


"""def buildmyEngineeringPresets():
    global myEngineeringPresets
    with open("./data/client_string_set.txt") as f:
        lines = f.readlines()
        f.close()
    presetList = ""
    no = 0
    for line in lines:
        text = line.strip()
        if text == "Engineering Presets":
            presetList = lines[no + 1].strip()
        no += 1

    presets = presetList.split(",")
    presets.pop(-1)
    no = 0
    for line in lines:
        text = line.strip()
        if text in presets:
            presetData = lines[no + 1].strip()
            dataList = presetData.split(";")
            dataList.pop(-1)
            settingData = {}
            for setting in dataList:
                items = setting.split(",")
                try:
                    settingIndex = int(items[0])
                except:
                    settingIndex = items[0]
                newitems = []
                try:
                    for item in items[1:]:
                        newitems.append(float(item))
                except:
                    for item in items[1:]:
                        if item == "True":
                            newitems.append(True)
                        else:
                            newitems.append(item)
                if settingIndex == "display":
                    displaySet = False
                    if items[1] == "True":
                        displaySet = True
                    settingData.update({settingIndex: displaySet})
                elif settingIndex == "hotkey":
                    settingData.update({settingIndex: items[1]})
                else:
                    settingData.update({settingIndex: newitems})
            myEngineeringPresets.update({text: settingData})
        no += 1"""


"""def AddPreset(): #checked and ready for presetn manager
    global PresetText, PresetPosition, PresetSelected, hotListPos, EditPresetSelected, NewPreset, presetList, myEngineeringPresets, scriptrunning
    presetdata = {}
    for x in range(8):
        presetdata.update({x: [1.0, 0]})
    presetdata.update({"hotkey": "Unassigned",
                       "display": False})
    myEngineeringPresets.update({PresetText: presetdata})


def EngineeringPresetTriggers(event):
    global PresetText, PresetPosition, PresetSelected, hotListPos, EditPresetSelected, NewPreset, presetList, myEngineeringPresets, scriptrunning, deletedPresets
    if "-PresetManmenuDisplay-" in event.sub_tag:
        # display on the mini menu
        eventinfo = event.sub_tag.split("-")
        preset = eventinfo[2]
        presetData = myEngineeringPresets.get(preset)
        state = presetData.get("display")
        presetData.update({"display": not state})
        crender("")

    if "-PresetCreate" in event.sub_tag:
        # create a new preset
        if len(PresetText) > 20 or PresetText == "":
            PresetText = "ERROR"
        else:
            AddPreset()
            EditPresetSelected = PresetText
        crender("")

    if "-PresetManclick-" in event.sub_tag:
        # select a preset on the manager menu
        eventinfo = event.sub_tag.split("-")
        preset = eventinfo[2]
        if preset == EditPresetSelected:
            EditPresetSelected = None
            PresetText = ""
        else:
            EditPresetSelected = preset
            PresetText = preset
        crender("")

    if "-PresetManSliderRST-" in event.sub_tag:
        # slider reset
        eventinfo = event.sub_tag.split("-")
        presetNo = int(eventinfo[2])
        presetData = myEngineeringPresets.get(EditPresetSelected)
        dataList = presetData.get(presetNo)
        presetData.update({presetNo: [1, dataList[1]]})
        crender("")

    if "-PresetManDelete-" in event.sub_tag:
        # delete a preset
        eventinfo = event.sub_tag.split("-")
        preset = eventinfo[2]
        deletedPresets.append(preset)
        del myEngineeringPresets[preset]
        crender("")

    if "-PresetManSlider-" in event.sub_tag:
        # power slider
        eventinfo = event.sub_tag.split("-")
        preset = eventinfo[2]
        data = myEngineeringPresets.get(EditPresetSelected)
        currentsetting = data.get(int(preset))
        data.update({int(preset): [float(event.sub_float) / 100, currentsetting[1]]})
        crender("")

    if "-PresetCManSlider-" in event.sub_tag:
        # coolant slider
        eventinfo = event.sub_tag.split("-")
        preset = eventinfo[2]
        data = myEngineeringPresets.get(EditPresetSelected)
        currentsetting = data.get(int(preset))
        totalCoolant = 0
        for x in range(4):
            totalCoolant += data.get(x)[1]
        totalCoolant -= currentsetting[1]
        if totalCoolant + int(event.sub_float) <= 8:
            data.update({int(preset): [currentsetting[0], int(event.sub_float)]})
        crender("")

    if "-PresetCManSliderRST-" in event.sub_tag:
        # coolant reset
        eventinfo = event.sub_tag.split("-")
        presetNo = int(eventinfo[2])
        presetData = myEngineeringPresets.get(EditPresetSelected)
        dataList = presetData.get(presetNo)
        presetData.update({presetNo: [dataList[0], 0]})
        crender("")

    if "-PresetManRename" in event.sub_tag:
        # input for preset names
        PresetText = event.value_tag

    if "-PresetUpdate" in event.sub_tag:
        # update a preset
        data = myEngineeringPresets.pop(EditPresetSelected)
        if PresetText in myEngineeringPresets.keys():
            pass
        else:
            if PresetText == "":
                PresetText = EditPresetSelected
            myEngineeringPresets.update({PresetText: data.copy()})
            EditPresetSelected = None
            PresetText = ""
        crender("")

    if "-Hotkeysetting-" in event.sub_tag:
        # update the preset with a hotkey
        eventinfo = event.sub_tag.split("-")
        data = myEngineeringPresets.pop(EditPresetSelected)
        if data.get("hotkey") == eventinfo[2]:
            data.update({"hotkey": "Unassigned"})
        else:
            data.update({"hotkey": eventinfo[2]})
        myEngineeringPresets.update({PresetText: data.copy()})
        EditPresetSelected = PresetText
        #updatePreset(EditPresetSelected, PresetText, data.copy())
        crender("")

    if "-Preset-scroll" in event.sub_tag:
        PresetPosition = abs(int(event.sub_float))
        crender("")

    if "-Hotkeys-scroll" in event.sub_tag:
        hotListPos = abs(int(event.sub_float))
        crender("")

    if "-save-to-file" in event.sub_tag:
        savemyEngineeringPresets()


def crender(tag):
    sbs.send_gui_clear(0, tag)
    engineeringpresetGUI()
    sbs.send_gui_complete(0, tag)


def engineeringpresetGUI():
    global PresetText, PresetPosition, PresetSelected, hotListPos, EditPresetSelected, NewPreset, presetList, myEngineeringPresets, scriptrunning
    #preset menu shown on System Management panel
    posx = 2
    posy = 11
    presetList = list(myEngineeringPresets.items())
    sbs.send_gui_button(0, "", "-save-to-file", "text:Save to file", 78, 5, 98, 9)
    GUI.menuBackground(0, "", f"-Preset", 2, 10, 30, 38, text="Power Config", colour="#999966", currentPos=PresetPosition, maxLength=len(presetList), background=True, scrollbar=True)
    for x in range(PresetPosition, min(len(presetList), PresetPosition + 7)):
        presetdata = presetList[x]
        name = presetdata[0]
        data = presetdata[1]
        if name == "position":
            pass
        else:
            if isinstance(data.get("hotkey"), str):
                hotkey = f"{data.get('hotkey')}"
            else:
                hotkey = "UNASSIGNED"
            if EditPresetSelected == name:
                colour = "#006600"
            else:
                colour = "#ff3300"
            GUI.TabletButton(0, "", f"-PresetManclick-{name}", posx + 2, posy, 24, 5, text=name, subtext=hotkey, buttoncolour=colour)
            if data.get("display"):
                menuDisplay = "white"
            else:
                menuDisplay = "gray"
            sbs.send_gui_rawiconbutton(0, "", f"-PresetManmenuDisplay-{name}", f"icon_index: 31; color: {menuDisplay}", posx + 25, posy, posx + 29, posy + 4)
            sbs.send_gui_rawiconbutton(0, "", f"-PresetManDelete-{name}", f"icon_index: 97; color: red", posx, posy, posx + 2, posy + 2)
            posy += 5.2

    if EditPresetSelected:
        presetdata = myEngineeringPresets.get(EditPresetSelected)
        xpos = 1
        sbs.send_gui_typein(0, "", f"-PresetManRename", f"text:{PresetText}; font: gui-1", xpos, 55, xpos + 20, 58)
        sbs.send_gui_button(0, "", f"-PresetUpdate", "text: Update; font: smallest", xpos + 25, 55, xpos + 30, 58)
        # power setting sliders
        GUI.menuBackground(0, "", f"-Preset", xpos, 62, 55, 33, text="Power", colour="white")
        for key, value in presetdata.items():
            if isinstance(key, int):
                name = tsn_databases.EngineeringPowerSliderDatabase.get(key)
                sbs.send_gui_text(0, "", f"-PresetManTitle-{key}", f"text:{name}; font: smallest; justify: center", xpos, 62, xpos + 6, 68)
                sbs.send_gui_text(0, "", f"-PresetManValue-{key}", f"text: {int(presetdata.get(key)[0] * 100)}%; font: smallest; justify: center", xpos, 65, xpos + 6, 68)
                sbs.send_gui_slider(0, "", f"-PresetManSlider-{key}", presetdata.get(key)[0] * 100, f"high: 300; low: 0", xpos + 2, 68, xpos + 4, 90)
                sbs.send_gui_text(0, "", f"-PresetManRSTText-{key}", f"text:Reset; color: white; font: smallest; justify:center", xpos, 90, xpos + 6, 94)
                sbs.send_gui_clickregion(0, "", f"-PresetManSliderRST-{key}", f"text:Reset; color: orange; font: smallest", xpos, 90, xpos + 6, 94)
                xpos += 7
        # coolant sliders
        GUI.menuBackground(0, "", f"-Coolant", xpos-1, 62, 28, 33, text="Coolant", colour="#29f500")
        for key, value in presetdata.items():
            if isinstance(key, int) and key < 4:
                name = tsn_databases.EngineeringCoolantDatabase.get(key)
                sbs.send_gui_text(0, "", f"-PresetCManTitle-{key}", f"text:{name}; font: smallest; justify: center", xpos, 62, xpos + 6, 68)
                sbs.send_gui_text(0, "", f"-PresetCManValue-{key}", f"text: {int(presetdata.get(key)[1])}; font: smallest; justify: center", xpos, 65, xpos + 6, 68)
                sbs.send_gui_slider(0, "", f"-PresetCManSlider-{key}", presetdata.get(key)[1], "high: 8; low: 0", xpos + 2, 68, xpos + 4, 90)
                sbs.send_gui_text(0, "", f"-PresetManCRSTText-{key}", f"text:Reset; color: white; font: smallest; justify:center", xpos, 90, xpos + 6, 94)
                sbs.send_gui_clickregion(0, "", f"-PresetCManSliderRST-{key}", f"text:Reset; color: orange; font: smallest", xpos, 90, xpos + 6, 94)
                xpos += 7

        #showing the hotkey menu
        posy = 63
        hotkeyList = tsn_databases.hotkeys
        maxvalue = min(hotListPos + 10, len(hotkeyList))
        GUI.menuBackground(0, "", f"-Hotkeys", xpos, 62, 15, 33, text="HotKey", colour="blue", currentPos=hotListPos, maxLength=len(hotkeyList), background=True, scrollbar=True)
        for x in range(hotListPos, maxvalue):
            hotkeyname = list(hotkeyList)[x]

            assignedkey = presetdata.get("hotkey")
            if assignedkey == hotkeyname:
                colour = "#006600"
            else:
                colour = "#ff3300"

            GUI.ToggleButton(0, "", f"-Hotkeysetting-{hotkeyname}", xpos + 1, posy, 13, 3, text=hotkeyname, font="smallest", togglecolour=colour)
            posy += 3
    else:
        sbs.send_gui_typein(0, "", f"-PresetManRename", f"text:{PresetText}; font: gui-1", 1, 55, 41, 58)
        sbs.send_gui_button(0, "", f"-PresetCreate", "text: Create; font: smallest", 46, 55, 56, 58)"""
