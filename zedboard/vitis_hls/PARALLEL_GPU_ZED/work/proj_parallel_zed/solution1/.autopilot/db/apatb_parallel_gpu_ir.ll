; ModuleID = 'D:/QGPU/zedboard/vitis_hls/PARALLEL_GPU_ZED/work/proj_parallel_zed/solution1/.autopilot/db/a.g.ld.5.gdce.bc'
source_filename = "llvm-link"
target datalayout = "e-m:e-i64:64-i128:128-i256:256-i512:512-i1024:1024-i2048:2048-i4096:4096-n8:16:32:64-S128-v16:16-v24:32-v32:32-v48:64-v96:128-v192:256-v256:256-v512:512-v1024:1024"
target triple = "fpga64-xilinx-none"

; Function Attrs: inaccessiblemem_or_argmemonly noinline willreturn
define void @apatb_parallel_gpu_ir(i32* noalias nocapture nonnull readonly "fpga.decayed.dim.hint"="8" "partition" %a, i32* noalias nocapture nonnull readonly "fpga.decayed.dim.hint"="8" "partition" %b, i32* noalias nocapture nonnull "fpga.decayed.dim.hint"="8" "partition" %c, i32 %opcode, i32* noalias nocapture nonnull %status) local_unnamed_addr #0 {
entry:
  %0 = bitcast i32* %a to [8 x i32]*
  %a_copy_0 = alloca i32, align 512
  %a_copy_1 = alloca i32, align 512
  %a_copy_2 = alloca i32, align 512
  %a_copy_3 = alloca i32, align 512
  %a_copy_4 = alloca i32, align 512
  %a_copy_5 = alloca i32, align 512
  %a_copy_6 = alloca i32, align 512
  %a_copy_7 = alloca i32, align 512
  %1 = bitcast i32* %b to [8 x i32]*
  %b_copy_0 = alloca i32, align 512
  %b_copy_1 = alloca i32, align 512
  %b_copy_2 = alloca i32, align 512
  %b_copy_3 = alloca i32, align 512
  %b_copy_4 = alloca i32, align 512
  %b_copy_5 = alloca i32, align 512
  %b_copy_6 = alloca i32, align 512
  %b_copy_7 = alloca i32, align 512
  %2 = bitcast i32* %c to [8 x i32]*
  %c_copy_0 = alloca i32, align 512
  %c_copy_1 = alloca i32, align 512
  %c_copy_2 = alloca i32, align 512
  %c_copy_3 = alloca i32, align 512
  %c_copy_4 = alloca i32, align 512
  %c_copy_5 = alloca i32, align 512
  %c_copy_6 = alloca i32, align 512
  %c_copy_7 = alloca i32, align 512
  %status_copy = alloca i32, align 512
  call void @copy_in([8 x i32]* nonnull %0, i32* nonnull align 512 %a_copy_0, i32* nonnull align 512 %a_copy_1, i32* nonnull align 512 %a_copy_2, i32* nonnull align 512 %a_copy_3, i32* nonnull align 512 %a_copy_4, i32* nonnull align 512 %a_copy_5, i32* nonnull align 512 %a_copy_6, i32* nonnull align 512 %a_copy_7, [8 x i32]* nonnull %1, i32* nonnull align 512 %b_copy_0, i32* nonnull align 512 %b_copy_1, i32* nonnull align 512 %b_copy_2, i32* nonnull align 512 %b_copy_3, i32* nonnull align 512 %b_copy_4, i32* nonnull align 512 %b_copy_5, i32* nonnull align 512 %b_copy_6, i32* nonnull align 512 %b_copy_7, [8 x i32]* nonnull %2, i32* nonnull align 512 %c_copy_0, i32* nonnull align 512 %c_copy_1, i32* nonnull align 512 %c_copy_2, i32* nonnull align 512 %c_copy_3, i32* nonnull align 512 %c_copy_4, i32* nonnull align 512 %c_copy_5, i32* nonnull align 512 %c_copy_6, i32* nonnull align 512 %c_copy_7, i32* nonnull %status, i32* nonnull align 512 %status_copy)
  call void @apatb_parallel_gpu_hw(i32* %a_copy_0, i32* %a_copy_1, i32* %a_copy_2, i32* %a_copy_3, i32* %a_copy_4, i32* %a_copy_5, i32* %a_copy_6, i32* %a_copy_7, i32* %b_copy_0, i32* %b_copy_1, i32* %b_copy_2, i32* %b_copy_3, i32* %b_copy_4, i32* %b_copy_5, i32* %b_copy_6, i32* %b_copy_7, i32* %c_copy_0, i32* %c_copy_1, i32* %c_copy_2, i32* %c_copy_3, i32* %c_copy_4, i32* %c_copy_5, i32* %c_copy_6, i32* %c_copy_7, i32 %opcode, i32* %status_copy)
  call void @copy_back([8 x i32]* %0, i32* %a_copy_0, i32* %a_copy_1, i32* %a_copy_2, i32* %a_copy_3, i32* %a_copy_4, i32* %a_copy_5, i32* %a_copy_6, i32* %a_copy_7, [8 x i32]* %1, i32* %b_copy_0, i32* %b_copy_1, i32* %b_copy_2, i32* %b_copy_3, i32* %b_copy_4, i32* %b_copy_5, i32* %b_copy_6, i32* %b_copy_7, [8 x i32]* %2, i32* %c_copy_0, i32* %c_copy_1, i32* %c_copy_2, i32* %c_copy_3, i32* %c_copy_4, i32* %c_copy_5, i32* %c_copy_6, i32* %c_copy_7, i32* %status, i32* %status_copy)
  ret void
}

