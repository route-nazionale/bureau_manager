bureau_manager
==================
Gestione delle segreterie della Route Nazionale 2014:
 - segreteria centrale
 - segreterie sottocampo
 - segreteria OneTeam

Installazione
=============
Requisiti:

* virtualenv (consigliato ma non obbligatorio)
* python 2
* django 1.7

Procedura di installazione:

```sh
sudo apt-get install virtualenvwrapper
mkvirtualenv rn-bureau_manager
git clone git@github.com:route-nazionale/bureau_manager.git
cd bureau_manager
pip install -r requirements.txt
cp bureau_manager/settings_dist.py bureau_manager/settings.py
```

Per avviare il server di sviluppo, non adatto per il deploy:

```sh
# per entrare nel virtualenv
workon rn-bureau_manager
cd bureau_manager
python manage.py runserver

# per uscire dal virtualenv
deactivate
```

Il repository contiene un DB sqlite che ha dentro alcuni dati di test.

Per visualizzare e modificare i dati, utilizzate la comoda interfaccia di admin di django.

http://localhost:8000/admin

Potete accedere con nome utente 'admin' e password 'admin'

