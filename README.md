<p align="center"><img src="banner.svg" alt="Gurmaan Singh: software for sensors, tracking and control" width="100%"></p>

<p align="center"><img src="badges.svg" alt="C++20, CMake, Python, Linux and Windows, open to a summer job in 2027"></p>

<p align="center"><img src="roles.svg" alt="Multi-target tracking, real-time C++, sensor data, testing" width="620"></p>

I'm an engineering student at Fontys University of Applied Sciences. I like software that has to be right in real time: sensors, tracking, control, and anything that runs close to hardware.

## Looking for

**Summer job or internship, summer 2027**, in defence and security software: tracking and sensor fusion, command and control, real-time or embedded C++. Open to Sweden, Norway, Finland, Denmark and the Netherlands.

## Featured: vakt

[**vakt**](https://github.com/gurmaan-singh/vakt) (Swedish for *guard* or *watch*) is a multi-target radar tracker. It takes noisy measurements of several aircraft, keeps one track per target and says where each is heading. C++20, no frameworks.

<p align="center"><img src="results.svg" alt="vakt results: the IMM cuts identity switches from 271 to 60 and mean GOSPA from 144 m to 124 m" width="760"></p>

| Part | How |
|---|---|
| **Filters** | IMM (constant velocity + coordinated turn) over extended Kalman filters |
| **Association** | Hungarian global nearest neighbour, M-of-N track confirmation |
| **Evaluation** | seeded Monte Carlo runs, GOSPA, RMS error, identity switches |
| **Interfaces** | ASTERIX CAT048 in and out, JSON track picture over UDP |
| **Concurrency** | rx, tracker and tx threads joined by lock-free SPSC queues |
| **Quality** | 34 unit tests, zero warnings at MSVC /W4 |

## Skills

- **Languages:** C++20, Python, MATLAB
- **Methods:** Kalman filtering, multi-target tracking, data association, Monte Carlo evaluation, control (PID and optimised)
- **Tools:** CMake, GoogleTest, Git, Linux and Windows, KiCad, Arduino and PlatformIO

## Also

- **AUV autopilot simulation:** a control study comparing a PID controller with an optimised one for a small underwater vehicle.

## Next

A web map of the live track picture (MapLibre, military symbols) fed by vakt, with ADS-B as a real data source.
