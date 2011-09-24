.PHONY: all clean

all: logs docs

clean:
	rm -f *.pyc
	rm -rf html
	rm -rf logs

logs:
	mkdir logs

docs:
	epydoc -v *.py
