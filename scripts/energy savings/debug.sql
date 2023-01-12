SET search_path TO "MC_results_database";

--select * from current_msr_mat;
--select * from current_msr_mat where "NormUnit" is NULL;
--174 rows, all have NormUnit not null

--select * from sim_annual;
--select * from sim_annual where "normunit" is NULL;
--select * from sim_annual where "BldgHVAC" is NULL;
--select distinct "TechID", "SizingID", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC" from sim_annual;
--365 rows, all have normunit not null, all are distinct
--What's missing: failed sim runs (3), and DMo&0&rNCGF&New (16)

--select * from sfm_annual;
--select * from sfm_annual where "normunit" is NULL;
--select distinct "TechID", "SizingID", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC" from sfm_annual;
--192 rows, all have normunit not null, all are distinct

--365+192=557

--R1
--select * from sim_annual_twtd_2022;
--select * from sim_annual_twtd_2022 where "normunit" is NULL;
--SELECT distinct "TechID", "SizingID", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC" from sim_annual_twtd_2022;
--461 rows, all have normunit, all are distinct
--After fix NumStor for SFm&Ex, 557 rows, all have normunit, and all are distinct

--R3
select * from sim_annual_wtd;
--select * from sim_annual_wtd where "normunit" is NULL;
--461 rows, all have normunit
--SELECT distinct "TechID", "SizingID", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC" from sim_annual_wtd;
--... and all are unique

--R2
--select * from sim_hourly_twtd_2022;
--168265 rows, no normunit column
--SELECT distinct "TechID", "SizingID", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC" from sim_hourly_twtd_2022;
--461 unique combos excluding daynum
--R4
--select * from sim_hourly_wb_wtd;
--168265 rows, no normunit column
--SELECT distinct "TechID", "SizingID", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC" from sim_hourly_wb_wtd;
--461 unique combos excluding daynum

--P1
--select * from sim_peakper;
--461 rows
--SELECT distinct "TechID", "SizingID", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC"
--FROM sim_peakper;
--461 rows

--P2 creates meas_impacts_2022, but table is modified later
--select * from meas_impacts_2022;
--270 rows
--select distinct "EnergyImpactID", "PA", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC"
--from "meas_impacts_2022";
--270 rows
--select * from meas_impacts_2022 where "NormUnit" is NULL;
--48 rows

--P3 meas_impacts_hvactmp
--select * from meas_impacts_hvactmp;
--174 rows
--select * from meas_impacts_hvactmp where "NormUnit" is NULL;
--32 rows

--P4 meas_impacts_hvacwtd
--select * from meas_impacts_hvactmp;

--select * from meas_impacts_tmp3_2022;
--select distinct "EnergyImpactID", "PA", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC" from meas_impacts_tmp3_2022;

--select * from meas_impacts_wtd_2022;
--414 rows
--select distinct "EnergyImpactID", "PA", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC" from meas_impacts_wtd_2022;
--366 rows
--select * from meas_impacts_wtd_2022 where "NormUnit" is NULL;
--96 rows
--select distinct "EnergyImpactID", "PA", "BldgType", "BldgVint", "BldgLoc", "BldgHVAC" from meas_impacts_wtd_2022 where "NormUnit" is not NULL;
--318 rows
