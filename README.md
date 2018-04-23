#### Overview
API utlizes blockchain and off-blockchain data storage. Blockchain side enables users to ensure the authenticity of information related to Aircrafts, in particular its' current ownership and all the historical transactions. In addition, not encrypted metadata regarding transactions, among others contents of all the formulars, are stored in a centralized database.

Stucture of the database intentionally doesn't make use of relations to enable easy switch to decentalized storage (such as BitTorrent network, [StorJ](https://storj.io/), [FileCoin](https://filecoin.io/) etc.), in case it will be recommended in the future.

##### Blockchain contract storage
Fingerprints of all the fields from particular formulars are stored in [Ethereum](https://www.ethereum.org/) blockchain using smart contract writen in [Solidity language](https://solidity.readthedocs.io/en/v0.4.23/). They are generated using [SHA-224](https://en.wikipedia.org/wiki/SHA-2) cryptographic hash function, thus even a small change in the message will result in a mostly different hash, due to the [avalanche effect](https://en.wikipedia.org/wiki/Avalanche_effect). Example static content of contract stored in blockchain is presented below.
```json
{
   "transferee_name":"1123c599095afde714bd13b6457c482f77fa64a4fe988e2b3eb57750",
   "transferee_address":"78d8045d684abd2eece923758f3cd781489df3a48e1278982466017f",
   "transferee_nationality":"076d364250f10e230a3a28b2a4175d7431b24bc290a8fe4f76f7c054",
   "transferor_name":"bd1a1bdf6eae5ee14c3fee371cca975a5e052009bc67ce8f11cb7271",
   "transferor_address":"78d8045d684abd2eece923758f3cd781489df3a48e1278982466017f",
   "transferor_nationality":"78d8045d684abd2eece923758f3cd781489df3a48e1278982466017f",
   "manufacturer_and_model":"78d8045d684abd2eece923758f3cd781489df3a48e1278982466017f",
   "manufactured":"86665612b0b232cb14f8605473d3a7e0d2f303ff7003c6f8916fdc4f",
   "last_maintenance":"0298f0bd0619d34fbe508628cef38adc827fcf4d93c700588f607adc",
   "serial_number":"83dd3a4315c03a802c7ab4bf6b61b2bd847976c1295e8e7284ec59b7",
   "registration_number":"4cfc3a1811fe40afa401b25ef7fa0379f1f7c1930a04f8755d678474",
   "transfered":"86665612b0b232cb14f8605473d3a7e0d2f303ff7003c6f8916fdc4f"
}
```
Data are stored in custom contract, in its only sttic field, as serialized JSON string (in order to make contract elastic, in sense no ingerention in solidity is required to store additional data – all the required changes can be done by performing quite standard changes in model and serializer).

It is possible to switch to [ERC721](https://medium.com/crypto-currently/the-anatomy-of-erc721-e9db77abfc24) tokens with ease, but they seem to be a way too complex as it comes to the current needs.

#### Prerequirements and technology
API was developed in Python programing language, utilizing [Django REST framework](http://www.django-rest-framework.org/), as well as [web3.py](https://github.com/ethereum/web3.py) interface for interacting with the Ethereum blockchain and ecosystem. Apart from these and other python-related requirements (cf. _requirements.txt_ file) two additional application have two be installed in target system, namely:
- the [solc Solidity compiler](http://solidity.readthedocs.io/en/v0.4.21/installing-solidity.html) (used to compile smart contract before they are signed and send),
- [geth](https://geth.ethereum.org/) or equivalent interface for running a full ethereum node (since contract has to be signed using private key, for security purposes external services such as [Infura](https://infura.io/) do not provide this functionality).

After installing geth type `geth account new` in order to create an account that will be used for sending contract-related transactions to network. Account's keyfile and password should be provided in configuration file for proper system functioning (type `geth account list` to find out where is the relevant keystore file located).

#### Running, testing, API documentation
In order to install python requirements type `pip install -r requirements.txt`.

Make sure _geth_ is running and all the required settings are provided in the configuration file. System can be tested eg. using [Rinkeby Ethereum Testnet](https://www.rinkeby.io/). In this case _geth_ has to be run with an `--rinkeby` option.

Then type simply run server using `python manage.py runserver` command in the main project directory. It will be available at [127.0.0.1:8000](http://127.0.0.1:8000/) by default, where the detailed API documentation should appear.

![(View of API documentation)](docs/static/api.png)
