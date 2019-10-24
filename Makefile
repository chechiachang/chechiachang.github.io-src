init:
	git submodule update --init --remote

title:
	if [ -z $${TITLE} ]; then echo 'TITLE env is required.' && exit 1; fi

talk: title
	hugo new --kind talk talk/$${TITLE}

project: title
	hugo new --kind project project/$${TITLE}

post: title
	hugo new --kind post post/$${TITLE}

slides: title
	hugo new --kind slides slides/$${TITLE}

server:
	hugo server -D --bind 0.0.0.0 --port 1313

hugo:
	hugo

publish: hugo
	cd public; git add . && git commit -m "Generate from src" && git push origin master
