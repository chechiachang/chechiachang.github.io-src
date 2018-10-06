THEME := "hugo-theme-air"

server:
	hugo server -D

clean: 
	rm -rf public

hugo:
	hugo

publish: clean hugo
	cd public; git add . && git commit -m "Generate from src" && git push origin master
