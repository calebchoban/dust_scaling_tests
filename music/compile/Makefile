HPC ?= tscc

TEMP_DIR = temp
MUSIC_DIR = $(TEMP_DIR)/music
MUSIC_URL = https://bitbucket.org/ohahn/music/get/tip.tar.gz

.PHONY: compile
compile: bin/MUSIC

bin/MUSIC: | $(MUSIC_DIR)
	cp $(HPC)/Makefile $(MUSIC_DIR)
	source $(HPC)/module-reset.sh && cd $(MUSIC_DIR) && make
	mkdir -p bin
	mv $(MUSIC_DIR)/MUSIC $@
	ln -s $(PWD)/$@ ../run/MUSIC

$(MUSIC_DIR):
	mkdir -p $(TEMP_DIR)
	cd $(TEMP_DIR) && curl $(MUSIC_URL) | tar xz
	mv $(TEMP_DIR)/ohahn-music-* $@
