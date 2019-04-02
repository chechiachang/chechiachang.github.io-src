THEME := "hugo-theme-air"

init:
	git submodule update --init

server:
	hugo server -D

clean:
	rm -rf public

hugo: clean
	hugo

publish: init hugo
	cd public; git add . && git commit -m "Generate from src" && git push origin master
