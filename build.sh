# quip version $1
# quip clean --macfilesonly
python setup.py sdist bdist_wheel
pip uninstall maiden
pip install --upgrade --find-links=./dist/ --pre maiden
a=$PWD
cd ..
python -c "import maiden; print(maiden.__version__)"
cd $a