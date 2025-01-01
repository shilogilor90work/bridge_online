# bridge_online
bridge online

### Setup
Update the System
```bash
sudo apt-get update
```
To get this repository, run the following command inside your git enabled terminal
```bash
git clone https://github.com/shilogilor90work/bridge_online.git
```
You will need django to be installed in you computer to run this app. Head over to https://www.djangoproject.com/download/ for the download guide

Download django using pip
```bash
sudo apt install python3-pip -y
```
```bash
pip install django
```

Start the server by following command

```bash
python3 manage.py runserver
```

Once the server is hosted, head over to http://127.0.0.1:8000 for the App.


ssh -i private_key.pem ec2-user@16.170.223.167


the server is running in a "screen" (if you dont know what this is google it)
attach to the screen:
screen -r bridge

ctrl+c (to stop the server)
git pull
python3 manage.py runserver 0.0.0.0:8000 (to start the server)
ctrl+a (let go) and click d (to detach from screen)

 and you could exit the connection

but you could simply click the up arrow and enter (find the command in history, should be once or twice)



To checkout sidebranch for testing:
git checkout -b interactive_bids origin/interactive_bids

And to go back to main:
git checkout main
git pull origin main
