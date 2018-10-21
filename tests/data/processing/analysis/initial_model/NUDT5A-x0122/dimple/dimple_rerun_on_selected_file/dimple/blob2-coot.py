#!/usr/bin/env coot
# python script for coot - generated by dimple
set_nomenclature_errors_on_read("ignore")
molecule = read_pdb("/dls/labxchem/data/2018/lb18145-71/processing/analysis/initial_model/NUDT5A-x0122/dimple/dimple_rerun_on_selected_file/dimple/final.pdb")
set_rotation_centre(-10.62, -9.51, -11.24)
set_zoom(30.)
set_view_quaternion(0.334988, 0.203087, 0, 0.920075)
mtz = "/dls/labxchem/data/2018/lb18145-71/processing/analysis/initial_model/NUDT5A-x0122/dimple/dimple_rerun_on_selected_file/dimple/final.mtz"
map21 = make_and_draw_map(mtz, "FWT", "PHWT", "", 0, 0)
map11 = make_and_draw_map(mtz, "DELFWT", "PHDELWT", "", 0, 1)
