
SETLOCAL
set "DEERROOT=C:\Users\nfette\source\repos\deer-dual-fuel-models"
REM set "mycmd=call modelkit rake --dry-run"
set "mycmd=call modelkit rake"

set mydirs=^
  SFm_Furnace_1975 ^
  SFm_Furnace_1985 ^
  "SFm_SEER Rated AC_HP_1975" ^
  "SFm_SEER Rated AC_HP_1985"

REM call :compose
call :run

ENDLOCAL
exit /b


:compose
REM Building the pxv and idf input files
for %%v in (%mydirs%) do (
  cd "%DEERROOT%\Analysis\%%~v"
  %mycmd% compose
  @echo on
)
exit /b

:run
for %%v in (%mydirs%) do (
  cd "%DEERROOT%\Analysis\%%~v"
  %mycmd% run
  @echo on
)
exit /b