import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import Chart from "chart.js/auto";
import { Container, Row, Col, Card } from "react-bootstrap";
import "./Hypothesis.css";
import Sidebar from "../../components/Navbar/NavbarComponent";

function WeaponAnalysis() {
  const [weaponStats, setWeaponStats] = useState([]);
  const weaponChartRef = useRef(null);

  useEffect(() => {
    // Fetch weapon analysis data
    axios.get("http://localhost:8000/data/weapon-analysis").then((response) => {
      setWeaponStats(response.data.weapon_stats);
    });
  }, []);

  const createOrUpdateChart = (chartRef, canvasId, config) => {
    if (chartRef.current) {
      chartRef.current.destroy();
    }
    const ctx = document.getElementById(canvasId).getContext("2d");
    chartRef.current = new Chart(ctx, config);
  };

  useEffect(() => {
    if (weaponStats.length > 0) {
      const labels = weaponStats.map((item) => item.Weapon_Type);
      const avgCasualties = weaponStats.map((item) => item.avg_casualties);
      const usageCounts = weaponStats.map((item) => item.usage_count);

      createOrUpdateChart(weaponChartRef, "weaponChart", {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Average Casualties",
              data: avgCasualties,
              backgroundColor: "rgba(135, 206, 235, 0.6)",
              borderColor: "rgba(70, 130, 180, 1)",
              borderWidth: 1,
              yAxisID: "y1",
            },
            {
              label: "Usage Frequency",
              data: usageCounts,
              type: "line",
              borderColor: "rgba(220, 20, 60, 1)",
              backgroundColor: "rgba(220, 20, 60, 0.3)",
              yAxisID: "y2",
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true, // Включение фиксированного соотношения
          scales: {
            x: {
              beginAtZero: true,
            },
            y1: {
              type: "linear",
              position: "left",
              title: {
                display: true,
                text: "Average Casualties",
              },
              grid: {
                drawOnChartArea: false,
              },
            },
            y2: {
              type: "linear",
              position: "right",
              title: {
                display: true,
                text: "Usage Frequency",
              },
              grid: {
                drawOnChartArea: false,
              },
            },
          },
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Weapon Popularity vs Casualties",
            },
          },
        },
      });
    }
  }, [weaponStats]);

  return (
    <>
      <Sidebar />
      {/* <div className="data-visualization-page"> */}
      <Container fluid className="w-100">
        <Row>
          <Col>
            <h2 className="text-center my-4">Weapon Analysis</h2>
            <div className="charts-grid-hypothesis">
              <Card border="info" style={{ width: "50rem" }}>
                {/* <div className="chart-container-hypothesis"> */}
                <Card.Title>
                  Hypothesis: The frequency of choosing a particular weapon
                  depends on the average number of victims
                </Card.Title>
                <Card.Text>
                  Based on the analysis, the hypothesis that the choice of
                  weapon depends on the average statistical number of victims
                  was refuted. The null hypothesis, which asserts the
                  independence of these variables, could not be rejected. This
                  means that the frequency of choosing a weapon does not depend
                  on the number of victims in terrorist attacks. Therefore, the
                  choice of weapon is most likely determined by other factors
                  that require additional research.
                </Card.Text>
                {/* <h3>Weapon Popularity vs Casualties</h3> */}
                <canvas id="weaponChart"></canvas>
              </Card>
              {/* </div> */}
            </div>
          </Col>
        </Row>
      </Container>
      {/* </div> */}
    </>
  );
}

export default WeaponAnalysis;
