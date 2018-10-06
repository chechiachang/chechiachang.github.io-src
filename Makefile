THEME := "hugo-theme-air"

server:
	hugo server -D

clean: 
	rm -rf public

hugo:
	hugo

publish: clean hugo
	cp -r public/* ..
