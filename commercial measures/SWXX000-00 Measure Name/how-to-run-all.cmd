
SETLOCAL
set "DEERROOT=%~dp0"
REM set "mycmd=call modelkit rake --dry-run"
set "mycmd=call modelkit rake"

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

REM call :compose
call :run

ENDLOCAL
exit /b


:compose
REM Building the pxv and idf input files
for %%v in (%mydirs%) do (
  cd "%DEERROOT%\%%~v"
  %mycmd% compose
  @echo on
)
exit /b

:run
for %%v in (%mydirs%) do (
  cd "%DEERROOT%\%%~v"
  %mycmd% run
  @echo on
)
exit /b
