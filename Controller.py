# -*- coding: ISO-8859-1 -*-
#
# generated by wxGlade 0.9.3 on Fri Jun 28 16:25:14 2019
#

import wx
from icons import *
from K40Controller import get_code_string_from_code
from ThreadConstants import *


class Controller(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Controller.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW | wx.STAY_ON_TOP
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((507, 507))
        self.button_controller_control = wx.ToggleButton(self, wx.ID_ANY, "Start Controller")
        self.text_controller_status = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_usb_connect = wx.ToggleButton(self, wx.ID_ANY, "Connect Usb")
        self.text_usb_status = wx.TextCtrl(self, wx.ID_ANY, "")
        self.gauge_buffer = wx.Gauge(self, wx.ID_ANY, 10)
        self.text_buffer_length = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_buffer_viewer = wx.BitmapButton(self, wx.ID_ANY, icons8_comments_50.GetBitmap())
        self.packet_count_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.rejected_packet_count_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.packet_text_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.last_packet_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_0 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_desc = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_2 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_3 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_4 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_5 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_stop = wx.BitmapButton(self, wx.ID_ANY, icons8_stop_sign_50.GetBitmap())

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_button_start_controller, self.button_controller_control)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_button_start_usb, self.button_usb_connect)
        self.Bind(wx.EVT_BUTTON, self.on_button_emergency_stop, self.button_stop)
        self.Bind(wx.EVT_BUTTON, self.on_button_bufferview, self.button_buffer_viewer)
        # end wxGlade
        self.Bind(wx.EVT_CLOSE, self.on_close, self)
        self.project = None
        self.dirty = False
        self.status_data = None
        self.packet_data = None
        self.packet_string = b''
        self.buffer_size = 0
        self.buffer_max = 0
        self.usb_status = ""
        self.control_state = None

        self.update_packet_string = False
        self.update_packet_data = False
        self.update_packet_count = False
        self.update_rejected_count = False
        self.update_status_data = False
        self.update_buffer_size = False
        self.update_control_state = False
        self.update_usb_status = False

    def set_project(self, project):
        self.project = project
        project["status", self.update_status] = self
        project["packet", self.update_packet] = self
        project["packet_text", self.update_packet_text] = self
        project["buffer", self.on_buffer_update] = self
        project["usb_status", self.on_usbstatus] = self
        project["control_thread", self.on_control_state] = self
        self.set_controller_button_by_state()

    def on_close(self, event):
        self.project["status", self.update_status] = None
        self.project["packet", self.update_packet] = None
        self.project["packet_text", self.update_packet_text] = None
        self.project["buffer", self.on_buffer_update] = None
        self.project["usb_status", self.on_usbstatus] = None
        self.project["control_thread", self.on_control_state] = None
        try:
            del self.project.windows["controller"]
        except KeyError:
            pass
        self.project = None
        event.Skip()  # delegate destroy to super

    def __set_properties(self):
        # begin wxGlade: Controller.__set_properties
        self.SetTitle("Controller")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_usb_connector_50.GetBitmap())
        self.SetIcon(_icon)
        self.button_controller_control.SetBackgroundColour(wx.Colour(102, 255, 102))
        self.button_controller_control.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.button_controller_control.SetBitmap(icons8_play_50.GetBitmap())
        self.button_controller_control.SetBitmapPressed(icons8_pause_50.GetBitmap())
        self.button_usb_connect.SetBackgroundColour(wx.Colour(102, 255, 102))
        self.button_usb_connect.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.button_usb_connect.SetBitmap(icons8_connected_50.GetBitmap())
        self.button_usb_connect.SetBitmapPressed(icons8_disconnected_50.GetBitmap())
        self.text_buffer_length.SetMinSize((165, 23))
        self.button_buffer_viewer.SetSize(self.button_buffer_viewer.GetBestSize())
        self.packet_count_text.SetMinSize((77, 23))
        self.rejected_packet_count_text.SetMinSize((77, 23))
        self.text_byte_0.SetMinSize((77, 23))
        self.text_byte_1.SetMinSize((77, 23))
        self.text_desc.SetMinSize((75, 23))
        self.text_byte_2.SetMinSize((77, 23))
        self.text_byte_3.SetMinSize((77, 23))
        self.text_byte_4.SetMinSize((77, 23))
        self.text_byte_5.SetMinSize((77, 23))
        self.button_stop.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.button_stop.SetSize(self.button_stop.GetBestSize())
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Controller.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        byte_data_sizer = wx.BoxSizer(wx.HORIZONTAL)
        byte5sizer = wx.BoxSizer(wx.VERTICAL)
        byte4sizer = wx.BoxSizer(wx.VERTICAL)
        byte3sizer = wx.BoxSizer(wx.VERTICAL)
        byte2sizer = wx.BoxSizer(wx.VERTICAL)
        byte1sizer = wx.BoxSizer(wx.VERTICAL)
        byte0sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9.Add(self.button_controller_control, 0, wx.EXPAND, 0)
        label_12 = wx.StaticText(self, wx.ID_ANY, "Controller")
        label_12.SetMinSize((80, 16))
        sizer_17.Add(label_12, 1, 0, 0)
        sizer_17.Add(self.text_controller_status, 0, wx.EXPAND, 0)
        sizer_9.Add(sizer_17, 0, 0, 0)
        sizer_1.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_18.Add(self.button_usb_connect, 0, wx.EXPAND, 0)
        label_7 = wx.StaticText(self, wx.ID_ANY, "Usb Status")
        label_7.SetMinSize((80, 16))
        sizer_15.Add(label_7, 1, 0, 0)
        sizer_15.Add(self.text_usb_status, 0, 0, 0)
        sizer_18.Add(sizer_15, 0, 0, 0)
        sizer_1.Add(sizer_18, 0, wx.EXPAND, 0)
        static_line_2 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_2, 0, wx.EXPAND, 0)
        sizer_1.Add(self.gauge_buffer, 0, wx.EXPAND, 0)
        label_8 = wx.StaticText(self, wx.ID_ANY, "Buffer")
        sizer_5.Add(label_8, 0, 0, 0)
        sizer_5.Add(self.text_buffer_length, 10, 0, 0)
        sizer_5.Add(self.button_buffer_viewer, 1, 0, 0)
        sizer_1.Add(sizer_5, 0, 0, 0)
        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.EXPAND, 0)
        label_11 = wx.StaticText(self, wx.ID_ANY, "Packet Count  ")
        sizer_2.Add(label_11, 0, 0, 0)
        sizer_2.Add(self.packet_count_text, 0, 0, 0)
        sizer_16.Add(sizer_2, 10, wx.EXPAND, 0)
        label_13 = wx.StaticText(self, wx.ID_ANY, "Rejected Packets")
        sizer_3.Add(label_13, 0, 0, 0)
        sizer_3.Add(self.rejected_packet_count_text, 0, 0, 0)
        sizer_16.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_16, 0, 0, 0)
        label_10 = wx.StaticText(self, wx.ID_ANY, "Packet Text  ")
        sizer_14.Add(label_10, 1, 0, 0)
        sizer_14.Add(self.packet_text_text, 11, 0, 0)
        sizer_1.Add(sizer_14, 0, 0, 0)
        label_9 = wx.StaticText(self, wx.ID_ANY, "Last Packet  ")
        sizer_13.Add(label_9, 1, 0, 0)
        sizer_13.Add(self.last_packet_text, 11, 0, 0)
        sizer_1.Add(sizer_13, 0, 0, 0)
        byte0sizer.Add(self.text_byte_0, 0, 0, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, "Byte 0")
        byte0sizer.Add(label_1, 0, 0, 0)
        byte_data_sizer.Add(byte0sizer, 1, wx.EXPAND, 0)
        byte1sizer.Add(self.text_byte_1, 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Byte 1")
        byte1sizer.Add(label_2, 0, 0, 0)
        byte1sizer.Add(self.text_desc, 0, 0, 0)
        byte_data_sizer.Add(byte1sizer, 1, wx.EXPAND, 0)
        byte2sizer.Add(self.text_byte_2, 0, 0, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, "Byte 2")
        byte2sizer.Add(label_3, 0, 0, 0)
        byte_data_sizer.Add(byte2sizer, 1, wx.EXPAND, 0)
        byte3sizer.Add(self.text_byte_3, 0, 0, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "Byte 3")
        byte3sizer.Add(label_4, 0, 0, 0)
        byte_data_sizer.Add(byte3sizer, 1, wx.EXPAND, 0)
        byte4sizer.Add(self.text_byte_4, 0, 0, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, "Byte 4")
        byte4sizer.Add(label_5, 0, 0, 0)
        byte_data_sizer.Add(byte4sizer, 1, wx.EXPAND, 0)
        byte5sizer.Add(self.text_byte_5, 0, 0, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, "Byte 5")
        byte5sizer.Add(label_6, 0, 0, 0)
        byte_data_sizer.Add(byte5sizer, 1, wx.EXPAND, 0)
        sizer_1.Add(byte_data_sizer, 0, wx.EXPAND, 0)
        sizer_1.Add(self.button_stop, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def post_update(self):
        if not self.dirty:
            self.dirty = True
            wx.CallAfter(self.post_update_on_gui_thread)

    def post_update_on_gui_thread(self):
        if self.project is None:
            return  # was closed this is just a leftover update.

        update = False
        if self.update_packet_string:
            string_data = self.packet_string
            if string_data is not None and len(string_data) != 0:
                self.packet_text_text.SetValue(str(string_data))
            self.packet_string = b''
            update = True

        if self.update_packet_data:
            self.update_packet_data = False
            self.last_packet_text.SetValue(str(self.packet_data))
            update = True

        if self.update_packet_count:
            self.update_packet_count = False
            self.packet_count_text.SetValue(str(self.project.controller.packet_count))
            self.rejected_packet_count_text.SetValue(str(self.project.controller.rejected_count))

        if self.update_status_data:
            self.update_status_data = False
            status_data = self.status_data
            if status_data is not None:
                if isinstance(status_data, int):
                    self.text_desc.SetValue(str(status_data))
                    self.text_desc.SetValue(get_code_string_from_code(status_data))
                else:
                    if len(status_data) == 6:
                        self.text_byte_0.SetValue(str(status_data[0]))
                        self.text_byte_1.SetValue(str(status_data[1]))
                        self.text_byte_2.SetValue(str(status_data[2]))
                        self.text_byte_3.SetValue(str(status_data[3]))
                        self.text_byte_4.SetValue(str(status_data[4]))
                        self.text_byte_5.SetValue(str(status_data[5]))
                        self.text_desc.SetValue(get_code_string_from_code(status_data[1]))
            update = True
        if self.update_buffer_size:
            self.update_buffer_size = False
            self.text_buffer_length.SetValue(str(self.buffer_size))
            self.gauge_buffer.SetValue(self.buffer_size)
            self.gauge_buffer.SetRange(self.buffer_max)
            update = True
        if self.update_control_state:
            self.update_control_state = False
            self.text_controller_status.SetValue(get_state_string_from_state(self.control_state))
            self.set_controller_button_by_state()
            update = True
        if self.update_usb_status:
            self.update_usb_status = False
            self.text_usb_status.SetValue(self.usb_status)
            self.set_usb_button_by_state()
            update = True
        if update:
            pass
        self.dirty = False

    def on_button_start_controller(self, event):  # wxGlade: Controller.<event_handler>
        state = self.control_state
        if state == THREAD_STATE_UNSTARTED or state == THREAD_STATE_FINISHED:
            self.project.controller.start_queue_consumer()
        elif state == THREAD_STATE_PAUSED:
            self.project.controller.resume()
        elif state == THREAD_STATE_STARTED:
            self.project.controller.pause()
        elif state == THREAD_STATE_ABORT:
            self.project.controller.reset_thread()
            self.project("abort", 0)

    def on_button_start_usb(self, event):  # wxGlade: Controller.<event_handler>
        if self.project.controller.usb is None:
            self.project.controller.start_usb()
        else:
            self.project.controller.stop_usb()

    def on_button_emergency_stop(self, event):  # wxGlade: Controller.<event_handler>
        self.project("abort", 1)
        self.project.controller.emergency_stop()

    def on_button_bufferview(self, event):  # wxGlade: Controller.<event_handler>
        self.project.close_old_window("bufferview")
        from BufferView import BufferView
        window = BufferView(None, wx.ID_ANY, "")
        window.set_project(self.project)
        window.Show()
        self.project.windows["bufferview"] = window

    def update_status(self, data):
        self.update_status_data = True
        self.status_data = data
        self.post_update()

    def update_packet(self, data):
        self.update_packet_data = True
        self.packet_data = data
        self.post_update()

    def update_packet_text(self, string_data):
        self.update_packet_string = True
        self.packet_string = string_data
        self.post_update()

    def on_usbstatus(self, status):
        self.update_usb_status = True
        self.usb_status = status
        self.post_update()

    def on_buffer_update(self, value):
        self.update_buffer_size = True
        self.buffer_size = value
        if self.buffer_size > self.buffer_max:
            self.buffer_max = self.buffer_size
        self.post_update()

    def on_control_state(self, state):
        self.update_control_state = True
        self.control_state = state
        self.post_update()

    def set_usb_button_by_state(self):
        status = self.usb_status
        if status == "Not Found":
            self.button_usb_connect.SetBackgroundColour("#ff0000")
            self.button_usb_connect.SetLabel(status)
            self.button_usb_connect.SetValue(True)
            self.button_usb_connect.Enable()
        elif status == "Uninitialized" or status == "Disconnected":
            self.button_usb_connect.SetBackgroundColour("#ffff00")
            self.button_usb_connect.SetLabel("Connect")
            self.button_usb_connect.SetValue(True)
            self.button_usb_connect.Enable()
        elif status == "Disconnecting":
            self.button_usb_connect.SetBackgroundColour("#ffff00")
            self.button_usb_connect.SetLabel("Disconnecting...")
            self.button_usb_connect.SetValue(True)
            self.button_usb_connect.Disable()
        elif status == "Connected":
            self.button_usb_connect.SetBackgroundColour("#00ff00")
            self.button_usb_connect.SetLabel("Disconnect")
            self.button_usb_connect.SetValue(False)
            self.button_usb_connect.Enable()
        elif status == "Connecting":
            self.button_usb_connect.SetBackgroundColour("#00ff00")
            self.button_usb_connect.SetLabel("Connecting...")
            self.button_usb_connect.SetValue(False)
            self.button_usb_connect.Disable()
        else:
            print(status)

    def set_controller_button_by_state(self):
        state = self.control_state
        if state == THREAD_STATE_UNSTARTED or state == THREAD_STATE_FINISHED:
            self.button_controller_control.SetBackgroundColour("#00ff00")
            self.button_controller_control.SetLabel("Start Controller")
            self.button_controller_control.SetValue(False)
        elif state == THREAD_STATE_PAUSED:
            self.button_controller_control.SetBackgroundColour("#00dd00")
            self.button_controller_control.SetLabel("Resume Controller")
            self.button_controller_control.SetValue(False)
        elif state == THREAD_STATE_STARTED:
            self.button_controller_control.SetBackgroundColour("#ffff00")
            self.button_controller_control.SetLabel("Pause Controller")
            self.button_controller_control.SetValue(True)
        elif state == THREAD_STATE_ABORT:
            self.button_controller_control.SetBackgroundColour("#ff0000")
            self.button_controller_control.SetLabel("Manual Reset")
            self.button_controller_control.SetValue(True)

# end of class Controller
