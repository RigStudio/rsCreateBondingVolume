# rsCreateBoundingVolume
# @author Roberto Rubio
# @date 2013-06-14
# @file rsCreateBoundingVolume.py

import win32com.client
from win32com.client import constants

Application = win32com.client.Dispatch('XSI.Application').Application
XSIFactory = win32com.client.Dispatch('XSI.Factory')

null = None
false = 0
true = 1


##
# Load plugin event.
# @param in_reg: register
# @return Boolean
def XSILoadPlugin(in_reg):
    in_reg.Author = "Roberto Rubio"
    in_reg.Name = "rsCreateBoundingVolume"
    in_reg.Email = "info@rigstudio.com"
    in_reg.URL = "www.rigstudio.com"
    in_reg.Help = 'http://rigstudio.com/tools/rscreateboundingvolume/#rsCreateBoundingVolume_options'
    in_reg.Major = 1
    in_reg.Minor = 0

    in_reg.RegisterProperty("rsCreateBoundingVolume")
    in_reg.RegisterMenu(constants.siMenuTbModelCreateCurveID, "rsCreateBoundingVolume_Menu", false, false)
    in_reg.RegisterMenu(constants.siMenuTbAnimateCreateCurveID, "rsCreateBoundingVolume_Menu", false, false)
    in_reg.RegisterCommand("rsCreateBoundingVolumeCmd", "rsCreateBoundingVolumeCmd")

    #RegistrationInsertionPoint - do not remove this line

    return True


##
# Load plugin event.
# @param in_reg: register
# @return Boolean
def XSIUnloadPlugin(in_reg):
    strPluginName = in_reg.Name
    Application.LogMessage(str(strPluginName) + str(" has been unloaded."), constants.siVerbose)
    return True


##
# UI parameters setup.
# @param in_ctxt: context
# @return Boolean
def rsCreateBoundingVolume_Define(in_ctxt):
    oCustomProperty = in_ctxt.Source
    oCustomProperty.AddParameter2("Unique", constants.siBool, true, null, null, null, null, constants.siClassifUnknown, constants.siPersistable)
    oCustomProperty.AddParameter2("SubComponent_Island", constants.siBool, false, null, null, null, null, constants.siClassifUnknown, constants.siReadOnly)
    oCustomProperty.AddParameter2("Color", constants.siString, "Custom", null, null, null, null, constants.siClassifUnknown, constants.siPersistable + constants.siKeyable)
    oCustomProperty.AddParameter2("Position", constants.siBool, true, null, null, null, null, constants.siClassifUnknown, constants.siPersistable)
    oCustomProperty.AddParameter2("Rotation", constants.siBool, true, null, null, null, null, constants.siClassifUnknown, constants.siPersistable)
    oCustomProperty.AddParameter2("Scale", constants.siBool, true, null, null, null, null, constants.siClassifUnknown, constants.siPersistable)
    oCustomProperty.AddParameter3("RedCbv", constants.siDouble, 0, 0, 255, False, False)
    oCustomProperty.AddParameter3("GreenCbv", constants.siDouble, 0, 0, 255, False, False)
    oCustomProperty.AddParameter3("BlueCbv", constants.siDouble, 0, 0, 255, False, False)
    return True


##
# Define the GUI to set the options to rsCreateBoundingVolumeCmd Command.
# @param in_ctxt: context
# @return Boolean
def rsCreateBoundingVolume_DefineLayout(in_ctxt):
    oLayout = in_ctxt.Source
    oLayout.Clear()
    oLayout.AddTab("rsCreateBoundingVolume")
    oLayout.AddGroup("For Selection")
    oLayout.AddItem("Unique")
    oLayout.AddItem("SubComponent_Island")
    oLayout.EndGroup()
    oLayout.AddGroup("")
    l_colour = ("Custom", "Custom", "Black", "Black", "Red", "Red", "Blue", "Blue", "Green", "Green", "Orange", "Orange", "Light_Green", "Light_Green",
                "Purple", "Purple", "Fuchsia", "Fuchsia", "Gold", "Gold", "Teal", "Teal", "Pink", "Pink", "Yellow", "Yellow", "Brown", "Brown")
    oLayout.AddEnumControl("Color", l_colour, "Color", constants.siControlCombo)
    oLayout.AddColor("RedCbv", " ")
    oLayout.EndGroup()
    oLayout.AddGroup("Transforms")
    oLayout.AddItem("Position")
    oLayout.AddItem("Rotation")
    oLayout.AddItem("Scale")
    oLayout.EndGroup()
    oLayout.AddGroup("Execute")
    oLayout.AddRow()
    oLayout.AddButton("Create")
    oLayout.AddSpacer(25)
    oLayout.AddButton("Close")
    oLayout.EndRow()
    oLayout.EndGroup()
    return True


