# Tweetmojo

Tweetmojo creates Instamojo offers based on tweets.

You can find more information on how to use it at http://tweetmojo.herokuapp.com

## Usage

* Tweets should contain one pair of field identifier and field value on each line.
* Field ID and field value should be separated by a hyphen.
* For example, to create an offer with title "My New Offer" and base price INR 50, the tweet shoul look like this:

	t - My New Offer
	c - INR
	p - 50 	

## Field Identifiers

* t - Title.
* d - Description
* c - Currency (INR or USD)
* p - Base Price (>= INR 9 or USD 0.49)
* q - Quantity (0 for unlimited)
* s - Start Date (YYYY-MM-DD hh:mm)
* e - End Date (YYYY-MM-DD hh:mm)
* z - Timezone (ex: "Asia/Kolkata")
* v - Venue
* u - Redirect URL
* n - Note
* f - File Upload JSON
* i - Cover Image JSON
