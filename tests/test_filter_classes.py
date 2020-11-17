import pytest
from unittest import mock
import numpy as np
import numpy.testing as npt
import pyfar.dsp.classes as fo
from pyfar import Signal


def test_filter_init_empty_coefficients():
    filt = fo.Filter(coefficients=None, state=None)
    assert filt._coefficients is None
    assert filt._state is None
    assert filt.comment is None


def test_filter_init_empty_coefficients_with_state():
    with pytest.raises(ValueError):
        fo.Filter(coefficients=None, state=[1, 0])


def test_filter_init():
    coeff = np.array([[[1, 0, 0], [1, 0, 0]]])
    filt = fo.Filter(coefficients=coeff)
    npt.assert_array_equal(filt._coefficients, coeff)


def test_filter_init_empty_state():
    coeff = np.array([[[1, 0, 0], [1, 0, 0]]])
    filt = fo.Filter(coefficients=coeff, state=None)
    npt.assert_array_equal(filt._coefficients, coeff)
    assert filt._state is None


def test_filter_init_with_state():
    coeff = np.array([[[1, 0, 0], [1, 0, 0]]])
    state = np.array([[[1, 0]]])
    filt = fo.Filter(coefficients=coeff, state=state)
    npt.assert_array_equal(filt._coefficients, coeff)
    npt.assert_array_equal(filt._state, state)


def test_filter_comment():
    filt = fo.Filter(coefficients=None, state=None, comment='Bla')
    assert filt.comment == 'Bla'
    filt.comment = 'Blub'
    assert filt.comment == 'Blub'
    filt.comment = 500
    assert filt.comment == '500'


def test_filter_iir_init():
    coeff = np.array([[1, 1/2, 0], [1, 0, 0]])
    filt = fo.FilterIIR(coeff)
    npt.assert_array_equal(filt._coefficients, coeff[np.newaxis])


def test_filter_fir_init():
    coeff = np.array([1, 1/2, 0])
    desired = np.array([[[1, 1/2, 0], [1, 0, 0]]])
    filt = fo.FilterFIR(coeff)
    npt.assert_array_equal(filt._coefficients, desired)


def test_filter_fir_init_multi_dim():
    coeff = np.array([
        [1, 1/2, 0],
        [1, 1/4, 1/8]])
    desired = np.array([
        [[1, 1/2, 0], [1, 0, 0]],
        [[1, 1/4, 1/8], [1, 0, 0]]
        ])
    filt = fo.FilterFIR(coeff)
    npt.assert_array_equal(filt._coefficients, desired)


def test_filter_sos_init():
    sos = np.array([[1, 1/2, 0, 1, 0, 0]])
    filt = fo.FilterSOS(sos)
    npt.assert_array_equal(filt._coefficients, sos[np.newaxis])


