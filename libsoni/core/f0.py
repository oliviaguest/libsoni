import numpy as np


def sonify_f0(time_f0: np.ndarray,
              partials: np.ndarray = np.array([1]),
              partials_amplitudes: np.ndarray = np.array([1]),
              duration: int = None,
              fs: int = 22050) -> np.ndarray:
    # TODO: correct documentation
    """This function sonifies a F0 trajectory from a 2D Numpy array.
    The sonification is related to the principle of a so-called numerical oscillator.
    The parameters partials and partials_amplitudes can be used to generate a desired sound through a specific
    overtone behavior.

    Parameters
    ----------
    time_f0 : np.ndarray
        2D array of time positions and f0s
    partials : np.ndarray (default = [1])
        An array containing the desired partials of the fundamental frequencies for sonification.
            An array [1] leads to sonification with only the fundamental frequency core,
            while an array [1,2] causes sonification with the fundamental frequency and twice the fundamental frequency.
    partials_amplitudes : np.ndarray (default = [1])
        Array containing the amplitudes for partials.
            An array [1,0.5] causes the sinusoid with frequency core to have amplitude 1,
            while the sinusoid with frequency 2*core has amplitude 0.5.
    duration : int (default = None)
        Duration of audio (given in samples)
    fs: int (default = 22050)
        Sampling rate (in Samples per second)

    Returns
    -------
    y: np.ndarray
        Sonified f0-trajectory.
    """
    times = time_f0[:, 0]
    f0s = time_f0[:, 1]
    num_samples = int(np.ceil(times[-1] * fs))

    if duration is not None:
        duration_in_sec = duration / fs

        # if duration equals num_samples, do nothing
        if duration == num_samples:
            pass

        # if duration is less than num_samples, crop the arrays
        elif duration < num_samples:
            times = times[times < duration_in_sec]
            f0s = f0s[times < duration_in_sec]

        # if duration is greater than num_samples, append
        else:
            times = np.append(times, duration_in_sec)
            f0s = f0s.append(f0s, 0.0)

        num_samples = int(np.ceil(times[-1] * fs))

    f0s_strached = np.zeros(num_samples)
    f0_sonification = np.zeros(num_samples)

    # Strach f0s_strached to match the given time positions.
    for i, (time, f0) in enumerate(zip(times, f0s)):
        if i == time_f0.shape[0] - 1:
            break
        next_time = times[i+1]
        f0s_strached[int(time*fs):int(next_time*fs)] = f0

    #
    for partial, partial_amplitude in zip(partials, partials_amplitudes):
        phase = 0
        phase_result = []
        for f0 in f0s_strached:
            phase_step = 2 * np.pi * f0 * partial * 1 / fs
            phase += phase_step
            phase_result.append(phase)

        f0_sonification += np.sin(phase_result) * partial_amplitude

    return f0_sonification
