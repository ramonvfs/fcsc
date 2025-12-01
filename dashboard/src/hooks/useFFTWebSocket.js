import { useState, useEffect } from "react";

export function useFFTWebSocket(wsUrl) {
  const [accelData, setAccelData] = useState({ X: [], Y: [], Z: [] });
  const [fftData, setFFTData] = useState({ X: null, Y: null, Z: null });
  const [distance, setDistance] = useState(0);
  const [status, setStatus] = useState("normal");
  const [statusFFT, setStatusFFT] = useState({ X: "normal", Y: "normal", Z: "normal" });
  useEffect(() => {
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log("WebSocket conectado!");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.distance !== undefined) {
        setDistance(data.distance);
        setStatus(data.status_distance);
      }

      if (data.status_fft) {
        setStatusFFT(prev => ({
        ...prev,
          [axis]: data.status_fft
        }));
      }
      
      const axis = data.axis;
      if (!["X", "Y", "Z"].includes(axis)) return;

      // Atualiza acelerações
      if (data.accel) {
        setAccelData((prev) => ({
          ...prev,
          [axis]: data.accel,
        }));
      }

      // Atualiza FFT
      if (data.frequencies && data.magnitudes) {
        setFFTData((prev) => ({
          ...prev,
          [axis]: {
            frequencies: data.frequencies,
            magnitudes: data.magnitudes
          }
        }));
      }
    };

    return () => ws.close();
  }, [wsUrl]);

  return { accelData, fftData, distance, status, statusFFT };
}
