# reachy2_module
A module to control the reachy2 robot


# How to run the basic movement demo in RPL:
1. Go to "reachy2.cels.anl.gov:8000" while on snowcrash.
2. In the General section, click on "Movement".
3. Press the start button to run the demo. 


# How to run teleop with the Meta Quest (for now):
1. Follow the installation and setup steps listed here: https://github.com/spiglerg/reachy2_quest_teleop
2. Turn the headset on and run `bash scripts/start_quest.sh` from within the teleop repo
3.  within the virtual environment you set up for the repo and from within the teleop repo folder, run `python scripts/teleop_reachy2.py --host 146.137.240.56 --dataset-name <your dataset name> \
    --instruction "your instructions"`
