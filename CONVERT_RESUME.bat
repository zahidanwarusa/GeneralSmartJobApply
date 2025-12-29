@echo off
echo ================================================================================
echo                    RESUME TO JSON CONVERTER
echo ================================================================================
echo.
echo Choose your method:
echo.
echo 1. Paste resume in input_your_resume.txt (then press Enter)
echo 2. Convert PDF file
echo 3. Convert DOCX file
echo 4. Convert with job optimization
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto paste_method
if "%choice%"=="2" goto pdf_method
if "%choice%"=="3" goto docx_method
if "%choice%"=="4" goto optimize_method
if "%choice%"=="5" goto end

:paste_method
echo.
echo Opening input_your_resume.txt...
echo.
echo Instructions:
echo 1. Delete all template text
echo 2. Paste your complete resume
echo 3. Save and close the file (Ctrl+S, then close)
echo 4. Press any key here to continue...
echo.
notepad input_your_resume.txt
pause
echo.
echo Converting your resume...
python convert_my_resume.py
goto end

:pdf_method
echo.
set /p pdffile="Enter PDF file path: "
echo.
echo Converting %pdffile%...
python convert_my_resume.py --file "%pdffile%"
goto end

:docx_method
echo.
set /p docxfile="Enter DOCX file path: "
echo.
echo Converting %docxfile%...
python convert_my_resume.py --file "%docxfile%"
goto end

:optimize_method
echo.
set /p resumefile="Enter resume file path (PDF/DOCX/TXT or press Enter for input_your_resume.txt): "
set /p jobfile="Enter job JSON file path: "
echo.
if "%resumefile%"=="" (
    echo Converting and optimizing...
    python convert_my_resume.py --optimize --job-file "%jobfile%"
) else (
    echo Converting and optimizing %resumefile%...
    python convert_my_resume.py --file "%resumefile%" --optimize --job-file "%jobfile%"
)
goto end

:end
echo.
echo Done!
echo.
pause
