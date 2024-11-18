import sbs


class MainMenu:
    def __init__(self):
        pass

    def menuGUI(self):
        sbs.send_gui_button(0, "", "choice-TSNSandbox", "text:TSN Sandbox^Engineering Preset^Configurations", 10, 10, 50, 30)

    def menuTriggers(self, event):
        pass

    def menuRender(self):
        tag = ""
        sbs.send_gui_clear(0, tag)
        self.menuGUI()
        sbs.send_gui_complete(0, tag)
