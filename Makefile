.PHONY: all clean

all: dist/server docs

clean:
	rm -f *.pyc
	rm -rf html
	rm -rf logs
	rm -rf dist
	rm -rf dist/logs

dist/server: server.py
	cxfreeze server.py

docs:
	epydoc --graph classtree -v *.py
