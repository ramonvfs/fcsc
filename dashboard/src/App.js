import "./App.css";
import { useFFTWebSocket } from "./hooks/useFFTWebSocket";
import AccelChart from "./components/AccelChart";
import FFTChart from "./components/FFTChart";
import DistanceCard from "./components/DistanceCard";

function App() {
  const { accelData, fftData, distance, status, statusFFT } = useFFTWebSocket("ws://localhost:8080/ws/fft_data");

  return (
    <div className="App">
      <h1>Dashboard de Monitoramento</h1>
      
      <DistanceCard distance={distance} status={status} />
      <div className="dashboard-container">
        <div className="chart-card">
          <AccelChart accelData={accelData} />
        </div>

        <div className="chart-card">
          <FFTChart fftData={fftData} statusFFT={statusFFT}/>
        </div>
      </div>
    </div>
  );
}

export default App;
