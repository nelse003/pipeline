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
data['rama'] = [('A', '  66 ', 'PRO', 0.04022645536994239, (-14.191999999999995, -7.74, -27.138)), ('B', '  66 ', 'PRO', 0.03860927841955039, (-1.5069999999999992, 13.863, -17.075)), ('B', '  66 ', 'PRO', 0.03860927841955039, (-1.5069999999999992, 13.863, -17.075)), ('B', ' 161 ', 'LYS', 0.07752640065536033, (6.301, 17.342, -2.692)), ('C', '  66 ', 'PRO', 0.030894556681831768, (-36.036, 27.827999999999996, -38.191)), ('D', '  66 ', 'PRO', 0.05991579326490823, (-45.84899999999999, 4.613999999999997, -47.961)), ('D', '  66 ', 'PRO', 0.05991579326490823, (-45.84899999999999, 4.613999999999997, -47.961)), ('D', ' 190 ', 'HIS', 0.003585268936230457, (-22.442999999999998, 2.195999999999999, -42.65700000000001))]
data['omega'] = [('B', ' 208 ', 'ASN', None, (-7.041999999999997, 3.5680000000000005, -33.887))]
data['rota'] = [('A', '  14 ', 'LYS', 0.0, (15.486, -0.625, -2.289)), ('A', '  43 ', 'THR', 0.05881724847052638, (10.273999999999997, -0.546, 8.807)), ('A', '  70 ', 'ARG', 0.04310513768443936, (-19.346999999999994, -6.8900000000000015, -38.712)), ('A', ' 125 ', 'GLU', 0.09578921556044803, (-3.451999999999999, -9.936999999999998, -27.842000000000002)), ('A', ' 191 ', 'LEU', 0.002060317350958233, (-24.946, 2.5669999999999984, -12.332000000000004)), ('B', '  31 ', 'LEU', 0.08937398475593941, (-13.924999999999999, -7.042999999999998, 5.189000000000001)), ('B', '  38 ', 'ASP', 0.05655147514307663, (-30.307999999999996, -12.681, -6.412)), ('B', '  43 ', 'THR', 0.02705827905745082, (-30.69399999999999, -15.038, -0.853)), ('B', ' 205 ', 'LYS', 0.07001395354553752, (-3.494, 1.71, -30.236)), ('B', ' 208 ', 'ASN', 0.18839909541821306, (-6.706999999999999, 2.7809999999999997, -35.099)), ('C', '  31 ', 'LEU', 0.0224570907073012, (-19.499000000000002, 14.713999999999997, -63.397000000000006)), ('C', '  45 ', 'THR', 0.2551226793611592, (-21.781, 1.5519999999999996, -64.243)), ('C', ' 136 ', 'LEU', 0.29546076167373925, (-27.607999999999993, 11.289999999999992, -58.715)), ('C', ' 164 ', 'ASP', 0.002828774267982226, (-23.116999999999997, 40.173, -52.952)), ('D', '  24 ', 'SER', 0.2018437290726665, (-20.778999999999996, 18.17, -70.97)), ('D', '  43 ', 'THR', 0.028558605117723346, (-25.114000000000004, 39.32899999999999, -65.65)), ('D', '  72 ', 'LEU', 0.03123931568832482, (-55.67799999999999, -2.317000000000001, -33.892)), ('D', ' 196 ', 'ARG', 0.0, (-36.43799999999999, 13.956, -47.367)), ('D', ' 196 ', 'ARG', 0.0, (-36.43799999999999, 13.956, -47.367))]
data['cbeta'] = [('A', '  82 ', 'GLN', ' ', 0.31096198420075494, (-23.139, -7.993, -13.293000000000001)), ('D', '  52 ', 'THR', ' ', 0.3003731116872809, (-30.370999999999988, 13.938999999999995, -70.8)), ('D', '  74 ', 'TYR', ' ', 0.2509477636888974, (-48.132, 1.3089999999999984, -34.303))]
data['probe'] = [(' D 196 DARG  HG3', ' D 196 DARG HH21', -1.167, (-36.458, 15.584, -50.068)), (' D 196 BARG  HG3', ' D 196 BARG HH21', -1.167, (-36.458, 15.584, -50.068)), (' D 196 DARG  HG3', ' D 196 DARG  NH2', -0.947, (-35.19, 15.714, -49.975)), (' D 196 BARG  HG3', ' D 196 BARG  NH2', -0.947, (-35.19, 15.714, -49.975)), (' C 125  GLU  OE1', ' C 403  HOH  O  ', -0.789, (-35.495, 18.111, -33.326)), (' C 104  THR HG23', ' C 107  ALA  H  ', -0.764, (-20.946, 25.287, -36.376)), (' D 120  LYS  H  ', ' D 155  ASN HD21', -0.753, (-49.712, -4.242, -51.262)), (' D 196 BARG  CG ', ' D 196 BARG HH21', -0.725, (-36.37, 15.463, -50.319)), (' D 196 DARG  CG ', ' D 196 DARG HH21', -0.725, (-36.37, 15.463, -50.319)), (' B  92  ILE HD11', ' B 191  LEU HD13', -0.682, (8.363, 0.329, -14.853)), (' B 104  THR HG23', ' B 107  ALA  H  ', -0.616, (-10.96, 19.371, -7.283)), (' D 194  ASP  OD1', ' D 196 CARG  HD3', -0.599, (-34.983, 12.398, -49.977)), (' C 203  ALA  HB3', ' D 203  ALA  HB3', -0.589, (-42.66, 16.39, -41.067)), (' D 189  GLU  O  ', ' D 190  HIS  C  ', -0.589, (-24.578, 1.982, -43.09)), (' D 194  ASP  OD1', ' D 196 AARG  HD3', -0.583, (-34.508, 11.974, -49.811)), (' C 132  MET  HE1', ' C 196  ARG  CZ ', -0.582, (-32.376, 20.269, -50.257)), (' C 302  MG  MG  ', ' C 454  HOH  O  ', -0.58, (-26.023, 31.072, -49.224)), (' A 203  ALA  HB3', ' B 203  ALA  HB3', -0.574, (-7.669, 4.059, -25.149)), (' D 104  THR HG23', ' D 107  ALA  H  ', -0.559, (-50.129, 8.107, -62.345)), (' C 200  TYR  OH ', ' D 206  HIS  HD2', -0.552, (-39.398, 20.824, -37.545)), (' C 403  HOH  O  ', ' D 206  HIS  HE1', -0.549, (-36.241, 19.201, -33.688)), (' A 104  THR HG23', ' A 107  ALA  H  ', -0.549, (-5.802, -19.521, -22.26)), (' A 200  TYR  CD1', ' B 203  ALA  HB2', -0.54, (-9.264, 1.374, -25.274)), (' B 125 DGLU  HG3', ' B 447  HOH  O  ', -0.539, (-13.277, 13.166, -18.947)), (' B 125 CGLU  HG3', ' B 447  HOH  O  ', -0.539, (-13.277, 13.166, -18.947)), (' C 203  ALA  HB2', ' D 200  TYR  CD1', -0.537, (-43.217, 13.702, -43.327)), (' B 301  EDO  C2 ', ' B 404  HOH  O  ', -0.537, (2.729, 23.304, -26.234)), (' A 132  MET  HE1', ' A 196  ARG  CZ ', -0.534, (-10.608, -4.426, -13.609)), (' B 194  ASP  OD2', ' B 196  ARG  NH2', -0.516, (-4.739, -0.111, -11.546)), (' D 196 BARG  CG ', ' D 196 BARG  NH2', -0.509, (-35.737, 14.519, -49.531)), (' D 196 DARG  CG ', ' D 196 DARG  NH2', -0.509, (-35.737, 14.519, -49.531)), (' C 206 AHIS  HD2', ' D 200  TYR  OH ', -0.504, (-46.265, 11.373, -43.749)), (' C 206 BHIS  HD2', ' D 200  TYR  OH ', -0.504, (-46.265, 11.373, -43.749)), (' B 189  GLU  HB3', ' B 191  LEU HD12', -0.504, (10.015, -1.636, -15.052)), (' B 125 DGLU  HG2', ' B 145 DTHR  HB ', -0.503, (-10.364, 14.552, -18.958)), (' B 125 CGLU  HG2', ' B 145 CTHR  HB ', -0.503, (-10.364, 14.552, -18.958)), (' B 145 CTHR HG23', ' E   1 CLIG  C10', -0.503, (-5.978, 14.074, -20.705)), (' B 145 DTHR HG23', ' E   1 DLIG  C10', -0.503, (-5.978, 14.074, -20.705)), (' A  54  ARG  HD3', ' A  60  ASP  OD1', -0.498, (-5.123, -14.021, -7.508)), (' C 132  MET  O  ', ' D 196 DARG  NH1', -0.486, (-32.432, 14.47, -51.748)), (' C 132  MET  O  ', ' D 196 BARG  NH1', -0.486, (-32.432, 14.47, -51.748)), (' A 200  TYR  OH ', ' B 206  HIS  HD2', -0.48, (-9.039, -1.575, -27.82)), (' B 301  EDO  H22', ' B 404  HOH  O  ', -0.48, (2.669, 23.398, -26.499)), (' D 189  GLU  O  ', ' D 191  LEU  HG ', -0.478, (-26.217, 2.298, -42.153)), (' A 206 AHIS  HD2', ' B 200  TYR  OH ', -0.472, (-5.573, 10.557, -22.773)), (' D  71  THR  O  ', ' D  73  HIS  ND1', -0.472, (-54.231, -4.374, -36.425)), (' A 206 BHIS  HD2', ' B 200  TYR  OH ', -0.472, (-5.573, 10.557, -22.773)), (' C  15  GLN  N  ', ' C 404  HOH  O  ', -0.472, (-21.084, -5.907, -52.642)), (' A 104  THR  CG2', ' A 107  ALA  H  ', -0.465, (-5.833, -19.751, -22.516)), (' A 191  LEU  C  ', ' A 191  LEU HD23', -0.459, (-23.354, 3.152, -13.517)), (' B  14  LYS  HE3', ' B  39  PRO  HB2', -0.454, (-33.914, -11.668, -11.695)), (' A 125  GLU  OE1', ' B 206  HIS  HE1', -0.453, (-4.505, -4.457, -29.2)), (' A  71  THR HG23', ' A 151  ASP  OD2', -0.452, (-18.672, -8.531, -42.365)), (' A 179  LEU HD23', ' A 205 ALYS  HD2', -0.446, (-14.603, 11.339, -24.355)), (' A 179  LEU HD23', ' A 205 BLYS  HD2', -0.446, (-14.552, 11.83, -24.593)), (' A 125  GLU  HG3', ' A 145  THR  HB ', -0.443, (-5.285, -7.5, -27.797)), (' A 206 DHIS  HD2', ' B 200  TYR  OH ', -0.442, (-6.142, 10.403, -22.893)), (' A  64  VAL  O  ', ' A  66  PRO  HD3', -0.441, (-13.708, -6.924, -23.216)), (' A 206 CHIS  HD2', ' B 200  TYR  OH ', -0.441, (-5.75, 10.217, -22.992)), (' D  16  TYR  OH ', ' D  37  MET  HE2', -0.44, (-31.092, 41.01, -68.673)), (' C 179  LEU HD11', ' C 198  TYR  CZ ', -0.439, (-47.763, 19.281, -50.132)), (' D 189  GLU  O  ', ' D 191  LEU  N  ', -0.432, (-24.698, 2.391, -42.363)), (' D  64  VAL  O  ', ' D  66 DPRO  HD3', -0.426, (-42.714, 6.268, -49.171)), (' A  65  ILE  HA ', ' A  66  PRO  HD3', -0.424, (-13.272, -5.67, -24.022)), (' D  64  VAL  O  ', ' D  66 CPRO  HD3', -0.423, (-42.638, 6.516, -49.512)), (' D 152  ASP  OD2', ' D 154  GLU  N  ', -0.42, (-54.625, -8.59, -50.233)), (' D  38  ASP  OD1', ' D  40  THR  N  ', -0.418, (-29.248, 42.632, -60.249)), (' A 203  ALA  HB2', ' B 200  TYR  CD1', -0.404, (-6.582, 6.32, -22.394)), (' D  67 DVAL  HA ', ' D  76  CYS  O  ', -0.403, (-46.427, 3.433, -43.46)), (' C  74  TYR  HB3', ' C 426  HOH  O  ', -0.401, (-48.797, 27.625, -35.351))]
gui = coot_molprobity_todo_list_gui(data=data)
