import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";

export default function AccelChart({ accelData }) {
  const data = Array.from({ length: Math.max(
    accelData.X.length,
    accelData.Y.length,
    accelData.Z.length
  ) }).map((_, i) => ({
    index: i,
    X: accelData.X[i] ?? null,
    Y: accelData.Y[i] ?? null,
    Z: accelData.Z[i] ?? null,
  }));

  return (
    <div>
      <h2>Acelerações (X, Y, Z)</h2>
      <LineChart width={800} height={300} data={data}>
        <Line type="monotone" dataKey="X" stroke="red" dot={false} />
        <Line type="monotone" dataKey="Y" stroke="green" dot={false} />
        <Line type="monotone" dataKey="Z" stroke="blue" dot={false} />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="index" />
        <YAxis />
        <Tooltip />
        <Legend />
      </LineChart>
    </div>
  );
}
