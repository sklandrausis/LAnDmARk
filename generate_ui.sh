#!/bin/bash

pyuic5  resources/main_view.ui -o views/main_view_ui.py
pyuic5  resources/query_view.ui -o views/query_view_ui.py
pyuic5  resources/run_view.ui -o views/run_view_ui.py
pyuic5  resources/setup_view.ui -o views/setup_view_ui.py
pyuic5  resources/check_view.ui -o views/check_view_ui.py

