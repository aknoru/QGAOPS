// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
// Tool Version Limit: 2025.11
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// 
// ==============================================================
#ifndef __linux__

#include "xstatus.h"
#ifdef SDT
#include "xparameters.h"
#endif
#include "xseq_gpu.h"

extern XSeq_gpu_Config XSeq_gpu_ConfigTable[];

#ifdef SDT
XSeq_gpu_Config *XSeq_gpu_LookupConfig(UINTPTR BaseAddress) {
	XSeq_gpu_Config *ConfigPtr = NULL;

	int Index;

	for (Index = (u32)0x0; XSeq_gpu_ConfigTable[Index].Name != NULL; Index++) {
		if (!BaseAddress || XSeq_gpu_ConfigTable[Index].Control_BaseAddress == BaseAddress) {
			ConfigPtr = &XSeq_gpu_ConfigTable[Index];
			break;
		}
	}

	return ConfigPtr;
}

int XSeq_gpu_Initialize(XSeq_gpu *InstancePtr, UINTPTR BaseAddress) {
	XSeq_gpu_Config *ConfigPtr;

	Xil_AssertNonvoid(InstancePtr != NULL);

	ConfigPtr = XSeq_gpu_LookupConfig(BaseAddress);
	if (ConfigPtr == NULL) {
		InstancePtr->IsReady = 0;
		return (XST_DEVICE_NOT_FOUND);
	}

	return XSeq_gpu_CfgInitialize(InstancePtr, ConfigPtr);
}
#else
XSeq_gpu_Config *XSeq_gpu_LookupConfig(u16 DeviceId) {
	XSeq_gpu_Config *ConfigPtr = NULL;

	int Index;

	for (Index = 0; Index < XPAR_XSEQ_GPU_NUM_INSTANCES; Index++) {
		if (XSeq_gpu_ConfigTable[Index].DeviceId == DeviceId) {
			ConfigPtr = &XSeq_gpu_ConfigTable[Index];
			break;
		}
	}

	return ConfigPtr;
}

int XSeq_gpu_Initialize(XSeq_gpu *InstancePtr, u16 DeviceId) {
	XSeq_gpu_Config *ConfigPtr;

	Xil_AssertNonvoid(InstancePtr != NULL);

	ConfigPtr = XSeq_gpu_LookupConfig(DeviceId);
	if (ConfigPtr == NULL) {
		InstancePtr->IsReady = 0;
		return (XST_DEVICE_NOT_FOUND);
	}

	return XSeq_gpu_CfgInitialize(InstancePtr, ConfigPtr);
}
#endif

#endif

