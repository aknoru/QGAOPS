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
#include "xqgpu_ga_parallel_top.h"

extern XQgpu_ga_parallel_top_Config XQgpu_ga_parallel_top_ConfigTable[];

#ifdef SDT
XQgpu_ga_parallel_top_Config *XQgpu_ga_parallel_top_LookupConfig(UINTPTR BaseAddress) {
	XQgpu_ga_parallel_top_Config *ConfigPtr = NULL;

	int Index;

	for (Index = (u32)0x0; XQgpu_ga_parallel_top_ConfigTable[Index].Name != NULL; Index++) {
		if (!BaseAddress || XQgpu_ga_parallel_top_ConfigTable[Index].Control_BaseAddress == BaseAddress) {
			ConfigPtr = &XQgpu_ga_parallel_top_ConfigTable[Index];
			break;
		}
	}

	return ConfigPtr;
}

int XQgpu_ga_parallel_top_Initialize(XQgpu_ga_parallel_top *InstancePtr, UINTPTR BaseAddress) {
	XQgpu_ga_parallel_top_Config *ConfigPtr;

	Xil_AssertNonvoid(InstancePtr != NULL);

	ConfigPtr = XQgpu_ga_parallel_top_LookupConfig(BaseAddress);
	if (ConfigPtr == NULL) {
		InstancePtr->IsReady = 0;
		return (XST_DEVICE_NOT_FOUND);
	}

	return XQgpu_ga_parallel_top_CfgInitialize(InstancePtr, ConfigPtr);
}
#else
XQgpu_ga_parallel_top_Config *XQgpu_ga_parallel_top_LookupConfig(u16 DeviceId) {
	XQgpu_ga_parallel_top_Config *ConfigPtr = NULL;

	int Index;

	for (Index = 0; Index < XPAR_XQGPU_GA_PARALLEL_TOP_NUM_INSTANCES; Index++) {
		if (XQgpu_ga_parallel_top_ConfigTable[Index].DeviceId == DeviceId) {
			ConfigPtr = &XQgpu_ga_parallel_top_ConfigTable[Index];
			break;
		}
	}

	return ConfigPtr;
}

int XQgpu_ga_parallel_top_Initialize(XQgpu_ga_parallel_top *InstancePtr, u16 DeviceId) {
	XQgpu_ga_parallel_top_Config *ConfigPtr;

	Xil_AssertNonvoid(InstancePtr != NULL);

	ConfigPtr = XQgpu_ga_parallel_top_LookupConfig(DeviceId);
	if (ConfigPtr == NULL) {
		InstancePtr->IsReady = 0;
		return (XST_DEVICE_NOT_FOUND);
	}

	return XQgpu_ga_parallel_top_CfgInitialize(InstancePtr, ConfigPtr);
}
#endif

#endif

