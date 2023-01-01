
```bash title="silt"
arducopter -S --model gazebo-iris --speedup 1 --slave 0 --defaults /home/user/git/ardupilot/Tools/autotest/default_params/copter.parm,/home/user/git/ardupilot/Tools/autotest/default_params/gazebo-iris.parm -I0
```

```bash title="mavproxy"
"mavproxy.py" "--out" "127.0.0.1:14550" "--out" "127.0.0.1:14551" "--master" "tcp:127.0.0.1:5760" "--sitl" "127.0.0.1:5501"
```

# Reference
- [rishabsingh3003](https://github.com/rishabsingh3003/Precision_Landing_ArduPilot/blob/master/AirSim/air_sim_to_mavlink.py)