// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
#ifndef XPARALLEL_GPU_H
#define XPARALLEL_GPU_H

#ifdef __cplusplus
extern "C" {
#endif

/***************************** Include Files *********************************/
#ifndef __linux__
#include "xil_types.h"
#include "xil_assert.h"
#include "xstatus.h"
#include "xil_io.h"
#else
#include <stdint.h>
#include <assert.h>
#include <dirent.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stddef.h>
#endif
#include "xparallel_gpu_hw.h"

/**************************** Type Definitions ******************************/
#ifdef __linux__
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;
#else
typedef struct {
#ifdef SDT
    char *Name;
#else
    u16 DeviceId;
#endif
    u64 Control_BaseAddress;
} XParallel_gpu_Config;
#endif

typedef struct {
    u64 Control_BaseAddress;
    u32 IsReady;
} XParallel_gpu;

typedef u32 word_type;

/***************** Macros (Inline Functions) Definitions *********************/
#ifndef __linux__
#define XParallel_gpu_WriteReg(BaseAddress, RegOffset, Data) \
    Xil_Out32((BaseAddress) + (RegOffset), (u32)(Data))
#define XParallel_gpu_ReadReg(BaseAddress, RegOffset) \
    Xil_In32((BaseAddress) + (RegOffset))
#else
#define XParallel_gpu_WriteReg(BaseAddress, RegOffset, Data) \
    *(volatile u32*)((BaseAddress) + (RegOffset)) = (u32)(Data)
#define XParallel_gpu_ReadReg(BaseAddress, RegOffset) \
    *(volatile u32*)((BaseAddress) + (RegOffset))

#define Xil_AssertVoid(expr)    assert(expr)
#define Xil_AssertNonvoid(expr) assert(expr)

#define XST_SUCCESS             0
#define XST_DEVICE_NOT_FOUND    2
#define XST_OPEN_DEVICE_FAILED  3
#define XIL_COMPONENT_IS_READY  1
#endif

/************************** Function Prototypes *****************************/
#ifndef __linux__
#ifdef SDT
int XParallel_gpu_Initialize(XParallel_gpu *InstancePtr, UINTPTR BaseAddress);
XParallel_gpu_Config* XParallel_gpu_LookupConfig(UINTPTR BaseAddress);
#else
int XParallel_gpu_Initialize(XParallel_gpu *InstancePtr, u16 DeviceId);
XParallel_gpu_Config* XParallel_gpu_LookupConfig(u16 DeviceId);
#endif
int XParallel_gpu_CfgInitialize(XParallel_gpu *InstancePtr, XParallel_gpu_Config *ConfigPtr);
#else
int XParallel_gpu_Initialize(XParallel_gpu *InstancePtr, const char* InstanceName);
int XParallel_gpu_Release(XParallel_gpu *InstancePtr);
#endif

void XParallel_gpu_Start(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_IsDone(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_IsIdle(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_IsReady(XParallel_gpu *InstancePtr);
void XParallel_gpu_EnableAutoRestart(XParallel_gpu *InstancePtr);
void XParallel_gpu_DisableAutoRestart(XParallel_gpu *InstancePtr);

void XParallel_gpu_Set_a_0(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_a_0(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_a_1(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_a_1(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_a_2(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_a_2(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_a_3(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_a_3(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_a_4(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_a_4(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_a_5(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_a_5(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_a_6(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_a_6(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_a_7(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_a_7(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_b_0(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_b_0(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_b_1(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_b_1(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_b_2(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_b_2(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_b_3(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_b_3(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_b_4(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_b_4(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_b_5(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_b_5(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_b_6(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_b_6(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_b_7(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_b_7(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_0(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_0_vld(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_1(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_1_vld(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_2(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_2_vld(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_3(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_3_vld(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_4(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_4_vld(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_5(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_5_vld(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_6(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_6_vld(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_7(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_c_7_vld(XParallel_gpu *InstancePtr);
void XParallel_gpu_Set_opcode(XParallel_gpu *InstancePtr, u32 Data);
u32 XParallel_gpu_Get_opcode(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_status(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_Get_status_vld(XParallel_gpu *InstancePtr);

void XParallel_gpu_InterruptGlobalEnable(XParallel_gpu *InstancePtr);
void XParallel_gpu_InterruptGlobalDisable(XParallel_gpu *InstancePtr);
void XParallel_gpu_InterruptEnable(XParallel_gpu *InstancePtr, u32 Mask);
void XParallel_gpu_InterruptDisable(XParallel_gpu *InstancePtr, u32 Mask);
void XParallel_gpu_InterruptClear(XParallel_gpu *InstancePtr, u32 Mask);
u32 XParallel_gpu_InterruptGetEnabled(XParallel_gpu *InstancePtr);
u32 XParallel_gpu_InterruptGetStatus(XParallel_gpu *InstancePtr);

#ifdef __cplusplus
}
#endif

#endif
