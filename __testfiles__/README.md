# \_\_testfiles\_\_

This `__testfiles__` directory containts some test inputs and test output  files i.e. enceypt and decrypt file, this directory required to `../test_project.py`. do not delete `__testfiles__` directory 🙅. if delets `../test_project.py` give some error.

#### Directory Stucture 🗃️:

```bash
├───inputs
│       145308_(1080p).mp4
│       cat-551554_1280.jpg
│       house-chords-12112.mp3
│       massages.txt
│       
├───keys
│   ├───KEYS_20240305_110825_858294
│   │       private.pem
│   │       public.pem
│   │       
│   └───KEYS_20240305_110840_641535
│           private.pem
│           public.pem
│
└───testing_module
```

#### `inputs` 📂:
- `inputs` contains sone input files i.e. audio, video, image, text files etc. thise foler are required `../test_project.py` python script to function.

#### `keys` 📂:
- `keys` contain RSA kys set private key + public key files. thise foler are required `../test_project.py` python script to function.

#### `testing_module` 📂:
- When you run `../test_project.py` python script the `testing_module` folders are created automatically. You can **delete** this folder after unit testing. 
