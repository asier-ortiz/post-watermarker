run:
	export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$$DYLD_LIBRARY_PATH && \
	source .venv/bin/activate && \
	python add_logo.py
