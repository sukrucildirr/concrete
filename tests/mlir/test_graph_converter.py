"""
Tests of `GraphConverter` class.
"""

import numpy as np
import pytest

import concrete.numpy as cnp

# pylint: disable=line-too-long


@pytest.mark.parametrize(
    "function,encryption_statuses,inputset,expected_error,expected_message",
    [
        pytest.param(
            lambda x, y: (x - y, x + y),
            {"x": "encrypted", "y": "clear"},
            [(np.random.randint(0, 2 ** 3), np.random.randint(0, 2 ** 3)) for _ in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                       # EncryptedScalar<uint3>
%1 = y                       # ClearScalar<uint3>
%2 = subtract(%0, %1)        # EncryptedScalar<int4>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only a single output is supported
%3 = add(%0, %1)             # EncryptedScalar<uint4>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only a single output is supported
return (%2, %3)

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: x * 1.5,
            {"x": "encrypted"},
            [2.5 * x for x in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                       # EncryptedScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only unsigned integer inputs are supported
%1 = 1.5                     # ClearScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer constants are supported
%2 = multiply(%0, %1)        # EncryptedScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: np.sin(x),
            {"x": "encrypted"},
            range(100),
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x              # EncryptedScalar<uint7>
%1 = sin(%0)        # EncryptedScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
return %1

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x, y: np.concatenate((x, y)),
            {"x": "encrypted", "y": "clear"},
            [
                (
                    np.random.randint(0, 2 ** 3, size=(3, 2)),
                    np.random.randint(0, 2 ** 3, size=(3, 2)),
                )
                for _ in range(100)
            ],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                            # EncryptedTensor<uint3, shape=(3, 2)>
%1 = y                            # ClearTensor<uint3, shape=(3, 2)>
%2 = concatenate((%0, %1))        # EncryptedTensor<uint3, shape=(6, 2)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only all encrypted concatenate is supported
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x, w: cnp.conv2d(x, w),
            {"x": "encrypted", "w": "encrypted"},
            [
                (
                    np.random.randint(0, 2, size=(1, 1, 4, 4)),
                    np.random.randint(0, 2, size=(1, 1, 1, 1)),
                )
                for _ in range(100)
            ],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                                                                               # EncryptedTensor<uint1, shape=(1, 1, 4, 4)>
%1 = w                                                                               # EncryptedTensor<uint1, shape=(1, 1, 1, 1)>
%2 = conv2d(%0, %1, [0], pads=(0, 0, 0, 0), strides=(1, 1), dilations=(1, 1))        # EncryptedTensor<uint1, shape=(1, 1, 4, 4)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only conv2d with encrypted input and clear weight is supported
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x, y: np.dot(x, y),
            {"x": "encrypted", "y": "encrypted"},
            [
                (
                    np.random.randint(0, 2 ** 2, size=(1,)),
                    np.random.randint(0, 2 ** 2, size=(1,)),
                )
                for _ in range(100)
            ],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                  # EncryptedTensor<uint2, shape=(1,)>
%1 = y                  # EncryptedTensor<uint2, shape=(1,)>
%2 = dot(%0, %1)        # EncryptedScalar<uint4>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only dot product between encrypted and clear is supported
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: x[0],
            {"x": "clear"},
            [np.random.randint(0, 2 ** 3, size=(4,)) for _ in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x            # ClearTensor<uint3, shape=(4,)>
%1 = %0[0]        # ClearScalar<uint3>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only encrypted indexing supported
return %1

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x, y: x @ y,
            {"x": "encrypted", "y": "encrypted"},
            [
                (
                    np.random.randint(0, 2 ** 2, size=(1, 1)),
                    np.random.randint(0, 2 ** 2, size=(1, 1)),
                )
                for _ in range(100)
            ],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                     # EncryptedTensor<uint2, shape=(1, 1)>
%1 = y                     # EncryptedTensor<uint2, shape=(1, 1)>
%2 = matmul(%0, %1)        # EncryptedTensor<uint4, shape=(1, 1)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only matrix multiplication between encrypted and clear is supported
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x, y: x * y,
            {"x": "encrypted", "y": "encrypted"},
            [(np.random.randint(0, 2 ** 3), np.random.randint(0, 2 ** 3)) for _ in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                       # EncryptedScalar<uint3>
%1 = y                       # EncryptedScalar<uint3>
%2 = multiply(%0, %1)        # EncryptedScalar<uint6>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only multiplication between encrypted and clear is supported
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: -x,
            {"x": "clear"},
            [np.random.randint(0, 2 ** 3) for _ in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                   # ClearScalar<uint3>
%1 = negative(%0)        # ClearScalar<int4>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only encrypted negation is supported
return %1

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: x.reshape((3, 2)),
            {"x": "clear"},
            [np.random.randint(0, 2 ** 3, size=(2, 3)) for _ in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                                   # ClearTensor<uint3, shape=(2, 3)>
%1 = reshape(%0, newshape=(3, 2))        # ClearTensor<uint3, shape=(3, 2)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only encrypted reshape is supported
return %1

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: x - 1,
            {"x": "clear"},
            [np.random.randint(0, 2 ** 3, size=(2, 3)) for _ in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                       # ClearTensor<uint3, shape=(2, 3)>
%1 = 1                       # ClearScalar<uint1>
%2 = subtract(%0, %1)        # ClearTensor<int4, shape=(2, 3)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only subtraction of encrypted from clear is supported
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: np.sum(x),
            {"x": "clear"},
            [np.random.randint(0, 2, size=(1,)) for _ in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x              # ClearTensor<uint1, shape=(1,)>
%1 = sum(%0)        # ClearScalar<uint1>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only encrypted sum is supported
return %1

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x, y: np.maximum(x, y),
            {"x": "encrypted", "y": "clear"},
            [
                (np.random.randint(0, 2, size=(1,)), np.random.randint(0, 2, size=(1,)))
                for _ in range(100)
            ],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                      # EncryptedTensor<uint1, shape=(1,)>
%1 = y                      # ClearTensor<uint1, shape=(1,)>
%2 = maximum(%0, %1)        # EncryptedTensor<uint1, shape=(1,)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only single input table lookups are supported
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: np.maximum(x, np.array([3])),
            {"x": "clear"},
            [np.random.randint(0, 2, size=(1,)) for _ in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                      # ClearTensor<uint1, shape=(1,)>
%1 = [3]                    # ClearTensor<uint2, shape=(1,)>
%2 = maximum(%0, %1)        # ClearTensor<uint2, shape=(1,)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ one of the operands must be encrypted
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: x + 200,
            {"x": "encrypted"},
            range(200),
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR:

%0 = x                  # EncryptedScalar<uint8>
%1 = 200                # ClearScalar<uint8>
%2 = add(%0, %1)        # EncryptedScalar<uint9>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only up to 8-bit integers are supported
return %2

            """,  # noqa: E501
        ),
        pytest.param(
            lambda x: np.transpose(x),
            {"x": "clear"},
            [np.random.randint(0, 2, size=(3, 2)) for _ in range(100)],
            RuntimeError,
            """

Function you are trying to compile cannot be converted to MLIR

%0 = x                    # ClearTensor<uint1, shape=(3, 2)>
%1 = transpose(%0)        # ClearTensor<uint1, shape=(2, 3)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only encrypted transpose is supported
return %1

            """,  # noqa: E501
        ),
    ],
)
def test_graph_converter_bad_convert(
    function,
    encryption_statuses,
    inputset,
    expected_error,
    expected_message,
    helpers,
):
    """
    Test unsupported graph conversion.
    """

    configuration = helpers.configuration()
    compiler = cnp.Compiler(function, encryption_statuses, configuration)

    with pytest.raises(expected_error) as excinfo:
        compiler.compile(inputset)

    helpers.check_str(expected_message, str(excinfo.value))


# pylint: enable=line-too-long
