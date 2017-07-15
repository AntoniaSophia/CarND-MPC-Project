#**Term 2 : MPC Controller Project**


**MPC Controller Project**

The goals / steps of this project are the following:

[//]: # (Image References)

[image0]: ./../master/tools/Predictive_Model_Equations.png "model_equations.png"
[image1]: ./../master/tools/initial_position.png "waypoint_rotation.png"

## Rubric Points
Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/896/view) individually and describe how I addressed each point in my implementation.  


###Student describes their model in detail. This includes the state, actuators and update equations.

I just used the vehicle model equations described in the Udacity classroom and derived in lesson 18 (Vehicle Models)

![Model Equations][image0]

You can see the use of those equations in MPC.cpp lines 145-162 and main.cpp lines 149-165 (here the latency prediction is carried out). 

However this model is very simple and doesn't consider any forces like friction, air resistanc, tire forces,....
I left these equations untouched and multiplied the steering angle by -1 as proposed in the tipps&tricks section (see main.cpp line 185). Reason for this is the fliped left/right orientation in the Udacity simulator.

The x-coordinate (x), y-coordinate (y), angle (psi), the cross-track error (cte) and the orientation error (epsi) are being calculated from the vehicle model equations. In opposite to that the actuator update - steering angle (delta) and the throttle ((a) - are being calculated by the so-called IPOPT algorithm "Interior Point OPTimizer" (see https://en.wikipedia.org/wiki/IPOPT), which can be found in MPC.cpp lines 173-312. 

###Student discusses the reasoning behind the chosen N (timestep length) and dt (elapsed duration between timesteps) values. Additionally the student details the previous values tried.

The prediction horizon is N * dt in seconds. That means at N = 10 and dt = 0.1 we have a prediction horizon of 1 second.
Short prediction horizons lead to more responsive controllers, but might be instable in case the horizon of 1 second is too short. Especially in curved roads this is visible. A longer prediction horizon generally should lead to smoother controls but also needs more computing power which might lead to an additional latency.  
In my case I was not able to produce good results with a longer prediction horizon than 1 second....
I even ended up with an optimal prediction horizon of only 0.8 seconds as I could gain more speed considering latency. Possibly the higher speed compensated the lower prediction horizon!?

###If the student preprocesses waypoints, the vehicle state, and/or actuators prior to the MPC procedure it is described.

At the beginning I've tried to visualize the waypoints in lake_track_waypoints.csv and wrote a small python script /./../showLakeTrackWaypoints.py.
I've combined 
* a rotation by angle psi (in simulator coordinate system)
* a translation by the current vehicle position (also in simulator coordinate system)
in order to transform from the simulator coordinate system to the vehicle coordinate system.

The following image shows the situation of the waypoints at the starting position of the simulator:
* the original waypoints in simulator coordinate system (red color)
* the rotated and translated waypoints which are now in vehicle's coordinate system (dark-green color)
(keep in mind that the heading of the vehicle is always the x-axis direction !! That means: drawing this in one coordinate system implies that the vehicle's heading is to the right along the x-axis, which is correct now as at (0,0) the heading is now towards the x-axis - it took me some time to really grasp this.... ;-))
* the interpolated polynomial of third order of the waypoints which are relevant for the starting position (light-green color)
![Waypoint Visualization][image1]

Now the heading of the vehicle system is correct (towards the x-axis), and the starting point in this coordinate system is now:
* x = 0 (because of x-translation)
* y = 0 (because of y-translation)
* psi = 0 (because of rotation)

This simplifies the calculation of the cross-track error (cte) and the orientation error (epsi) tremenously (see lines main.cpp 122-132)!

At the end I transfered this python script to main.cpp which resulted in the the following lines 113+114
* `double x_rot = (ptsx[i]-px) * cos(-psi) - (ptsy[i]-py) * sin(-psi);`
* `double y_rot = (ptsx[i]-px) * sin(-psi) + (ptsy[i]-py) * cos(-psi);`


###The student implements Model Predictive Control that handles a 100 millisecond latency. Student provides details on how they deal with latency.

After rotating and translation to center of vehicle coordinate system I calculate a forcast of my model: where is the vehicle in 100ms? That means I don't feed the current measurement values, but values which contain a prediction for the latency already.
This can be seen in main.cpp lines 149-165. 
* calculate position x in 100ms: `pred_px   = 0 + v * cos(0) * dt;`
* calculate position y in 100ms: `pred_py   = 0 + v * sin(0) * dt;`
* calculate angle  psi in 100ms: `pred_psi  = 0 - v * delta / Lf * dt;`
* calculate speed v in    100ms: `pred_v    = v + a * dt;`
* calculate cte in 100ms:  `pred_cte  = cte - v * sin(epsi) * dt;`
* calculate epsie in 100ms: `pred_epsi = epsi - v * delta / Lf * dt;`
* finally assign this predicted values as input for the solver: `state << pred_px, pred_py, pred_psi, pred_v, pred_cte, pred_epsi;`


Adding this in combination with reducing N to value 8 and thus the prediction horizon to 0.8 seconds only brought a tremendous improvement in terms a stability at high speed. At the end I could run the track with a speed < 100 mph without leaving the road. The limit without considering latency was around 70 mph before...
However this solution still contains a problem: actually the latency should be considered *after* the new values have been calculated. I guess this produces even better results, but haven't tried out ....