##
# OnInit event.
# @param None.
# @return Boolean
def rsCreateBoundingVolume_OnInit():
    Application.LogMessage("rsCreateBoundingVolume_OnInit called", constants.siVerbose)
    return True


##
# OnClosed event.
# @param None.
# @return Boolean
def rsCreateBoundingVolume_OnClosed():
    Application.LogMessage("rsCreateBoundingVolume_OnClosed called", constants.siVerbose)
    Application.DeleteObj(PPG.Inspected(0))
    PPG.Close()
    return True


##
# Menu Init event.
# @param in_ctxt: context
# @return Boolean
def rsCreateBoundingVolume_Menu_Init(in_ctxt):
    Application.LogMessage("rsCreateBoundingVolume_Menu_Init called", constants.siVerbose)
    oMenu = in_ctxt.Source
    oMenu.AddCallbackItem("rsCreateBoundingVolume", "rsCreateBoundingVolume_Menu_Clicked")
    return True


##
# Unique OnChanged event.
# @param None.
# @return Boolean
def rsCreateBoundingVolume_Unique_OnChanged():
    b_unique = PPG.Unique.Value
    if not b_unique:
        PPG.SubComponent_Island.ReadOnly = False
        PPG.SubComponent_Island.Value = True
    else:
        PPG.SubComponent_Island.ReadOnly = True
        PPG.SubComponent_Island.Value = False
    PPG.Refresh()
    return True


##
# Color OnChanged event.
# @param None.
# @return Boolean
def rsCreateBoundingVolume_Color_OnChanged():
    d_color = {"Red": (0.878, 0, 0), "Blue": (0, 0.125, 0.627), "Green": (0.06, 0.4, 0.224), "Orange": (1, 0.5, 0),
               "Light_Green": (0.125, 0.878, 0.125), "Purple": (0.5, 0, 0.5), "Fuchsia": (1, 0, 1),
               "Gold": (0.878, 0.753, 0.251), "Teal": (0.125, 0.878, 0.753), "Pink": (1, 0.75, 0.79),
               "Yellow": (0.878, 0.878, 0), "Brown": (0.647, 0.164, 0.164), "Black": (0, 0, 0)}
    s_color = PPG.Color.Value
    if s_color in d_color:
        PPG.RedCbv.ReadOnly = True
        PPG.GreenCbv.ReadOnly = True
        PPG.BlueCbv.ReadOnly = True
        PPG.RedCbv.Value = d_color[s_color][0]
        PPG.GreenCbv.Value = d_color[s_color][1]
        PPG.BlueCbv.Value = d_color[s_color][2]
    else:
        PPG.RedCbv.ReadOnly = False
        PPG.GreenCbv.ReadOnly = False
        PPG.BlueCbv.ReadOnly = False
    return True


##
# Menu Clicked event. Open the UI.
# @param in_ctxt: context
# @return Boolean
def rsCreateBoundingVolume_Menu_Clicked(in_ctxt):
    Application.LogMessage("rsCreateBoundingVolume_Menu_Clicked called", constants.siVerbose)
    o_root = Application.ActiveProject.ActiveScene.Root
    o_layBoVo = Application.Dictionary.GetObject('%s.rsCreateBoundingVolume*' % (o_root), False)
    if o_layBoVo != None:
        Application.DeleteObj(o_layBoVo)
    o_customProperty = XSIFactory.CreateObject('rsCreateBoundingVolume')
    Application.InspectObj(o_customProperty, '', 'rsCreateBoundingVolume', constants.siLock, False)
    return True


