manage="${VENV}/bin/python ${INSTALLDIR}/${REPO}/manage.py"

if [ ! -f ${INSTALLDIR}/chmscontrol-installed ]; then
    su - postgres -c "createdb chmscontrol"
    su - postgres -c "psql chmscontrol -c 'CREATE EXTENSION hstore;'"

    mkdir ${INSTALLDIR}/${REPO}/chmscontrol/static

    chown -R ubuntu:ubuntu ${INSTALLDIR}/${REPO}/media
    chown -R ubuntu:ubuntu ${INSTALLDIR}/${REPO}/static

    $manage syncdb --noinput
    $manage collectstatic --noinput
    touch ${INSTALLDIR}/chmscontrol-installed
else
    $manage migrate --noinput
    $manage collectstatic --noinput
fi