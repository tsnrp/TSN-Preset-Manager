import sbs
import MainMenu
import SandboxPresets

scriptrunning = False

mainmenu = MainMenu.MainMenu()
sandboxPresets = SandboxPresets.TSNSandboxPresets()


def StartScript():
    global scriptrunning
    if scriptrunning == False:
        scriptrunning = True
        mainmenu.menuRender()
        sbs.suppress_client_connect_dialog(0)


def cosmos_event_handler(sim, event):
    StartScript()

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
