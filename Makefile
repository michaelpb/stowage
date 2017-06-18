.PHONY: help clean clean-pyc clean-build list test test-all coverage release sdist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 stowage test

test:
	py.test

test-all:
	tox

coverage:
	coverage run --source stowage setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

build: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel

release: clean
	python3 setup.py sdist upload
	python3 setup.py bdist_wheel upload

sdist: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel upload
	ls -l dist
