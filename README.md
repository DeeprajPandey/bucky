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
Bucky has come a long way since 24 hours ago. To see it in action, run
```sh
  $ node app.js
```
And go to `localhost:8080` (if you want to log in using Facebook, you will need ngrok as it needs https connections) to drop the video file.
It might time out after a while when the TextExtractor is running. Don't fret, it would have saved the source code as a text file `SourceCode.txt` in the root directory by now.

### Bucket List
- [ ] How does the code morph throughout the video.
- [ ] Move away from hacky fix for the file uploads - migrate to Cloud Storage, even if it means you'll go broke.
- [ ] Prettyprint the source code? Even more ambitious - figure out the language *and* indent the code.
- [ ] Face your nightmare aka UI.
- [ ] Memoization - save videos which have been analysed.
- [x] Can we do better than Jaro-Winkler? *Not in this use case. :3*
