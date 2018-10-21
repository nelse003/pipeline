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
data['rama'] = [('A', '  66 ', 'PRO', 0.046368638112274076, (-14.085999999999999, -7.741999999999999, -27.049)), ('A', ' 189 ', 'GLU', 0.011903347691063342, (-29.92, 5.164, -14.336999999999998)), ('A', ' 189 ', 'GLU', 0.011903347691063342, (-29.92, 5.164, -14.336999999999998)), ('A', ' 190 ', 'HIS', 0.02039193984067091, (-27.537999999999997, 5.088999999999999, -11.318)), ('A', ' 190 ', 'HIS', 0.02039193984067091, (-27.537999999999997, 5.088999999999999, -11.318)), ('B', '  66 ', 'PRO', 0.06349830088261102, (-1.3840000000000012, 13.997, -17.123)), ('C', '  53 ', 'THR', 0.038713364735454246, (-13.029000000000005, 18.258999999999993, -52.833999999999996)), ('C', '  53 ', 'THR', 0.039034513314741, (-13.024000000000001, 18.258999999999993, -52.833999999999996)), ('C', '  66 ', 'PRO', 0.04096366323014981, (-35.852, 27.824000000000005, -38.25399999999999))]
data['omega'] = [('B', ' 208 ', 'ASN', None, (-7.022, 3.569000000000001, -33.976)), ('D', ' 208 ', 'ASN', None, (-45.67900000000001, 18.327999999999996, -32.833)), ('D', ' 208 ', 'ASN', None, (-45.67900000000001, 18.327999999999996, -32.833))]
data['rota'] = [('A', '  14 ', 'LYS', 0.03461248063836893, (15.531, -0.501, -2.441)), ('A', '  38 ', 'ASP', 0.10898164074343979, (11.073, 1.966, 3.11)), ('A', '  54 ', 'ARG', 0.29079569140683614, (-4.863999999999999, -18.253, -6.132)), ('A', '  54 ', 'ARG', 0.29079569140683614, (-4.863999999999999, -18.253, -6.132)), ('A', '  70 ', 'ARG', 0.01942827344098466, (-19.217, -6.9060000000000015, -38.743)), ('A', ' 191 ', 'LEU', 0.0003661821983993503, (-24.922999999999995, 2.595999999999999, -12.457999999999998)), ('A', ' 191 ', 'LEU', 0.0003661821983993503, (-24.922999999999995, 2.595999999999999, -12.457999999999998)), ('A', ' 191 ', 'LEU', 0.00050476494986306, (-24.929, 2.6080000000000005, -12.475)), ('A', ' 191 ', 'LEU', 0.00050476494986306, (-24.929, 2.6080000000000005, -12.475)), ('B', '  31 ', 'LEU', 0.0876408178233369, (-13.749999999999998, -6.893, 5.264)), ('B', '  38 ', 'ASP', 0.2761723559683721, (-30.192, -12.577000000000002, -6.464)), ('B', '  43 ', 'THR', 0.12710978293404113, (-30.398999999999997, -14.991000000000001, -0.813)), ('C', '  29 ', 'VAL', 0.1324199191898509, (-19.107999999999997, 20.788, -59.909)), ('C', '  35 ', 'THR', 0.061958584832823446, (-18.049000000000007, 1.4659999999999958, -61.953)), ('C', '  71 ', 'THR', 0.0013599335943581536, (-45.48, 33.966999999999985, -26.669999999999995)), ('C', ' 136 ', 'LEU', 0.027539859575267035, (-27.043999999999997, 11.431000000000001, -58.509999999999984)), ('C', ' 136 ', 'LEU', 0.027018551985618006, (-27.04500000000001, 11.430999999999992, -58.510999999999996)), ('C', ' 189 ', 'GLU', 0.16175302588524554, (-46.84400000000001, 32.30499999999999, -58.56399999999999)), ('D', '  23 ', 'ILE', 0.1399328995386961, (-20.356, 21.808999999999997, -71.074)), ('D', '  45 ', 'THR', 0.1344099140361442, (-23.025, 32.593, -64.022)), ('D', '  72 ', 'LEU', 0.0006653269203468928, (-55.49199999999999, -2.248000000000001, -33.922)), ('D', ' 208 ', 'ASN', 0.03007472088344335, (-46.425999999999995, 18.339, -31.36)), ('D', ' 208 ', 'ASN', 0.03007472088344335, (-46.425999999999995, 18.339, -31.36))]
data['cbeta'] = [('A', '  82 ', 'GLN', ' ', 0.26238629972465544, (-22.761, -7.773, -13.264)), ('C', ' 190 ', 'HIS', ' ', 0.2528129480075813, (-44.072999999999986, 29.855, -61.994)), ('D', '  52 ', 'THR', ' ', 0.2543051641513241, (-30.351999999999997, 13.607999999999995, -71.219))]
data['probe'] = [(' C 125  GLU  OE1', ' C 403  HOH  O  ', -0.867, (-35.343, 18.028, -33.42)), (' B  92  ILE HD11', ' B 191  LEU HD13', -0.85, (7.928, 0.343, -15.417)), (' D 120  LYS  H  ', ' D 155  ASN HD21', -0.821, (-49.646, -4.459, -51.434)), (' A 104  THR HG23', ' A 107  ALA  H  ', -0.775, (-5.552, -19.39, -22.568)), (' C 203  ALA  HB3', ' D 203  ALA  HB3', -0.728, (-42.177, 16.329, -41.294)), (' B 301  EDO  H22', ' B 404  HOH  O  ', -0.725, (2.664, 23.468, -26.821)), (' B 301  EDO  C2 ', ' B 404  HOH  O  ', -0.682, (3.099, 23.315, -26.109)), (' B 196 DARG  NH2', ' F   8 DHOH  O  ', -0.672, (-3.352, 2.292, -10.137)), (' B 196 CARG  NH2', ' F   8 CHOH  O  ', -0.672, (-3.352, 2.292, -10.137)), (' A 191 DLEU  C  ', ' A 191 DLEU HD23', -0.669, (-23.316, 2.735, -13.494)), (' A 191 CLEU  C  ', ' A 191 CLEU HD23', -0.669, (-23.316, 2.735, -13.494)), (' A 191 ALEU  C  ', ' A 191 ALEU HD23', -0.656, (-23.309, 2.726, -13.497)), (' A 191 BLEU  C  ', ' A 191 BLEU HD23', -0.656, (-23.309, 2.726, -13.497)), (' A 203  ALA  HB3', ' B 203  ALA  HB3', -0.627, (-8.056, 4.552, -24.925)), (' C 179  LEU HD11', ' C 198  TYR  CZ ', -0.623, (-47.699, 19.243, -50.177)), (' C 104  THR HG23', ' C 107  ALA  H  ', -0.608, (-20.877, 25.278, -35.944)), (' D 205  LYS  O  ', ' D 208 BASN  HB2', -0.597, (-43.146, 17.037, -32.357)), (' D 205  LYS  O  ', ' D 208 AASN  HB2', -0.597, (-43.146, 17.037, -32.357)), (' A 189 BGLU  O  ', ' A 190 BHIS  CB ', -0.583, (-29.614, 4.912, -12.332)), (' A 189 AGLU  O  ', ' A 190 AHIS  CB ', -0.583, (-29.614, 4.912, -12.332)), (' C 403  HOH  O  ', ' D 206  HIS  HE1', -0.577, (-36.136, 18.68, -33.586)), (' B 104  THR HG23', ' B 107  ALA  H  ', -0.572, (-11.271, 19.602, -7.573)), (' A 200  TYR  CD1', ' B 203  ALA  HB2', -0.569, (-9.162, 1.399, -25.294)), (' A 179  LEU HD23', ' A 205  LYS  HD2', -0.558, (-14.435, 11.566, -24.897)), (' C 200  TYR  CD1', ' D 203  ALA  HB2', -0.551, (-40.834, 18.211, -40.872)), (' A  71  THR HG23', ' A 151  ASP  OD2', -0.541, (-18.616, -9.284, -42.234)), (' A 125  GLU  OE1', ' B 206  HIS  HE1', -0.54, (-4.504, -4.47, -29.496)), (' C 132  MET  O  ', ' D 196 DARG  NH1', -0.532, (-32.307, 14.428, -51.327)), (' A 191 DLEU  C  ', ' A 191 DLEU  CD2', -0.53, (-23.648, 3.025, -14.074)), (' A 191 CLEU  C  ', ' A 191 CLEU  CD2', -0.53, (-23.648, 3.025, -14.074)), (' A 191 BLEU  C  ', ' A 191 BLEU  CD2', -0.529, (-23.649, 3.022, -14.066)), (' A 191 ALEU  C  ', ' A 191 ALEU  CD2', -0.529, (-23.649, 3.022, -14.066)), (' C 132  MET  O  ', ' D 196 BARG  NH1', -0.528, (-32.133, 14.7, -51.724)), (' A 206  HIS  HE1', ' B 125  GLU  OE1', -0.528, (-10.77, 13.692, -22.587)), (' B 301  EDO  H21', ' F  31 DHOH  O  ', -0.525, (2.673, 25.84, -25.473)), (' C 200  TYR  OH ', ' D 206  HIS  HD2', -0.522, (-39.364, 20.569, -37.523)), (' D 152  ASP  OD2', ' D 154  GLU  N  ', -0.521, (-54.333, -8.532, -50.433)), (' B  60 AASP  OD2', ' B 139 ACYS  HA ', -0.509, (-13.716, 3.249, -3.512)), (' B  60 BASP  OD2', ' B 139 BCYS  HA ', -0.509, (-13.716, 3.249, -3.512)), (' B  62 CVAL HG12', ' B 142  HIS  HB2', -0.499, (-11.532, 12.05, -9.495)), (' B  62 DVAL HG12', ' B 142  HIS  HB2', -0.499, (-11.532, 12.05, -9.495)), (' C 125  GLU  HG2', ' C 402  HOH  O  ', -0.499, (-31.322, 16.826, -34.923)), (' A 189 CGLU  O  ', ' A 190 CHIS  C  ', -0.49, (-27.658, 3.728, -12.539)), (' A 189 DGLU  O  ', ' A 190 DHIS  C  ', -0.49, (-27.658, 3.728, -12.539)), (' A 132  MET  O  ', ' B 196 BARG  NH2', -0.487, (-6.542, -0.99, -10.828)), (' C 206  HIS  HE1', ' D 125  GLU  OE1', -0.483, (-50.679, 13.57, -46.778)), (' A 132  MET  O  ', ' B 196 AARG  NH2', -0.48, (-6.654, -1.333, -10.516)), (' B  62 DVAL  HA ', ' B 142  HIS  O  ', -0.474, (-9.867, 10.015, -9.539)), (' A 206  HIS  HD2', ' B 200  TYR  OH ', -0.473, (-5.619, 10.638, -22.816)), (' C  84  ARG  HG3', ' D 134 BPRO  HB2', -0.472, (-33.118, 26.526, -56.379)), (' C  84  ARG  HG3', ' D 134 APRO  HB2', -0.471, (-33.36, 26.973, -56.265)), (' C 191  LEU  C  ', ' C 191  LEU HD12', -0.465, (-42.979, 27.718, -56.003)), (' B  62 CVAL  HA ', ' B 142  HIS  O  ', -0.465, (-9.886, 10.32, -9.995)), (' B 301  EDO  C2 ', ' F  31 DHOH  O  ', -0.461, (2.837, 25.663, -25.567)), (' C 203  ALA  HB2', ' D 200  TYR  CD1', -0.457, (-42.847, 13.595, -43.182)), (' C 206  HIS  HD2', ' D 200  TYR  OH ', -0.456, (-46.18, 11.416, -43.773)), (' A 203  ALA  HB2', ' B 200  TYR  CD1', -0.451, (-6.353, 6.557, -22.589)), (' A  49  VAL HG21', ' B  49 AVAL HG11', -0.441, (-9.319, -5.284, 0.924)), (' A  49  VAL HG21', ' B  49 BVAL HG11', -0.441, (-9.319, -5.284, 0.924)), (' C 165  GLY  HA2', ' C 167  PHE  CE1', -0.437, (-26.278, 38.921, -56.015)), (' D  71  THR  O  ', ' D  73 DHIS  ND1', -0.435, (-54.055, -4.332, -36.45)), (' A  70  ARG  HD3', ' A 409  HOH  O  ', -0.434, (-20.536, -4.758, -35.613)), (' C  62  VAL HG12', ' C 142 CHIS  HB2', -0.433, (-25.327, 21.107, -41.38)), (' C  62  VAL HG12', ' C 142 DHIS  HB2', -0.432, (-25.326, 21.106, -41.38)), (' B  51 CARG  NH2', ' B  98  LEU HD21', -0.43, (-7.837, 5.595, -0.446)), (' B  51 DARG  NH2', ' B  98  LEU HD21', -0.43, (-7.837, 5.595, -0.446)), (' A  33 CLYS  HE3', ' A  45  THR HG21', -0.427, (2.746, -3.342, 10.866)), (' A  33 DLYS  HE3', ' A  45  THR HG21', -0.427, (2.746, -3.342, 10.866)), (' C 132  MET  HE1', ' C 196  ARG  CZ ', -0.425, (-31.829, 20.15, -50.116)), (' A 132  MET  HE1', ' A 196  ARG  CZ ', -0.423, (-10.666, -4.063, -13.318)), (' D 206  HIS  O  ', ' D 208 AASN  C  ', -0.423, (-44.11, 20.331, -32.893)), (' D 206  HIS  O  ', ' D 208 BASN  C  ', -0.423, (-44.11, 20.331, -32.893)), (' D 208 AASN  ND2', ' D 415  HOH  O  ', -0.422, (-45.743, 14.42, -29.828)), (' D 208 BASN  ND2', ' D 415  HOH  O  ', -0.422, (-45.743, 14.42, -29.828)), (' A  71  THR  O  ', ' A  73  HIS  HD2', -0.421, (-22.239, -4.651, -40.963)), (' A 104  THR  CG2', ' A 107  ALA  H  ', -0.419, (-5.802, -19.844, -22.588)), (' D 132 AMET  HE1', ' D 196 AARG  HD2', -0.416, (-34.58, 14.416, -52.086)), (' B 189  GLU  OE2', ' B 191  LEU HD11', -0.41, (10.898, 0.578, -14.144)), (' A 200  TYR  OH ', ' B 206  HIS  HD2', -0.409, (-9.427, -1.623, -27.861)), (' D  17  ILE HD12', ' D  34  THR  CG2', -0.408, (-29.615, 30.113, -66.193)), (' A  58 BTHR  OG1', ' A 142  HIS  NE2', -0.408, (-1.589, -14.599, -16.543)), (' A  58 ATHR  OG1', ' A 142  HIS  NE2', -0.408, (-1.589, -14.599, -16.543)), (' A  38  ASP  C  ', ' A  38  ASP  OD1', -0.405, (12.418, 3.139, 3.49)), (' A 188 CGLU  C  ', ' A 189 CGLU  HG2', -0.403, (-29.852, 5.235, -16.732)), (' C 200  TYR  OH ', ' D 206  HIS  CD2', -0.403, (-39.583, 20.77, -37.103)), (' A 188 DGLU  C  ', ' A 189 DGLU  HG2', -0.403, (-29.852, 5.235, -16.732))]
gui = coot_molprobity_todo_list_gui(data=data)
