# etikettenschwindel

Flask app to print labels defined as ooffice templates (*.ott).
We use it with a Brother QL-710W label printer.

You need to have libreoffice installed. Tested with 5.1.4.2 10m0(Build:2).
Make sure libreoffice is not running while using the app.

## INSTALL

```
git clone https://github.com/Eigenbaukombinat/etikettenschwindel.git
cd etikettenschwindel
virtualenv .
bin/pip install flask
bin/pip install odfpy
```

## CONFIGURATION

```cp config_example.json config.json```

Edit config.json as needed.

## RUN

```
FLASK_APP=server.py bin/flask run
```


## TODO

* Add bar/qr code support
* Styling of frontend
