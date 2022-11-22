# TcControl

TwinCAT library for PID control.

## Contains

- `InfiniteImpulseResponse`: Infinite impulse response (IIR) filter.
- `Pid`: PID controller
  - `Pid.DifferentialPartLimit`: Limit the differential part. Convenient when the output is calculated for the first time. The limit prevents it from having a very large value after the first call.
  - `Pid.PreviousIntegralPart`: Set previous integral part on first call. Prevents integrator term for needing to build up.
