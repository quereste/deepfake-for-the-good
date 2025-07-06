@echo off
setlocal enabledelayedexpansion

REM Check if the target_folder argument is provided
if "%~1"=="" (
    echo Usage: %~nx0 target_folder
    goto :eof
)
set "TARGET_FOLDER=%~1"

REM Activate the environment
call conda activate torch_gpu_test

REM Define paths
set "BASE_DIR=%TARGET_FOLDER%\gs"
set "MODEL_PATH=%BASE_DIR%\gaussian_white"

REM Path to the source transforms_train_main.json (located one folder above target_folder)
set "TRAIN_MAIN_JSON=%TARGET_FOLDER%\..\transforms_train_main.json"

REM Path to the transforms_test.json file in the gs folder
set "TEST_JSON=%BASE_DIR%\transforms_test.json"

REM Check if files exist
if not exist "%TRAIN_MAIN_JSON%" (
    echo File not found: %TRAIN_MAIN_JSON%
    goto :eof
)

if not exist "%TEST_JSON%" (
    echo File not found: %TEST_JSON%
    goto :eof
)

REM Backup transforms_test.json
echo Backing up transforms_test.json...
copy "%TEST_JSON%" "%TEST_JSON%.bak" > nul

REM Navigate to the Gaussian Splatting directory
cd /d "C:\Users\jerzy\gaussian-splatting"

REM Run training
echo Running training...
python train.py -s "%BASE_DIR%" --eval --model_path "%MODEL_PATH%"

REM Check the return code after training
if errorlevel 1 (
    echo Training failed.
    goto :eof
)

REM Replace the contents of transforms_test.json with transforms_train_main.json
echo Replacing transforms_test.json with transforms_train_main.json...
copy /Y "%TRAIN_MAIN_JSON%" "%TEST_JSON%" > nul

REM Run rendering
echo Running rendering...
python render.py -s "%BASE_DIR%" --skip_train --model_path "%MODEL_PATH%"

REM Check the return code after rendering
if errorlevel 1 (
    echo Rendering failed. Restoring original transforms_test.json...
    move /Y "%TEST_JSON%.bak" "%TEST_JSON%" > nul
    goto :eof
)

REM Restore the original transforms_test.json
echo Restoring original transforms_test.json...
move /Y "%TEST_JSON%.bak" "%TEST_JSON%" > nul

echo Process completed successfully.
endlocal
