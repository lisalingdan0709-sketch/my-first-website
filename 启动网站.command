#!/bin/bash
cd "$(dirname "$0")"
/usr/local/bin/python3 -m streamlit run app.py --server.runOnSave true