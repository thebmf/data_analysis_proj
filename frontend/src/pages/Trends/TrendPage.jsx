import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import Chart from "chart.js/auto";
import { Container, Row, Col, Card } from "react-bootstrap";
import Sidebar from "../../components/Navbar/NavbarComponent";
import "./TrendPage.css";
import { useLoading } from "../../LoadingContext";
// import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
function TrendPage() {
  const { startLoading, stopLoading } = useLoading();
  const [data, setData] = useState({
    regionCasualties: {},
    yearlyCasualties: {},
    attackTypesOverTime: [],
    globalDistribution: [],
  });

  // Refs to store chart instances
  const regionChartRef = useRef(null);
  const yearlyChartRef = useRef(null);
  const attackTypesChartRef = useRef(null);

  useEffect(() => {
    // Fetch data from endpoints
    Promise.all([
      axios.get("http://localhost:8000/data/total-casualties-by-region"),
      axios.get("http://localhost:8000/data/annual-trends-casualties"),
      axios.get("http://localhost:8000/data/attack-types-over-time"),
      axios.get("http://localhost:8000/data/global-distribution"),
    ]).then(([regionRes, yearlyRes, attackRes, globalRes]) => {
      setData({
        regionCasualties: regionRes.data.region_casualties,
        yearlyCasualties: yearlyRes.data.yearly_casualties,
        attackTypesOverTime: attackRes.data.attack_types_over_time,
        globalDistribution: globalRes.data.global_distribution,
      });
    });
  }, []);

  const createOrUpdateChart = (chartRef, canvasId, config) => {
    if (chartRef.current) {
      chartRef.current.destroy(); // Destroy existing chart instance
    }
    const ctx = document.getElementById(canvasId).getContext("2d");
    chartRef.current = new Chart(ctx, config);
  };

  const renderRegionCasualtiesChart = () => {
    const labels = Object.keys(data.regionCasualties.Total_Casualties || {});
    const values = Object.values(data.regionCasualties.Total_Casualties || {});
    createOrUpdateChart(regionChartRef, "regionCasualtiesChart", {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Total Casualties by Region",
            data: values,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
          },
        ],
      },
    });
  };

  const renderYearlyCasualtiesChart = () => {
    const labels = Object.keys(data.yearlyCasualties.Num_Killed || {});
    const killed = Object.values(data.yearlyCasualties.Num_Killed || {});
    const wounded = Object.values(data.yearlyCasualties.Num_Wounded || {});
    createOrUpdateChart(yearlyChartRef, "yearlyCasualtiesChart", {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Killed",
            data: killed,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
          },
          {
            label: "Wounded",
            data: wounded,
            backgroundColor: "rgba(255, 206, 86, 0.2)",
            borderColor: "rgba(255, 206, 86, 1)",
            borderWidth: 1,
          },
        ],
      },
    });
  };

  const renderAttackTypesOverTimeChart = () => {
    const groupedData = {};
    data.attackTypesOverTime.forEach((entry) => {
      if (!groupedData[entry.Year]) {
        groupedData[entry.Year] = {};
      }
      groupedData[entry.Year][entry.Attack_Type] = entry.Count;
    });

    const years = Object.keys(groupedData);
    const attackTypes = [
      ...new Set(data.attackTypesOverTime.map((d) => d.Attack_Type)),
    ];
    const datasets = attackTypes.map((type) => ({
      label: type,
      data: years.map((year) => groupedData[year][type] || 0),
      backgroundColor: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${
        Math.random() * 255
      }, 0.2)`,
      borderColor: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${
        Math.random() * 255
      }, 1)`,
      borderWidth: 1,
    }));

    createOrUpdateChart(attackTypesChartRef, "attackTypesOverTimeChart", {
      type: "line",
      data: {
        labels: years,
        datasets,
      },
    });
  };

  useEffect(() => {
    startLoading();
    if (Object.keys(data.regionCasualties).length > 0) {
      renderRegionCasualtiesChart();
    }
    if (Object.keys(data.yearlyCasualties).length > 0) {
      renderYearlyCasualtiesChart();
    }
    if (data.attackTypesOverTime.length > 0) {
      renderAttackTypesOverTimeChart();
    }
    stopLoading();
  }, [data]);

  return (
    <>
      <Sidebar />
      {/* <div className="data-visualization-page"> */}
      <Container fluid>
        <Row>
          <Col>
            <h2 className="text-center my-4">Data Visualization</h2>
            <div className="charts-grid-trends">
              {/* <div className="chart-container-trends"> */}
              <Card border="info" style={{ width: "50rem" }}>
                {/* <h3>Total Casualties by Region</h3> */}
                <Card.Title>Total Casualties by Region</Card.Title>
                <Card.Text>
                  The graph below shows the total number of casualties (killed
                  and wounded) by region. The stacked bar chart represents the
                  number of people killed and wounded in each region, with the
                  height of each bar indicating the total number of casualties.
                  The number of casualties for each category is labeled on the
                  bars.
                </Card.Text>
                <canvas id="regionCasualtiesChart"></canvas>
              </Card>
              {/* </div> */}
              {/* <div className="chart-container-trends"> */}
              <Card border="info" style={{ width: "50rem" }}>
                {/* <h3>Yearly Casualties</h3> */}
                <Card.Title>Yearly Casualties</Card.Title>
                <Card.Text>
                  The graph below shows the yearly trends in casualties, with
                  separate lines representing the number of people killed and
                  wounded each year.
                </Card.Text>
                <canvas id="yearlyCasualtiesChart"></canvas>
              </Card>
              {/* </div> */}
              {/* <div className="chart-container-trends"> */}
              <Card border="info" style={{ width: "50rem" }}>
                {/* <h3>Attack Types Over Time</h3> */}
                <Card.Title>Attack Types Over Time</Card.Title>
                <Card.Text>
                  This chart displays the number of attacks by year, categorized
                  by attack type and region. It allows users to observe the
                  trend in attack counts for each type over time, with animation
                  by year.
                </Card.Text>
                <canvas id="attackTypesOverTimeChart"></canvas>
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
export default TrendPage;
