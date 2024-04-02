-- Delete indexes related to the entity descriptor field that has been removed.
DROP INDEX IF EXISTS idx_entity_descriptor_sample_label_trgm,
idx_entity_descriptor_subject_id_trgm,
idx_entity_descriptor_batch,
idx_entity_descriptor_group,
idx_entity_descriptor_disease_type_trgm,
idx_entity_descriptor_disease_status,
idx_entity_descriptor_io_drug,
idx_entity_descriptor_io_treatment,
idx_entity_descriptor_confirmed_bor,
idx_entity_descriptor_pfs_event,
idx_entity_descriptor_description_trgm,
idx_entity_descriptor_biosample_source_trgm,
idx_entity_descriptor_biosample_treatment_trgm,
idx_entity_descriptor__general__organ,
idx_entity_descriptor__general__biosample_source,
idx_entity_descriptor__disease_information__organ_part,
idx_entity_descriptor__disease_information__biopsy_site,
idx_entity_descriptor__pathological_information__organ_part,
idx_entity_descriptor__pathological_information__biopsy_site,
idx_entity_descriptor__general__biosample_treatment,
idx_entity_descriptor__treatment_type__drug,
idx_entity_descriptor__immuno_oncology_treatment_type__io_drug,
idx_entity_descriptor__response_and_survival_analysis__clinical_benefit,
idx_entity_descriptor__response_and_survival_analysis__confirmed_bor,
idx_entity_descriptor__response_and_survival_analysis__unconfirmed_bor,
idx_entity_descriptor__response_and_survival_analysis__pfs,
idx_entity_descriptor__response_and_survival_analysis__os,
idx_entity_descriptor__response_and_survival_analysis__dfs,
idx_entity_descriptor__response_and_survival_analysis__ttp;