; Function Attrs: argmemonly noinline norecurse willreturn
define void @arraycpy_hls.p0a8i32([8 x i32]* "orig.arg.no"="0" %dst, [8 x i32]* readonly "orig.arg.no"="1" %src, i64 "orig.arg.no"="2" %num) local_unnamed_addr #1 {
entry:
  %0 = icmp eq [8 x i32]* %src, null
  %1 = icmp eq [8 x i32]* %dst, null
  %2 = or i1 %1, %0
  br i1 %2, label %ret, label %copy

copy:                                             ; preds = %entry
  %for.loop.cond1 = icmp sgt i64 %num, 0
  br i1 %for.loop.cond1, label %for.loop.lr.ph, label %copy.split

for.loop.lr.ph:                                   ; preds = %copy
  br label %for.loop

for.loop:                                         ; preds = %for.loop, %for.loop.lr.ph
  %for.loop.idx2 = phi i64 [ 0, %for.loop.lr.ph ], [ %for.loop.idx.next, %for.loop ]
  %dst.addr = getelementptr [8 x i32], [8 x i32]* %dst, i64 0, i64 %for.loop.idx2
  %src.addr = getelementptr [8 x i32], [8 x i32]* %src, i64 0, i64 %for.loop.idx2
  %3 = load i32, i32* %src.addr, align 4
  store i32 %3, i32* %dst.addr, align 4
  %for.loop.idx.next = add nuw nsw i64 %for.loop.idx2, 1
  %exitcond = icmp ne i64 %for.loop.idx.next, %num
  br i1 %exitcond, label %for.loop, label %copy.split

copy.split:                                       ; preds = %for.loop, %copy
  br label %ret

ret:                                              ; preds = %copy.split, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse willreturn
define internal fastcc void @onebyonecpy_hls.p0i32(i32* noalias align 512 %dst, i32* noalias readonly %src) unnamed_addr #2 {
entry:
  %0 = icmp eq i32* %dst, null
  %1 = icmp eq i32* %src, null
  %2 = or i1 %0, %1
  br i1 %2, label %ret, label %copy

