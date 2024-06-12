rm -rf build/ dist/ ../__pycache__/
rm MET\ Search.spec
pyinstaller --name "MET Search" --windowed metsearch.py