def test_filter_iir_process(impulse_mock):
    coeff = np.array([[1, 1/2, 0], [1, 0, 0]])
    filt = fo.FilterIIR(coeff)
    res = filt.process(impulse_mock)

    npt.assert_allclose(res.time[:3], coeff[0])

    coeff = np.array([[1, 1/2, 0], [1, 1/8, 0]])
    filt = fo.FilterIIR(coeff)
    res = filt.process(impulse_mock)

    desired = np.array([
        1.00000000e+000,  3.75000000e-001, -4.68750000e-002,
        5.85937500e-003, -7.32421875e-004,  9.15527344e-005,
       -1.14440918e-005,  1.43051147e-006, -1.78813934e-007,
        2.23517418e-008, -2.79396772e-009,  3.49245965e-010,
       -4.36557457e-011,  5.45696821e-012, -6.82121026e-013,
        8.52651283e-014, -1.06581410e-014,  1.33226763e-015,
       -1.66533454e-016,  2.08166817e-017, -2.60208521e-018,
        3.25260652e-019, -4.06575815e-020,  5.08219768e-021,
       -6.35274710e-022,  7.94093388e-023, -9.92616735e-024,
        1.24077092e-024, -1.55096365e-025,  1.93870456e-026,
       -2.42338070e-027,  3.02922588e-028, -3.78653235e-029,
        4.73316543e-030, -5.91645679e-031,  7.39557099e-032,
       -9.24446373e-033,  1.15555797e-033, -1.44444746e-034,
        1.80555932e-035, -2.25694915e-036,  2.82118644e-037,
       -3.52648305e-038,  4.40810382e-039, -5.51012977e-040,
        6.88766221e-041, -8.60957776e-042,  1.07619722e-042,
       -1.34524653e-043,  1.68155816e-044, -2.10194770e-045,
        2.62743462e-046, -3.28429328e-047,  4.10536659e-048,
       -5.13170824e-049,  6.41463530e-050, -8.01829413e-051,
        1.00228677e-051, -1.25285846e-052,  1.56607307e-053,
       -1.95759134e-054,  2.44698918e-055, -3.05873647e-056,
        3.82342059e-057, -4.77927573e-058,  5.97409467e-059,
       -7.46761833e-060,  9.33452292e-061, -1.16681536e-061,
        1.45851921e-062, -1.82314901e-063,  2.27893626e-064,
       -2.84867032e-065,  3.56083790e-066, -4.45104738e-067,
        5.56380923e-068, -6.95476153e-069,  8.69345192e-070,
       -1.08668149e-070,  1.35835186e-071, -1.69793983e-072,
        2.12242478e-073, -2.65303098e-074,  3.31628873e-075,
       -4.14536091e-076,  5.18170113e-077, -6.47712642e-078,
        8.09640802e-079, -1.01205100e-079,  1.26506375e-080,
       -1.58132969e-081,  1.97666211e-082, -2.47082764e-083,
        3.08853455e-084, -3.86066819e-085,  4.82583524e-086,
       -6.03229405e-087,  7.54036756e-088, -9.42545945e-089,
        1.17818243e-089, -1.47272804e-090,  1.84091005e-091,
       -2.30113756e-092,  2.87642195e-093, -3.59552744e-094,
        4.49440930e-095, -5.61801163e-096,  7.02251453e-097,
       -8.77814317e-098,  1.09726790e-098, -1.37158487e-099,
        1.71448109e-100, -2.14310136e-101,  2.67887670e-102,
       -3.34859587e-103,  4.18574484e-104, -5.23218105e-105,
        6.54022631e-106, -8.17528289e-107,  1.02191036e-107,
       -1.27738795e-108,  1.59673494e-109, -1.99591868e-110,
        2.49489834e-111, -3.11862293e-112,  3.89827866e-113,
       -4.87284833e-114,  6.09106041e-115, -7.61382551e-116,
        9.51728189e-117, -1.18966024e-117,  1.48707530e-118,
       -1.85884412e-119,  2.32355515e-120, -2.90444394e-121,
        3.63055492e-122, -4.53819365e-123,  5.67274206e-124,
       -7.09092758e-125,  8.86365947e-126, -1.10795743e-126,
        1.38494679e-127, -1.73118349e-128,  2.16397936e-129,
       -2.70497420e-130,  3.38121776e-131, -4.22652219e-132,
        5.28315274e-133, -6.60394093e-134,  8.25492616e-135,
       -1.03186577e-135,  1.28983221e-136, -1.61229027e-137,
        2.01536283e-138, -2.51920354e-139,  3.14900443e-140,
       -3.93625553e-141,  4.92031941e-142, -6.15039927e-143,
        7.68799909e-144, -9.60999886e-145,  1.20124986e-145,
       -1.50156232e-146,  1.87695290e-147, -2.34619113e-148,
        2.93273891e-149, -3.66592364e-150,  4.58240455e-151,
       -5.72800568e-152,  7.16000710e-153, -8.95000888e-154,
        1.11875111e-154, -1.39843889e-155,  1.74804861e-156,
       -2.18506076e-157,  2.73132595e-158, -3.41415744e-159,
        4.26769680e-160, -5.33462100e-161,  6.66827625e-162,
       -8.33534531e-163,  1.04191816e-163, -1.30239770e-164,
        1.62799713e-165, -2.03499641e-166,  2.54374552e-167,
       -3.17968190e-168,  3.97460237e-169, -4.96825296e-170,
        6.21031620e-171, -7.76289525e-172,  9.70361907e-173,
       -1.21295238e-173,  1.51619048e-174, -1.89523810e-175,
        2.36904762e-176, -2.96130953e-177,  3.70163691e-178,
       -4.62704614e-179,  5.78380768e-180, -7.22975960e-181,
        9.03719949e-182, -1.12964994e-182,  1.41206242e-183,
       -1.76507803e-184,  2.20634753e-185, -2.75793442e-186,
        3.44741802e-187, -4.30927252e-188,  5.38659066e-189,
       -6.73323832e-190,  8.41654790e-191, -1.05206849e-191,
        1.31508561e-192, -1.64385701e-193,  2.05482126e-194,
       -2.56852658e-195,  3.21065823e-196, -4.01332278e-197,
        5.01665348e-198, -6.27081685e-199,  7.83852106e-200,
       -9.79815132e-201,  1.22476892e-201, -1.53096114e-202,
        1.91370143e-203, -2.39212679e-204,  2.99015849e-205,
       -3.73769811e-206,  4.67212263e-207, -5.84015329e-208,
        7.30019161e-209, -9.12523952e-210,  1.14065494e-210,
       -1.42581867e-211,  1.78227334e-212, -2.22784168e-213,
        2.78480210e-214, -3.48100262e-215,  4.35125328e-216,
       -5.43906660e-217,  6.79883325e-218, -8.49854156e-219,
        1.06231770e-219, -1.32789712e-220,  1.65987140e-221,
       -2.07483925e-222,  2.59354906e-223, -3.24193633e-224,
        4.05242041e-225, -5.06552551e-226,  6.33190689e-227,
       -7.91488361e-228,  9.89360451e-229, -1.23670056e-229,
        1.54587570e-230, -1.93234463e-231,  2.41543079e-232,
       -3.01928849e-233,  3.77411061e-234, -4.71763826e-235,
        5.89704782e-236, -7.37130978e-237,  9.21413722e-238,
       -1.15176715e-238,  1.43970894e-239, -1.79963618e-240,
        2.24954522e-241, -2.81193153e-242,  3.51491441e-243,
       -4.39364301e-244,  5.49205376e-245, -6.86506720e-246,
        8.58133400e-247, -1.07266675e-247,  1.34083344e-248,
       -1.67604180e-249,  2.09505225e-250, -2.61881531e-251,
        3.27351914e-252, -4.09189892e-253,  5.11487365e-254,
       -6.39359206e-255,  7.99199008e-256, -9.98998760e-257,
        1.24874845e-257, -1.56093556e-258,  1.95116945e-259,
       -2.43896182e-260,  3.04870227e-261, -3.81087784e-262,
        4.76359730e-263, -5.95449662e-264,  7.44312077e-265,
       -9.30390097e-266,  1.16298762e-266, -1.45373453e-267,
        1.81716816e-268, -2.27146020e-269,  2.83932525e-270,
       -3.54915656e-271,  4.43644570e-272, -5.54555712e-273,
        6.93194640e-274, -8.66493300e-275,  1.08311663e-275,
       -1.35389578e-276,  1.69236973e-277, -2.11546216e-278,
        2.64432770e-279, -3.30540962e-280,  4.13176203e-281,
       -5.16470254e-282,  6.45587817e-283, -8.06984771e-284,
        1.00873096e-284, -1.26091371e-285,  1.57614213e-286,
       -1.97017766e-287,  2.46272208e-288, -3.07840260e-289,
        3.84800325e-290, -4.81000406e-291,  6.01250508e-292,
       -7.51563135e-293,  9.39453919e-294, -1.17431740e-294,
        1.46789675e-295, -1.83487094e-296,  2.29358867e-297,
       -2.86698584e-298,  3.58373230e-299, -4.47966537e-300,
        5.59958171e-301, -6.99947714e-302,  8.74934642e-303,
       -1.09366830e-303,  1.36708538e-304, -1.70885672e-305,
        2.13607090e-306, -2.67008863e-307,  3.33761079e-308,
       -4.17201348e-309,  5.21501686e-310, -6.51877107e-311,
        8.14846384e-312, -1.01855798e-312,  1.27319747e-313,
       -1.59149684e-314,  1.98937105e-315, -2.48671382e-316,
        3.10839227e-317, -3.88549034e-318,  4.85686292e-319,
       -6.07107866e-320,  7.58884832e-321, -9.48606040e-322,
        1.18575755e-322, -1.48219694e-323,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000,  0.00000000e+000,  0.00000000e+000,
        0.00000000e+000])

    npt.assert_allclose(res.time, desired)