copy:                                             ; preds = %entry
  %3 = load i32, i32* %src, align 4
  store i32 %3, i32* %dst, align 512
  br label %ret

ret:                                              ; preds = %copy, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse willreturn
define void @arraycpy_hls.p0a8i32.32.33(i32* "orig.arg.no"="0" "unpacked"="0.0" %dst_0, i32* "orig.arg.no"="0" "unpacked"="0.1" %dst_1, i32* "orig.arg.no"="0" "unpacked"="0.2" %dst_2, i32* "orig.arg.no"="0" "unpacked"="0.3" %dst_3, i32* "orig.arg.no"="0" "unpacked"="0.4" %dst_4, i32* "orig.arg.no"="0" "unpacked"="0.5" %dst_5, i32* "orig.arg.no"="0" "unpacked"="0.6" %dst_6, i32* "orig.arg.no"="0" "unpacked"="0.7" %dst_7, [8 x i32]* readonly "orig.arg.no"="1" %src, i64 "orig.arg.no"="2" %num) #1 {
entry:
  %0 = icmp eq [8 x i32]* %src, null
  %1 = icmp eq i32* %dst_0, null
  %2 = or i1 %1, %0
  br i1 %2, label %ret, label %copy

copy:                                             ; preds = %entry
  %for.loop.cond1 = icmp sgt i64 %num, 0
  br i1 %for.loop.cond1, label %for.loop.lr.ph, label %copy.split

for.loop.lr.ph:                                   ; preds = %copy
  br label %for.loop

for.loop:                                         ; preds = %dst.addr.exit, %for.loop.lr.ph
  %for.loop.idx2 = phi i64 [ 0, %for.loop.lr.ph ], [ %for.loop.idx.next, %dst.addr.exit ]
  %src.addr = getelementptr [8 x i32], [8 x i32]* %src, i64 0, i64 %for.loop.idx2
  %3 = load i32, i32* %src.addr, align 4
  switch i64 %for.loop.idx2, label %dst.addr.exit [
    i64 0, label %dst.addr.case.0
    i64 1, label %dst.addr.case.1
    i64 2, label %dst.addr.case.2
    i64 3, label %dst.addr.case.3
    i64 4, label %dst.addr.case.4
    i64 5, label %dst.addr.case.5
    i64 6, label %dst.addr.case.6
    i64 7, label %dst.addr.case.7
  ]

dst.addr.case.0:                                  ; preds = %for.loop
  store i32 %3, i32* %dst_0, align 4
  br label %dst.addr.exit

dst.addr.case.1:                                  ; preds = %for.loop
  store i32 %3, i32* %dst_1, align 4
  br label %dst.addr.exit

dst.addr.case.2:                                  ; preds = %for.loop
  store i32 %3, i32* %dst_2, align 4
  br label %dst.addr.exit

dst.addr.case.3:                                  ; preds = %for.loop
  store i32 %3, i32* %dst_3, align 4
  br label %dst.addr.exit

dst.addr.case.4:                                  ; preds = %for.loop
  store i32 %3, i32* %dst_4, align 4
  br label %dst.addr.exit

dst.addr.case.5:                                  ; preds = %for.loop
  store i32 %3, i32* %dst_5, align 4
  br label %dst.addr.exit

dst.addr.case.6:                                  ; preds = %for.loop
  store i32 %3, i32* %dst_6, align 4
  br label %dst.addr.exit

dst.addr.case.7:                                  ; preds = %for.loop
  store i32 %3, i32* %dst_7, align 4
  br label %dst.addr.exit

dst.addr.exit:                                    ; preds = %dst.addr.case.7, %dst.addr.case.6, %dst.addr.case.5, %dst.addr.case.4, %dst.addr.case.3, %dst.addr.case.2, %dst.addr.case.1, %dst.addr.case.0, %for.loop
  %for.loop.idx.next = add nuw nsw i64 %for.loop.idx2, 1
  %exitcond = icmp ne i64 %for.loop.idx.next, %num
  br i1 %exitcond, label %for.loop, label %copy.split

