# bucky
The project for team 7 in I-Stem Hackathon 2019.

## Setup

### Authentication
Bucky is still under development. You would need to setup credentials from a Vision API enabled account on GCP to get him up and running on your device.

### Install Dependencies
1. Install [pip](https://pip.pypa.io) and [virtualenv](https://virtualenv.pypa.io/)

2. Create a virtualenv and activate it
> ```sh
> $ virtualenv --python python3 env
> $ source env/bin/activate
> ```
If you're on Windows, you may have to specify the full path to your python installation directory
> ```sh
> $ virtualenv --python "c:\python36\python.exe" env
> $ .\env\Scripts\activate
> ```
3. Install the dependencies required by Gina
> ```sh
> $ pip install -r requirements.txt
> ```

### Run
Bucky writes only the first frame to the terminal for now.
```sh
  $ python test.py
```
