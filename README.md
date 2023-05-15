# Project name: NFT-wallet
The project aims to provide the user with:

* Quick checking of the 50 collections with the highest volume on the market https://minted.network/.
* Listing all NFTs according to the wallet address, including collection names and quantity.
* Calculating the value of each collection and the entire wallet based on the current floor price on markets https://minted.network/ and https://app.ebisusbay.com/.
* Both markets often have problems with fast page loading due to a lot of graphics on their pages. Thanks to our program, this data can be retrieved in a matter of seconds, while checking this data on the market pages often takes several dozen minutes.
* A useful tool for people with weaker hardware or internet.

## System requirements

* Python 3.9

## Installation

* Clone this repository.
* Install dependencies using the command pip install -r requirements.txt pip install Flask pip install Flask-SQLAlchemy
* Run the app.py script.
## Usage
* Go to the website: http://127.0.0.1:5000.
* Register at first use, and then log in using your credentials.
* A list of NFT collections with the highest volume in the last 24 hours on the Minted market will be displayed. Collections are sorted by volume size from largest to smallest. The difference in price from the last 24 hours and the current floor price is given for each collection.
* The application uses colors to make it easier to recognize price changes. Green indicates a price increase below 20%, red indicates a price decrease to 20%, and yellow indicates price changes of more than 20%.
* Each collection has a "GO" button that takes you to a page displaying the 10 next NFTs from the collection with the lowest floor price.
* Click "WALLET" on the navigation bar, enter your wallet address, and click "enter." The application will take you to a page displaying your NFT state, listed by collection names, quantity, and current floor price on the Ebisusbay market.
* To check the valuation of your collections on the Minted market, click the "Minted" button - you will be taken to a page where you will get results from that exchange.
## Contact
* In case of any questions or problems with the project, please contact us via email.

## License
* The project is released under the MIT license.