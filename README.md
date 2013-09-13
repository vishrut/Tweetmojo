# Tweetmojo

Tweetmojo creates Instamojo offers based on tweets.

You can find the working instance at http://tweetmojo.herokuapp.com/tweetrieve/views/search_tweets?handle=Vishrut42

Note: All offers created on vrp101's Instamojo account.

## Usage

* Tweets should contain one pair of field identifier and field value on each line.
* Field ID and field value should be separated by a hyphen.

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
