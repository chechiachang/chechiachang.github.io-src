THEME := "hugo-theme-air"

init:
	git submodule update --init

server:
	hugo server -D

hugo:
	hugo

publish: hugo
	cd public; git add . && git commit -m "Generate from src" && git push origin master
