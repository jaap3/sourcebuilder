.PHONY : help init tests\
         coverage checkstyle readme\
         clean fullclean

FILES       = build dist *.egg-info checkstyle.txt pylint.html README.html htmlcov/ .coverage
OTHER_FILES = .installed.cfg .tox bin develop-eggs eggs parts unittest2-*

help:
	@echo "make init:"
	@echo "  runs bootstrap.py && bin/buildout."
	@echo
	@echo "make tests:"
	@echo "  runs the tests (use bin/tox for tox)"
	@echo "make coverage:"
	@echo "  reports test coverage"
	@echo
	@echo "make checkstyle"
	@echo "  generates pep8, pyflakes and pylint reports"
	@echo "make readme:"
	@echo "  converts README to html and opens it in"
	@echo "  a browser"
	@echo
	@echo "make clean:"
	@echo "  removes build/dist files."
	@echo "make fullclean:"
	@echo "  removes all build/dist/mbuildout/tox files."

init:
	@echo "Running buildout, this will take a while..."
	python bootstrap.py && bin/buildout
	@echo "Done!"

tests:
	bin/python setup.py test

coverage:
	bin/coverage run setup.py test
	bin/coverage html
	python -m webbrowser -t file://$(PWD)/htmlcov/index.html

checkstyle:
	echo 'pep8' > checkstyle.txt
	-bin/pep8 -r --show-source --show-pep8 --count --statistics sourcebuilder >> checkstyle.txt
	echo '' >> checkstyle.txt
	echo 'pyflakes' >> checkstyle.txt
	echo '' >> checkstyle.txt
	-bin/pyflakes sourcebuilder >> checkstyle.txt
	-bin/pylint -f html > pylint.html
	python -m webbrowser -t file://$(PWD)/checkstyle.txt
	python -m webbrowser -t file://$(PWD)/pylint.html

readme:
	bin/rst2 html README.rst > README.html
	python -m webbrowser -t file://$(PWD)/README.html

clean:
	@echo "Removing files..."
	-rm -rf $(FILES)
	@echo "Done!"

fullclean: override FILES += $(OTHER_FILES)
fullclean: clean
