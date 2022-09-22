if [[ -z "$(which python3)" ]]; then
    echo "Install python3!"
    exit 1
else
    pip3 install python-magic
    pip3 install psutil
    pip3 install git+https://github.com/rthalley/dnspython
    pip3 install pyinstaller
fi
