# assets

`assets` folder contains Crypto50 GUI softwer icon images, user genarated keys and user added public keys file. please do not delete this `assets` directory 🙅. if you **delete** Crypto50 give some error.


#### Directory Stucture 📂:

```bash
├───icons
│
└───keys
    │
    ├───my_keys
    │   ├───KEYS_20240306_011637_073329
    │   │       private.pem
    │   │       public.pem
    │   │
    │   └───....
    │
    └───public_keys
        ├───PUB_20240306_012425_632366
        │       public.pem
        │
        └───....
```

#### `icon` 📂:

- This `icon` folder contains all icon images files, they are required Crypto50 GUI softwer to function. please do not delete this `icon` directory and any icon images file. if you **delete** Crypto50 give some error.

#### ` keys` 📂:
- Keys directory contains user genarated public + private keys and and user added public keys. please do not delete this `keys` directory. if you **delete** Crypto50 give some error.

#### `my_keys` 📂:
- When you genarate new RSA key set at frist time useing Crypto50 GUI softwe the `my_keys` folders are created automatically and store your genarated keys. if you **delete** this folder Crypto50 softwer not found your keys and give some error when you open key, delete key etc. but you can **delete** this folder when you upload or push this source code in GitHub.

#### `public_keys` 📂:
- When you add new RSA public key at frist time useing Crypto50 GUI softwer the `public_keys` folders are created automatically and store your added public keys. if you **delete** this folder Crypto50 softwer not found your added public keys and give some error. but you can **delete** this folder when you upload or push this source code in GitHub.