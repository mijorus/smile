if [ -d "dotool" ]; then
        echo "Directory 'dotool' already exists. Skipping download."
else
        if  command -v git &> /dev/null; then
            git clone https://git.sr.ht/~geb/dotool
        else
            wget https://git.sr.ht/~geb/dotool/archive/1.6.tar.gz -O dotool.tar.gz
            tar -xzvf dotool.tar.gz
            mv dotool-1.6 dotool
            rm dotool.tar.gz
        fi
fi

cd dotool
./build.sh && sudo ./build.sh install
sudo udevadm control --reload && sudo udevadm trigger

# Add an "input" group and add yourself to it
groupadd -f input
sudo usermod -a -G input $USER
