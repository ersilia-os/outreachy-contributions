SHELL=/bin/bash

.PHONY: install-packages load-tdc-data  featurize-data all

install-packages:
	pip install pytdc git+https://github.com/ersilia-os/compound-embedding-lite.git

load-tdc-data:
	(cd scripts && python load_data.py)

featurize-data:
	(cd scripts && python featurize_data.py)

all: install-packages load-tdc-data featurize-data