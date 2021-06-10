import cv2
import PySimpleGUI as ObjGui
import time

Default_URL = 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'#For testing only
########Details of camera 1 Start#############
DEF_CamIp_1 = "192.168.178.191"
DEF_CamUser_1 = "admin"
DEF_CamPass_1 = "12345"
CAM_URL_1 = "rtsp://" + DEF_CamUser_1 + ":" + DEF_CamPass_1 + "@" + DEF_CamIp_1 + ":554/live"
########Details of camera 1 End###############

########Details of camera 2 Start#############
DEF_CamIp_2 = "192.168.178.192"
DEF_CamUser_2 = "admin"
DEF_CamPass_2 = "pullach1"
CAM_URL_2 = "rtsp://" + DEF_CamUser_2 + ":" + DEF_CamPass_2 + "@" + DEF_CamIp_2 + ":554/live"
########Details of camera 1 End###############

########Basic settings Start##################
MonitorResolutionX = 940#940    #Screen resolution width (X)
MonitorResolutionY = 1000       #Screen resolution height (Y)
Screentotate = True
OPDimenssion = (MonitorResolutionX,MonitorResolutionY)
ResizeInterpolation = cv2.INTER_NEAREST

if(Screentotate):#used to automatically adjust when screen rotation
    Xpos = MonitorResolutionY
    MonitorResolutionY = MonitorResolutionX
    MonitorResolutionX = Xpos
########DBasic settings End###################
Gui_Theme = "Black"#Background theme
ObjGui.theme(Gui_Theme)
layout = [[ObjGui.Image('', size=(MonitorResolutionX, MonitorResolutionY), key='-VID_OUT-'),
          ObjGui.Image('', size=(MonitorResolutionX, MonitorResolutionY), key='-VID_OUT1-')]]
window = ObjGui.Window('CCTV STREAMER', layout,location = (0,0) , element_justification='center', finalize=True, resizable=True)
window['-VID_OUT-'].expand(True, True)                


camera_1 = cv2.VideoCapture(Default_URL)
time.sleep(1)
camera_2 = cv2.VideoCapture(Default_URL)
time.sleep(1)

while True:                    # The PSG "Event Loop"
    event, values = window.Read(timeout=20, timeout_key='timeout')      # get events for the window with 20ms max wait
    if event == ObjGui.WIN_CLOSED:
        break
        
    ret1 , cap1 = camera_1.read()
    ret2 , cap2 = camera_2.read()
    if(ret1):
        if(Screentotate):
            frame1 = cv2.rotate(cap1, cv2.ROTATE_90_CLOCKWISE)
            window.FindElement('-VID_OUT-').Update(data=cv2.imencode('.png',cv2.resize(frame1, OPDimenssion, interpolation = ResizeInterpolation))[1].tobytes()) # Update image in window
        else:
            window.FindElement('-VID_OUT-').Update(data=cv2.imencode('.png',cv2.resize(cap1, OPDimenssion, interpolation = ResizeInterpolation))[1].tobytes())
    if(ret2):
        if(Screentotate):
            frame2 = cv2.rotate(cap2, cv2.ROTATE_90_CLOCKWISE)
            window.FindElement('-VID_OUT1-').Update(data=cv2.imencode('.png',cv2.resize(frame2, OPDimenssion, interpolation = ResizeInterpolation))[1].tobytes())
        else:
            window.FindElement('-VID_OUT1-').Update(data=cv2.imencode('.png',cv2.resize(cap2, OPDimenssion, interpolation = ResizeInterpolation))[1].tobytes())
window.close()

