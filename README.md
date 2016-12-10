# etikettenschwindel

Flask app to print labels defined as ooffice templates (*.ott).
We use it with a Brother QL-710W label printer.

You need to have libreoffice installed. Tested with 5.1.4.2 10m0(Build:2).
Make sure libreoffice is not running while using the app.

## INSTALL & RUN

```
virtualenv .
bin/pip install flask
bin/pip install odfpy
```

## CONFIGURATION

For now, edit server.py.

## RUN

```
FLASK_APP=server.py bin/flask run
```


## TODO

* Use a config file for settings and available templates
* Add bar/qr code support