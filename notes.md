- a package will be nicknamed, bucket
- I am coming into rate limit issues
	- I was able to decrease the amount of api calls by isolating some request calls for the `Bucket` object
	- According to [this reply](https://stackoverflow.com/a/25683955/12135693), authenticating the bft user could increase the rate limit from 60 (default) to 5000.
		- getting access token via command line: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app#using-the-device-flow-to-generate-a-user-access-token
	- I don't expect a bft user making 5000+ requests
	- to check for github api current rate limit: `curl -L https://api.github.com/rate_limit`
