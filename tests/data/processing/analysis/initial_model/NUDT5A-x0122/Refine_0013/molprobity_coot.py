# script auto-generated by phenix.molprobity


from __future__ import division
import cPickle
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui (object) :
  def __init__ (self, title) :
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window (self) :
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window (self, *args) :
    self.window.destroy()
    self.window = None

  def confirm_data (self, data) :
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists (self, data) :
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui (coot_extension_gui) :
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None) :
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__ (self, data_file=None, data=None) :
    assert ([data, data_file].count(None) == 1)
    if (data is None) :
      data = load_pkl(data_file)
    if not self.confirm_data(data) :
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets (self, data_key, box) :
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots (self, *args) :
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots (self, *args) :
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui (coot_extension_gui) :
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list (object) :
  def __init__ (self, columns, column_types, rows, box,
      default_size=(380,200)) :
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)) :
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns) :
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange (self, treeview) :
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots (show_dots, overlaps_only) :
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects) :
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects) :
      set_display_generic_object(object_number, 0)

def load_pkl (file_name) :
  pkl = open(file_name, "rb")
  data = cPickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', '  66 ', 'PRO', 0.043803598440920494, (-14.082, -7.728, -27.052999999999994)), ('A', ' 189 ', 'GLU', 0.0047968274745059936, (-30.154000000000003, 4.655999999999999, -15.651999999999996)), ('A', ' 189 ', 'GLU', 0.0047968274745059936, (-30.154000000000003, 4.655999999999999, -15.651999999999996)), ('A', ' 190 ', 'HIS', 0.005286265468406201, (-27.677, 5.3229999999999995, -12.834)), ('A', ' 190 ', 'HIS', 0.005286265468406201, (-27.677, 5.3229999999999995, -12.834)), ('B', '  66 ', 'PRO', 0.062321600819393044, (-1.3740000000000014, 13.989999999999997, -17.131)), ('C', '  53 ', 'THR', 0.024911558889471903, (-12.982, 18.14799999999999, -52.628)), ('C', '  53 ', 'THR', 0.025019409737626095, (-12.982, 18.14799999999999, -52.628)), ('C', '  66 ', 'PRO', 0.041563124357055704, (-35.844, 27.831000000000003, -38.26))]
