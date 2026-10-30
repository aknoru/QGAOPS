// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
#ifndef XSEQ_GPU_H
#define XSEQ_GPU_H

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
#include "xseq_gpu_hw.h"

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
} XSeq_gpu_Config;
#endif

typedef struct {
    u64 Control_BaseAddress;
    u32 IsReady;
} XSeq_gpu;

typedef u32 word_type;

/***************** Macros (Inline Functions) Definitions *********************/
#ifndef __linux__
#define XSeq_gpu_WriteReg(BaseAddress, RegOffset, Data) \
    Xil_Out32((BaseAddress) + (RegOffset), (u32)(Data))
#define XSeq_gpu_ReadReg(BaseAddress, RegOffset) \
    Xil_In32((BaseAddress) + (RegOffset))
#else
#define XSeq_gpu_WriteReg(BaseAddress, RegOffset, Data) \
    *(volatile u32*)((BaseAddress) + (RegOffset)) = (u32)(Data)
#define XSeq_gpu_ReadReg(BaseAddress, RegOffset) \
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
int XSeq_gpu_Initialize(XSeq_gpu *InstancePtr, UINTPTR BaseAddress);
XSeq_gpu_Config* XSeq_gpu_LookupConfig(UINTPTR BaseAddress);
#else
int XSeq_gpu_Initialize(XSeq_gpu *InstancePtr, u16 DeviceId);
XSeq_gpu_Config* XSeq_gpu_LookupConfig(u16 DeviceId);
#endif
int XSeq_gpu_CfgInitialize(XSeq_gpu *InstancePtr, XSeq_gpu_Config *ConfigPtr);
#else
int XSeq_gpu_Initialize(XSeq_gpu *InstancePtr, const char* InstanceName);
int XSeq_gpu_Release(XSeq_gpu *InstancePtr);
#endif

void XSeq_gpu_Start(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_IsDone(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_IsIdle(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_IsReady(XSeq_gpu *InstancePtr);
void XSeq_gpu_EnableAutoRestart(XSeq_gpu *InstancePtr);
void XSeq_gpu_DisableAutoRestart(XSeq_gpu *InstancePtr);

void XSeq_gpu_Set_opcode(XSeq_gpu *InstancePtr, u32 Data);
u32 XSeq_gpu_Get_opcode(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_status(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_status_vld(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_a_BaseAddress(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_a_HighAddress(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_a_TotalBytes(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_a_BitWidth(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_a_Depth(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Write_a_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length);
u32 XSeq_gpu_Read_a_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length);
u32 XSeq_gpu_Write_a_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length);
u32 XSeq_gpu_Read_a_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length);
u32 XSeq_gpu_Get_b_BaseAddress(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_b_HighAddress(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_b_TotalBytes(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_b_BitWidth(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_b_Depth(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Write_b_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length);
u32 XSeq_gpu_Read_b_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length);
u32 XSeq_gpu_Write_b_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length);
u32 XSeq_gpu_Read_b_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length);
u32 XSeq_gpu_Get_c_BaseAddress(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_c_HighAddress(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_c_TotalBytes(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_c_BitWidth(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Get_c_Depth(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_Write_c_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length);
u32 XSeq_gpu_Read_c_Words(XSeq_gpu *InstancePtr, int offset, word_type *data, int length);
u32 XSeq_gpu_Write_c_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length);
u32 XSeq_gpu_Read_c_Bytes(XSeq_gpu *InstancePtr, int offset, char *data, int length);

void XSeq_gpu_InterruptGlobalEnable(XSeq_gpu *InstancePtr);
void XSeq_gpu_InterruptGlobalDisable(XSeq_gpu *InstancePtr);
void XSeq_gpu_InterruptEnable(XSeq_gpu *InstancePtr, u32 Mask);
void XSeq_gpu_InterruptDisable(XSeq_gpu *InstancePtr, u32 Mask);
void XSeq_gpu_InterruptClear(XSeq_gpu *InstancePtr, u32 Mask);
u32 XSeq_gpu_InterruptGetEnabled(XSeq_gpu *InstancePtr);
u32 XSeq_gpu_InterruptGetStatus(XSeq_gpu *InstancePtr);

#ifdef __cplusplus
}
#endif

#endif
