# reachy2_module
A module to control the reachy2 robot


# How to run the basic movement demo in RPL:
1. Go to "reachy2.cels.anl.gov:8000" while on snowcrash.
2. In the General section, click on "Movement".
3. Press the start button to run the demo. 


# How to run teleop with the Meta Quest:
1. Install python ~= 3.10:  https://www.python.org/downloads/release/python-31022/
2. install the apt packages android-sdk-platform-tools for installing packages on your quest, and liblzma-dev as a dependency for the later python code: `sudo apt install android-sdk-platform-tools liblzma-dev`
3. Ensure that your Meta Quest headset is in developer mode: https://developers.meta.com/vr/documentation/android-apps/enable-developer-mode/, and connected with a Thunderbolt cable to your computer
4. Download the `quest_teleop_v1.apk` file from here:  https://github.com/AD-SDL/tavis/releases/tag/v0.1.1
5. From the folder where you downloaded the file, run `adb install -r quest_teleop.apk_v1.apk`
6. Clone the forked reachy2_quest_teleop here: https://github.com/AD-SDL/reachy2_quest_teleop, and cd into it `cd reachy2_quest_teleop`
7. create a virtual environment using python 3.10: `python3.10 -m venv .venv`, then activate it `source .venv/bin/activate`
8. within the virtual environment, run `pip install -e ".[ik,test]"`
9. additionally install your desired `lerobot` version, as it is not included as a dependency for the package.
10. run `pip install rustypot==1.0`
11. Turn the headset on and run `./scripts/start_quest.sh` from within the teleop repo
12.  within the virtual environment you set up for the repo and from within the teleop repo folder, run: \
     `python scripts/teleop_reachy2.py --host <your robot ip> --dataset-name <your dataset name> --instruction <your instructions>`
13. Put on the headset and align the controllers with the robot hands, which will turn the text green. Press 'Y' to start the arm tracking. Futher instructions can be found in the repo readme: https://github.com/AD-SDL/reachy2_quest_teleop