##
# Create OnClicked event. Set the UI options to rsCreateBoundingVolumeCmd Command.
# @param in_ctxt: context
# @return Boolean
def rsCreateBoundingVolume_Create_OnClicked():
    Application.LogMessage("rsCreateBoundingVolume_Create_OnClicked called", constants.siVerbose)
    b_unique = PPG.Unique.Value
    b_subComIs = PPG.SubComponent_Island.Value
    s_color = PPG.Color.Value
    b_position = PPG.Position.Value
    b_rotation = PPG.Rotation.Value
    b_scale = PPG.Scale.Value
    f_colorR = PPG.RedCbv.Value
    f_colorG = PPG.GreenCbv.Value
    f_colorB = PPG.BlueCbv.Value
    l_objects = Application.GetValue("SelectionList")
    if l_objects.count != 0:
        rsCreateBoundingVolumeCmd_Execute(l_objects, s_color, b_unique, b_subComIs, b_position, b_rotation, b_scale, f_colorR, f_colorG, f_colorB)
        Application.SelectObj(l_objects, "", True)
    else:
        Application.LogMessage("Select one object at least", 4)
    return True


##
# Close OnClicked event.
# @param None.
# @return Boolean
def rsCreateBoundingVolume_Close_OnClicked():
    Application.LogMessage("rsCreateBoundingVolume_Close_OnClicked called", constants.siVerbose)
    Application.DeleteObj(PPG.Inspected(0))
    PPG.Close()
    return True


##
# Command setup.
# @param in_ctxt: context
# @return Boolean
def rsCreateBoundingVolumeCmd_Init(in_ctxt):
    Application.LogMessage("rsCreateBoundingVolumeCmd_Init called", constants.siVerbose)
    o_cmd = in_ctxt.Source
    o_cmd.ReturnValue = False
    o_args = o_cmd.Arguments
    o_args.AddWithHandler("Objects List", "Collection")
    o_args.Add("Color", constants.siArgumentInput, "None", constants.siString)
    o_args.Add("Unique", constants.siArgumentInput, 1, constants.siBool)
    o_args.Add("SubComponent_Island", constants.siArgumentInput, 0, constants.siBool)
    o_args.Add("Position", constants.siArgumentInput, 1, constants.siBool)
    o_args.Add("Rotation", constants.siArgumentInput, 1, constants.siBool)
    o_args.Add("Scale", constants.siArgumentInput, 1, constants.siBool)
    o_args.Add("ColorR", constants.siArgumentInput, 0.0, constants.siFloat)
    o_args.Add("ColorG", constants.siArgumentInput, 0.0, constants.siFloat)
    o_args.Add("ColorB", constants.siArgumentInput, 0.0, constants.siFloat)
    return True


##
# Command Execute. Create BoundingVolumeCurve in objects in list.
# @param l_objects: XSICollection: Object list.
# @param s_color: String: Defines the bounding volume color.
# @param b_unique: Boolean: Indicates if the bounding volume curve is an unique object or not .
# @param b_subComIs: Boolean: Only for type subComponent. Indicates if the bounding volume curve is an unique object or one for each island subcomponents.
# @param b_pos: Boolean: Defines if will catch the position of the original object.
# @param b_rot: Boolean: Defines if will catch the rotation of the original object.
# @param b_scal: Boolean: Defines if will catch the scale of the original object.
# @param f_colorR: Float: Red color for wireframe color.
# @param f_colorG: Float: Green color for wireframe color.
# @param f_colorB: Float: Blue color for wireframe color.
# @return XSICollection or None: If the function finish successfully return a XSICollection with the created curves. In other case the function returns None.
def rsCreateBoundingVolumeCmd_Execute(l_objects, s_color="None", b_unique=1, b_subComIs=0, b_pos=1, b_rot=1, b_scal=1, f_colorR=0.0, f_colorG=0.0, f_colorB=0.0):
    l_ori = l_objects
    for o_part in l_ori:
        if Application.ClassName(o_part) == "Cluster":
            o_memberPart = Application.SelectMembers(o_part, False, "")(0)
            l_objects.remove(o_part)
            l_objects.Add(o_memberPart)
    l_ori = l_objects
    if not b_unique and b_subComIs:
        for o_part in l_ori:
            if o_part.Type == "edgeSubComponent" or o_part.Type == "polySubComponent" or (o_part.Type == "pntSubComponent" and o_part.SubComponent.Parent3DObject.Type == "polymsh"):
                l_subComIs = rsSubCompIsland(o_part)
                if len(l_subComIs) > 1:
                    l_objects.remove(o_part)
                    for o_subComIs in l_subComIs:
                        l_objects.Add(o_subComIs)
    l_boundings = XSIFactory.CreateObject('XSI.Collection')
    if l_objects.Count > 0:
        l_select = Application.GetValue("SelectionList")
        if b_unique:
            o_bounding = rsExecuteCurveBoundingVolume(l_objects, s_color, b_pos, b_rot, b_scal, f_colorR, f_colorG, f_colorB)
            l_boundings.Add(o_bounding)
        else:
            for o_object in l_objects:
                o_bounding = rsExecuteCurveBoundingVolume(o_object, s_color, b_pos, b_rot, b_scal, f_colorR, f_colorG, f_colorB)
                l_boundings.Add(o_bounding)
        Application.SelectObj(l_select, "", True)
        return l_boundings
    else:
        Application.LogMessage("Curve Bounding Volue: Need one object at least", 4)
        return None


