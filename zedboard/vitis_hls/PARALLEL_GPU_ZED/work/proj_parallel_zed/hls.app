<AutoPilot:project xmlns:AutoPilot="com.autoesl.autopilot.project" projectType="C/C++" top="parallel_gpu" name="proj_parallel_zed" ideType="classic">
    <files>
        <file name="D:/QGPU/HW/hls/PARALLEL_GPU/src/parallel_gpu.cpp" sc="0" tb="false" cflags="-std=c++14 -ID:/QGPU/HW/hls/common/include -ID:/QGPU/HW/hls/PARALLEL_GPU/include" csimflags="" blackbox="false"/>
        <file name="D:/QGPU/HW/hls/PARALLEL_GPU/testbench/tb_parallel_gpu.cpp" sc="0" tb="1" cflags="-std=c++14 -ID:/QGPU/HW/hls/common/include -ID:/QGPU/HW/hls/common/tests -ID:/QGPU/HW/hls/PARALLEL_GPU/include -Wno-unknown-pragmas" csimflags="" blackbox="false"/>
    </files>
    <solutions>
        <solution name="solution1" status=""/>
    </solutions>
    <Simulation argv="">
        <SimFlow name="csim" setup="false" optimizeCompile="false" clean="false" ldflags="" mflags=""/>
    </Simulation>
</AutoPilot:project>
