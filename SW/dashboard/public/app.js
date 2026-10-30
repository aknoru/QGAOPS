// app.js - Live Telemetry, 3D GA Visualizer, and Controls
let activeArch = "PARALLEL_GPU";
let hudVisible = true;
let frameCount = 0;

// Canvas setup
const canvas = document.getElementById("ga-canvas");
const ctx = canvas.getContext("2d");

let palmNormal = [0, 0, 1];
let rotAngle = 0;

function setArchitecture(arch) {
  activeArch = arch;
  document.querySelectorAll(".arch-btn").forEach(btn => btn.classList.remove("active"));
  if (arch === "SOFTWARE_ONLY") document.getElementById("btn-arch-sw").classList.add("active");
  if (arch === "SEQ_GPU") document.getElementById("btn-arch-seq").classList.add("active");
  if (arch === "PARALLEL_GPU") document.getElementById("btn-arch-par").classList.add("active");

  // Update telemetry display
  const dspVal = document.getElementById("dsp-util");
  const dspSub = document.getElementById("dsp-sub");
  const bitHash = document.getElementById("bit-hash");

  if (arch === "SEQ_GPU") {
    dspVal.innerText = "16 / 1,248";
    dspSub.innerText = "1.3% (Sequential Shared Core)";
    bitHash.innerText = "E3B605A1C165FAA4CE064E593F4AA36B58FD3BF16DACDFD6CE60E64AD63D82A5";
  } else if (arch === "PARALLEL_GPU") {
    dspVal.innerText = "832 / 1,248";
    dspSub.innerText = "66.7% (Unrolled 64-Product Tree)";
    bitHash.innerText = "4E17A691195FF37CB56DB83AA993ACE6999BEDA8FFE73676A55193368A8119F7";
  } else {
    dspVal.innerText = "0 / 1,248 (Host CPU)";
    dspSub.innerText = "0.0% (Software Simulation)";
    bitHash.innerText = "N/A (Host-Only Python Reference)";
  }

  fetch(`/api/set_arch?arch=${arch}`).catch(err => console.log(err));
}

function toggleOverlay() {
  hudVisible = !hudVisible;
  const overlay = document.getElementById("video-overlay");
  overlay.style.display = hudVisible ? "flex" : "none";
  document.getElementById("btn-toggle-hud").classList.toggle("active", hudVisible);
}

function triggerBenchmark() {
  const btn = document.getElementById("btn-run-bench");
  btn.innerText = "⏳ Running...";
  btn.disabled = true;

  fetch("/api/run_benchmark")
    .then(res => res.json())
    .then(data => {
      alert(`Benchmark Completed!\nThroughput: ${data.throughput_ops_s} ops/s\nKernel: ${data.pl_latency_us} µs`);
      btn.innerText = "⚡ Run Live Benchmark";
      btn.disabled = false;
    })
    .catch(err => {
      btn.innerText = "⚡ Run Live Benchmark";
      btn.disabled = false;
    });
}

