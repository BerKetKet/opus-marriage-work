# Scripts (copy them to `/home/bgg/projects/opus_marriage_work/tools_manager/`)

Capture one Kindle state (screenshot + layout XML + index row; warns if the screen did not change):
```
python3 tools_manager/survey_capture.py K012 "Aa sheet, Theme tab" --path "open book > tap centre > tap Aa" --out specs/kindle_survey
```
Same screen with layout bounds on (second image, same id plus suffix):
```
python3 tools_manager/survey_capture.py K012 "Aa sheet, Theme tab" --suffix _bounds --no-xml --out specs/kindle_survey
```
Wireframe plus element table (px and dp) from a captured XML:
```
python3 tools_manager/xml_to_wireframe.py specs/kindle_survey/xml/K012.xml specs/kindle_survey/wireframes/K012
```
Build the report zip (refuses duplicates, missing descriptions, forbidden files, forbidden strings):
```
python3 tools_manager/make_report.py --n 002 --staging deliverables/report_002 --forbid YOUR_DEVICE_SERIAL
```
If `uiautomator dump` fails on a screen (the app may block it), capture the screenshot anyway with `--no-xml` and measure bounds from the screenshot; say so in `interactions.md`.