def test_filter_fir_process(impulse_mock):
    coeff = np.array([1, 1/2, 0])
    filt = fo.FilterFIR(coeff)
    res = filt.process(impulse_mock)

    npt.assert_allclose(res.time[:3], coeff)


def test_filter_iir_process_multi_dim_filt(impulse_mock):
    coeff = np.array([
        [[1, 1/2, 0], [1, 0, 0]],
        [[1, 1/4, 0], [1, 0, 0]]])
    filt = fo.FilterIIR(coeff)

    res = filt.process(impulse_mock)

    npt.assert_allclose(res.time[:, :3], coeff[:, 0])


def test_filter_fir_process_multi_dim_filt(impulse_mock):
    coeff = np.array([
        [1, 1/2, 0],
        [1, 1/4, 0]])

    filt = fo.FilterFIR(coeff)
    res = filt.process(impulse_mock)
    npt.assert_allclose(res.time[:, :3], coeff)


def test_filter_sos_process(impulse_mock):
    sos = np.array([[1, 1/2, 0, 1, 0, 0]])
    filt = fo.FilterSOS(sos)
    coeff = np.array([[1, 1/2, 0], [1, 0, 0]])
    # coeff = np.array([
    #     [[1, 1/2, 0], [1, 0, 0]],
    #     [[1, 1/4, 0], [1, 0, 0]]])
    filt = fo.FilterSOS(sos)
    res = filt.process(impulse_mock)

    npt.assert_allclose(res.time[:3], coeff[0])


