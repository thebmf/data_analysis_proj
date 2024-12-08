import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import Home from "./components/Home";
// import DataOverview from "./components/DataOverview";
import EDAPage from "./pages/EDA/EDAPage";
import TrendPage from "./pages/Trends/TrendPage";
import WeaponAnalysis from "./pages/Hypothesis/Hypothesis";
import "./App.css";
// import Hypothesis from "./components/Hypothesis";

function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<Home />} /> */}
        <Route path="/eda" element={<EDAPage />} />
        <Route path="/trends" element={<TrendPage />} />
        <Route path="/hypothesis" element={<WeaponAnalysis />} />
      </Routes>
    </Router>
  );
}

export default App;
