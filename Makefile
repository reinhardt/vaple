dist::
	cp -R vaple vaple_core dist/
	cd dist && zip -r vaple.zip manage.py vaple vaple_core python wkhtmltox wkhtmltopdf Django-2.1.7 django-wkhtmltopdf-3.2.0 pytz-2018.9 vcruntime140.dll

dist_no_deps::
	cp -R vaple vaple_core dist/
	cd dist && zip -r vaple_no_deps.zip manage.py vaple vaple_core
