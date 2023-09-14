init:
	git submodule update --init --remote

title:
	if [ -z $${TITLE} ]; then echo 'TITLE env is required.' && exit 1; fi

DATE := $(shell date +%Y-%m-%d)

talk: title
	hugo new --kind talk content/zh-hant/talk/$(DATE)-$${TITLE}

project: title
	hugo new --kind project content/zh-hant/project/$(DATE)-$${TITLE}

post: title
	hugo new --kind post content/zh-hant/post/$(DATE)-$${TITLE}.md

slides: title
	hugo new --kind slides content/zh-hant/slides/$(DATE) $${TITLE}

dev:
	hugo server --disableFastRender -D --bind 0.0.0.0 --port 1313

prod:
	hugo server --disableFastRender -D -e production --bind 0.0.0.0 --port 1313


.PHONY: hugo publish

hugo:
	hugo

clean:
	rm -rf public/*

cname:
	echo "chechia.net" > public/CNAME

publish: clean cname hugo
	cd public; git add . && git commit -m "Generate from src" && git push origin master
