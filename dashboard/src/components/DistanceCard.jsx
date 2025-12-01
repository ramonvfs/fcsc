export default function DistanceCard({ distance, status }) {
  return (
    <div className="distance-card">
      <h2>Distância</h2>

      <div className={`distance-value ${status}`}>
        {distance} mm
      </div>

      <div className={`distance-status ${status}`}>
        Status: {status === "normal" ? "🟢 Normal" : "🔴 Alerta"}
      </div>
    </div>
  );
}
