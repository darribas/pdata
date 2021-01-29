container:
	docker build -t dogsheep .
setup:
	mkdir -p dbs
	mkdir -p auths
	# Pocket
	docker run --rm -ti -v ${PWD}:/mnt dogsheep \
			pocket-to-sqlite auth --auth /mnt/auths/pocket_auth.json
pocket:
	docker run -ti \
			   --rm \
			   -v ${PWD}:/mnt \
			   dogsheep \
			   pocket-to-sqlite fetch \
			   		--auth /mnt/auths/pocket_auth.json \
					/mnt/dbs/pocket.db
