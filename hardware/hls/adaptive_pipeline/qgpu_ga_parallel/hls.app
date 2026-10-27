<AutoPilot:project xmlns:AutoPilot="com.autoesl.autopilot.project" top="qgpu_ga_parallel_top" name="qgpu_ga_parallel" ideType="classic" projectType="C/C++">
    <files>
        <file name="../ga_engine/src/qgpu_ga_engine_parallel.cpp" sc="0" tb="false" cflags="-I../ga_engine/include" csimflags="" blackbox="false"/>
        <file name="../ga_engine/src/qgpu_ga_parallel_top.cpp" sc="0" tb="false" cflags="-I../ga_engine/include" csimflags="" blackbox="false"/>
        <file name="../../../ga_engine/vectors/golden_vectors.csv" sc="0" tb="1" cflags="-Wno-unknown-pragmas" csimflags="" blackbox="false"/>
        <file name="../../../ga_engine/tb/tb_qgpu_ga_engine.cpp" sc="0" tb="1" cflags="-I../../../ga_engine/include -DQGPU_TEST_PARALLEL_ONLY -Wno-unknown-pragmas" csimflags="" blackbox="false"/>
    </files>
    <Simulation argv="../ga_engine/vectors/golden_vectors.csv">
        <SimFlow name="csim" setup="false" optimizeCompile="false" clean="false" ldflags="" mflags=""/>
    </Simulation>
    <solutions>
        <solution name="solution1" status=""/>
    </solutions>
</AutoPilot:project>