data['omega'] = [('D', ' 161 ', 'LYS', None, (-40.751999999999995, -6.952, -56.997))]
data['rota'] = [('A', '  14 ', 'LYS', 0.07375810238226398, (15.539, -0.5069999999999999, -2.415)), ('A', '  38 ', 'ASP', 0.08970305903469476, (11.086, 1.979, 3.127)), ('A', '  70 ', 'ARG', 0.021912442989181075, (-19.213, -6.892000000000002, -38.747)), ('A', ' 125 ', 'GLU', 0.1331386259304624, (-3.384999999999998, -9.893999999999998, -27.92899999999999)), ('A', ' 191 ', 'LEU', 0.0, (-24.947, 2.7119999999999997, -12.482999999999999)), ('A', ' 191 ', 'LEU', 0.0, (-24.947, 2.7119999999999997, -12.482999999999999)), ('A', ' 191 ', 'LEU', 0.016649835068428827, (-24.916, 2.553, -12.561)), ('A', ' 191 ', 'LEU', 0.016649835068428827, (-24.916, 2.553, -12.561)), ('B', '  31 ', 'LEU', 0.07568077079721457, (-13.762, -6.869, 5.271)), ('B', '  38 ', 'ASP', 0.26792028203349566, (-30.188000000000006, -12.571000000000002, -6.464)), ('B', '  53 ', 'THR', 0.2666611394172743, (-14.526999999999994, 5.924999999999998, 6.197)), ('B', '  53 ', 'THR', 0.2666611394172743, (-14.526999999999994, 5.924999999999998, 6.197)), ('B', ' 208 ', 'ASN', 0.004666796882625504, (-9.501999999999999, 4.373, -35.59)), ('B', ' 208 ', 'ASN', 0.004666796882625504, (-9.501999999999999, 4.373, -35.59)), ('B', ' 208 ', 'ASN', 0.0, (-9.616, 4.619999999999999, -35.501)), ('B', ' 208 ', 'ASN', 0.0, (-9.616, 4.619999999999999, -35.501)), ('C', '  29 ', 'VAL', 0.06464116996846782, (-19.116000000000007, 20.770999999999994, -59.884)), ('C', '  35 ', 'THR', 0.07710695136296482, (-18.053, 1.4649999999999999, -61.965)), ('C', '  71 ', 'THR', 0.016713442604974062, (-45.485, 33.96, -26.664999999999996)), ('C', ' 136 ', 'LEU', 0.016999727211393992, (-27.034000000000002, 11.431000000000001, -58.51699999999999)), ('C', ' 136 ', 'LEU', 0.01689764110842617, (-27.03500000000001, 11.430999999999996, -58.518)), ('C', ' 189 ', 'GLU', 0.20397674992483997, (-46.85300000000001, 32.319, -58.609999999999985)), ('D', '  23 ', 'ILE', 0.29811569651457026, (-20.346000000000004, 21.861999999999995, -71.039)), ('D', '  45 ', 'THR', 0.14985232628715073, (-23.022000000000002, 32.61299999999999, -64.004)), ('D', '  72 ', 'LEU', 0.0003784257707785305, (-55.493999999999986, -2.253, -33.907))]
data['cbeta'] = [('A', '  82 ', 'GLN', ' ', 0.26753375312793565, (-22.747000000000007, -7.757000000000002, -13.252)), ('C', ' 190 ', 'HIS', ' ', 0.2520129753446382, (-44.05, 29.875000000000014, -61.99799999999998))]
data['probe'] = [(' B  92  ILE HD11', ' B 191  LEU HD13', -0.881, (7.89, 0.327, -15.419)), (' C 125  GLU  OE1', ' C 403  HOH  O  ', -0.877, (-35.348, 18.027, -33.401)), (' D 120  LYS  H  ', ' D 155  ASN HD21', -0.825, (-49.882, -4.044, -51.905)), (' A 104  THR HG23', ' A 107  ALA  H  ', -0.798, (-5.597, -19.355, -22.813)), (' B 208 AASN  C  ', ' B 208 AASN  OD1', -0.745, (-8.066, 3.316, -37.028)), (' B 208 BASN  C  ', ' B 208 BASN  OD1', -0.745, (-8.066, 3.316, -37.028)), (' C 203  ALA  HB3', ' D 203  ALA  HB3', -0.741, (-42.437, 15.948, -41.539)), (' B 301  EDO  H22', ' B 404  HOH  O  ', -0.74, (2.686, 23.456, -26.84)), (' B 196 DARG  NH2', ' F   8 DHOH  O  ', -0.702, (-3.323, 2.268, -10.106)), (' B 196 CARG  NH2', ' F   8 CHOH  O  ', -0.702, (-3.323, 2.268, -10.106)), (' B 301  EDO  C2 ', ' B 404  HOH  O  ', -0.686, (3.117, 23.322, -26.127)), (' A  92  ILE HD11', ' A 191 DLEU HD11', -0.678, (-25.1, 1.194, -17.887)), (' A  92  ILE HD11', ' A 191 CLEU HD11', -0.675, (-24.534, 1.139, -18.177)), (' A 191 ALEU  N  ', ' A 191 ALEU HD22', -0.667, (-25.512, 3.924, -13.677)), (' A 191 BLEU  N  ', ' A 191 BLEU HD22', -0.667, (-25.512, 3.924, -13.677)), (' A 203  ALA  HB3', ' B 203  ALA  HB3', -0.636, (-8.068, 4.57, -24.935)), (' C 179  LEU HD11', ' C 198  TYR  CZ ', -0.618, (-47.685, 19.245, -50.155)), (' C 104  THR HG23', ' C 107  ALA  H  ', -0.598, (-20.886, 25.274, -35.947)), (' A 179  LEU HD23', ' A 205  LYS  HD2', -0.59, (-14.445, 11.623, -24.888)), (' C 403  HOH  O  ', ' D 206  HIS  HE1', -0.585, (-36.117, 18.677, -33.574)), (' B 104  THR HG23', ' B 107  ALA  H  ', -0.569, (-11.264, 19.611, -7.568)), (' A 191 DLEU  C  ', ' A 191 DLEU HD23', -0.562, (-23.1, 2.993, -14.114)), (' A 191 CLEU  C  ', ' A 191 CLEU HD23', -0.562, (-23.1, 2.993, -14.114)), (' A 200  TYR  CD1', ' B 203  ALA  HB2', -0.562, (-9.159, 1.407, -25.295)), (' C 200  TYR  CD1', ' D 203  ALA  HB2', -0.559, (-40.84, 18.21, -40.873)), (' A 191 BLEU  H  ', ' A 191 BLEU HD22', -0.546, (-25.239, 4.628, -13.646)), (' A 191 ALEU  H  ', ' A 191 ALEU HD22', -0.546, (-25.239, 4.628, -13.646)), (' A 125  GLU  OE1', ' B 206  HIS  HE1', -0.542, (-4.501, -4.472, -29.488)), (' A 206  HIS  HE1', ' B 125  GLU  OE1', -0.536, (-10.761, 13.693, -22.599)), (' A  71  THR HG23', ' A 151  ASP  OD2', -0.53, (-18.569, -8.874, -42.573)), (' C 132  MET  O  ', ' D 196 BARG  NH1', -0.527, (-32.001, 14.512, -51.74)), (' C 132  MET  O  ', ' D 196 DARG  NH1', -0.526, (-32.003, 14.525, -51.739)), (' C 200  TYR  OH ', ' D 206  HIS  HD2', -0.506, (-39.192, 20.76, -37.517)), (' C 206  HIS  HE1', ' D 125  GLU  OE1', -0.496, (-50.692, 13.603, -46.767)), (' C  84  ARG  HG3', ' D 134 APRO  HB2', -0.492, (-33.324, 26.998, -56.244)), (' C  84  ARG  HG3', ' D 134 BPRO  HB2', -0.492, (-32.858, 26.562, -56.375)), (' A 206  HIS  HD2', ' B 200  TYR  OH ', -0.488, (-5.61, 10.639, -22.825)), (' B  60 AASP  OD2', ' B 139 ACYS  HA ', -0.486, (-13.741, 3.271, -3.509)), (' B  60 BASP  OD2', ' B 139 BCYS  HA ', -0.486, (-13.741, 3.271, -3.509)), (' B 301  EDO  H21', ' F  31 DHOH  O  ', -0.485, (2.682, 25.853, -25.511)), (' D  71  THR  O  ', ' D  73 BHIS  ND1', -0.484, (-54.04, -4.34, -36.449)), (' C 125  GLU  HG2', ' C 402  HOH  O  ', -0.474, (-31.307, 16.776, -34.856)), (' C  62  VAL HG12', ' C 142 CHIS  HB2', -0.467, (-25.319, 21.129, -41.462)), (' B  62 CVAL HG12', ' B 142  HIS  HB2', -0.466, (-11.538, 12.03, -9.433)), (' B  62 DVAL HG12', ' B 142  HIS  HB2', -0.466, (-11.538, 12.03, -9.433)), (' C  62  VAL HG12', ' C 142 DHIS  HB2', -0.466, (-25.319, 21.128, -41.461)), (' D 207 BALA  O  ', ' D 208 BASN  HB2', -0.465, (-46.576, 18.067, -32.157)), (' D 207 AALA  O  ', ' D 208 AASN  HB2', -0.465, (-46.576, 18.067, -32.157)), (' C  61  GLY  O  ', ' C 141 BILE  HA ', -0.464, (-24.788, 19.713, -45.01)), (' A  33 CLYS  HE3', ' A  45  THR HG21', -0.46, (2.576, -3.092, 10.877)), (' A  33 DLYS  HE3', ' A  45  THR HG21', -0.46, (2.576, -3.092, 10.877)), (' A 132  MET  O  ', ' B 196 BARG  NH2', -0.459, (-6.556, -0.992, -10.825)), (' A  92  ILE HD12', ' A 191 DLEU HD21', -0.458, (-22.917, 2.17, -16.981)), (' C 203  ALA  HB2', ' D 200  TYR  CD1', -0.457, (-42.844, 13.595, -43.172)), (' B  62 DVAL  HA ', ' B 142  HIS  O  ', -0.457, (-9.867, 10.517, -9.513)), (' A  92  ILE HD12', ' A 191 CLEU HD21', -0.456, (-22.649, 1.913, -17.324)), (' D 207 BALA  O  ', ' D 208 BASN  CB ', -0.455, (-47.149, 18.152, -32.352)), (' D 207 AALA  O  ', ' D 208 AASN  CB ', -0.455, (-47.149, 18.152, -32.352)), (' C  86  PRO  O  ', ' D 138 AASN  HB3', -0.453, (-32.347, 23.11, -63.828)), (' A 203  ALA  HB2', ' B 200  TYR  CD1', -0.451, (-6.347, 6.563, -22.589)), (' B  62 CVAL  HA ', ' B 142  HIS  O  ', -0.448, (-9.874, 10.306, -9.975)), (' A 132  MET  O  ', ' B 196 AARG  NH2', -0.448, (-6.638, -1.316, -10.524)), (' C  86  PRO  O  ', ' D 138 BASN  HB3', -0.446, (-32.508, 23.579, -63.681)), (' C  61  GLY  O  ', ' C 141 AILE  HA ', -0.446, (-24.62, 20.157, -44.925)), (' B 189  GLU  OE2', ' B 191  LEU HD11', -0.445, (10.505, 0.407, -13.926)), (' A  70  ARG  HD3', ' A 409  HOH  O  ', -0.444, (-20.349, -4.747, -35.817)), (' B 301  EDO  C2 ', ' F  31 DHOH  O  ', -0.439, (2.855, 25.67, -25.585)), (' A 132  MET  HE1', ' A 196  ARG  CZ ', -0.437, (-10.66, -4.062, -13.341)), (' C 191  LEU  C  ', ' C 191  LEU HD12', -0.433, (-42.717, 27.711, -55.909)), (' C 206  HIS  HD2', ' D 200  TYR  OH ', -0.433, (-46.339, 11.243, -43.79)), (' A  92  ILE  CD1', ' A 191 CLEU HD11', -0.431, (-24.025, 1.085, -17.569)), (' A  92  ILE  CD1', ' A 191 DLEU HD11', -0.431, (-24.025, 1.085, -17.569)), (' C 165  GLY  HA2', ' C 167  PHE  CE1', -0.427, (-26.27, 38.915, -55.986)), (' C  92  ILE HD12', ' C 191  LEU HD11', -0.416, (-43.202, 28.582, -52.875)), (' D  17  ILE HD12', ' D  34  THR  CG2', -0.413, (-29.258, 29.95, -66.148)), (' C  31  LEU HD23', ' C  32  GLU  N  ', -0.413, (-20.093, 12.277, -64.206)), (' C 132  MET  HE1', ' C 196  ARG  CZ ', -0.412, (-31.848, 20.108, -50.14)), (' A  71  THR  O  ', ' A  73  HIS  HD2', -0.412, (-22.233, -4.635, -40.967)), (' C  31  LEU HD23', ' C  32  GLU  H  ', -0.412, (-20.031, 11.959, -63.762)), (' C  74  TYR  HB3', ' C 426  HOH  O  ', -0.41, (-48.355, 27.627, -35.255)), (' A  49  VAL HG21', ' B  49 AVAL HG11', -0.409, (-9.344, -5.277, 1.005)), (' A  49  VAL HG21', ' B  49 BVAL HG11', -0.409, (-9.344, -5.277, 1.005)), (' A  86  PRO  HD3', ' B  46  TRP  CD1', -0.409, (-19.396, -8.356, -3.696)), (' A 200  TYR  OH ', ' B 206  HIS  HD2', -0.406, (-9.429, -1.621, -27.871)), (' A  58 BTHR  OG1', ' A 142  HIS  NE2', -0.404, (-1.601, -14.599, -16.568)), (' A  58 ATHR  OG1', ' A 142  HIS  NE2', -0.404, (-1.601, -14.599, -16.568))]
gui = coot_molprobity_todo_list_gui(data=data)