copy.split:                                       ; preds = %dst.addr.exit, %copy
  br label %ret

ret:                                              ; preds = %copy.split, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse willreturn
define internal void @onebyonecpy_hls.p0a8i32.31.34(i32* noalias align 512 "orig.arg.no"="0" "unpacked"="0.0" %dst_0, i32* noalias align 512 "orig.arg.no"="0" "unpacked"="0.1" %dst_1, i32* noalias align 512 "orig.arg.no"="0" "unpacked"="0.2" %dst_2, i32* noalias align 512 "orig.arg.no"="0" "unpacked"="0.3" %dst_3, i32* noalias align 512 "orig.arg.no"="0" "unpacked"="0.4" %dst_4, i32* noalias align 512 "orig.arg.no"="0" "unpacked"="0.5" %dst_5, i32* noalias align 512 "orig.arg.no"="0" "unpacked"="0.6" %dst_6, i32* noalias align 512 "orig.arg.no"="0" "unpacked"="0.7" %dst_7, [8 x i32]* noalias readonly "orig.arg.no"="1" %src) #2 {
entry:
  %0 = icmp eq i32* %dst_0, null
  %1 = icmp eq [8 x i32]* %src, null
  %2 = or i1 %0, %1
  br i1 %2, label %ret, label %copy

copy:                                             ; preds = %entry
  call void @arraycpy_hls.p0a8i32.32.33(i32* nonnull %dst_0, i32* %dst_1, i32* %dst_2, i32* %dst_3, i32* %dst_4, i32* %dst_5, i32* %dst_6, i32* %dst_7, [8 x i32]* nonnull %src, i64 8)
  br label %ret

ret:                                              ; preds = %copy, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse willreturn
define internal void @copy_in([8 x i32]* noalias readonly "orig.arg.no"="0", i32* noalias align 512 "orig.arg.no"="1" "unpacked"="1.0" %_0, i32* noalias align 512 "orig.arg.no"="1" "unpacked"="1.1" %_1, i32* noalias align 512 "orig.arg.no"="1" "unpacked"="1.2" %_2, i32* noalias align 512 "orig.arg.no"="1" "unpacked"="1.3" %_3, i32* noalias align 512 "orig.arg.no"="1" "unpacked"="1.4" %_4, i32* noalias align 512 "orig.arg.no"="1" "unpacked"="1.5" %_5, i32* noalias align 512 "orig.arg.no"="1" "unpacked"="1.6" %_6, i32* noalias align 512 "orig.arg.no"="1" "unpacked"="1.7" %_7, [8 x i32]* noalias readonly "orig.arg.no"="2", i32* noalias align 512 "orig.arg.no"="3" "unpacked"="3.0" %_01, i32* noalias align 512 "orig.arg.no"="3" "unpacked"="3.1" %_12, i32* noalias align 512 "orig.arg.no"="3" "unpacked"="3.2" %_23, i32* noalias align 512 "orig.arg.no"="3" "unpacked"="3.3" %_34, i32* noalias align 512 "orig.arg.no"="3" "unpacked"="3.4" %_45, i32* noalias align 512 "orig.arg.no"="3" "unpacked"="3.5" %_56, i32* noalias align 512 "orig.arg.no"="3" "unpacked"="3.6" %_67, i32* noalias align 512 "orig.arg.no"="3" "unpacked"="3.7" %_78, [8 x i32]* noalias readonly "orig.arg.no"="4", i32* noalias align 512 "orig.arg.no"="5" "unpacked"="5.0" %_09, i32* noalias align 512 "orig.arg.no"="5" "unpacked"="5.1" %_110, i32* noalias align 512 "orig.arg.no"="5" "unpacked"="5.2" %_211, i32* noalias align 512 "orig.arg.no"="5" "unpacked"="5.3" %_312, i32* noalias align 512 "orig.arg.no"="5" "unpacked"="5.4" %_413, i32* noalias align 512 "orig.arg.no"="5" "unpacked"="5.5" %_514, i32* noalias align 512 "orig.arg.no"="5" "unpacked"="5.6" %_615, i32* noalias align 512 "orig.arg.no"="5" "unpacked"="5.7" %_716, i32* noalias readonly "orig.arg.no"="6", i32* noalias align 512 "orig.arg.no"="7") #3 {
entry:
  call void @onebyonecpy_hls.p0a8i32.31.34(i32* align 512 %_0, i32* align 512 %_1, i32* align 512 %_2, i32* align 512 %_3, i32* align 512 %_4, i32* align 512 %_5, i32* align 512 %_6, i32* align 512 %_7, [8 x i32]* %0)
  call void @onebyonecpy_hls.p0a8i32.31.34(i32* align 512 %_01, i32* align 512 %_12, i32* align 512 %_23, i32* align 512 %_34, i32* align 512 %_45, i32* align 512 %_56, i32* align 512 %_67, i32* align 512 %_78, [8 x i32]* %1)
  call void @onebyonecpy_hls.p0a8i32.31.34(i32* align 512 %_09, i32* align 512 %_110, i32* align 512 %_211, i32* align 512 %_312, i32* align 512 %_413, i32* align 512 %_514, i32* align 512 %_615, i32* align 512 %_716, [8 x i32]* %2)
  call fastcc void @onebyonecpy_hls.p0i32(i32* align 512 %4, i32* %3)
  ret void
}

