import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";

export default function FFTChart({ fftData, statusFFT }) {
  const maxLength = Math.max(
    fftData.X?.frequencies?.length || 0,
    fftData.Y?.frequencies?.length || 0,
    fftData.Z?.frequencies?.length || 0
  );

  const data = Array.from({ length: maxLength }).map((_, i) => ({
    freq: fftData.X?.frequencies?.[i] ?? fftData.Y?.frequencies?.[i] ?? fftData.Z?.frequencies?.[i] ?? 0,
    X: fftData.X?.magnitudes?.[i] ?? null,
    Y: fftData.Y?.magnitudes?.[i] ?? null,
    Z: fftData.Z?.magnitudes?.[i] ?? null,
  }));

  return (
    <div>
      <div style={{
          display: "flex",
          justifyContent: "center",
          gap: "40px",   // espaço entre os cards
          marginBottom: "15px",
          fontSize: "18px"
          // fontWeight: "bold"
        }}> Status:
        <div>X: {statusFFT.X === "normal" ? "🟢" : "🔴"}</div>
        <div>Y: {statusFFT.Y === "normal" ? "🟢" : "🔴"}</div>
        <div>Z: {statusFFT.Z === "normal" ? "🟢" : "🔴"}</div>
      </div>
      <h2>FFT (X, Y, Z)</h2>
      <LineChart width={800} height={300} data={data}>
        <Line type="monotone" dataKey="X" stroke="red" dot={false} />
        <Line type="monotone" dataKey="Y" stroke="green" dot={false} />
        <Line type="monotone" dataKey="Z" stroke="blue" dot={false} />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="freq" />
        <YAxis />
        <Tooltip />
        <Legend />
      </LineChart>
    </div>
  );
}
