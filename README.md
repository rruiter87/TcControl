# TcControl

TwinCAT library for PID control and signal filtering.

## Examples

### `Signal`

The basic unit of this library is the `Signal` function block. The most basic usage would be the following where a new value is added and can be retrieved.

```
PROGRAM MAIN
VAR
    signal : Signal;
    value : LREAL;
END_VAR

signal.Update(value:=5); // Add new value to signal
value := signal.Out; // Retrieve the current value, in this case it would be 5
```

The power of signal becomes clear when combined with `.Differentiate`

```
PROGRAM MAIN
VAR
    signal : Signal;
    value : LREAL;
END_VAR

signal.Update(value:=1).Differentiate(deltaTime:=1);
value := signal.Update(value:=2).Differentiate(deltaTime:=1).Out; // 1
```

Or `.Iir`

```
PROGRAM MAIN
VAR
    signal : Signal;
    value : LREAL;
END_VAR

signal.Update(value:=1.4).Iir(decay:=0.5);
value := signal.Update(value:=8.6).Iir(decay:=0.5).Out; // 4.65
```

Or combining both

```
PROGRAM MAIN
VAR
    signal : Signal;
END_VAR

signal.Update(value:=7).Differentiate(deltaTime:=1).Iir(decay:=0.5); // singal.Out = 0
signal.Update(value:=8).Differentiate(deltaTime:=1).Iir(decay:=0.5); // signal.Out = 0.5
signal.Update(value:=9).Differentiate(deltaTime:=1).Iir(decay:=0.5); // signal.Out = 0.75
```

Finally the differentiated/filtered signal can be put into a controller. Currently the library only contains the simple `PidController`

```
PROGRAM MAIN
VAR
    signal : Signal;
    parameters : PidParameters := (Kp:=2, Ki:=0.25, Kd:=0.5);
    pid : PidController;
END_VAR

pid(parameters:=parameters, cycleTime:=1);
signal.Controller := pid;
signal.Update(3).Control(setpoint:=4); // signal.Out = 2.75
signal.Update(3.5).Control(setpoint:=4); // signal.Out = 1.125
```

See the unit tests `Singal_Tests` for more examples.

## Custom controller

You can define your own controller, as long as it implements the `IController` interface. Then you pass it to your signal instance via `signal.Controller := customController;`.

## Other function blocks

The function blocks used in `Signal` can also be used as stand-alone function blocks. The following function blocks are defined.

- `Derivative`: Take derivative of a value.
- `InfiniteImpulseResponse`: Infinite impulse response (IIR) filter.
- `Pid`: PID controller
  - `Pid.DifferentialPartLimit`: Limit the differential part. Convenient when the output is calculated for the first time. The limit prevents it from having a very large value after the first call.
  - `Pid.PreviousIntegralPart`: Set previous integral part on first call. Prevents integrator term for needing to build up.

### `Derivative`

```
PROGRAM MAIN
VAR
    derivative : Derivative;
END_VAR

derivative(value:=1, deltatime:=1); // derivative.Out = 0 (derivative is always 0 on the initial call)
derivative(value:=2, deltatime:=1); // derivative.Out = 1
```

See `Derivative_Tests` for more examples.

### `InfiniteImpulseResponse`

```
PROGRAM MAIN
VAR
    iir : InfiniteImpulseResponse;
END_VAR

iir(new:=5, decay:=0.95); // iir.Out = 0.25
iir(new:=5, decay:=0.95); // iir.Out = 0.4875
iir(new:=5, decay:=0.95); // iir.Out = 0.71313
```

See `InfiniteImpulseResponse_Tests` for more examples.

### `PidController`

```
PROGRAM MAIN
VAR
    pid : PidController;
    parameters : PidParameters := (Kp:=0.1, Ki:=0, Kd:=0.01);
END_VAR

// limits the difference on the initial call
pid.DifferentialPartLimit := 3;
// pass the pid parameters (only need to be done once, unless you change them)
pid(parameters:=parameters, cycleTime:=1);
// Cyclicly call Update
pid.Update(setpoint:=10, actual:=6); // pid.Out = 0.4
pid.Update(setpoint:=10, actual:=8); // pid.Out = 0.18
```
