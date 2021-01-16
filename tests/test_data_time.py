import numpy as np
import numpy.testing as npt
import pytest
from pyfar.signal import TimeData as TimeData


def test_data_time_init_with_defaults():
    """
    Test to init without optional parameters.
    Test getter for domain, time, times, length, and n_samples.
    """
    data = [1, 0, -1]
    times = [0, .1, .3]

    time = TimeData(data, times)
    assert isinstance(time, TimeData)
    npt.assert_allclose(time.time, np.atleast_2d(np.asarray(data)))
    npt.assert_allclose(time.times, np.atleast_1d(np.asarray(times)))
    assert time.signal_length == .3
    assert time.n_samples == 3
    assert time.domain == 'time'


def test_data_time_init_wrong_number_of_times():
    """Test if entering a wrong number of times raises an assertion."""
    data = [1, 0, -1]
    times = [0, .1]

    with pytest.raises(ValueError):
        TimeData(data, times)


def test_data_time_setter_time():
    """Test the setter for the time data."""
    data_a = [1, 0, -1]
    data_b = [2, 0, -2]
    times = [0, .1, .3]

    time = TimeData(data_a, times)
    time.time = data_b
    npt.assert_allclose(time.time, np.atleast_2d(np.asarray(data_b)))


def test_reshape():

    # test reshape with tuple
    data_in = TimeData(np.random.rand(6, 256), range(256))
    data_out = data_in.reshape((3, 2))
    npt.assert_allclose(data_in._data.reshape(3, 2, -1), data_out._data)
    assert id(data_in) != id(data_out)

    data_out = data_in.reshape((3, -1))
    npt.assert_allclose(data_in._data.reshape(3, 2, -1), data_out._data)
    assert id(data_in) != id(data_out)

    # test reshape with int
    data_in = TimeData(np.random.rand(3, 2, 256), range(256))
    data_out = data_in.reshape(6)
    npt.assert_allclose(data_in._data.reshape(6, -1), data_out._data)
    assert id(data_in) != id(data_out)


def test_reshape_exceptions():
    data_in = TimeData(np.random.rand(6, 256), range(256))
    data_out = data_in.reshape((3, 2))
    npt.assert_allclose(data_in._data.reshape(3, 2, -1), data_out._data)
    # test assertion for non-tuple input
    with pytest.raises(ValueError):
        data_out = data_in.reshape([3, 2])

    # test assertion for wrong dimension
    with pytest.raises(ValueError, match='Can not reshape signal of cshape'):
        data_out = data_in.reshape((3, 4))


def test_flatten():

    # test 2D signal (flatten should not change anything)
    x = np.random.rand(2, 256)
    data_in = TimeData(x, range(256))
    data_out = data_in.flatten()

    npt.assert_allclose(data_in._data, data_out._data)
    assert id(data_in) != id(data_out)

    # test 3D signal
    x = np.random.rand(3, 2, 256)
    data_in = TimeData(x, range(256))
    data_out = data_in.flatten()

    npt.assert_allclose(data_in._data.reshape((6, -1)), data_out._data)
    assert id(data_in) != id(data_out)


def test_data_time_find_nearest():
    """Test the find nearest function for a single number and list entry."""
    data = [1, 0, -1]
    times = [0, .1, .3]
    time = TimeData(data, times)

    # test for a single number
    idx = time.find_nearest_time(.15)
    assert idx == 1

    # test for a list
    idx = time.find_nearest_time([.15, .4])
    npt.assert_allclose(idx, np.asarray([1, 2]))


def test_separation_from_data_frequency():
    """Check if attributes from DataFrequency are really not available."""
    data = [1, 0, -1]
    times = [0, .1, .3]
    time = TimeData(data, times)

    with pytest.raises(AttributeError):
        time.freq
    with pytest.raises(AttributeError):
        time.frequencies
    with pytest.raises(AttributeError):
        time.n_bins
    with pytest.raises(AttributeError):
        time.find_nearest_frequency


def test_separation_from_signal():
    """Check if attributes from Signal are really not available."""
    data = [1, 0, -1]
    times = [0, .1, .3]
    time = TimeData(data, times)

    with pytest.raises(AttributeError):
        time.sampling_rate
    with pytest.raises(AttributeError):
        time.domain = 'time'