; Function Attrs: argmemonly noinline norecurse willreturn
define void @arraycpy_hls.p0a8i32.66.67([8 x i32]* "orig.arg.no"="0" %dst, i32* readonly "orig.arg.no"="1" "unpacked"="1.0" %src_0, i32* readonly "orig.arg.no"="1" "unpacked"="1.1" %src_1, i32* readonly "orig.arg.no"="1" "unpacked"="1.2" %src_2, i32* readonly "orig.arg.no"="1" "unpacked"="1.3" %src_3, i32* readonly "orig.arg.no"="1" "unpacked"="1.4" %src_4, i32* readonly "orig.arg.no"="1" "unpacked"="1.5" %src_5, i32* readonly "orig.arg.no"="1" "unpacked"="1.6" %src_6, i32* readonly "orig.arg.no"="1" "unpacked"="1.7" %src_7, i64 "orig.arg.no"="2" %num) #1 {
entry:
  %0 = icmp eq i32* %src_0, null
  %1 = icmp eq [8 x i32]* %dst, null
  %2 = or i1 %1, %0
  br i1 %2, label %ret, label %copy

copy:                                             ; preds = %entry
  %for.loop.cond1 = icmp sgt i64 %num, 0
  br i1 %for.loop.cond1, label %for.loop.lr.ph, label %copy.split

for.loop.lr.ph:                                   ; preds = %copy
  br label %for.loop

for.loop:                                         ; preds = %src.addr.exit, %for.loop.lr.ph
  %for.loop.idx2 = phi i64 [ 0, %for.loop.lr.ph ], [ %for.loop.idx.next, %src.addr.exit ]
  %dst.addr = getelementptr [8 x i32], [8 x i32]* %dst, i64 0, i64 %for.loop.idx2
  switch i64 %for.loop.idx2, label %src.addr.exit [
    i64 0, label %src.addr.case.0
    i64 1, label %src.addr.case.1
    i64 2, label %src.addr.case.2
    i64 3, label %src.addr.case.3
    i64 4, label %src.addr.case.4
    i64 5, label %src.addr.case.5
    i64 6, label %src.addr.case.6
    i64 7, label %src.addr.case.7
  ]

src.addr.case.0:                                  ; preds = %for.loop
  %_0 = load i32, i32* %src_0, align 4
  br label %src.addr.exit

