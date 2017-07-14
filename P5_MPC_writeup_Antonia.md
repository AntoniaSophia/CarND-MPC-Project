#**Term 2 : MPC Controller Project**


**MPC Controller Project**

The goals / steps of this project are the following:

[//]: # (Image References)

[image0]: ./../camera_cal/calibration1.jpg "calibration1.jpg"


## Rubric Points
Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/896/view) individually and describe how I addressed each point in my implementation.  


###Student describes their model in detail. This includes the state, actuators and update equations.

A just used 

###Student discusses the reasoning behind the chosen N (timestep length) and dt (elapsed duration between timesteps) values. Additionally the student details the previous values tried.

The prediction horizon is N * dt in seconds. That means at N = 10 and dt = 0.1 we have a prediction horizon of 1 second.
Short prediction horizons lead to more responsive controllers, but might be instable in case the horizon of 1 second is too short. Especially in curved roads this is visible. A longer prediction horizon generally should lead to smoother controls but also needs more computing power which might lead to an additional latency.  
In my case I was not able to produce good results with a longer prediction horizon than 1 second....
I even ended up with an optimal prediction horizon of only 0.8 seconds as I could gain more speed considering latency. Possibly the higher speed compensated the lower prediction horizon!?

###If the student preprocesses waypoints, the vehicle state, and/or actuators prior to the MPC procedure it is described.

rotation + translation


###The student implements Model Predictive Control that handles a 100 millisecond latency. Student provides details on how they deal with latency.

After rotating and translation to center of vehicle coordinate system I calculate a forcast of my model: where is the vehicle in 100ms? That means I don't feed the current measurement values, but values which contain a prediction for the latency already.
This can be seen in main.cpp lines 149-165. Adding this in combination with reducing N to value 8 and thus the prediction horizon to 0.8 seconds only brought a tremendous improvement in terms a stability at high speed. At the end I could run the track with a speed < 100 mph without leaving the road. The limit without considering latency was around 70 mph before...
However this solution still contains a problem: actually the latency should be considered *after* the new values have been calculated. I guess this produces even better results, but haven't tried out ....