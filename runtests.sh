#!/bin/sh
export DATABASE_URL='postgres://postgres:@/test_chms_control'
export DJANGO_SETTINGS_MODULE="chms_control.testsettings"
./manage.py test "$@"
