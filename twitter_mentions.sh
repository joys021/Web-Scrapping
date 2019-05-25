while true

do
	python3 /home/nebuchednezzar/scrape_test.py
	python3 /home/nebuchednezzar/yahoo_finance.py AMZN
	touch /home/nebuchednezzar/COMPLETE_MENTIONS.csv
	touch /home/nebuchednezzar/COMPLETE_COUNTS.csv
	cat /home/nebuchednezzar/tweets.csv >> /home/nebuchednezzar/COMPLETE_MENTIONS.csv
	date +'%r'>>COMPLETE_COUNTS.csv;cat /home/nebuchednezzar/tweets.csv | grep 'AMZN' | wc -l >> /home/nebuchednezzar/COMPLETE_COUNTS.csv
	date +'%r'>>COMPLETE_COUNTS.csv;cat /home/nebuchednezzar/AMZN-summary.json >> /home/nebuchednezzar/COMPLETE_STOCKS.json
	sleep 10m
done

