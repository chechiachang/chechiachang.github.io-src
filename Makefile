init:
	git submodule update --init --remote

talk:
	hugo new --kind talk talk/new

server:
	hugo server -D

hugo:
	hugo

publish: hugo
	cd public; git add . && git commit -m "Generate from src" && git push origin master