##
# rsExecuteCurveBoundingVolume. Create one BoundingVolumeCurve for objects in list.
# @param l_objects: XSICollection: Object list.
# @param s_color: String: Defines the bounding volume color.
# @param b_unique: Boolean: Indicates if the bounding volume curve is an unique object or not .
# @param b_pos: Boolean: Defines if will catch the position of the original object.
# @param b_rot: Boolean: Defines if will catch the rotation of the original object.
# @param b_scal: Boolean: Defines if will catch the scale of the original object.
# @param f_colorR: Float: Red color for wireframe color.
# @param f_colorG: Float: Green color for wireframe color.
# @param f_colorB: Float: Blue color for wireframe color.
# @return 3D object: If the function finish successfully return the created curve.
def rsExecuteCurveBoundingVolume(l_objects, s_color, b_pos, b_rot, b_scal, f_colorR, f_colorG, f_colorB):
    d_color = {"Red": (0.878, 0, 0), "Blue": (0, 0.125, 0.627), "Green": (0.06, 0.4, 0.224), "Orange": (1, 0.5, 0),
               "Light_Green": (0.125, 0.878, 0.125), "Purple": (0.5, 0, 0.5), "Fuchsia": (1, 0, 1),
               "Gold": (0.878, 0.753, 0.251), "Teal": (0.125, 0.878, 0.753), "Pink": (1, 0.75, 0.79),
               "Yellow": (0.878, 0.878, 0), "Brown": (0.647, 0.164, 0.164), "Black": (0, 0, 0), "Custom": (f_colorR, f_colorG, f_colorB)}
    b_logValue = Application.GetValue("preferences.scripting.cmdlog")
    if b_logValue:
        Application.SetValue("preferences.scripting.cmdlog", False, "")
    b_logMValue = Application.GetValue("preferences.scripting.msglog")
    if b_logMValue:
        Application.SetValue("preferences.scripting.msglog", False, "")
    try:
        o_numObj = len(l_objects)
    except:
        o_numObj = 1
    l_boundingBox = Application.GetBBox(l_objects)
    f_xmin = l_boundingBox(0)
    f_ymin = l_boundingBox(1)
    f_zmin = l_boundingBox(2)
    f_xmax = l_boundingBox(3)
    f_ymax = l_boundingBox(4)
    f_zmax = l_boundingBox(5)
    s_curve = Application.SICreateCurve("crvlist", 1, 1)
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmin, f_ymin, f_zmax, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmin, f_ymax, f_zmax, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmax, f_ymax, f_zmax, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmax, f_ymin, f_zmax, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmin, f_ymin, f_zmax, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmin, f_ymin, f_zmin, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmin, f_ymax, f_zmin, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmin, f_ymax, f_zmax, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmax, f_ymax, f_zmax, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmax, f_ymax, f_zmin, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmin, f_ymax, f_zmin, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmin, f_ymin, f_zmin, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmax, f_ymin, f_zmin, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmax, f_ymax, f_zmin, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmax, f_ymin, f_zmin, False, 0, "")
    Application.SIAddPointOnCurveAtEnd(s_curve, f_xmax, f_ymin, f_zmax, False, 0, "")
    Application.ApplyTopoOp("CrvOpenClose", s_curve, 3, "siPersistentOperation", "")
    l_traslation = s_curve.Kinematics.Global.Transform
    if b_scal:
        l_traslation.SclX = 0
        l_traslation.SclY = 0
        l_traslation.SclZ = 0
    l_ccen = []
    for z in range(o_numObj):
        try:
            o_object = l_objects[z]
        except:
            o_object = l_objects
        if "SubComponent" in str(o_object.Type) or Application.ClassName(o_object) == "Cluster":
            l_boundingB = Application.GetBBox(l_objects)
            f_transX = (l_boundingB(0) + l_boundingB(3)) / 2
            f_transY = (l_boundingB(1) + l_boundingB(4)) / 2
            f_transZ = (l_boundingB(2) + l_boundingB(5)) / 2
            o_null = Application.GetPrim("Null", "", "", "")
            Application.Translate(o_null, f_transX, f_transY, f_transZ, "siAbsolute", "siGlobal", "siObj", "siXYZ", "", "", "", "", "", "", "", "", "", 0, "")
            l_ccen.append(o_null)
            if b_rot:
                Application.MatchTransform(o_null, o_object.SubComponent.Parent3DObject, "siRot", "")
            if b_scal:
                Application.MatchTransform(o_null, o_object.SubComponent.Parent3DObject, "siScl", "")
            o_object = o_null
        if b_pos:
            l_traslation.PosX = l_traslation.PosX + (o_object.Kinematics.Global.Transform.PosX / o_numObj)
            l_traslation.PosY = l_traslation.PosY + (o_object.Kinematics.Global.Transform.PosY / o_numObj)
            l_traslation.PosZ = l_traslation.PosZ + (o_object.Kinematics.Global.Transform.PosZ / o_numObj)
        if b_rot:
            l_traslation.RotX = l_traslation.RotX + (o_object.Kinematics.Global.Transform.RotX / o_numObj)
            l_traslation.RotY = l_traslation.RotY + (o_object.Kinematics.Global.Transform.RotY / o_numObj)
            l_traslation.RotZ = l_traslation.RotZ + (o_object.Kinematics.Global.Transform.RotZ / o_numObj)
        if b_scal:
            l_traslation.SclX = l_traslation.SclX + (o_object.Kinematics.Global.Transform.SclX / o_numObj)
            l_traslation.SclY = l_traslation.SclY + (o_object.Kinematics.Global.Transform.SclY / o_numObj)
            l_traslation.SclZ = l_traslation.SclZ + (o_object.Kinematics.Global.Transform.SclZ / o_numObj)
    if l_ccen != []:
        Application.DeleteObj(l_ccen)
    if b_pos or b_rot or b_scal:
        o_null = Application.GetPrim("Null", "", "", "")
        o_null.Kinematics.Global.Transform = l_traslation
        Application.CopyPaste(s_curve, "", "B:%s" % (o_null), 1)
        Application.ResetTransform(s_curve, "siCtr", "siSRT", "siXYZ")
    Application.FreezeObj(s_curve, "", "")
    Application.CutObj(s_curve)
    o_sceneColor = Application.ActiveProject.ActiveScene.Colors.geocol
    l_rgbaColor = rsLongToRgba(o_sceneColor.Value)
    if s_color in d_color:
        if l_rgbaColor[0] == d_color[s_color][0] and l_rgbaColor[1] == d_color[s_color][1] and l_rgbaColor[2] == d_color[s_color][2]:
            Application.LogMessage("Color not modified: Color is default geometry color.", constants.siVerbose)
        else:
            Application.MakeLocal("%s.display" % (s_curve), "siNodePropagation")
            Application.SetValue("%s.display.wirecolorr" % (s_curve), d_color[s_color][0], "")
            Application.SetValue("%s.display.wirecolorg" % (s_curve), d_color[s_color][1], "")
            Application.SetValue("%s.display.wirecolorb" % (s_curve), d_color[s_color][2], "")
    if b_pos or b_rot or b_scal:
        Application.DeleteObj(o_null)
    if b_logMValue:
        Application.SetValue("preferences.scripting.msglog", True, "")
    if b_logValue:
        Application.SetValue("preferences.scripting.cmdlog", True, "")
    return s_curve


