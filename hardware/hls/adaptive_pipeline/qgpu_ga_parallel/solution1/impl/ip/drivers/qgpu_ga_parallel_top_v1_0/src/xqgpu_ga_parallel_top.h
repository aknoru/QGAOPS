// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
#ifndef XQGPU_GA_PARALLEL_TOP_H
#define XQGPU_GA_PARALLEL_TOP_H

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
#include "xqgpu_ga_parallel_top_hw.h"

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
} XQgpu_ga_parallel_top_Config;
#endif

typedef struct {
    u64 Control_BaseAddress;
    u32 IsReady;
} XQgpu_ga_parallel_top;

typedef u32 word_type;

/***************** Macros (Inline Functions) Definitions *********************/
#ifndef __linux__
#define XQgpu_ga_parallel_top_WriteReg(BaseAddress, RegOffset, Data) \
    Xil_Out32((BaseAddress) + (RegOffset), (u32)(Data))
#define XQgpu_ga_parallel_top_ReadReg(BaseAddress, RegOffset) \
    Xil_In32((BaseAddress) + (RegOffset))
#else
#define XQgpu_ga_parallel_top_WriteReg(BaseAddress, RegOffset, Data) \
    *(volatile u32*)((BaseAddress) + (RegOffset)) = (u32)(Data)
#define XQgpu_ga_parallel_top_ReadReg(BaseAddress, RegOffset) \
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
int XQgpu_ga_parallel_top_Initialize(XQgpu_ga_parallel_top *InstancePtr, UINTPTR BaseAddress);
XQgpu_ga_parallel_top_Config* XQgpu_ga_parallel_top_LookupConfig(UINTPTR BaseAddress);
#else
int XQgpu_ga_parallel_top_Initialize(XQgpu_ga_parallel_top *InstancePtr, u16 DeviceId);
XQgpu_ga_parallel_top_Config* XQgpu_ga_parallel_top_LookupConfig(u16 DeviceId);
#endif
int XQgpu_ga_parallel_top_CfgInitialize(XQgpu_ga_parallel_top *InstancePtr, XQgpu_ga_parallel_top_Config *ConfigPtr);
#else
int XQgpu_ga_parallel_top_Initialize(XQgpu_ga_parallel_top *InstancePtr, const char* InstanceName);
int XQgpu_ga_parallel_top_Release(XQgpu_ga_parallel_top *InstancePtr);
#endif

void XQgpu_ga_parallel_top_Start(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_IsDone(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_IsIdle(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_IsReady(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_EnableAutoRestart(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_DisableAutoRestart(XQgpu_ga_parallel_top *InstancePtr);

void XQgpu_ga_parallel_top_Set_a_0(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_a_0(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_a_1(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_a_1(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_a_2(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_a_2(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_a_3(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_a_3(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_a_4(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_a_4(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_a_5(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_a_5(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_a_6(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_a_6(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_a_7(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_a_7(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_b_0(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_b_0(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_b_1(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_b_1(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_b_2(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_b_2(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_b_3(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_b_3(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_b_4(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_b_4(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_b_5(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_b_5(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_b_6(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_b_6(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_b_7(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_b_7(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_0(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_0_vld(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_1(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_1_vld(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_2(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_2_vld(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_3(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_3_vld(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_4(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_4_vld(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_5(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_5_vld(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_6(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_6_vld(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_7(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_c_7_vld(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_opcode(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_opcode(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_status(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_Get_status_vld(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_Set_dma_len(XQgpu_ga_parallel_top *InstancePtr, u32 Data);
u32 XQgpu_ga_parallel_top_Get_dma_len(XQgpu_ga_parallel_top *InstancePtr);

void XQgpu_ga_parallel_top_InterruptGlobalEnable(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_InterruptGlobalDisable(XQgpu_ga_parallel_top *InstancePtr);
void XQgpu_ga_parallel_top_InterruptEnable(XQgpu_ga_parallel_top *InstancePtr, u32 Mask);
void XQgpu_ga_parallel_top_InterruptDisable(XQgpu_ga_parallel_top *InstancePtr, u32 Mask);
void XQgpu_ga_parallel_top_InterruptClear(XQgpu_ga_parallel_top *InstancePtr, u32 Mask);
u32 XQgpu_ga_parallel_top_InterruptGetEnabled(XQgpu_ga_parallel_top *InstancePtr);
u32 XQgpu_ga_parallel_top_InterruptGetStatus(XQgpu_ga_parallel_top *InstancePtr);

#ifdef __cplusplus
}
#endif

#endif
