from flask import session
from myforum  import app
app.secret_key = 'cxblmawefl345lrgf435f43ac541fanlm2356y0xvn1234'
app.PER_PAGE = 3
app.run(host='127.0.0.1', debug=True)
