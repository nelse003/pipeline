from rest_framework import serializers

from xchem_db.models import Target, Compounds, Reference, SoakdbFiles, Crystal, DataProcessing, Dimple, Lab, \
    Refinement, PanddaAnalysis, PanddaRun, PanddaSite, PanddaEvent, ProasisOut, Proposals, PanddaEventStats


class ProposalsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposals
        fields = ("proposal", "title", "fedids",)


class TargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Target
        fields = ("target_name",)


class CompoundsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Compounds
        fields = ("smiles",)


class ReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reference
        fields = ("reference_pdb",)


class SoakdbFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoakdbFiles
        fields = (
            "filename",
            "modification_date",
            "proposal",
            "visit",
            "status",
        )


class CrystalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crystal
        fields = (
            "crystal_name",
            "target",
            "compound",
            "visit",
            "status",
        )


class DataProcessingSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataProcessing
        fields = (
            "cchalf_high",
            "cchalf_low",
            "cchalf_overall",
            "completeness_high",
            "completeness_low",
            "completeness_overall",
            "crystal_name",
            "isig_high",
            "isig_low",
            "isig_overall",
            "lattice",
            "multiplicity_high",
            "multiplicity_low",
            "multiplicity_overall",
            "point_group",
            "program",
            "r_cryst",
            "r_free",
            "r_merge_high",
            "r_merge_low",
            "r_merge_overall",
            "res_high",
            "res_high_15_sigma",
            "res_high_outer_shell",
            "res_low",
            "res_low_inner_shell",
            "res_overall",
            "score",
            "spacegroup",
            "unique_ref_overall",
            "unit_cell",
            "unit_cell_vol",
        )


class DimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dimple
        fields = (
            "crystal_name",
            "r_free",
            "res_high",
            "reference",
        )


class LabSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lab
        fields = (
            "cryo_frac",
            "cryo_status",
            "cryo_stock_frac",
            "cryo_transfer_vol",
            "crystal_name",
            "data_collection_visit",
            "expr_conc",
            "harvest_status",
            "library_name",
            "library_plate",
            "mounting_result",
            "mounting_time",
            "soak_status",
            "soak_time",
            "soak_vol",
            "solv_frac",
            "stock_conc",
            "visit",

        )


class RefinementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Refinement
        fields = (
            "bound_conf",
            "cif",
            "cif_prog",
            "cif_status",
            "crystal_name",
            "lig_bound_conf",
            "lig_cc",
            "lig_confidence",
            "matrix_weight",
            "molprobity_score",
            "mtz_free",
            "mtz_latest",
            "outcome",
            "pdb_latest",
            "r_free",
            "ramachandran_favoured",
            "ramachandran_outliers",
            "rcryst",
            "refinement_path",
            "res",
            "rmsd_angles",
            "rmsd_bonds",
            "spacegroup",
        )


class PanddaAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = PanddaAnalysis
        fields = (
            "pandda_dir",
        )


class PanddaRunSerializer(serializers.ModelSerializer):

    class Meta:
        model = PanddaRun
        fields = (
            "input_dir",
            "pandda_analysis",
            "pandda_log",
            "pandda_version",
            "sites_file",
            "events_file",
        )


class PanddaSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PanddaSite
        fields = (
            "pandda_run",
            "site",
            "site_aligned_centroid_x",
            "site_aligned_centroid_y",
            "site_aligned_centroid_z",
            "site_native_centroid_x",
            "site_native_centroid_y",
            "site_native_centroid_z",
        )


class PanddaEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = PanddaEvent
        fields = (
            "crystal",
            "site",
            "pandda_run",
            "event",
            "event_centroid_x",
            "event_centroid_y",
            "event_centroid_z",
            "event_dist_from_site_centroid",
            "lig_centroid_x",
            "lig_centroid_y",
            "lig_centroid_z",
            "lig_dist_event",
            "lig_id",
            "pandda_event_map_native",
            "pandda_event_map_cut"
            "pandda_model_pdb",
            "pandda_input_mtz",
            "pandda_input_pdb",
            "ligand_confidence_inspect",
            "ligand_confidence",
        )


class ProasisOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProasisOut
        fields = (
            "crystal",
            "proasis",
            "ligand",
            "ligid",
            "root",
            "start",
            "curated",
            "sdf",
            "apo",
            "mol",
            "mol2",
            "h_mol",
            "stripped",
            "event",
            "mtz",
            "contacts",
            "acc",
            "don",
            "lip",
            "pmap",
            "ppdb",
            "pjson",
            "pmtz",
        )


class PanddaEventStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PanddaEventStats
        fields = (
            'event',
            'one_minus_bdc',
            'cluster_size',
            'glob_corr_av_map',
            'glob_corr_mean_map',
            'loc_corr_av_map',
            'loc_corr_mean_map',
            'z_mean',
            'z_peak',
            'b_factor_scaled',
            'high_res',
            'low_res',
            'r_free',
            'r_work',
            'ref_rmsd',
            'wilson_scaled_b',
            'wilson_scaled_ln_dev',
            'wilson_scaled_ln_dev_z',
            'wilson_scaled_ln_rmsd',
            'wilson_scaled_ln_rmsd_z',
            'wilson_scaled_below_four_rmsd',
            'wilson_scaled_below_four_rmsd_z',
            'wilson_scaled_above_four_rmsd',
            'wilson_scaled_above_four_rmsd_z',
            'wilson_scaled_rmsd_all',
            'wilson_scaled_rmsd_all_z',
            'wilson_unscaled',
            'wilson_unscaled_ln_dev',
            'wilson_unscaled_ln_dev_z',
            'wilson_unscaled_ln_rmsd',
            'wilson_unscaled_ln_rmsd_z',
            'wilson_unscaled_below_four_rmsd',
            'wilson_unscaled_below_four_rmsd_z',
            'wilson_unscaled_above_four_rmsd',
            'wilson_unscaled_above_four_rmsd_z',
            'wilson_unscaled_rmsd_all',
            'wilson_unscaled_rmsd_all_z',
            'resolution',
            'map_uncertainty',
            'obs_map_mean',
            'obs_map_rms',
            'z_map_kurt',
            'z_map_mean',
            'z_map_skew',
            'z_map_std',
            'scl_map_mean',
            'scl_map_rms',
        )


class FragspectEventView(serializers.ModelSerializer):
    class Meta:
        model = PanddaEvent
        fields = (
            'crystal',
            'site',
            'event',
            'lig_id',
            'ligand_confidence_inspect',
            'ligand_confidence',
        )


class FragspectCrystalSerializer(serializers.ModelSerializer):

    # refinement = RefinementSerializer(read_only=True, source='crystal_name')
    # data_proc = DataProcessingSerializer(read_only=True, source='crystal_name')

    crystal = serializers.SerializerMethodField()
    site_number = serializers.SerializerMethodField()
    event_number = serializers.SerializerMethodField()
    # code = serializers.SerializerMethodField()
    # lig_id = serializers.SerializerMethodField()
    target_name = serializers.SerializerMethodField()
    event_map_info = serializers.SerializerMethodField()
    # sigmaa_map_info = serializers.SerializerMethodField()
    # spider_plot_info = serializers.SerializerMethodField()
    # two_d_density_map = serializers.SerializerMethodField()
    crystal_status = serializers.SerializerMethodField()
    # event_status = serializers.SerializerMethodField()
    confidence = serializers.SerializerMethodField()
    crystal_resolution = serializers.SerializerMethodField()
    smiles = serializers.SerializerMethodField()
    spacegroup = serializers.SerializerMethodField()
    cell = serializers.SerializerMethodField()
    # cell_angles = serializers.SerializerMethodField()
    event_comment = serializers.SerializerMethodField()
    # interesting = serializers.SerializerMethodField()

    def get_crystal(self, obj):
        return obj.crystal.crystal_name

    def get_site_number(self, obj):
        return obj.site.site

    def get_event_number(self, obj):
        return obj.event

    # def get_code(self, obj):
    #     return None

    def get_target_name(self, obj):
        return obj.crystal.target.target_name

    def get_event_map_info(self, obj):
        return obj.pandda_event_map_native

    # def get_sigmaa_map_info(self, obj):
    #     return None
    #
    # def get_spider_plot_info(self, obj):
    #     return None
    #
    # def get_two_d_density_map(self, obj):
    #     return None

    def get_crystal_status(self, obj):
        try:
            refinement = Refinement.objects.get(crystal_name=obj.crystal)
            return refinement.outcome
        except:
            return 'unknown'

    # def get_event_status(self, obj):
    #     return obj.

    def get_confidence(self, obj):
        return obj.ligand_confidence

    def get_crystal_resolution(self, obj):
        try:
            refinement = Refinement.objects.get(crystal_name=obj.crystal)
            return refinement.res
        except:
            return 'unknown'

    def get_smiles(self, obj):
        return obj.crystal.compound.smiles

    def get_spacegroup(self, obj):
        try:
            refinement = Refinement.objects.get(crystal_name=obj.crystal)
            return refinement.spacegroup
        except:
            return 'unknown'

    def get_cell(self, obj):
        try:
            dataproc = DataProcessing.objects.get(crystal_name=obj.crystal)
            return dataproc.unit_cell
        except:
            return 'unknown'


    # def get_cell_angles(self, obj):
    #     return None

    def get_event_comment(self, obj):
        return obj.comment
    #
    # def get_interesting(self, obj):
    #     return None

    class Meta:
        model = PanddaEvent
        fields = (
            'crystal',
            'site_number',
            'event_number',
            # 'code',
            'lig_id',
            'target_name',
            'event_map_info',
            # 'sigmaa_map_info',
            # 'spider_plot_info',
            # 'two_d_density_map',
            'crystal_status',
            # 'event_status',
            'confidence',
            'crystal_resolution',
            'smiles',
            'spacegroup',
            'cell',
            # 'cell_angles',
            # 'event_comment'
            # 'interesting',
        )
