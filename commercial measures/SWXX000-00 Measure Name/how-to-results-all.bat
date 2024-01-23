
SETLOCAL
set "DEERROOT=%~dp0"

REM set mydirs=^
REM   "SWXX000-00 Measure Name_1975" ^
REM   "SWXX000-00 Measure Name_1985" ^
REM   "SWXX000-00 Measure Name_1996" ^
REM   "SWXX000-00 Measure Name_2003" ^
REM   "SWXX000-00 Measure Name_2007" ^
REM   "SWXX000-00 Measure Name_2011" ^
REM   "SWXX000-00 Measure Name_2015" ^
REM   "SWXX000-00 Measure Name_2017" ^
REM   "SWXX000-00 Measure Name_2020" ^
REM   "SWXX000-00 Measure Name_2023" ^
REM   "SWXX000-00 Measure Name_Htl_1975" ^
REM   "SWXX000-00 Measure Name_Htl_1985" ^
REM   "SWXX000-00 Measure Name_Htl_1996" ^
REM   "SWXX000-00 Measure Name_Htl_2003" ^
REM   "SWXX000-00 Measure Name_Htl_2007" ^
REM   "SWXX000-00 Measure Name_Htl_2011" ^
REM   "SWXX000-00 Measure Name_Htl_2015" ^
REM   "SWXX000-00 Measure Name_Htl_2017" ^
REM   "SWXX000-00 Measure Name_Htl_2020"

set mydirs=^
  "SWXX000-00 Measure Name_Htl_1975" ^
  "SWXX000-00 Measure Name_Htl_1985" ^
  "SWXX000-00 Measure Name_Htl_1996" ^
  "SWXX000-00 Measure Name_Htl_2003" ^
  "SWXX000-00 Measure Name_Htl_2007" ^
  "SWXX000-00 Measure Name_Htl_2011" ^
  "SWXX000-00 Measure Name_Htl_2015" ^
  "SWXX000-00 Measure Name_Htl_2017" ^
  "SWXX000-00 Measure Name_Htl_2020"

call :readresult

ENDLOCAL
exit /b

:readresult
REM Building the pxv and idf input files
for %%v in (%mydirs%) do (
  python result.py -q query_com_benchmark.txt -d "%%~v.results-sizing-detail.csv" -a "%%~v.results-sizing-agg.csv" "%%~v"
)
exit /b