src.addr.case.1:                                  ; preds = %for.loop
  %_1 = load i32, i32* %src_1, align 4
  br label %src.addr.exit

src.addr.case.2:                                  ; preds = %for.loop
  %_2 = load i32, i32* %src_2, align 4
  br label %src.addr.exit

src.addr.case.3:                                  ; preds = %for.loop
  %_3 = load i32, i32* %src_3, align 4
  br label %src.addr.exit

src.addr.case.4:                                  ; preds = %for.loop
  %_4 = load i32, i32* %src_4, align 4
  br label %src.addr.exit

src.addr.case.5:                                  ; preds = %for.loop
  %_5 = load i32, i32* %src_5, align 4
  br label %src.addr.exit

src.addr.case.6:                                  ; preds = %for.loop
  %_6 = load i32, i32* %src_6, align 4
  br label %src.addr.exit

src.addr.case.7:                                  ; preds = %for.loop
  %_7 = load i32, i32* %src_7, align 4
  br label %src.addr.exit

src.addr.exit:                                    ; preds = %src.addr.case.7, %src.addr.case.6, %src.addr.case.5, %src.addr.case.4, %src.addr.case.3, %src.addr.case.2, %src.addr.case.1, %src.addr.case.0, %for.loop
  %3 = phi i32 [ %_0, %src.addr.case.0 ], [ %_1, %src.addr.case.1 ], [ %_2, %src.addr.case.2 ], [ %_3, %src.addr.case.3 ], [ %_4, %src.addr.case.4 ], [ %_5, %src.addr.case.5 ], [ %_6, %src.addr.case.6 ], [ %_7, %src.addr.case.7 ], [ undef, %for.loop ]
  store i32 %3, i32* %dst.addr, align 4
  %for.loop.idx.next = add nuw nsw i64 %for.loop.idx2, 1
  %exitcond = icmp ne i64 %for.loop.idx.next, %num
  br i1 %exitcond, label %for.loop, label %copy.split

copy.split:                                       ; preds = %src.addr.exit, %copy
  br label %ret

ret:                                              ; preds = %copy.split, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse willreturn
define internal void @onebyonecpy_hls.p0a8i32.65.68([8 x i32]* noalias "orig.arg.no"="0" %dst, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.0" %src_0, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.1" %src_1, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.2" %src_2, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.3" %src_3, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.4" %src_4, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.5" %src_5, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.6" %src_6, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.7" %src_7) #2 {
entry:
  %0 = icmp eq [8 x i32]* %dst, null
  %1 = icmp eq i32* %src_0, null
  %2 = or i1 %0, %1
  br i1 %2, label %ret, label %copy

copy:                                             ; preds = %entry
  call void @arraycpy_hls.p0a8i32.66.67([8 x i32]* nonnull %dst, i32* nonnull %src_0, i32* %src_1, i32* %src_2, i32* %src_3, i32* %src_4, i32* %src_5, i32* %src_6, i32* %src_7, i64 8)
  br label %ret

ret:                                              ; preds = %copy, %entry
  ret void
}

