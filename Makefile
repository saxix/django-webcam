BUILDDIR=~build
PYTHONPATH := ${PWD}/demo/:${PWD}
DJANGO_SETTINGS_MODULE:=demoproject.settings
CASPERJS_DIR=${BUILDDIR}/casperjs
PHANTOMJS_DIR=${BUILDDIR}/phantomjs

mkbuilddir:
	mkdir -p ${BUILDDIR}

ci:
	@[ "${DJANGO}" = "1.4.x" ] && pip install django==1.4.8 || :
	@[ "${DJANGO}" = "1.5.x" ] && pip install django==1.5.4 || :
	@[ "${DJANGO}" = "1.6.x" ] && pip install https://www.djangoproject.com/m/releases/1.6/Django-1.6b4.tar.gz || :
	@[ "${DJANGO}" = "dev" ] && pip install git+git://github.com/django/django.git || :

	@[ "${DBENGINE}" = "pg" ] && pip install -q psycopg2 || :
	@[ "${DBENGINE}" = "mysql" ] && pip install git+git@github.com:django/django.git || :

	@pip install coverage
	@python -c "from __future__ import print_function;import django;print('Django version:', django.get_version())"

	coverage run demo/manage.py test webcam --settings=demoproject.settings_travis

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml pytest.xml .cache MANIFEST
	find . -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf


docs: mkbuilddir
	mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs/source ${BUILDDIR}/docs
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif

