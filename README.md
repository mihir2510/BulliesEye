<div align='center'>
    <img src='https://cdn4.iconfinder.com/data/icons/football-soccer-sports-outline/512/goal_target_arrow_espa_dartboard_bullseye_focus-512.png' width=200 height=200>
</div>

# Bullies-Eye
---

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/mihir2510/BulliesEye.git
$ cd BulliesEye/Ourapp
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv --no-site-packages env
$ source env/bin/activate
$
$ # Install modules
$ pip3 install -r requirements.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$
$ # Enable debug (for development)
$ # (Unix/Mac) export FLASK_ENV=development
$
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
```

<br/>

### Model Details

- Trained custom word embeddings using `word2vec` algorithm on the "hatespeech" dataset from Kaggle
- Model architecture involved,
  
  ```
    Embedding layer
    SpatialDropout
    BiDirectional LSTM
    Conv1D
    GlobalAveragePooling
    Dense
  ```
- After training the model for 5 epochs accuracy of ~97% accuracy was achieved

### Scraper Details

- The scraper uses [Tweepy](https://www.tweepy.org/) for scraping tweets from Twitter which is passed into the model to check for abusive content
- Top X most offensive tweets were displayed on admin's dashboard with an option to auto-generate FIR report for each offensive/cyberbullying tweet.
- Admin can also search for tweets with specific offensive words.


### TODO

- [ ] Implement Transformer architecture
- [ ] Currently its deployed as a Twitter and Telegram Bot, target other platforms like Reddit and Facebook
- [ ] Turn the Dashboard into a PWA 

### Contributors
- [@KaustubhDamania](https://github.com/KaustubhDamania/)
- [@mihir2510](https://github.com/mihir2510)
- [@anay121](https://github.com/anay121)
- [@2knal](https://github.com/2knal)
- [@vtg2000](https://github.com/vtg2000)
- [@fate2703](https://github.com/fate2703/)

---
#### Dashboard Credits
[Flask Dashboard AdminLTE](https://appseed.us/admin-dashboards/flask-dashboard-adminlte) - provided by **AppSeed**
