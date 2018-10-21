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
data['rama'] = [('A', '  66 ', 'PRO', 0.040219738580266326, (-14.181000000000001, -7.732999999999999, -27.137)), ('B', '  66 ', 'PRO', 0.09366275956334387, (-1.521, 13.870999999999999, -17.109)), ('B', '  66 ', 'PRO', 0.09366275956334387, (-1.521, 13.870999999999999, -17.109)), ('B', '  66 ', 'PRO', 0.033187295486402854, (-1.496, 13.868999999999998, -17.056)), ('B', '  66 ', 'PRO', 0.033187295486402854, (-1.496, 13.868999999999998, -17.056)), ('B', ' 161 ', 'LYS', 0.06232753741780106, (6.281, 17.345, -2.705)), ('C', '  66 ', 'PRO', 0.03163735963575535, (-36.039, 27.829999999999995, -38.19)), ('D', '  66 ', 'PRO', 0.059545846447471934, (-45.81999999999999, 4.611, -47.929)), ('D', '  66 ', 'PRO', 0.059545846447471934, (-45.81999999999999, 4.611, -47.929))]
data['omega'] = []
data['rota'] = [('A', '  14 ', 'LYS', 0.0, (15.503999999999994, -0.547, -2.248)), ('A', '  38 ', 'ASP', 0.283367279649806, (10.970999999999997, 1.8359999999999999, 3.210000000000001)), ('A', '  43 ', 'THR', 0.03837660686105795, (10.290999999999997, -0.5409999999999997, 8.788)), ('A', '  70 ', 'ARG', 0.03954961560277217, (-19.330999999999992, -6.899000000000001, -38.716)), ('A', ' 125 ', 'GLU', 0.08133516305769342, (-3.4559999999999995, -9.931999999999999, -27.842000000000002)), ('A', ' 191 ', 'LEU', 0.001013817196948723, (-24.947, 2.567, -12.336000000000002)), ('B', '  31 ', 'LEU', 0.058797044237679494, (-13.918999999999995, -7.04, 5.183)), ('B', '  38 ', 'ASP', 0.04385558536493549, (-30.304999999999993, -12.677, -6.405)), ('B', '  43 ', 'THR', 0.014015134186098704, (-30.689999999999987, -15.021999999999998, -0.879)), ('B', ' 188 ', 'GLU', 0.2029958651955593, (13.246999999999993, -5.105, -18.774)), ('B', ' 205 ', 'LYS', 0.014850762541779267, (-3.488999999999999, 1.7079999999999984, -30.229)), ('B', ' 208 ', 'ASN', 0.0, (-6.567999999999997, 2.9300000000000006, -35.127)), ('C', '  31 ', 'LEU', 0.003121932682432913, (-19.490000000000002, 14.741999999999999, -63.40500000000001)), ('C', '  45 ', 'THR', 0.19791756408088362, (-21.787999999999997, 1.546999999999997, -64.237)), ('C', ' 136 ', 'LEU', 0.23256867587035632, (-27.593, 11.319999999999993, -58.711)), ('C', ' 164 ', 'ASP', 0.0014628092914535382, (-23.206999999999994, 40.31100000000001, -52.92700000000001)), ('C', ' 189 ', 'GLU', 0.25440983565927583, (-47.11399999999999, 32.376999999999995, -58.603)), ('D', '  24 ', 'SER', 0.16280298855719344, (-20.787, 18.15299999999999, -70.978)), ('D', '  43 ', 'THR', 0.02920861224319588, (-25.091, 39.286999999999985, -65.686)), ('D', '  72 ', 'LEU', 0.037588813552274725, (-55.679999999999986, -2.3320000000000007, -33.901)), ('D', ' 196 ', 'ARG', 0.0, (-36.438, 13.959, -47.353)), ('D', ' 196 ', 'ARG', 0.0, (-36.438, 13.959, -47.353)), ('D', ' 208 ', 'ASN', 0.001883837187882967, (-46.576, 18.372999999999994, -31.245)), ('D', ' 208 ', 'ASN', 0.001883837187882967, (-46.576, 18.372999999999994, -31.245))]
data['cbeta'] = [('A', '  82 ', 'GLN', ' ', 0.3055339135979129, (-23.159, -8.014000000000003, -13.289000000000003)), ('D', '  52 ', 'THR', ' ', 0.28095925082892254, (-30.452999999999996, 13.900000000000002, -70.873)), ('D', '  74 ', 'TYR', ' ', 0.25032400196287075, (-48.15899999999999, 1.312999999999998, -34.302))]
data['probe'] = [(' D 196 DARG  CG ', ' D 196 DARG HH21', -1.293, (-36.511, 15.317, -50.171)), (' D 196 BARG  CG ', ' D 196 BARG HH21', -1.293, (-36.511, 15.317, -50.171)), (' D 196 DARG  HG3', ' D 196 DARG  NH2', -1.092, (-35.368, 15.921, -49.973)), (' D 196 BARG  HG3', ' D 196 BARG  NH2', -1.092, (-35.368, 15.921, -49.973)), (' C 176  ASN  HB3', ' F   3 DHOH  O  ', -0.903, (-49.444, 23.829, -36.172)), (' C 125  GLU  OE1', ' C 403  HOH  O  ', -0.781, (-35.477, 18.104, -33.344)), (' A  71  THR HG23', ' A 151  ASP  OD2', -0.765, (-18.77, -9.46, -42.19)), (' C 104  THR HG23', ' C 107  ALA  H  ', -0.76, (-20.935, 25.282, -36.377)), (' D 120  LYS  H  ', ' D 155  ASN HD21', -0.755, (-49.69, -4.245, -51.259)), (' D 196 DARG  N  ', ' D 196 DARG  NH2', -0.729, (-35.098, 14.224, -48.876)), (' D 196 BARG  N  ', ' D 196 BARG  NH2', -0.729, (-35.098, 14.224, -48.876)), (' B  92  ILE HD11', ' B 191  LEU HD13', -0.662, (7.745, 0.319, -15.138)), (' D 194  ASP  OD1', ' D 196 CARG  HD3', -0.646, (-34.794, 12.236, -50.146)), (' D 194  ASP  OD1', ' D 196 AARG  HD3', -0.643, (-34.571, 11.902, -49.813)), (' B 104  THR HG23', ' B 107  ALA  H  ', -0.64, (-10.925, 19.396, -7.248)), (' D 196 BARG  CG ', ' D 196 BARG  NH2', -0.636, (-35.491, 14.218, -49.005)), (' D 196 DARG  CG ', ' D 196 DARG  NH2', -0.636, (-35.491, 14.218, -49.005)), (' D 196 DARG  HG3', ' D 196 DARG HH21', -0.611, (-36.458, 15.776, -49.961)), (' D 196 BARG  HG3', ' D 196 BARG HH21', -0.611, (-36.458, 15.776, -49.961)), (' C 132  MET  HE1', ' C 196  ARG  CZ ', -0.595, (-32.373, 20.281, -50.25)), (' C 203  ALA  HB3', ' D 203  ALA  HB3', -0.59, (-42.654, 16.38, -41.067)), (' A 203  ALA  HB3', ' B 203  ALA  HB3', -0.585, (-7.672, 4.054, -25.13)), (' A 206 AHIS  HD2', ' B 200  TYR  OH ', -0.579, (-5.508, 10.579, -22.979)), (' A 206 BHIS  HD2', ' B 200  TYR  OH ', -0.579, (-5.508, 10.579, -22.979)), (' A 104  THR HG23', ' A 107  ALA  H  ', -0.572, (-5.806, -19.518, -22.27)), (' C 200  TYR  OH ', ' D 206  HIS  HD2', -0.568, (-39.39, 20.816, -37.547)), (' D 104  THR HG23', ' D 107  ALA  H  ', -0.56, (-50.129, 8.116, -62.354)), (' C 403  HOH  O  ', ' D 206  HIS  HE1', -0.554, (-36.239, 19.208, -33.696)), (' A 132  MET  HE1', ' A 196  ARG  CZ ', -0.542, (-10.597, -4.425, -13.625)), (' A 200  TYR  CD1', ' B 203  ALA  HB2', -0.54, (-9.304, 0.954, -25.163)), (' B 208  ASN  H  ', ' B 208  ASN HD22', -0.536, (-5.749, 3.671, -33.45)), (' C 203  ALA  HB2', ' D 200  TYR  CD1', -0.533, (-43.218, 13.689, -43.32)), (' B 125 DGLU  HG3', ' B 447  HOH  O  ', -0.532, (-13.052, 13.006, -18.916)), (' B 125 CGLU  HG3', ' B 447  HOH  O  ', -0.532, (-13.052, 13.006, -18.916)), (' D 196 BARG  H  ', ' D 196 BARG  NH2', -0.531, (-34.761, 13.803, -48.608)), (' D 196 DARG  H  ', ' D 196 DARG  NH2', -0.531, (-34.761, 13.803, -48.608)), (' D  71  THR  O  ', ' D  73  HIS  ND1', -0.521, (-54.234, -4.372, -36.433)), (' B 301  EDO  C2 ', ' B 404  HOH  O  ', -0.515, (2.262, 23.398, -26.381)), (' D 196 BARG  CB ', ' D 196 BARG  NH2', -0.511, (-36.112, 14.132, -49.061)), (' D 196 DARG  CB ', ' D 196 DARG  NH2', -0.511, (-36.112, 14.132, -49.061)), (' D 196 DARG  CB ', ' D 196 DARG HH21', -0.505, (-36.25, 14.385, -48.828)), (' D 196 BARG  CB ', ' D 196 BARG HH21', -0.505, (-36.25, 14.385, -48.828)), (' D 152  ASP  OD2', ' D 154  GLU  N  ', -0.503, (-55.0, -8.589, -50.443)), (' B 208  ASN  H  ', ' B 208  ASN  ND2', -0.495, (-5.402, 4.313, -33.492)), (' A  54  ARG  HD3', ' A  60  ASP  OD1', -0.493, (-5.112, -14.025, -7.449)), (' C  15  GLN  N  ', ' C 404  HOH  O  ', -0.485, (-21.068, -5.907, -52.649)), (' A 200  TYR  OH ', ' B 206  HIS  HD2', -0.483, (-9.02, -1.565, -27.816)), (' B 125 DGLU  HG2', ' B 145 DTHR  HB ', -0.476, (-9.86, 14.869, -18.964)), (' B 125 CGLU  HG2', ' B 145 CTHR  HB ', -0.476, (-9.86, 14.869, -18.964)), (' B 189  GLU  HB3', ' B 191  LEU HD12', -0.472, (9.984, -1.617, -14.814)), (' D 196 BARG  CA ', ' D 196 BARG  NH2', -0.47, (-35.62, 14.517, -48.735)), (' D 196 DARG  CA ', ' D 196 DARG  NH2', -0.47, (-35.62, 14.517, -48.735)), (' A 125  GLU  OE1', ' B 206  HIS  HE1', -0.466, (-5.008, -4.295, -29.151)), (' A 125  GLU  HG3', ' A 145  THR  HB ', -0.461, (-5.272, -7.5, -27.81)), (' B 194  ASP  OD2', ' B 196  ARG  NH2', -0.46, (-4.736, -0.122, -11.554)), (' D  38  ASP  OD1', ' D  40  THR  N  ', -0.459, (-29.605, 42.798, -59.953)), (' D 113  LEU HD22', ' D 146 DVAL HG11', -0.456, (-48.078, 2.881, -52.171)), (' D 113  LEU HD22', ' D 146 CVAL HG11', -0.456, (-47.573, 2.971, -52.069)), (' A 104  THR  CG2', ' A 107  ALA  H  ', -0.454, (-5.837, -19.748, -22.526)), (' D  16  TYR  OH ', ' D  37  MET  HE2', -0.45, (-31.107, 41.035, -68.661)), (' D 119  TYR  CD1', ' D 148 CILE HG21', -0.444, (-47.895, -3.074, -47.911)), (' D 119  TYR  CD1', ' D 148 DILE HG21', -0.444, (-47.895, -3.074, -47.911)), (' B  14  LYS  HE3', ' B  39  PRO  HB2', -0.444, (-33.403, -11.709, -11.75)), (' A 191  LEU  C  ', ' A 191  LEU HD23', -0.438, (-23.354, 3.137, -13.541)), (' B 301  EDO  H22', ' B 404  HOH  O  ', -0.438, (2.705, 23.456, -26.46)), (' C 179  LEU HD11', ' C 198  TYR  CZ ', -0.426, (-47.78, 19.289, -50.136)), (' C 132  MET  O  ', ' D 196 DARG  NH1', -0.422, (-32.413, 14.326, -51.228)), (' A  64  VAL  O  ', ' A  66  PRO  HD3', -0.42, (-13.705, -6.902, -23.227)), (' A  65  ILE  HA ', ' A  66  PRO  HD3', -0.417, (-13.269, -5.648, -24.033)), (' D  64  VAL  O  ', ' D  66 DPRO  HD3', -0.416, (-42.704, 6.244, -49.172)), (' A 203  ALA  HB2', ' B 200  TYR  CD1', -0.411, (-6.603, 6.315, -22.835)), (' D  68 DLEU  HA ', ' D 148 DILE  HB ', -0.409, (-49.311, 0.01, -45.707)), (' D  68 CLEU  HA ', ' D 148 CILE  HB ', -0.409, (-49.311, 0.01, -45.707)), (' D  38  ASP  HB2', ' D  39  PRO  CD ', -0.407, (-29.922, 39.798, -58.85)), (' D  64  VAL  O  ', ' D  66 CPRO  HD3', -0.405, (-42.62, 6.543, -49.464)), (' C 132  MET  O  ', ' D 196 BARG  NH1', -0.404, (-32.351, 14.645, -51.636))]
gui = coot_molprobity_todo_list_gui(data=data)