; Function Attrs: argmemonly noinline norecurse willreturn
define internal void @copy_out([8 x i32]* noalias "orig.arg.no"="0", i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.0" %_0, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.1" %_1, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.2" %_2, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.3" %_3, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.4" %_4, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.5" %_5, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.6" %_6, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.7" %_7, [8 x i32]* noalias "orig.arg.no"="2", i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.0" %_01, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.1" %_12, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.2" %_23, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.3" %_34, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.4" %_45, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.5" %_56, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.6" %_67, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.7" %_78, [8 x i32]* noalias "orig.arg.no"="4", i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.0" %_09, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.1" %_110, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.2" %_211, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.3" %_312, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.4" %_413, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.5" %_514, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.6" %_615, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.7" %_716, i32* noalias "orig.arg.no"="6", i32* noalias readonly align 512 "orig.arg.no"="7") #4 {
entry:
  call void @onebyonecpy_hls.p0a8i32.65.68([8 x i32]* %0, i32* align 512 %_0, i32* align 512 %_1, i32* align 512 %_2, i32* align 512 %_3, i32* align 512 %_4, i32* align 512 %_5, i32* align 512 %_6, i32* align 512 %_7)
  call void @onebyonecpy_hls.p0a8i32.65.68([8 x i32]* %1, i32* align 512 %_01, i32* align 512 %_12, i32* align 512 %_23, i32* align 512 %_34, i32* align 512 %_45, i32* align 512 %_56, i32* align 512 %_67, i32* align 512 %_78)
  call void @onebyonecpy_hls.p0a8i32.65.68([8 x i32]* %2, i32* align 512 %_09, i32* align 512 %_110, i32* align 512 %_211, i32* align 512 %_312, i32* align 512 %_413, i32* align 512 %_514, i32* align 512 %_615, i32* align 512 %_716)
  call fastcc void @onebyonecpy_hls.p0i32(i32* %3, i32* align 512 %4)
  ret void
}

declare i8* @malloc(i64)

declare void @free(i8*)

declare void @apatb_parallel_gpu_hw(i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32, i32*)

; Function Attrs: argmemonly noinline norecurse willreturn
define internal void @copy_back([8 x i32]* noalias "orig.arg.no"="0", i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.0" %_0, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.1" %_1, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.2" %_2, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.3" %_3, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.4" %_4, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.5" %_5, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.6" %_6, i32* noalias readonly align 512 "orig.arg.no"="1" "unpacked"="1.7" %_7, [8 x i32]* noalias "orig.arg.no"="2", i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.0" %_01, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.1" %_12, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.2" %_23, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.3" %_34, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.4" %_45, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.5" %_56, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.6" %_67, i32* noalias readonly align 512 "orig.arg.no"="3" "unpacked"="3.7" %_78, [8 x i32]* noalias "orig.arg.no"="4", i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.0" %_09, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.1" %_110, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.2" %_211, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.3" %_312, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.4" %_413, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.5" %_514, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.6" %_615, i32* noalias readonly align 512 "orig.arg.no"="5" "unpacked"="5.7" %_716, i32* noalias "orig.arg.no"="6", i32* noalias readonly align 512 "orig.arg.no"="7") #4 {
entry:
  call void @onebyonecpy_hls.p0a8i32.65.68([8 x i32]* %2, i32* align 512 %_09, i32* align 512 %_110, i32* align 512 %_211, i32* align 512 %_312, i32* align 512 %_413, i32* align 512 %_514, i32* align 512 %_615, i32* align 512 %_716)
  call fastcc void @onebyonecpy_hls.p0i32(i32* %3, i32* align 512 %4)
  ret void
}

declare void @parallel_gpu_hw_stub(i32* noalias nocapture nonnull readonly, i32* noalias nocapture nonnull readonly, i32* noalias nocapture nonnull, i32, i32* noalias nocapture nonnull)

define void @parallel_gpu_hw_stub_wrapper(i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32*, i32, i32*) #5 {
entry:
  %26 = call i8* @malloc(i64 32)
  %27 = bitcast i8* %26 to [8 x i32]*
  %28 = call i8* @malloc(i64 32)
  %29 = bitcast i8* %28 to [8 x i32]*
  %30 = call i8* @malloc(i64 32)
  %31 = bitcast i8* %30 to [8 x i32]*
  call void @copy_out([8 x i32]* %27, i32* %0, i32* %1, i32* %2, i32* %3, i32* %4, i32* %5, i32* %6, i32* %7, [8 x i32]* %29, i32* %8, i32* %9, i32* %10, i32* %11, i32* %12, i32* %13, i32* %14, i32* %15, [8 x i32]* %31, i32* %16, i32* %17, i32* %18, i32* %19, i32* %20, i32* %21, i32* %22, i32* %23, i32* null, i32* %25)
  %32 = bitcast [8 x i32]* %27 to i32*
  %33 = bitcast [8 x i32]* %29 to i32*
  %34 = bitcast [8 x i32]* %31 to i32*
  call void @parallel_gpu_hw_stub(i32* %32, i32* %33, i32* %34, i32 %24, i32* %25)
  call void @copy_in([8 x i32]* %27, i32* %0, i32* %1, i32* %2, i32* %3, i32* %4, i32* %5, i32* %6, i32* %7, [8 x i32]* %29, i32* %8, i32* %9, i32* %10, i32* %11, i32* %12, i32* %13, i32* %14, i32* %15, [8 x i32]* %31, i32* %16, i32* %17, i32* %18, i32* %19, i32* %20, i32* %21, i32* %22, i32* %23, i32* null, i32* %25)
  call void @free(i8* %26)
  call void @free(i8* %28)
  call void @free(i8* %30)
  ret void
}

