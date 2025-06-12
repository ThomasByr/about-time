.PHONY: test format lint help batch clean

test:
	uvx pytest

format:
	uvx ruff format
	uvx ruff check --select I --fix

lint:
	uvx ruff check

help:
    # github main branch includes pull#74 which is not on pypi yet
	uvx --from git+https://github.com/Textualize/rich-cli rich README.md 

batch:
	uvx make-to-batch -i makefile -o make.bat
	@sed -i 's/-r \/F/\/S \/F/' make.bat
	@sed -i '/@sed/d' make.bat

build:
	uv build

clean:
	rm -r -f dist
