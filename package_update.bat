PowerShell -Command "Remove-Item -Recurse -Force dist"
python setup.py sdist bdist_wheel
twine upload dist/*
pip install --upgrade KdnTools[dev]
pip install --upgrade KdnTools