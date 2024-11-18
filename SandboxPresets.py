import sbs
import Console_GUI as GUI
import tsn_databases


class TSNSandboxPresets:
    def __init__(self):
        self.PresetText = ""
        self.PresetPosition = 0
        self.PresetSelected = "---"
        self.hotListPos = 0
        self.EditPresetSelected = None
        self.NewPreset = False
        self.presetList = []
        self.myEngineeringPresets = {}
        self.scriptrunning = False
        self.deletedPresets = []

    def menuGUI(self):
        # preset menu shown on System Management panel
        posx = 2
        posy = 11
        self.presetList = list(self.myEngineeringPresets.items())
        sbs.send_gui_button(0, "", "-save-to-file", "text:Save to file", 78, 5, 98, 9)
        GUI.menuBackground(0, "", f"-Preset", 2, 10, 30, 38, text="Power Config", colour="#999966",
                           currentPos=self.PresetPosition, maxLength=len(self.presetList), background=True, scrollbar=True)
        for x in range(self.PresetPosition, min(len(self.presetList), self.PresetPosition + 7)):
            presetdata = self.presetList[x]
            name = presetdata[0]
            data = presetdata[1]
            if name == "position":
                pass
            else:
                if isinstance(data.get("hotkey"), str):
                    hotkey = f"{data.get('hotkey')}"
                else:
                    hotkey = "UNASSIGNED"
                if self.EditPresetSelected == name:
                    colour = "#006600"
                else:
                    colour = "#ff3300"
                GUI.TabletButton(0, "", f"-PresetManclick-{name}", posx + 2, posy, 24, 5, text=name, subtext=hotkey,
                                 buttoncolour=colour)
                if data.get("display"):
                    menuDisplay = "white"
                else:
                    menuDisplay = "gray"
                sbs.send_gui_rawiconbutton(0, "", f"-PresetManmenuDisplay-{name}",
                                           f"icon_index: 31; color: {menuDisplay}", posx + 25, posy, posx + 29,
                                           posy + 4)
                sbs.send_gui_rawiconbutton(0, "", f"-PresetManDelete-{name}", f"icon_index: 97; color: red", posx, posy,
                                           posx + 2, posy + 2)
                posy += 5.2

        if self.EditPresetSelected:
            presetdata = self.myEngineeringPresets.get(self.EditPresetSelected)
            xpos = 1
            sbs.send_gui_typein(0, "", f"-PresetManRename", f"text:{self.PresetText}; font: gui-1", xpos, 55, xpos + 20, 58)
            sbs.send_gui_button(0, "", f"-PresetUpdate", "text: Update; font: smallest", xpos + 25, 55, xpos + 30, 58)
            # power setting sliders
            GUI.menuBackground(0, "", f"-Preset", xpos, 62, 55, 33, text="Power", colour="white")
            for key, value in presetdata.items():
                if isinstance(key, int):
                    name = tsn_databases.EngineeringPowerSliderDatabase.get(key)
                    sbs.send_gui_text(0, "", f"-PresetManTitle-{key}", f"text:{name}; font: smallest; justify: center",
                                      xpos, 62, xpos + 6, 68)
                    sbs.send_gui_text(0, "", f"-PresetManValue-{key}",
                                      f"text: {int(presetdata.get(key)[0] * 100)}%; font: smallest; justify: center",
                                      xpos, 65, xpos + 6, 68)
                    sbs.send_gui_slider(0, "", f"-PresetManSlider-{key}", presetdata.get(key)[0] * 100,
                                        f"high: 300; low: 0", xpos + 2, 68, xpos + 4, 90)
                    sbs.send_gui_text(0, "", f"-PresetManRSTText-{key}",
                                      f"text:Reset; color: white; font: smallest; justify:center", xpos, 90, xpos + 6,
                                      94)
                    sbs.send_gui_clickregion(0, "", f"-PresetManSliderRST-{key}",
                                             f"text:Reset; color: orange; font: smallest", xpos, 90, xpos + 6, 94)
                    xpos += 7
            # coolant sliders
            GUI.menuBackground(0, "", f"-Coolant", xpos - 1, 62, 28, 33, text="Coolant", colour="#29f500")
            for key, value in presetdata.items():
                if isinstance(key, int) and key < 4:
                    name = tsn_databases.EngineeringCoolantDatabase.get(key)
                    sbs.send_gui_text(0, "", f"-PresetCManTitle-{key}", f"text:{name}; font: smallest; justify: center",
                                      xpos, 62, xpos + 6, 68)
                    sbs.send_gui_text(0, "", f"-PresetCManValue-{key}",
                                      f"text: {int(presetdata.get(key)[1])}; font: smallest; justify: center", xpos, 65,
                                      xpos + 6, 68)
                    sbs.send_gui_slider(0, "", f"-PresetCManSlider-{key}", presetdata.get(key)[1], "high: 8; low: 0",
                                        xpos + 2, 68, xpos + 4, 90)
                    sbs.send_gui_text(0, "", f"-PresetManCRSTText-{key}",
                                      f"text:Reset; color: white; font: smallest; justify:center", xpos, 90, xpos + 6,
                                      94)
                    sbs.send_gui_clickregion(0, "", f"-PresetCManSliderRST-{key}",
                                             f"text:Reset; color: orange; font: smallest", xpos, 90, xpos + 6, 94)
                    xpos += 7

            # showing the hotkey menu
            posy = 63
            hotkeyList = tsn_databases.hotkeys
            maxvalue = min(self.hotListPos + 10, len(hotkeyList))
            GUI.menuBackground(0, "", f"-Hotkeys", xpos, 62, 15, 33, text="HotKey", colour="blue",
                               currentPos=self.hotListPos, maxLength=len(hotkeyList), background=True, scrollbar=True)
            for x in range(self.hotListPos, maxvalue):
                hotkeyname = list(hotkeyList)[x]

                assignedkey = presetdata.get("hotkey")
                if assignedkey == hotkeyname:
                    colour = "#006600"
                else:
                    colour = "#ff3300"

                GUI.ToggleButton(0, "", f"-Hotkeysetting-{hotkeyname}", xpos + 1, posy, 13, 3, text=hotkeyname,
                                 font="smallest", togglecolour=colour)
                posy += 3
        else:
            sbs.send_gui_typein(0, "", f"-PresetManRename", f"text:{self.PresetText}; font: gui-1", 1, 55, 41, 58)
            sbs.send_gui_button(0, "", f"-PresetCreate", "text: Create; font: smallest", 46, 55, 56, 58)

    def presetTriggers(self, event):
        if "-PresetManmenuDisplay-" in event.sub_tag:
            # display on the mini menu
            eventinfo = event.sub_tag.split("-")
            preset = eventinfo[2]
            presetData = self.myEngineeringPresets.get(preset)
            state = presetData.get("display")
            presetData.update({"display": not state})
            self.menuRender()

        if "-PresetCreate" in event.sub_tag:
            # create a new preset
            if len(self.PresetText) > 20 or self.PresetText == "":
                self.PresetText = "ERROR"
            else:
                self.AddPreset()
                self.EditPresetSelected = self.PresetText
            self.menuRender()

        if "-PresetManclick-" in event.sub_tag:
            # select a preset on the manager menu
            eventinfo = event.sub_tag.split("-")
            preset = eventinfo[2]
            if preset == self.EditPresetSelected:
                self.EditPresetSelected = None
                self.PresetText = ""
            else:
                self.EditPresetSelected = preset
                self.PresetText = preset
            self.menuRender()

        if "-PresetManSliderRST-" in event.sub_tag:
            # slider reset
            eventinfo = event.sub_tag.split("-")
            presetNo = int(eventinfo[2])
            presetData = self.myEngineeringPresets.get(self.EditPresetSelected)
            dataList = presetData.get(presetNo)
            presetData.update({presetNo: [1, dataList[1]]})
            self.menuRender()

        if "-PresetManDelete-" in event.sub_tag:
            # delete a preset
            eventinfo = event.sub_tag.split("-")
            preset = eventinfo[2]
            self.deletedPresets.append(preset)
            del self.myEngineeringPresets[preset]
            self.menuRender()

        if "-PresetManSlider-" in event.sub_tag:
            # power slider
            eventinfo = event.sub_tag.split("-")
            preset = eventinfo[2]
            data = self.myEngineeringPresets.get(self.EditPresetSelected)
            currentsetting = data.get(int(preset))
            data.update({int(preset): [float(event.sub_float) / 100, currentsetting[1]]})
            self.menuRender()

        if "-PresetCManSlider-" in event.sub_tag:
            # coolant slider
            eventinfo = event.sub_tag.split("-")
            preset = eventinfo[2]
            data = self.myEngineeringPresets.get(self.EditPresetSelected)
            currentsetting = data.get(int(preset))
            totalCoolant = 0
            for x in range(4):
                totalCoolant += data.get(x)[1]
            totalCoolant -= currentsetting[1]
            if totalCoolant + int(event.sub_float) <= 8:
                data.update({int(preset): [currentsetting[0], int(event.sub_float)]})
            self.menuRender()

        if "-PresetCManSliderRST-" in event.sub_tag:
            # coolant reset
            eventinfo = event.sub_tag.split("-")
            presetNo = int(eventinfo[2])
            presetData = self.myEngineeringPresets.get(self.EditPresetSelected)
            dataList = presetData.get(presetNo)
            presetData.update({presetNo: [dataList[0], 0]})
            self.menuRender()

        if "-PresetManRename" in event.sub_tag:
            # input for preset names
            self.PresetText = event.value_tag

        if "-PresetUpdate" in event.sub_tag:
            # update a preset
            data = self.myEngineeringPresets.pop(self.EditPresetSelected)
            if self.PresetText in self.myEngineeringPresets.keys():
                pass
            else:
                if self.PresetText == "":
                    self.PresetText = self.EditPresetSelected
                self.myEngineeringPresets.update({self.PresetText: data.copy()})
                self.EditPresetSelected = None
                self.PresetText = ""
            self.menuRender()

        if "-Hotkeysetting-" in event.sub_tag:
            # update the preset with a hotkey
            eventinfo = event.sub_tag.split("-")
            data = self.myEngineeringPresets.pop(self.EditPresetSelected)
            if data.get("hotkey") == eventinfo[2]:
                data.update({"hotkey": "Unassigned"})
            else:
                data.update({"hotkey": eventinfo[2]})
            self.myEngineeringPresets.update({self.PresetText: data.copy()})
            self.EditPresetSelected = self.PresetText
            # updatePreset(EditPresetSelected, PresetText, data.copy())
            self.menuRender()

        if "-Preset-scroll" in event.sub_tag:
            self.PresetPosition = abs(int(event.sub_float))
            self.menuRender()

        if "-Hotkeys-scroll" in event.sub_tag:
            self.hotListPos = abs(int(event.sub_float))
            self.menuRender()

        if "-save-to-file" in event.sub_tag:
            self.savemyEngineeringPresets()

    def menuRender(self):
        tag = ""
        sbs.send_gui_clear(0, tag)
        self.menuGUI()
        sbs.send_gui_complete(0, tag)

    def buildmyEngineeringPresets(self):
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
                self.myEngineeringPresets.update({text: settingData})
            no += 1

    def AddPreset(self): #checked and ready for presetn manager
        presetdata = {}
        for x in range(8):
            presetdata.update({x: [1.0, 0]})
        presetdata.update({"hotkey": "Unassigned",
                           "display": False})
        self.myEngineeringPresets.update({self.PresetText: presetdata})

    def savemyEngineeringPresets(self):
        with open("./data/client_string_set.txt", "r") as f:
            lines = f.readlines()
            newFile = ""
            presetItems = list(self.myEngineeringPresets.keys())
            presetslistcreated = False
            skipNextList = False
            for line in lines:
                text = line.strip()
                if text in presetItems:
                    data = self.myEngineeringPresets.get(text)
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
                    for preset in list(self.myEngineeringPresets.keys()):
                        presets += f"{preset},"
                    newFile += line + f"{presets}\n"
                    presetslistcreated = True
                    skipNextList = True
                elif text in self.deletedPresets:
                    skipNextList = True
                    pass
                elif skipNextList:
                    skipNextList = False
                else:
                    newFile += line
            if not presetslistcreated:
                presets = ""
                for preset in list(self.myEngineeringPresets.keys()):
                    presets += f"{preset},"
                newFile += "Engineering Presets\n" + f"{presets}\n"
            for newpreset in presetItems:
                data = self.myEngineeringPresets.get(newpreset)
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
            f.close()
