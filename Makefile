DOGSHEEP = 	docker run \
				-ti \
			    --rm \
			    -v ${PWD}:/mnt \
			    dogsheep 
container:
	docker build -t dogsheep .
# make datasette db=path/to/file.db
datasette:
	$(DOGSHEEP) datasette \
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
	# Github
	docker run --rm -ti -v ${PWD}:/mnt dogsheep \
			github-to-sqlite auth --auth /mnt/auths/github_auth.json
pocket:
	$(DOGSHEEP) pocket-to-sqlite fetch \
			   		--auth /mnt/auths/pocket_auth.json \
					/mnt/dbs/pocket.db
### Twitter ###
twitter: tw_tweets tw_followers tw_friends tw_favorites tw_lists
tw_ingest:
	$(DOGSHEEP) twitter-to-sqlite import \
			   /mnt/dbs/twitter_archive.db \
			   /mnt/twitter-2021-02-01-c361de3cedd9786e46ea8b2cd09690f988e3b22f6ffafba1424684360501883b/data
tw_tweets:
	$(DOGSHEEP) twitter-to-sqlite user-timeline \
			   		--since \
			   		--auth /mnt/auths/twitter_auth.json \
			   		/mnt/dbs/twitter.db
tw_followers:
	$(DOGSHEEP) twitter-to-sqlite followers \
			   		--auth /mnt/auths/twitter_auth.json \
			   		/mnt/dbs/twitter.db
tw_friends:
	$(DOGSHEEP) twitter_to_sqlite friends \
			   		--auth /mnt/auths/twitter_auth.json \
			   		/mnt/dbs/twitter.db
tw_favorites:
	$(DOGSHEEP) twitter_to_sqlite favorites \
			   		--auth /mnt/auths/twitter_auth.json \
			   		/mnt/dbs/twitter_favorites.db
tw_lists:
	$(DOGSHEEP) twitter_to_sqlite lists \
			   		--auth /mnt/auths/twitter_auth.json \
			   		/mnt/dbs/twitter_lists.db --members darribas

### Github ###
gh_repos:
	$(DOGSHEEP) github-to-sqlite repos \
			   		--readme --readme-html \
			   		-a /mnt/auths/github_auth.json \
			   		/mnt/dbs/github.db
