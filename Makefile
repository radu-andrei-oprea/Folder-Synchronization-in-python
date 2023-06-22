# Unzip the source archive and create the dest folder and log file.
build:
	unzip test_src.zip
	mkdir dest
	touch log.log

# Run the command with an optional delay interval.
# If no interval is provided, it defaults to 30 seconds.
run:
	python3 sync.py src dest log.log $(filter-out $@,$(MAKECMDGOALS))

# Delete the folders and the log file.
clean:
	rm -rf src
	rm -rf dest
	rm log.log

.PHONY: build run clean