def test_filter_sos_process_multi_dim_filt(impulse_mock):
    sos = np.array([
        [[1, 1/2, 0, 1, 0, 0]],
        [[1, 1/4, 0, 1, 0, 0]]])
    coeff = np.array([
        [[1, 1/2, 0], [1, 0, 0]],
        [[1, 1/4, 0], [1, 0, 0]]])
    filt = fo.FilterSOS(sos)
    res = filt.process(impulse_mock)

    npt.assert_allclose(res.time[:, :3], coeff[:, 0])


def test_atleast_3d_first_dim():
    arr = np.array([1, 0, 0])
    desired = np.array([[[1, 0, 0]]])

    arr_3d = fo.atleast_3d_first_dim(arr)
    npt.assert_array_equal(arr_3d, desired)
    arr = np.array([[1, 0, 0], [2, 2, 2]])

    desired = np.array([[[1, 0, 0], [2, 2, 2]]])
    arr_3d = fo.atleast_3d_first_dim(arr)
    npt.assert_array_equal(arr_3d, desired)

    arr = np.ones((2, 3, 5))
    desired = arr.copy()
    arr_3d = fo.atleast_3d_first_dim(arr)
    npt.assert_array_equal(arr_3d, desired)


def test_impulse_mock(impulse_mock):
    n_samples = 1000
    sampling_rate = 2000
    amplitude = 1
    signal_type = 'energy'

    signal = np.atleast_2d(np.zeros(n_samples, dtype=np.double))
    signal[:, 0] = amplitude

    assert impulse_mock.sampling_rate == sampling_rate
    assert impulse_mock.shape == (1,)
    assert impulse_mock.signal_type == signal_type
    npt.assert_allclose(impulse_mock.time, signal)


@pytest.fixture
def impulse_mock():
    """ Generate a signal mock object.
    Returns
    -------
    signal : Signal
        The noise signal
    """
    n_samples = 1000
    sampling_rate = 2000
    amplitude = 1
    signal_type = 'energy'
    shape = (1,)
    domain = 'time'

    signal = np.zeros(n_samples, dtype=np.double)
    signal[0] = amplitude

    # create a mock object of Signal class to test independently
    signal_object = mock.Mock(
        spec_set=Signal(signal, sampling_rate, n_samples, domain, signal_type))
    signal_object.time = np.atleast_2d(signal)
    signal_object.sampling_rate = sampling_rate
    signal_object.domain = domain
    signal_object.signal_type = signal_type
    signal_object.shape = shape

    return signal_object
