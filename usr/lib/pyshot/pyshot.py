#!/usr/bin/env python
try:
   import pygtk
   pygtk.require("2.0")
except:
   print "You do not have the required PyGTK for this application."
try:
   import gtk
   from time import sleep
   import threading
except:
   print "You do not appear to have PyGTK installed"

'''
PyShot is a small light weight screenshot utility written in pygtk.
Some features include zoom-in, zoom-out, delay setting, and allows the user to choose between JPEG and PNG formats.
Author: Ikey Doherty <contactjfreak@googlemail.com>
Further Development: Nick Canupp <asheguy79@gmail.com>
License: GPL
'''
class Shotter:

   ui_desc = """<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy project-wide -->
  <object class="GtkWindow" id="window">
    <property name="window_position">center</property>
    <property name="default_width">400</property>
    <property name="default_height">230</property>
    <property name="icon_name">user-desktop</property>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <property name="orientation">vertical</property>
        <property name="spacing">3</property>
        <child>
          <object class="GtkHBox" id="hbox1">
            <property name="visible">True</property>
            <child>
              <object class="GtkScrolledWindow" id="scrolledwindow1">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="hscrollbar_policy">automatic</property>
                <property name="vscrollbar_policy">automatic</property>
                <child>
                  <object class="GtkViewport" id="viewport1">
                    <property name="visible">True</property>
                    <property name="resize_mode">queue</property>
                    <child>
                      <object class="GtkImage" id="image">
                        <property name="visible">True</property>
                        <property name="stock">gtk-missing-image</property>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
              <packing>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkVBox" id="vbox2">
                <property name="visible">True</property>
                <property name="orientation">vertical</property>
                <child>
                  <object class="GtkFrame" id="frame1">
                    <property name="visible">True</property>
                    <property name="label_xalign">0</property>
                    <property name="shadow_type">none</property>
                    <child>
                      <object class="GtkAlignment" id="alignment1">
                        <property name="visible">True</property>
                        <property name="left_padding">12</property>
                        <child>
                          <object class="GtkVBox" id="vbox3">
                            <property name="visible">True</property>
                            <property name="orientation">vertical</property>
                            <child>
                              <object class="GtkCheckButton" id="checkbutton_hide_win">
                                <property name="label" translatable="yes">Hide window</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="receives_default">False</property>
                                <property name="active">True</property>
                                <property name="draw_indicator">True</property>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="position">0</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkCheckButton" id="checkbutton_delay">
                                <property name="label" translatable="yes">Use delay</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="receives_default">False</property>
                                <property name="draw_indicator">True</property>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="position">1</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkSpinButton" id="spinbutton">
                                <property name="visible">True</property>
                                <property name="sensitive">False</property>
                                <property name="can_focus">True</property>
                                <property name="max_length">2</property>
                                <property name="invisible_char">&#x25CF;</property>
                                <property name="numeric">True</property>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="position">2</property>
                              </packing>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child type="label">
                      <object class="GtkLabel" id="label_options">
                        <property name="visible">True</property>
                        <property name="label" translatable="yes">&lt;b&gt;Options&lt;/b&gt;</property>
                        <property name="use_markup">True</property>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkButton" id="button_shoot">
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">True</property>
                    <child>
                      <object class="GtkHBox" id="hbox2">
                        <property name="visible">True</property>
                        <child>
                          <object class="GtkImage" id="image1">
                            <property name="visible">True</property>
                            <property name="pixel_size">16</property>
                            <property name="icon_name">user-desktop</property>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="fill">False</property>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkLabel" id="label_shot">
                            <property name="visible">True</property>
                            <property name="label" translatable="yes">Shoot another</property>
                          </object>
                          <packing>
                            <property name="position">1</property>
                          </packing>
                        </child>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">False</property>
                    <property name="position">1</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkButton" id="button_zoom_in">
                    <property name="label">gtk-zoom-in</property>
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">True</property>
                    <property name="use_stock">True</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">False</property>
                    <property name="position">2</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkButton" id="button_zoom_out">
                    <property name="label">gtk-zoom-out</property>
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <property name="receives_default">True</property>
                    <property name="use_stock">True</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">False</property>
                    <property name="position">3</property>
                  </packing>
                </child>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkHButtonBox" id="hbuttonbox1">
            <property name="visible">True</property>
            <property name="spacing">3</property>
            <property name="layout_style">end</property>
            <child>
              <object class="GtkButton" id="button_close">
                <property name="label">gtk-close</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_stock">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="button_save">
                <property name="label">gtk-save-as</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_stock">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="pack_type">end</property>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>"""

   def __init__(self):
      self.ui = gtk.Builder()
      self.ui.add_from_string(self.ui_desc)
      self.spinner = self.ui.get_object("spinbutton")
      adj = gtk.Adjustment()
      adj.set_upper(30)
      adj.set_lower(0)
      adj.set_step_increment(1)
      self.spinner.set_adjustment(adj)

      self.scale_factor = 1
      self.ui.get_object("checkbutton_delay").connect("clicked", lambda x: self.spinner.set_sensitive(x.get_active()))
      self.ui.get_object("button_shoot").connect("clicked", self.shot_callback)
      self.ui.get_object("button_zoom_in").connect("clicked", self.zoom_in)
      self.ui.get_object("button_zoom_out").connect("clicked", self.zoom_out)
      self.ui.get_object("button_close").connect("clicked", gtk.main_quit)
      self.ui.get_object("button_save").connect("clicked", self.save_image)
      self.window = self.ui.get_object("window")
      self.window.connect("destroy", gtk.main_quit)
      self.window.set_title("Screenshot utility")
      
      self.take_screenie(False, None)
      self.window.show()

   def shot_callback(self, widget):
      self.window.set_sensitive(False)
      delay = None
      should_hide = self.ui.get_object("checkbutton_hide_win").get_active()
      if(self.ui.get_object("checkbutton_delay").get_active()):
         delay = self.spinner.get_value()
      t = threading.Thread(group=None, target=self.take_screenie, name="screenshot", args=(should_hide, delay), kwargs={})
      t.start()
      
   def take_screenie(self, should_hide, delay):
      gtk.gdk.threads_enter()
      if(should_hide):
         self.window.hide()
      gtk.gdk.threads_leave()
      if(delay is not None):
         sleep(delay)

      gtk.gdk.threads_enter()
      root = gtk.gdk.get_default_root_window()
      size = root.get_size()
      w = size[0]
      h = size[1]
      x = 0
      y = 0
      cmap = root.get_colormap()
      sshot = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,w,h)
      sshot.get_from_drawable(root, cmap, x, y, 0, 0, w, h)
      self.image = sshot
      self.ui.get_object("image").set_from_pixbuf(sshot)
      self.scale_factor = 0.04
      self.zoom_in(None)
      if(should_hide):
         self.window.show()
      self.window.set_sensitive(True)
      gtk.gdk.threads_leave()
      
   def zoom_in(self, widget):
      self.scale_factor += 0.20
      img = self.image
      h = float(img.get_height())
      w = float(img.get_width())
      h *= self.scale_factor
      w *= self.scale_factor
      img2 = img.scale_simple(int(w), int(h), gtk.gdk.INTERP_BILINEAR)
      self.ui.get_object("image").set_from_pixbuf(img2)
      
   def zoom_out(self, widget):
      self.scale_factor -= 0.20
      img = self.image
      h = float(img.get_height())
      w = float(img.get_width())
      h *= self.scale_factor
      w *= self.scale_factor
      if(h > 0 and w > 0):
         img2 = img.scale_simple(int(w), int(h), gtk.gdk.INTERP_BILINEAR)
         self.ui.get_object("image").set_from_pixbuf(img2)
      else:
         self.scale_factor += 0.20

   def save_image(self, widget):
      format = None
      frame = gtk.Frame("Image format")
      wid = gtk.VBox()
      jpg = gtk.RadioButton(None, "JPEG format")
      wid.pack_start(jpg, False, False)
      png = gtk.RadioButton(jpg, "PNG format")
      wid.pack_start(png, False, False)
      frame.add(wid)
      frame.show_all()
      fc = gtk.FileChooserDialog(title="Save screenshot", parent=self.window, action=gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
      fc.set_extra_widget(frame)
      resp = fc.run()
      if(resp == gtk.RESPONSE_CANCEL):
         fc.destroy()
      elif(resp == gtk.RESPONSE_OK):
         filetosave = fc.get_filename()
         fc.destroy()
         if(jpg.get_active()):
            format = "jpeg"
         else:
            format = "png"
            try:
               self.image.save(filetosave, format)
            except:
               msg = "Failed to save file: " + filetosave
               md = gtk.MessageDialog(parent=self.window, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format=msg)
               md.connect("response", lambda: md.destroy())
               md.show()
if __name__ == "__main__":
   gtk.gdk.threads_init()
   Shotter()
   gtk.main()
