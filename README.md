# luxdance
private software for lux dance operation systems

## Name and Age Assignment System

This is a web-based system where multiple devices can connect locally via browser. The server assigns a unique number to each unique name in the order they first appear. Data is persisted using SQLite.

### Local Development
Run the server:
```
python server.py
```
The server will start on `http://localhost:5000`.

### Accessing the App
- Open your web browser and go to `http://localhost:5000`.
- Enter your name and age in the form.
- Submit to get your assigned number.
- Multiple devices/tabs can connect simultaneously by opening the URL on different browsers or machines on the same network.
- Data is saved to `data.db` and persists locally.

### Deploying to Heroku (for Online Access)
1. Create a free Heroku account at https://heroku.com.
2. Install Heroku CLI: `npm install -g heroku` or download from https://devcenter.heroku.com/articles/heroku-cli.
3. Login: `heroku login`.
4. Create app: `heroku create luxdance` (or choose your name).
5. Push code: `git add . && git commit -m "Deploy" && git push heroku main`.
6. Open: `heroku open` or go to https://luxdance.herokuapp.com.

For a custom domain, buy one from a registrar and add it in Heroku dashboard under Settings > Domains.

Note: Free Heroku dynos sleep after inactivity, and data may reset on restarts. For persistent data, upgrade to a paid plan with Postgres.

The system is fully local for development and can be hosted online.
