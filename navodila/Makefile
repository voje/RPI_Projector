WKFLAGS = -B 25mm -T 25mm -L 25mm -R 25mm -q -s A4
%.pdf: %.html
	wkhtmltopdf $(WKFLAGS) $< $@

# PDFLAGS = --from=markdown_mmd+yaml_metadata_block+smart --standalone -s -V css=./air.css
PDFLAGS = --from=markdown_mmd+yaml_metadata_block --standalone -s -V css=./air.css
%.html: %.md
	pandoc $(PDFLAGS) $< > $@

all: clean convertall

MD_FILES=$(wildcard *.md)
PDF_FILES=$(MD_FILES:.md=.pdf)

convertall: $(PDF_FILES)

HTML_FILES=$(wildcard *.html)

clean: clean_pdf clean_html

clean_pdf:
	- rm -f ./*.pdf

clean_html:
	- rm -f ./*.html
