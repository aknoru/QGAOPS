/* Auto-generated committed golden regression test vectors for QGAOPS-QGPU */
/* Generated strictly from software/reference_model/qgaops_reference */
#ifndef TEST_VECTORS_H
#define TEST_VECTORS_H

#include <stdint.h>
#include <stdbool.h>
#include "../include/qgpu_types.h"
#include "../include/qgpu_operations.h"

typedef struct {
    int test_id;
    const char *category;
    uint32_t opcode;
    const char *op_name;
    int32_t a[GA_BLADES];
    int32_t b[GA_BLADES];
    int32_t expected[GA_BLADES];
    uint32_t expected_status;
    const char *description;
} test_vector_t;

#define NUM_TEST_VECTORS 285

static const test_vector_t TEST_VECTORS[NUM_TEST_VECTORS] = {
    {
        1, "EXHAUSTIVE_GP", 1, "geometric_product",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair 1 * 1"
    },
    {
        2, "EXHAUSTIVE_GP", 1, "geometric_product",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair 1 * e1"
    },
    {
        3, "EXHAUSTIVE_GP", 1, "geometric_product",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "GP basis pair 1 * e2"
    },
    {
        4, "EXHAUSTIVE_GP", 1, "geometric_product",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "GP basis pair 1 * e3"
    },
    {
        5, "EXHAUSTIVE_GP", 1, "geometric_product",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "GP basis pair 1 * e12"
    },
    {
        6, "EXHAUSTIVE_GP", 1, "geometric_product",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        0, "GP basis pair 1 * e13"
    },
    {
        7, "EXHAUSTIVE_GP", 1, "geometric_product",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "GP basis pair 1 * e23"
    },
    {
        8, "EXHAUSTIVE_GP", 1, "geometric_product",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "GP basis pair 1 * e123"
    },
    {
        9, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e1 * 1"
    },
    {
        10, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e1 * e1"
    },
    {
        11, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "GP basis pair e1 * e2"
    },
    {
        12, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        0, "GP basis pair e1 * e3"
    },
    {
        13, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "GP basis pair e1 * e12"
    },
    {
        14, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "GP basis pair e1 * e13"
    },
    {
        15, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "GP basis pair e1 * e23"
    },
    {
        16, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "GP basis pair e1 * e123"
    },
    {
        17, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "GP basis pair e2 * 1"
    },
    {
        18, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, -65536, 0, 0, 0},
        0, "GP basis pair e2 * e1"
    },
    {
        19, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e2 * e2"
    },
    {
        20, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "GP basis pair e2 * e3"
    },
    {
        21, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e2 * e12"
    },
    {
        22, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, -65536},
        0, "GP basis pair e2 * e13"
    },
    {
        23, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "GP basis pair e2 * e23"
    },
    {
        24, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, -65536, 0, 0},
        0, "GP basis pair e2 * e123"
    },
    {
        25, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "GP basis pair e3 * 1"
    },
    {
        26, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, -65536, 0, 0},
        0, "GP basis pair e3 * e1"
    },
    {
        27, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, -65536, 0},
        0, "GP basis pair e3 * e2"
    },
    {
        28, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e3 * e3"
    },
    {
        29, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "GP basis pair e3 * e12"
    },
    {
        30, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e3 * e13"
    },
    {
        31, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, -65536, 0, 0, 0, 0, 0},
        0, "GP basis pair e3 * e23"
    },
    {
        32, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "GP basis pair e3 * e123"
    },
    {
        33, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "GP basis pair e12 * 1"
    },
    {
        34, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, -65536, 0, 0, 0, 0, 0},
        0, "GP basis pair e12 * e1"
    },
    {
        35, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e12 * e2"
    },
    {
        36, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "GP basis pair e12 * e3"
    },
    {
        37, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {-65536, 0, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e12 * e12"
    },
    {
        38, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, -65536, 0},
        0, "GP basis pair e12 * e13"
    },
    {
        39, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        0, "GP basis pair e12 * e23"
    },
    {
        40, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, -65536, 0, 0, 0, 0},
        0, "GP basis pair e12 * e123"
    },
    {
        41, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        0, "GP basis pair e13 * 1"
    },
    {
        42, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, -65536, 0, 0, 0, 0},
        0, "GP basis pair e13 * e1"
    },
    {
        43, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, -65536},
        0, "GP basis pair e13 * e2"
    },
    {
        44, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e13 * e3"
    },
    {
        45, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "GP basis pair e13 * e12"
    },
    {
        46, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {-65536, 0, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e13 * e13"
    },
    {
        47, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, -65536, 0, 0, 0},
        0, "GP basis pair e13 * e23"
    },
    {
        48, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "GP basis pair e13 * e123"
    },
    {
        49, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "GP basis pair e23 * 1"
    },
    {
        50, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "GP basis pair e23 * e1"
    },
    {
        51, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, -65536, 0, 0, 0, 0},
        0, "GP basis pair e23 * e2"
    },
    {
        52, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "GP basis pair e23 * e3"
    },
    {
        53, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, -65536, 0, 0},
        0, "GP basis pair e23 * e12"
    },
    {
        54, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "GP basis pair e23 * e13"
    },
    {
        55, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {-65536, 0, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e23 * e23"
    },
    {
        56, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e23 * e123"
    },
    {
        57, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "GP basis pair e123 * 1"
    },
    {
        58, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "GP basis pair e123 * e1"
    },
    {
        59, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, -65536, 0, 0},
        0, "GP basis pair e123 * e2"
    },
    {
        60, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "GP basis pair e123 * e3"
    },
    {
        61, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, -65536, 0, 0, 0, 0},
        0, "GP basis pair e123 * e12"
    },
    {
        62, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "GP basis pair e123 * e13"
    },
    {
        63, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e123 * e23"
    },
    {
        64, "EXHAUSTIVE_GP", 1, "geometric_product",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {-65536, 0, 0, 0, 0, 0, 0, 0},
        0, "GP basis pair e123 * e123"
    },
    {
        65, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair 1 ^ 1"
    },
    {
        66, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair 1 ^ e1"
    },
    {
        67, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "Wedge basis pair 1 ^ e2"
    },
    {
        68, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "Wedge basis pair 1 ^ e3"
    },
    {
        69, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "Wedge basis pair 1 ^ e12"
    },
    {
        70, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        0, "Wedge basis pair 1 ^ e13"
    },
    {
        71, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "Wedge basis pair 1 ^ e23"
    },
    {
        72, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "Wedge basis pair 1 ^ e123"
    },
    {
        73, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e1 ^ 1"
    },
    {
        74, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e1 ^ e1"
    },
    {
        75, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "Wedge basis pair e1 ^ e2"
    },
    {
        76, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        0, "Wedge basis pair e1 ^ e3"
    },
    {
        77, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e1 ^ e12"
    },
    {
        78, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e1 ^ e13"
    },
    {
        79, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "Wedge basis pair e1 ^ e23"
    },
    {
        80, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e1 ^ e123"
    },
    {
        81, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e2 ^ 1"
    },
    {
        82, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, -65536, 0, 0, 0},
        0, "Wedge basis pair e2 ^ e1"
    },
    {
        83, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e2 ^ e2"
    },
    {
        84, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "Wedge basis pair e2 ^ e3"
    },
    {
        85, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e2 ^ e12"
    },
    {
        86, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, -65536},
        0, "Wedge basis pair e2 ^ e13"
    },
    {
        87, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e2 ^ e23"
    },
    {
        88, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e2 ^ e123"
    },
    {
        89, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "Wedge basis pair e3 ^ 1"
    },
    {
        90, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, -65536, 0, 0},
        0, "Wedge basis pair e3 ^ e1"
    },
    {
        91, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, -65536, 0},
        0, "Wedge basis pair e3 ^ e2"
    },
    {
        92, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e3 ^ e3"
    },
    {
        93, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "Wedge basis pair e3 ^ e12"
    },
    {
        94, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e3 ^ e13"
    },
    {
        95, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e3 ^ e23"
    },
    {
        96, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e3 ^ e123"
    },
    {
        97, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "Wedge basis pair e12 ^ 1"
    },
    {
        98, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e12 ^ e1"
    },
    {
        99, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e12 ^ e2"
    },
    {
        100, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "Wedge basis pair e12 ^ e3"
    },
    {
        101, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e12 ^ e12"
    },
    {
        102, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e12 ^ e13"
    },
    {
        103, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e12 ^ e23"
    },
    {
        104, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e12 ^ e123"
    },
    {
        105, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        0, "Wedge basis pair e13 ^ 1"
    },
    {
        106, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e13 ^ e1"
    },
    {
        107, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, -65536},
        0, "Wedge basis pair e13 ^ e2"
    },
    {
        108, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e13 ^ e3"
    },
    {
        109, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e13 ^ e12"
    },
    {
        110, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e13 ^ e13"
    },
    {
        111, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e13 ^ e23"
    },
    {
        112, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e13 ^ e123"
    },
    {
        113, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "Wedge basis pair e23 ^ 1"
    },
    {
        114, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "Wedge basis pair e23 ^ e1"
    },
    {
        115, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e23 ^ e2"
    },
    {
        116, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e23 ^ e3"
    },
    {
        117, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e23 ^ e12"
    },
    {
        118, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e23 ^ e13"
    },
    {
        119, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e23 ^ e23"
    },
    {
        120, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e23 ^ e123"
    },
    {
        121, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "Wedge basis pair e123 ^ 1"
    },
    {
        122, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e123 ^ e1"
    },
    {
        123, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e123 ^ e2"
    },
    {
        124, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e123 ^ e3"
    },
    {
        125, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e123 ^ e12"
    },
    {
        126, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e123 ^ e13"
    },
    {
        127, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e123 ^ e23"
    },
    {
        128, "EXHAUSTIVE_WEDGE", 2, "wedge",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Wedge basis pair e123 ^ e123"
    },
    {
        129, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair 1 . 1"
    },
    {
        130, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair 1 . e1"
    },
    {
        131, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair 1 . e2"
    },
    {
        132, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "Hestenes inner basis pair 1 . e3"
    },
    {
        133, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "Hestenes inner basis pair 1 . e12"
    },
    {
        134, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        0, "Hestenes inner basis pair 1 . e13"
    },
    {
        135, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "Hestenes inner basis pair 1 . e23"
    },
    {
        136, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "Hestenes inner basis pair 1 . e123"
    },
    {
        137, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e1 . 1"
    },
    {
        138, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e1 . e1"
    },
    {
        139, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e1 . e2"
    },
    {
        140, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e1 . e3"
    },
    {
        141, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e1 . e12"
    },
    {
        142, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e1 . e13"
    },
    {
        143, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e1 . e23"
    },
    {
        144, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "Hestenes inner basis pair e1 . e123"
    },
    {
        145, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e2 . 1"
    },
    {
        146, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e2 . e1"
    },
    {
        147, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e2 . e2"
    },
    {
        148, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e2 . e3"
    },
    {
        149, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e2 . e12"
    },
    {
        150, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e2 . e13"
    },
    {
        151, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e2 . e23"
    },
    {
        152, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, -65536, 0, 0},
        0, "Hestenes inner basis pair e2 . e123"
    },
    {
        153, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e3 . 1"
    },
    {
        154, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e3 . e1"
    },
    {
        155, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e3 . e2"
    },
    {
        156, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e3 . e3"
    },
    {
        157, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e3 . e12"
    },
    {
        158, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e3 . e13"
    },
    {
        159, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, -65536, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e3 . e23"
    },
    {
        160, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "Hestenes inner basis pair e3 . e123"
    },
    {
        161, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e12 . 1"
    },
    {
        162, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e12 . e1"
    },
    {
        163, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e12 . e2"
    },
    {
        164, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e12 . e3"
    },
    {
        165, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {-65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e12 . e12"
    },
    {
        166, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e12 . e13"
    },
    {
        167, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e12 . e23"
    },
    {
        168, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, -65536, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e12 . e123"
    },
    {
        169, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e13 . 1"
    },
    {
        170, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e13 . e1"
    },
    {
        171, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e13 . e2"
    },
    {
        172, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e13 . e3"
    },
    {
        173, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e13 . e12"
    },
    {
        174, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {-65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e13 . e13"
    },
    {
        175, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e13 . e23"
    },
    {
        176, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e13 . e123"
    },
    {
        177, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e23 . 1"
    },
    {
        178, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e23 . e1"
    },
    {
        179, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e23 . e2"
    },
    {
        180, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e23 . e3"
    },
    {
        181, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e23 . e12"
    },
    {
        182, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e23 . e13"
    },
    {
        183, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {-65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e23 . e23"
    },
    {
        184, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e23 . e123"
    },
    {
        185, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e123 . 1"
    },
    {
        186, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e123 . e1"
    },
    {
        187, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e123 . e2"
    },
    {
        188, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e123 . e3"
    },
    {
        189, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e123 . e12"
    },
    {
        190, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e123 . e13"
    },
    {
        191, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e123 . e23"
    },
    {
        192, "EXHAUSTIVE_INNER", 3, "hestenes_inner",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {-65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Hestenes inner basis pair e123 . e123"
    },
    {
        193, "ARITHMETIC_ADD", 4, "add",
        {65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536},
        {131072, 131072, 131072, 131072, 131072, 131072, 131072, 131072},
        {196608, 196608, 196608, 196608, 196608, 196608, 196608, 196608},
        0, "Add uniform_positive"
    },
    {
        194, "ARITHMETIC_SUB", 5, "subtract",
        {65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536},
        {131072, 131072, 131072, 131072, 131072, 131072, 131072, 131072},
        {-65536, -65536, -65536, -65536, -65536, -65536, -65536, -65536},
        0, "Subtract uniform_positive"
    },
    {
        195, "ARITHMETIC_ADD", 4, "add",
        {-65536, -65536, -65536, -65536, -65536, -65536, -65536, -65536},
        {65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Add cancellation_to_zero"
    },
    {
        196, "ARITHMETIC_SUB", 5, "subtract",
        {-65536, -65536, -65536, -65536, -65536, -65536, -65536, -65536},
        {65536, 65536, 65536, 65536, 65536, 65536, 65536, 65536},
        {-131072, -131072, -131072, -131072, -131072, -131072, -131072, -131072},
        0, "Subtract cancellation_to_zero"
    },
    {
        197, "ARITHMETIC_ADD", 4, "add",
        {2147418112, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {2147483647, 0, 0, 0, 0, 0, 0, 0},
        4, "Add near_max_scalar"
    },
    {
        198, "ARITHMETIC_SUB", 5, "subtract",
        {2147418112, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {2147352576, 0, 0, 0, 0, 0, 0, 0},
        0, "Subtract near_max_scalar"
    },
    {
        199, "ARITHMETIC_ADD", 4, "add",
        {-2147418112, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {-2147352576, 0, 0, 0, 0, 0, 0, 0},
        0, "Add near_min_scalar"
    },
    {
        200, "ARITHMETIC_SUB", 5, "subtract",
        {-2147418112, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {-2147483648, 0, 0, 0, 0, 0, 0, 0},
        0, "Subtract near_min_scalar"
    },
    {
        201, "ARITHMETIC_ADD", 4, "add",
        {32768, -16384, 98304, -131072, 8192, -4096, 196608, -81920},
        {32768, 16384, -98304, 131072, -8192, 4096, -196608, 81920},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Add mixed_grade_cancellation"
    },
    {
        202, "ARITHMETIC_SUB", 5, "subtract",
        {32768, -16384, 98304, -131072, 8192, -4096, 196608, -81920},
        {32768, 16384, -98304, 131072, -8192, 4096, -196608, 81920},
        {0, -32768, 196608, -262144, 16384, -8192, 393216, -163840},
        0, "Subtract mixed_grade_cancellation"
    },
    {
        203, "SCALAR_MUL", 6, "scalar_mul",
        {65536, 131072, -196608, 262144, -32768, 98304, -163840, 49152},
        {131072, 0, 0, 0, 0, 0, 0, 0},
        {131072, 262144, -393216, 524288, -65536, 196608, -327680, 98304},
        0, "Scalar mul scale_by_positive_2"
    },
    {
        204, "SCALAR_MUL", 6, "scalar_mul",
        {65536, 131072, -196608, 262144, -32768, 98304, -163840, 49152},
        {-65536, 0, 0, 0, 0, 0, 0, 0},
        {-65536, -131072, 196608, -262144, 32768, -98304, 163840, -49152},
        0, "Scalar mul scale_by_negative_1"
    },
    {
        205, "SCALAR_MUL", 6, "scalar_mul",
        {65536, 131072, -196608, 262144, -32768, 98304, -163840, 49152},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "Scalar mul scale_by_zero"
    },
    {
        206, "SCALAR_MUL", 6, "scalar_mul",
        {65536, 131072, -196608, 262144, -32768, 98304, -163840, 49152},
        {16384, 0, 0, 0, 0, 0, 0, 0},
        {16384, 32768, -49152, 65536, -8192, 24576, -40960, 12288},
        0, "Scalar mul scale_by_fraction_quarter"
    },
    {
        207, "SCALAR_MUL", 6, "scalar_mul",
        {65536000, 65536000, 65536000, 65536000, 65536000, 65536000, 65536000, 65536000},
        {65536000, 0, 0, 0, 0, 0, 0, 0},
        {2147483647, 2147483647, 2147483647, 2147483647, 2147483647, 2147483647, 2147483647, 2147483647},
        4, "Scalar mul scale_large_overflow"
    },
    {
        208, "GRADE_PROJECTION", 7, "grade_proj",
        {65536, 131072, 196608, 262144, 327680, 393216, 458752, 524288},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Project onto grade 0"
    },
    {
        209, "GRADE_PROJECTION", 7, "grade_proj",
        {65536, 131072, 196608, 262144, 327680, 393216, 458752, 524288},
        {1, 0, 0, 0, 0, 0, 0, 0},
        {0, 131072, 196608, 262144, 0, 0, 0, 0},
        0, "Project onto grade 1"
    },
    {
        210, "GRADE_PROJECTION", 7, "grade_proj",
        {65536, 131072, 196608, 262144, 327680, 393216, 458752, 524288},
        {2, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 327680, 393216, 458752, 0},
        0, "Project onto grade 2"
    },
    {
        211, "GRADE_PROJECTION", 7, "grade_proj",
        {65536, 131072, 196608, 262144, 327680, 393216, 458752, 524288},
        {3, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 524288},
        0, "Project onto grade 3"
    },
    {
        212, "REVERSION", 8, "reverse",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Reversion of basis blade 1"
    },
    {
        213, "REVERSION", 8, "reverse",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        0, "Reversion of basis blade e1"
    },
    {
        214, "REVERSION", 8, "reverse",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "Reversion of basis blade e2"
    },
    {
        215, "REVERSION", 8, "reverse",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 65536, 0, 0, 0, 0},
        0, "Reversion of basis blade e3"
    },
    {
        216, "REVERSION", 8, "reverse",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, -65536, 0, 0, 0},
        0, "Reversion of basis blade e12"
    },
    {
        217, "REVERSION", 8, "reverse",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, -65536, 0, 0},
        0, "Reversion of basis blade e13"
    },
    {
        218, "REVERSION", 8, "reverse",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, -65536, 0},
        0, "Reversion of basis blade e23"
    },
    {
        219, "REVERSION", 8, "reverse",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, -65536},
        0, "Reversion of basis blade e123"
    },
    {
        220, "REVERSION", 8, "reverse",
        {98304, -131072, 212992, -294912, 49152, -81920, 163840, -32768},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {98304, -131072, 212992, -294912, -49152, 81920, -163840, 32768},
        0, "Reversion of mixed multivector"
    },
    {
        221, "GRADE_INVOLUTION", 9, "grade_involution",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Grade involution of basis blade 1"
    },
    {
        222, "GRADE_INVOLUTION", 9, "grade_involution",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "Grade involution of basis blade e1"
    },
    {
        223, "GRADE_INVOLUTION", 9, "grade_involution",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, -65536, 0, 0, 0, 0, 0},
        0, "Grade involution of basis blade e2"
    },
    {
        224, "GRADE_INVOLUTION", 9, "grade_involution",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, -65536, 0, 0, 0, 0},
        0, "Grade involution of basis blade e3"
    },
    {
        225, "GRADE_INVOLUTION", 9, "grade_involution",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 65536, 0, 0, 0},
        0, "Grade involution of basis blade e12"
    },
    {
        226, "GRADE_INVOLUTION", 9, "grade_involution",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 65536, 0, 0},
        0, "Grade involution of basis blade e13"
    },
    {
        227, "GRADE_INVOLUTION", 9, "grade_involution",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 65536, 0},
        0, "Grade involution of basis blade e23"
    },
    {
        228, "GRADE_INVOLUTION", 9, "grade_involution",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, -65536},
        0, "Grade involution of basis blade e123"
    },
    {
        229, "GRADE_INVOLUTION", 9, "grade_involution",
        {98304, -131072, 212992, -294912, 49152, -81920, 163840, -32768},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {98304, 131072, -212992, 294912, 49152, -81920, 163840, 32768},
        0, "Grade involution of mixed multivector"
    },
    {
        230, "CLIFFORD_CONJUGATION", 10, "clifford_conj",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Clifford conjugation of basis blade 1"
    },
    {
        231, "CLIFFORD_CONJUGATION", 10, "clifford_conj",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "Clifford conjugation of basis blade e1"
    },
    {
        232, "CLIFFORD_CONJUGATION", 10, "clifford_conj",
        {0, 0, 65536, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, -65536, 0, 0, 0, 0, 0},
        0, "Clifford conjugation of basis blade e2"
    },
    {
        233, "CLIFFORD_CONJUGATION", 10, "clifford_conj",
        {0, 0, 0, 65536, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, -65536, 0, 0, 0, 0},
        0, "Clifford conjugation of basis blade e3"
    },
    {
        234, "CLIFFORD_CONJUGATION", 10, "clifford_conj",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, -65536, 0, 0, 0},
        0, "Clifford conjugation of basis blade e12"
    },
    {
        235, "CLIFFORD_CONJUGATION", 10, "clifford_conj",
        {0, 0, 0, 0, 0, 65536, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, -65536, 0, 0},
        0, "Clifford conjugation of basis blade e13"
    },
    {
        236, "CLIFFORD_CONJUGATION", 10, "clifford_conj",
        {0, 0, 0, 0, 0, 0, 65536, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, -65536, 0},
        0, "Clifford conjugation of basis blade e23"
    },
    {
        237, "CLIFFORD_CONJUGATION", 10, "clifford_conj",
        {0, 0, 0, 0, 0, 0, 0, 65536},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 65536},
        0, "Clifford conjugation of basis blade e123"
    },
    {
        238, "CLIFFORD_CONJUGATION", 10, "clifford_conj",
        {98304, -131072, 212992, -294912, 49152, -81920, 163840, -32768},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {98304, 131072, -212992, 294912, -49152, 81920, -163840, -32768},
        0, "Clifford conjugation of mixed multivector"
    },
    {
        239, "ROTOR_SANDWICH", 11, "sandwich",
        {46341, 0, 0, 0, -46341, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 65536, 0, 0, 0, 0, 0},
        0, "Rotor 90 deg rotation of e1 in xy-plane -> e2"
    },
    {
        240, "ROTOR_SANDWICH", 11, "sandwich",
        {0, 0, 0, 0, -65536, 0, 0, 0},
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, -65536, 0, 0, 0, 0, 0, 0},
        0, "Rotor 180 deg rotation of e1 -> -e1"
    },
    {
        241, "ROTOR_SANDWICH", 11, "sandwich",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 98304, -131072, 229376, 0, 0, 0, 0},
        {0, 98304, -131072, 229376, 0, 0, 0, 0},
        0, "Identity rotor rotation R=1"
    },
    {
        242, "ROTOR_NORM", 12, "rotor_norm",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Rotor norm squared unit_scalar"
    },
    {
        243, "ROTOR_NORM", 12, "rotor_norm",
        {0, 65536, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Rotor norm squared basis_e1"
    },
    {
        244, "ROTOR_NORM", 12, "rotor_norm",
        {0, 0, 0, 0, 65536, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Rotor norm squared basis_e12"
    },
    {
        245, "ROTOR_NORM", 12, "rotor_norm",
        {32768, 32768, 32768, 32768, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        0, "Rotor norm squared four_halves_norm_1"
    },
    {
        246, "ROTOR_NORM", 12, "rotor_norm",
        {65536, -131072, 196608, -262144, 32768, -98304, 131072, -32768},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {2408448, 0, 0, 0, 0, 0, 0, 0},
        0, "Rotor norm squared mixed_multivector_norm"
    },
    {
        247, "FIXED_POINT_ROUNDING", 1, "geometric_product",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "rounding_tie_down_to_even_0"
    },
    {
        248, "FIXED_POINT_ROUNDING", 1, "geometric_product",
        {196608, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        0, "rounding_tie_up_to_even_2"
    },
    {
        249, "FIXED_POINT_SATURATION", 4, "add",
        {2147483647, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {2147483647, 0, 0, 0, 0, 0, 0, 0},
        4, "Addition positive overflow saturating to MAX"
    },
    {
        250, "FIXED_POINT_SATURATION", 5, "subtract",
        {-2147483648, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {-2147483648, 0, 0, 0, 0, 0, 0, 0},
        4, "Subtraction negative underflow saturating to MIN"
    },
    {
        251, "FIXED_POINT_ACCUMULATOR_STRESS", 1, "geometric_product",
        {65536000, 65536000, 65536000, 65536000, 65536000, 65536000, 65536000, 65536000},
        {65536000, 65536000, 65536000, 65536000, 65536000, 65536000, 65536000, 65536000},
        {0, 0, 2147483647, 0, 2147483647, 0, 2147483647, 2147483647},
        4, "Large multivector product stress testing 67-bit accumulator"
    },
    {
        252, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {237536, -55251, -309034, -71917, -117317, -206497, -4161, 205569},
        {-224538, 48360, 112670, -249102, -244595, -234571, -106893, -215324},
        {-1620883, -141388, 1601150, 586643, -1218528, -1072584, 1609106, -1434486},
        0, "Randomized geometric_product seed 4242 rep 0"
    },
    {
        253, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {237536, -55251, -309034, -71917, -117317, -206497, -4161, 205569},
        {-224538, 48360, 112670, -249102, -244595, -234571, -106893, -215324},
        {-813841, 364581, 1467179, -656473, -351536, 120368, 925098, -1434486},
        0, "Randomized wedge seed 4242 rep 0"
    },
    {
        254, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {237536, -55251, -309034, -71917, -117317, -206497, -4161, 205569},
        {-224538, 48360, 112670, -249102, -244595, -234571, -106893, -215324},
        {-1620883, -1249184, 1175745, -586517, -650248, -1865562, -205903, -780444},
        0, "Randomized hestenes_inner seed 4242 rep 0"
    },
    {
        255, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {-171884, 123568, 110334, -174518, -35672, 270444, -107178, -118641},
        {-217427, -107328, -94665, -69122, -117426, -126457, -217740, 66404},
        {614627, -786813, -361428, 266924, 1482177, -1338407, 324294, 938297},
        0, "Randomized geometric_product seed 4242 rep 1"
    },
    {
        256, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {-171884, 123568, 110334, -174518, -35672, 270444, -107178, -118641},
        {-217427, -107328, -94665, -69122, -117426, -126457, -217740, 66404},
        {570255, -128465, -117770, 760283, 428529, -981717, 558199, 938297},
        0, "Randomized wedge seed 4242 rep 1"
    },
    {
        257, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {-171884, 123568, 110334, -174518, -35672, 270444, -107178, -118641},
        {-217427, -107328, -94665, -69122, -117426, -126457, -217740, 66404},
        {614627, 251039, -278926, -387580, 131149, 219869, 696280, -174161},
        0, "Randomized hestenes_inner seed 4242 rep 1"
    },
    {
        258, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {-9908, -38895, 202842, 146516, -14265, -218205, 72923, 269208},
        {-12743, 274842, 251050, 148967, 214254, 108735, -22004, -177719},
        {2112070, -1202724, 1108605, -466691, -766950, -1391686, 433724, 1239310},
        0, "Randomized geometric_product seed 4242 rep 2"
    },
    {
        259, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {-9908, -38895, 202842, 146516, -14265, -218205, 72923, 269208},
        {-12743, 274842, 251050, 148967, 214254, 108735, -22004, -177719},
        {1927, -33989, -77396, -51010, -1029284, -676874, -111043, 1239310},
        0, "Randomized wedge seed 4242 rep 2"
    },
    {
        260, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {-9908, -38895, 202842, 146516, -14265, -218205, 72923, 269208},
        {-12743, 274842, 251050, 148967, 214254, 108735, -22004, -177719},
        {2112070, -750038, 475804, -193843, -429710, 533623, 108801, 26868},
        0, "Randomized hestenes_inner seed 4242 rep 2"
    },
    {
        261, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {-180833, 79036, -55781, 240216, -182525, -165040, 140319, 18834},
        {-272397, -124801, 188200, 22580, -261296, -322033, -312295, 36101},
        {-356746, 405264, 59419, -1724915, 263245, 3465119, -661765, -1642529},
        0, "Randomized geometric_product seed 4242 rep 3"
    },
    {
        262, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {-180833, 79036, -55781, 240216, -182525, -165040, 140319, 18834},
        {-272397, -124801, 188200, 22580, -261296, -322033, -312295, 36101},
        {751623, 15853, -287448, -1060750, 1600391, 2059241, -430564, -1642529},
        0, "Randomized wedge seed 4242 rep 3"
    },
    {
        263, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {-180833, 79036, -55781, 240216, -182525, -165040, 140319, 18834},
        {-272397, -124801, 188200, 22580, -261296, -322033, -312295, 36101},
        {-356746, 1225046, 219354, -84319, 853317, 919311, 905251, -99613},
        0, "Randomized hestenes_inner seed 4242 rep 3"
    },
    {
        264, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {63565, 50695, 192187, -162208, 207468, -8891, -185310, -50647},
        {-167593, 198374, 216586, 198530, 318067, 3248, -79316, -254691},
        {-1292905, -984685, -1388994, 2068700, -179237, 2233002, 1111472, -878691},
        0, "Randomized geometric_product seed 4242 rep 4"
    },
    {
        265, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {63565, 50695, 192187, -162208, 207468, -8891, -185310, -50647},
        {-167593, 198374, 216586, 198530, 318067, 3248, -79316, -254691},
        {-162553, 62767, -281401, 607368, -636251, 670454, 1515225, -878691},
        0, "Randomized wedge seed 4242 rep 4"
    },
    {
        266, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {63565, 50695, 192187, -162208, 207468, -8891, -185310, -50647},
        {-167593, 198374, 216586, 198530, 318067, 3248, -79316, -254691},
        {-1292905, -1452463, 294349, 768752, 938886, 750042, -273945, -247031},
        0, "Randomized hestenes_inner seed 4242 rep 4"
    },
    {
        267, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {-10171, 298943, -181791, -82584, -133279, 21057, 126795, 237374},
        {-311032, 269332, 233611, -295215, -22828, -191609, -116265, 202300},
        {508169, -2305574, -76565, -158177, 791241, -1081805, 2030878, -1144652},
        0, "Randomized geometric_product seed 4242 rep 5"
    },
    {
        268, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {-10171, 298943, -181791, -82584, -133279, 21057, 126795, 237374},
        {-311032, 269332, 233611, -295215, -22828, -191609, -116265, 202300},
        {48271, -1460575, 826519, 437758, 2448803, -1077431, 529559, -1144652},
        0, "Randomized wedge seed 4242 rep 5"
    },
    {
        269, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {-10171, 298943, -181791, -82584, -133279, 21057, 126795, 237374},
        {-311032, 269332, 233611, -295215, -22828, -191609, -116265, 202300},
        {508169, -737973, -221895, -94288, -251382, 590899, 940837, -31396},
        0, "Randomized hestenes_inner seed 4242 rep 5"
    },
    {
        270, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {-121532, -194075, -27870, 257347, 76363, 264158, 321273, -166029},
        {306447, -264949, 110283, 114071, 51323, -237223, -280583, -277580},
        {2186000, 1775412, 965031, 2794407, -1588319, 1960530, 3517545, -940490},
        0, "Randomized geometric_product seed 4242 rep 6"
    },
    {
        271, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {-121532, -194075, -27870, 257347, 76363, 264158, 321273, -166029},
        {306447, -264949, 110283, 114071, 51323, -237223, -280583, -277580},
        {-568285, -416167, -334833, 991820, -177360, 2377718, 1541028, -940490},
        0, "Randomized wedge seed 4242 rep 6"
    },
    {
        272, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {-121532, -194075, -27870, 257347, 76363, 264158, 321273, -166029},
        {306447, -264949, 110283, 114071, 51323, -237223, -280583, -277580},
        {2186000, 2805446, -373554, 933723, -1185177, 321869, 1342333, 514753},
        0, "Randomized hestenes_inner seed 4242 rep 6"
    },
    {
        273, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {-83111, -261174, 163377, 237162, -148602, -196619, 36225, -215861},
        {218859, 25382, 315913, -63496, 232630, -261650, -254764, -170011},
        {-497599, -1808449, 1534168, 1562412, -3428583, 1749857, -1554752, 3109933},
        0, "Randomized geometric_product seed 4242 rep 7"
    },
    {
        274, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {-83111, -261174, 163377, 237162, -148602, -196619, 36225, -215861},
        {218859, 25382, 315913, -63496, 232630, -261650, -254764, -170011},
        {-277551, -904385, 144969, 872532, -2113527, -163605, -857460, 3109933},
        0, "Randomized wedge seed 4242 rep 7"
    },
    {
        275, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {-83111, -261174, 163377, 237162, -148602, -196619, 36225, -215861},
        {218859, 25382, 315913, -63496, 232630, -261650, -254764, -170011},
        {-497599, 428714, 104294, 102643, -910252, 755644, 1000613, 215603},
        0, "Randomized hestenes_inner seed 4242 rep 7"
    },
    {
        276, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {249191, 88, 133672, -288232, -126484, -72438, 290104, -48692},
        {239207, 169858, -162092, -242616, 188918, 97533, -300563, 283980},
        {3660095, -209577, -2582572, -993769, -1059187, -102667, -1438110, 912836},
        0, "Randomized geometric_product seed 4242 rep 8"
    },
    {
        277, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {249191, 88, 133672, -288232, -126484, -72438, 290104, -48692},
        {239207, 169858, -162092, -242616, 188918, 97533, -300563, 283980},
        {909549, 646181, -128427, -1974561, -90007, 853177, -1291714, 912836},
        0, "Randomized wedge seed 4242 rep 8"
    },
    {
        278, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {249191, 88, 133672, -288232, -126484, -72438, 290104, -48692},
        {239207, 169858, -162092, -242616, 188918, 97533, -300563, 283980},
        {3660095, -567590, -2251862, -987352, -530631, -208371, -1142465, 1079792},
        0, "Randomized hestenes_inner seed 4242 rep 8"
    },
    {
        279, "RANDOMIZED_VERIFICATION", 1, "geometric_product",
        {38138, -219726, -241347, -234135, 267166, 319037, -183448, -182916},
        {-4147, -138555, 313638, 115269, 220451, -171508, 255916, 155861},
        {-17105, 3122683, 1852581, 1246811, -3094720, 2108263, 2493058, -2844015},
        0, "Randomized geometric_product seed 4242 rep 9"
    },
    {
        280, "RANDOMIZED_VERIFICATION", 2, "wedge",
        {38138, -219726, -241347, -234135, 267166, 319037, -183448, -182916},
        {-4147, -138555, 313638, 115269, 220451, -171508, 255916, 155861},
        {-2413, -66727, 197790, 81895, -1450419, -1001468, 856547, -2844015},
        0, "Randomized wedge seed 4242 rep 9"
    },
    {
        281, "RANDOMIZED_VERIFICATION", 3, "hestenes_inner",
        {38138, -219726, -241347, -234135, 267166, 319037, -183448, -182916},
        {-4147, -138555, 313638, 115269, 220451, -171508, 255916, 155861},
        {-17105, 554769, 1116440, -935736, -428542, 474176, -373636, 90702},
        0, "Randomized hestenes_inner seed 4242 rep 9"
    },
    {
        282, "INVALID_OPCODE", 0, "INVALID_0",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        1, "Invalid opcode 0 expected to trigger STATUS_ERR_OP"
    },
    {
        283, "INVALID_OPCODE", 13, "INVALID_13",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        1, "Invalid opcode 13 expected to trigger STATUS_ERR_OP"
    },
    {
        284, "INVALID_OPCODE", 99, "INVALID_99",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        1, "Invalid opcode 99 expected to trigger STATUS_ERR_OP"
    },
    {
        285, "INVALID_OPCODE", 255, "INVALID_255",
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {65536, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0},
        1, "Invalid opcode 255 expected to trigger STATUS_ERR_OP"
    },
};

#endif /* TEST_VECTORS_H */
