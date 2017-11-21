import recalboxFiles
from generators.Generator import Generator
import os.path
import glob
import sys
import shutil

def generateControllerConf(fUaeConfig) :
    
    # ----- Controllers configuration ----- 
    fUaeConfig.save("config_version","2.8.1")
    fUaeConfig.save("joyport0","mouse")
    fUaeConfig.save("joyport0autofire","none")
    fUaeConfig.save("joyport0mode","mouse")
    fUaeConfig.save("joyportname0","MOUSE0")
    fUaeConfig.save("joyport1","joy0")
    fUaeConfig.save("joyport1autofire","normal")
    fUaeConfig.save("joyport1mode","djoy")
    fUaeConfig.save("joyportname1","JOY1")
    fUaeConfig.save("input.autofire_speed","0")
    fUaeConfig.save("input.mouse_speed","100")
    
def generateCD32ControllerConf(fUaeConfig,controller) :
    # ----- CD32 Controllers configuration ----- 
    fUaeConfig.save("config_version","2.8.1")
    fUaeConfig.save("joyport0","mouse")
    fUaeConfig.save("joyport0autofire","none")
    fUaeConfig.save("joyport0mode","mouse")
    fUaeConfig.save("joyportname0","MOUSE0")
    fUaeConfig.save("joyport1","joy0")
    fUaeConfig.save("joyport1autofire","normal")
    fUaeConfig.save("joyport1mode","cd32joy")
    fUaeConfig.save("joyportname1","JOY1")
    fUaeConfig.save("input.autofire_speed","0")
    fUaeConfig.save("input.mouse_speed","100")
    # Custom controls doesn't seem to work at all :)
    fUaeConfig.save("pandora.custom_controls","1")
    fUaeConfig.save("pandora.custom_up","-"+controller.inputs['up'].id)
    fUaeConfig.save("pandora.custom_down","-"+controller.inputs['down'].id)
    fUaeConfig.save("pandora.custom_left","-"+controller.inputs['left'].id)
    fUaeConfig.save("pandora.custom_right","-"+controller.inputs['right'].id)
    fUaeConfig.save("pandora.custom_a","-"+controller.inputs['a'].id)
    fUaeConfig.save("pandora.custom_b","-"+controller.inputs['b'].id)
    fUaeConfig.save("pandora.custom_x","-"+controller.inputs['x'].id)
    fUaeConfig.save("pandora.custom_y","-"+controller.inputs['y'].id)
    fUaeConfig.save("pandora.custom_l","-"+controller.inputs['l2'].id)
    fUaeConfig.save("pandora.custom_r","-"+controller.inputs['r2'].id)
    # fUaeConfig.save("pandora.move_x","-"+controller.inputs['pagedown'].id)
    # fUaeConfig.save("pandora.move_y","-"+controller.inputs['pageup'].id)
    # ---- Special keys
    hotkeyId = controller.inputs['hotkey'].id
    selectId = controller.inputs['select'].id
    fUaeConfig.save("button_for_menu",selectId)
    fUaeConfig.save("button_for_quit",hotkeyId)
    
def generateSpecialKeys(fUaeConfig,controller) :
    hotkeyId = controller.inputs['hotkey'].id
    selectId = controller.inputs['start'].id
    fUaeConfig.save("button_for_menu",selectId)
    fUaeConfig.save("button_for_quit",hotkeyId)
    