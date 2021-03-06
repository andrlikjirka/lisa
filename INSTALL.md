Install (L)Ubuntu 14.04
=======================

### Script installer

    wget https://raw.githubusercontent.com/mjirik/lisa/master/installer.sh -O installer.sh
    source installer.sh
    

You can run `installer.py` with parameter `devel` or `noclone` to control source files cloning

More information read [linux install notes](https://github.com/mjirik/lisa/blob/master/install_linux.md)


Install Mac OS
==============

 * Xcode, gcc and make

    Install Xcode from appstore. You will need an AppleID.
    Then add terminal tools (http://stackoverflow.com/questions/10265742/how-to-install-make-and-gcc-on-a-mac)
    * Start XCode
    * Go to XCode/Preferences.
    * Click the "Downloads" tab.
    * Click "Components".
    * Click "Install" on the command line tools line.


 * [Install Anaconda](http://continuum.io/downloads)

 * All other dependencies install with script


        curl https://raw.githubusercontent.com/mjirik/lisa/master/installer.sh -o installer.sh
        source installer.sh

     You can run `installer.py` with parameter `devel` or `noclone` to control source files cloning
 
   

Install Lisa for Windows with Anaconda
=========

Use [windows installer](http://147.228.240.61/queetech/install/setup_lisa.exe)

or

* Download and install [miniconda](http://conda.pydata.org/miniconda.html)
* Download and install [MS Visual C++ compiler](http://aka.ms/vcpython27)

* Run command line and create conda-virtualenv


        conda create --no-default-packages -y -c mjirik -c SimpleITK -n lisa pip lisa
        activate lisa

* In activated lisa virtualenv run following lines


        python -m wget https://raw.githubusercontent.com/mjirik/lisa/master/requirements_pip.txt
        pip install -r requirements_pip.txt
        conda install -y -c mjirik -c SimpleITK --file lisa

* Run Lisa

        activate lisa
        python -m lisa



Use VirtualBox (old Lisa version)
==============

* Install VirtualBox (https://www.virtualbox.org/)
* Download Lisa Image (http://uloz.to/xU4oHfKw/lisa-ubuntu14-04-vdi)

or 
* Download Lisa Image (http://147.228.240.61/queetech/install/lisa_ubuntu14.04.vdi)

In VirtualBox

* Create new computer

    * Name: Lisa
    * Type: Linux
    * Version: Ubuntu (32bit)
    
* Set memory size to 1024MB and more
* Use existing hard disk and locate downloaded Lisa Image (lisa_ubuntu14.04.vdi)
* Password to Lisa account is: L1v3r.


