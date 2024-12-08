import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import "bootstrap/dist/css/bootstrap.min.css";
import "leaflet/dist/leaflet.css";
import { LoadingProvider } from "./LoadingContext";
import GlobalSpinner from "./GlobalSpinner";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <LoadingProvider>
      <GlobalSpinner />
      <App />
    </LoadingProvider>
  </StrictMode>
);