attributes #0 = { inaccessiblemem_or_argmemonly noinline willreturn "fpga.wrapper.func"="wrapper" }
attributes #1 = { argmemonly noinline norecurse willreturn "fpga.wrapper.func"="arraycpy_hls" }
attributes #2 = { argmemonly noinline norecurse willreturn "fpga.wrapper.func"="onebyonecpy_hls" }
attributes #3 = { argmemonly noinline norecurse willreturn "fpga.wrapper.func"="copyin" }
attributes #4 = { argmemonly noinline norecurse willreturn "fpga.wrapper.func"="copyout" }
attributes #5 = { "fpga.wrapper.func"="stub" }

!llvm.dbg.cu = !{}
!llvm.ident = !{!0, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1, !1}
!llvm.module.flags = !{!2, !3, !4}
!blackbox_cfg = !{!5}
!datalayout.transforms.on.top = !{!6, !20, !32}

!0 = !{!"AMD/Xilinx clang version 16.0.6"}
!1 = !{!"clang version 7.0.0 "}
!2 = !{i32 2, !"Dwarf Version", i32 4}
!3 = !{i32 2, !"Debug Info Version", i32 3}
!4 = !{i32 1, !"wchar_size", i32 4}
!5 = !{}
!6 = !{!7, !9, !11}
!7 = !{!8}
!8 = !{!"0", [8 x i32]* null}
!9 = !{!10}
!10 = !{!"array_partition", !"type=Complete", !"dim=1"}
!11 = !{!12, !13, !14, !15, !16, !17, !18, !19}
!12 = !{!"0.0", i32* null}
!13 = !{!"0.1", i32* null}
!14 = !{!"0.2", i32* null}
!15 = !{!"0.3", i32* null}
!16 = !{!"0.4", i32* null}
!17 = !{!"0.5", i32* null}
!18 = !{!"0.6", i32* null}
!19 = !{!"0.7", i32* null}
!20 = !{!21, !9, !23}
!21 = !{!22}
!22 = !{!"1", [8 x i32]* null}
!23 = !{!24, !25, !26, !27, !28, !29, !30, !31}
!24 = !{!"1.0", i32* null}
!25 = !{!"1.1", i32* null}
!26 = !{!"1.2", i32* null}
!27 = !{!"1.3", i32* null}
!28 = !{!"1.4", i32* null}
!29 = !{!"1.5", i32* null}
!30 = !{!"1.6", i32* null}
!31 = !{!"1.7", i32* null}
!32 = !{!33, !9, !35}
!33 = !{!34}
!34 = !{!"2", [8 x i32]* null}
!35 = !{!36, !37, !38, !39, !40, !41, !42, !43}
!36 = !{!"2.0", i32* null}
!37 = !{!"2.1", i32* null}
!38 = !{!"2.2", i32* null}
!39 = !{!"2.3", i32* null}
!40 = !{!"2.4", i32* null}
!41 = !{!"2.5", i32* null}
!42 = !{!"2.6", i32* null}
!43 = !{!"2.7", i32* null}