##
# rsSubCompIsland. If the input object is an subComponent, return his island subcomponents.
# @param o_sel: XSICollection: Object list.
# @return XSICollection or None: If the input object is of type subComponent return a XSICollection with the island subcomponents. In other case the function returns None.
def rsSubCompIsland(o_sel):
    d_subType = {"polySubComponent": "poly", "edgeSubComponent": "edge", "pntSubComponent": "pnt"}
    l_subIsland = []
    if o_sel.Type == "edgeSubComponent" or o_sel.Type == "polySubComponent" or (o_sel.Type == "pntSubComponent" and o_sel.SubComponent.Parent3DObject.Type == "polymsh"):
        b_logValue = Application.GetValue("preferences.scripting.cmdlog")
        if b_logValue:
            Application.SetValue("preferences.scripting.cmdlog", False, "")
        Application.DeselectAll()
        l_subComps = o_sel.SubComponent.ElementArray
        l_subCompsFilt = list(l_subComps)
        l_adjSub = []
        for o_subSel in l_subComps:
            o_subComp = Application.GetValue("%s.%s[%s]" % (o_sel.SubComponent.Parent3DObject, d_subType[o_sel.SubComponent.Type], o_subSel))
            Application.GrowSelection(o_subComp)
            l_curAdjSub = Application.GetValue("SelectionList")[0]
            l_curAdjSubIndex = list(l_curAdjSub.SubComponent.ElementArray)
            l_curAbjSubIndexA = list(l_curAdjSub.SubComponent.ElementArray)
            if o_subSel in l_subCompsFilt:
                l_subCompsFilt.remove(o_subSel)
                l_adjSub.append([])
                l_adjSub[len(l_adjSub) - 1].append(o_subSel)
                b_flag = 1
                while b_flag:
                    z = 0
                    for i_curAdjSub in l_curAdjSubIndex:
                        if i_curAdjSub in l_subCompsFilt:
                            l_adjSub[len(l_adjSub) - 1].append(i_curAdjSub)
                            l_subCompsFilt.remove(i_curAdjSub)
                            z = z + 1
                        else:
                            l_curAbjSubIndexA.remove(i_curAdjSub)
                    if z != 0:
                        o_subComp = Application.GetValue("%s.%s[%s]" % (o_sel.SubComponent.Parent3DObject, d_subType[o_sel.SubComponent.Type], str(l_curAbjSubIndexA).replace("[", "").replace("]", "")))
                        Application.GrowSelection(o_subComp)
                        l_curAdjSub = Application.GetValue("SelectionList")[0]
                        l_curAdjSubIndex = list(l_curAdjSub.SubComponent.ElementArray)
                        l_curAbjSubIndexA = list(l_curAdjSub.SubComponent.ElementArray)
                    else:
                        b_flag = 0
        for o_adjSub in l_adjSub:
            o_subComp = Application.GetValue("%s.%s[%s]" % (o_sel.SubComponent.Parent3DObject, d_subType[o_sel.SubComponent.Type], str(o_adjSub).replace("[", "").replace("]", "")))
            l_subIsland.append(o_subComp)
        Application.SelectGeometryComponents(o_sel)
        if b_logValue:
            Application.SetValue("preferences.scripting.cmdlog", True, "")
        return l_subIsland
    else:
        Application.LogMessage("rsSubCompIsland: Only works with polymsh subComponents")
        return None


##
# rsLongToRgba. Convert one long value to RGB values.
# @param i_longColor: Entire: Long value.
# @return XSICollection: Red, Green, Blue and alpha values. RGB values divided by 255.
def rsLongToRgba(i_longColor):
    i_red = ((i_longColor >> 24) & 0xFF) / 255.0
    i_green = ((i_longColor >> 16) & 0xFF) / 255.0
    i_blue = ((i_longColor >> 8) & 0xFF) / 255.0
    i_alpha = (i_longColor & 0xFF) / 255.0
    return (i_red, i_green, i_blue, i_alpha)
