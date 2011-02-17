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
Some features include zoom-in, zoom-out, delay setting
Authors: Ikey Doherty <ikey@linuxmint.com>, Nick Canupp <asheguy79@gmail.com>
Packaging: Kendall Weaver <kendalltweaver@gmail.com>
License: GPL
'''
class Shotter:

   def __init__(self):
      self.ui_file = '/usr/lib/pyshot/interface.ui'
      self.ui = gtk.Builder()
      self.ui.add_from_file(self.ui_file)
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
      self.window.set_title("Take a screenshot")
      
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
	  # Format options
      format = None
      fc = gtk.FileChooserDialog(title="Save screenshot", parent=self.window, action=gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
      resp = fc.run()
      if(resp == gtk.RESPONSE_CANCEL):
         fc.destroy()
      elif(resp == gtk.RESPONSE_OK):
		filetosave = fc.get_filename()
		# Append .png if needed
		if not filetosave.lower().endswith(".png"):
			filetosave += ".png"
		fc.destroy()
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
