PortalBot
---------

PortalBot fires up a browser and uploads widget code to Portals. Modify the domain css and/or widget js files on your PC, then run PortalBot to upload them into your portal.

*Installation*

```bash

    $ pip install -r requirements.txt
```

*Usage*

```bash

$ python portalbot.py --help
portalbot - Portals Utility - update widget js and domain css

Usage:
    portalbot upload [options] --domain=<domain> --user=<user>
        [--widgetjs=<file> --portal=<id> --dashboard=<id> --widget=<id>]
        [--domaincss=<file>]
        [--noninteractive]

    Portalbot fills in your username and gives you 60 seconds to enter your 
    password.

    portal and dashboard ids can be taken from the dashboard url: 
    
      /view/<portal>/<dashboard>

    Finding your widget id requires inspecting the DOM. In Chrome, right click
    on the down arrow on the top right in the widget and select Inspect 
    Element. The id is from the id of that element, e.g. if you see 
    <img id="menuicon1" ... the widget id is 1.

    Currently only non-public dashboard ids are supported.

    By default, the browser is left open. Pass --noninteractive to quit when 
    upload completes.

Options:
    -h --help     Show this screen
    -v --version  Show version
```

Example:

```bash

    $ portalbot.py upload --domain=mydomain --user=myname@company.com --domaincss=domain.css --widgetjs=mywidget.js --portal=1219686468 --dashboard=1297260819 --widget=1
```