// 3D Multivector Canvas Rendering
function draw3DScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  rotAngle += 0.015;

  // Isometric projection helper
  function project(x, y, z) {
    const cosA = Math.cos(rotAngle);
    const sinA = Math.sin(rotAngle);
    const rx = x * cosA - y * sinA;
    const ry = x * sinA + y * cosA;
    const px = cx + (rx - ry) * 0.866 * 90;
    const py = cy + (rx + ry) * 0.5 * 90 - z * 90;
    return [px, py];
  }

  // Draw coordinate grid circle
  ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  for (let r = 20; r <= 100; r += 20) {
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
  }
  ctx.stroke();

  // Draw 3D Axes
  const origin = project(0, 0, 0);
  const pE1 = project(1, 0, 0);
  const pE2 = project(0, 1, 0);
  const pE3 = project(0, 0, 1);

  // e1 (Red)
  ctx.strokeStyle = "#F43F5E";
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(origin[0], origin[1]); ctx.lineTo(pE1[0], pE1[1]); ctx.stroke();

  // e2 (Green)
  ctx.strokeStyle = "#10B981";
  ctx.beginPath(); ctx.moveTo(origin[0], origin[1]); ctx.lineTo(pE2[0], pE2[1]); ctx.stroke();

  // e3 (Blue)
  ctx.strokeStyle = "#38BDF8";
  ctx.beginPath(); ctx.moveTo(origin[0], origin[1]); ctx.lineTo(pE3[0], pE3[1]); ctx.stroke();

  // Draw Rotated Palm Normal Vector
  const pNorm = project(palmNormal[0], palmNormal[1], palmNormal[2]);
  ctx.strokeStyle = "#F59E0B";
  ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(origin[0], origin[1]); ctx.lineTo(pNorm[0], pNorm[1]); ctx.stroke();
  ctx.fillStyle = "#F59E0B";
  ctx.beginPath(); ctx.arc(pNorm[0], pNorm[1], 5, 0, Math.PI * 2); ctx.fill();

  // Draw Palm Plane Bivector Disk
  ctx.fillStyle = "rgba(245, 158, 11, 0.15)";
  ctx.strokeStyle = "rgba(245, 158, 11, 0.6)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  const diskPts = 16;
  for (let k = 0; k <= diskPts; k++) {
    const phi = (k / diskPts) * Math.PI * 2;
    // Disk perpendicular to palm normal
    const dx = Math.cos(phi) * 0.6;
    const dy = Math.sin(phi) * 0.6;
    const pt = project(dx, dy, 0);
    if (k === 0) ctx.moveTo(pt[0], pt[1]);
    else ctx.lineTo(pt[0], pt[1]);
  }
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  requestAnimationFrame(draw3DScene);
}

// Telemetry Polling Loop
function pollTelemetry() {
  fetch("/api/telemetry")
    .then(res => res.json())
    .then(data => {
      frameCount++;
      document.getElementById("stream-timestamp").innerText = `Frames: ${frameCount}`;
      
      if (data.gesture) {
        document.getElementById("gesture-title").innerText = data.gesture;
        const confPct = Math.round((data.confidence || 0) * 100);
        document.getElementById("confidence-fill").style.width = `${confPct}%`;
        document.getElementById("confidence-text").innerText = `Confidence: ${confPct}%`;
      }

      if (data.palm_normal) {
        palmNormal = data.palm_normal;
      }

      if (data.finger_states && data.finger_states.length === 5) {
        const ids = ["f-thumb", "f-index", "f-middle", "f-ring", "f-pinky"];
        const names = ["Thumb", "Index", "Middle", "Ring", "Pinky"];
        data.finger_states.forEach((st, idx) => {
          const el = document.getElementById(ids[idx]);
          el.innerText = `${names[idx]}: ${st}`;
          el.classList.toggle("ext", st === "EXT");
        });
      }

      if (data.timings) {
        document.getElementById("hud-fps").innerText = `FPS: ${data.timings.fps.toFixed(1)}`;
        document.getElementById("hud-e2e").innerText = `E2E: ${(data.timings.total_us / 1000).toFixed(1)} ms`;

        document.getElementById("val-acq").innerText = `${data.timings.capture_us.toFixed(0)} µs`;
        document.getElementById("val-det").innerText = `${data.timings.detect_us.toFixed(0)} µs`;
        document.getElementById("val-enc").innerText = `${data.timings.encode_us.toFixed(0)} µs`;
        document.getElementById("val-pl").innerText = `${data.timings.pl_us.toFixed(0)} µs`;
        document.getElementById("val-cls").innerText = `${data.timings.classify_us.toFixed(0)} µs`;
      }
    })
    .catch(err => console.log(err));
}

// Start visualizer and polling
requestAnimationFrame(draw3DScene);
setInterval(pollTelemetry, 150);
