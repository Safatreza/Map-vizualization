@echo off
echo AboutWater Customer Data Processing
echo ===================================
echo.
echo Installing Python dependencies...
pip install -r requirements.txt
echo.
echo Processing customer data...
python improved_data_processor.py
echo.
echo Data processing complete!
echo.
echo Files created:
echo - customers_for_map.json (for the map)
echo - customer_summary_clean.csv (summary statistics)
echo.
echo Next: Open customer_map.html in your web browser
pause
