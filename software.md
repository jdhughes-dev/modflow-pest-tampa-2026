# Software Installation
Class participants will need to come prepared with a laptop computer that has Python installed. **If you are familiar with mamba environments and know how to create a new mamba environment using an environment.yml file, then skip ahead to Part 3**. For all others, we recommend using the Miniforge software to download and install Python and required dependencies needed for the workshop. 

The following instructions will guide you through the installation process and setup of a `tampa26mf6pp` environment and downloading the class materials.

## Part 1 -- Install git

If `git` is not installed, instructions for installing `git` can be found at [https://git-scm.com/downloads](https://git-scm.com/downloads).

## Part 2 -- Install Miniforge
1. Download and run the Miniforge installer (https://github.com/conda-forge/miniforge) for your operating system.

2. Click through the installer options, and select "Just Me (recommended)" if asked. Default installation options should be fine, with the exception that you should select an installation location that does not have any special characters or spaces in it.

3. After installation, you should see "Miniforge Prompt" as a program under the Windows Start menu.

## Part 3 -- Create an Environment File
We will use an environment file to create a containerized version of Python and the Python packages needed for the class. An environment file is simply a list of packages that we want to install in our environment.

### Windows
Using a text editor, such as Notepad or Notepad++, create a file called `environment.yml`. It should contain the information in [this environment file](https://github.com/jdhughes-dev/modflow-pest-tampa-2026/blob/main/environment.yml). Save this file to your hard drive, preferably in your user home folder so that it can be easily accessed in the next step. (Caution!  Notepad will automatically append a .txt suffix to your file name; you don't want this to happen.)

### Mac and Linux
Using a text editor, create a file called `environment.yml`. It should contain the information in [this environment file](https://github.com/jdhughes-dev/modflow-pest-tampa-2026/blob/main/nix-environment.yml). Save this file to your hard drive, preferably in your user home folder so that it can be easily accessed in the next step.


## Part 4. Create the `tampa26mf6pp` Environment

1. Start the miniforge prompt from the Windows start menu (or equivalent on Mac or Linux) to bring up a terminal.

2. At the terminal prompt enter the following command, where `<path to file>` is the location of the `environment.yml` file that you created in Part 2. You will need to be connected to the internet for this to work properly. The installation process may take a couple of minutes.
```
mamba env create --file <path to file>/environment.yml
```

3. After the environment has been installed, you may activate this new class environment with the following command
```
mamba activate tampa26mf6pp
```

4. The windows terminal prompt should reflect the current environment:
```
(tampa26mf6pp) C:\Users\JaneDoe>
```

5. We will be using jupyter notebooks in the workshop. To test if jupyter is installed and working properly use the following command. After entering this command, the default web browswer should open to a Jupyter Lab page.
```
jupyter lab
```

For most users, the setup is complete at this point. For those working on a Mac or Linux laptop, please proceed to Part 6.


## Part 5. Obtaining MODFLOW 6 and PEST++

We will be using the extended version of MODFLOW 6 in this workshop. 

### Windows

If you are working on Windows, you can install the extended version of MODFLOW 6 by activating the workshop environment using:

```
mamba activate tampa26mf6pp
```

and then running:
```
get-modflow --repo modflow6-nightly-build --ostag win64ext :python
```

and then running:
```
get-modflow --subset gridgen,triangle :python
```

and finally running:
```
get-pestpp --release-id 5.2.25 :python
```

You can also download the extended version of MODFLOW 6 from [here](https://github.com/MODFLOW-ORG/modflow6/releases). 

Note that we will also walk through this step during the workshop. The distribution file for windows that includes the parallel version is called `win64ext.zip`.

### Mac and Linux

If you are using a Mac or Linux laptop for the workshop, then you will need to build the parallel version of MODFLOW. We have simplified the build process, which can be completed in just a few minutes. You will need to install git on your laptop if you don't already have it. 

1. Download the workshop GitHub repository using:
```
git clone https://github.com/jdhughes-dev/modflow-pest-tampa-2026.git
```

2. Activate the tampa26mf6pp environment
```
mamba activate tampa26mf6pp
```

3. Navigate to the root directory of the workshop GitHub repository and run the MODFLOW 6 build script using:
```
sh nix-build.sh  
```

4. If the build is successful you should see the following:
```
 Normal termination of simulation.
――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
5/5 Parallel simulation test - 2 cores  OK              0.10s


Ok:                5   
Fail:              0   

Full log written to /path/to/the/class/github/repo/modflow-pest-tampa-2026/modflow6/builddir/meson-logs/testlog.txt

Finished...


```

## Part 6. Clone the class repo 

On Windows, start a CMD shell and clone the class repo using the following command:

```
git clone https://github.com/jdhughes-dev/modflow-pest-tampa-2026.git
```



