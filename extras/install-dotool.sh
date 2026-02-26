if [ -d "dotool" ]; then
        echo "Directory 'dotool' already exists. Skipping download."
else
        wget https://git.sr.ht/~geb/dotool/archive/1.6.tar.gz -O dotool-1.6.tar.gz
        tar -xzvf dotool-1.6.tar.gz
        rm dotool-1.6.tar.gz
fi

cd dotool-1.6
./build.sh && sudo ./build.sh install
sudo udevadm control --reload && sudo udevadm trigger

# Add an "input" group and add yourself to it
groupadd -f input
sudo usermod -a -G input $USER
