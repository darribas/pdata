container:
	docker build -t dogsheep .
# make datasette db=path/to/file.db
datasette:
	docker run --rm \
			  	-p 8001:8001 \
				-v `pwd`:/mnt \
				dogsheep datasette \
					-p 8001 \
					-h 0.0.0.0 \
					/mnt/$(db) \
					--load-extension=spatialite
setup:
	mkdir -p dbs
	mkdir -p auths
	# Pocket
	docker run --rm -ti -v ${PWD}:/mnt dogsheep \
			pocket-to-sqlite auth --auth /mnt/auths/pocket_auth.json
	# Twitter
	docker run --rm -ti -v ${PWD}:/mnt dogsheep \
			twitter-to-sqlite auth --auth /mnt/auths/twitter_auth.json
pocket:
	docker run -ti \
			   --rm \
			   -v ${PWD}:/mnt \
			   dogsheep \
			   pocket-to-sqlite fetch \
			   		--auth /mnt/auths/pocket_auth.json \
					/mnt/dbs/pocket.db
twitter:
	# Tweets
	docker run -ti \
			   --rm \
			   -v ${PWD}:/mnt \
			   dogsheep \
			   twitter-to-sqlite user-timeline \
			   		--since \
			   		--auth /mnt/auths/twitter_auth.json \
			   		/mnt/dbs/twitter.db
	# Followers
	docker run -ti \
			   --rm \
			   -v ${PWD}:/mnt \
			   dogsheep \
			   twitter-to-sqlite followers \
			   		--auth /mnt/auths/twitter_auth.json \
			   		/mnt/dbs/twitter.db
	# Followers
	# Friends
	# Favorited tweets
	# Lists
	#
