import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import Chart from "chart.js/auto";
import { Container, Row, Col, Card } from "react-bootstrap";
import { Link } from "react-router-dom";
import "./EDAPage.css";
import Sidebar from "../../components/Navbar/NavbarComponent";

function EDAPage() {
  const [data, setData] = useState({
    yearly_counts: {},
    top_countries: {},
    attack_types: {},
  });

  const yearlyChartRef = useRef(null);
  const countriesChartRef = useRef(null);
  const attackTypesChartRef = useRef(null);

  useEffect(() => {
    axios.get("http://localhost:8000/api/eda/all-graphs").then((response) => {
      setData(response.data);
    });
  }, []);

  const createChart = (chartRef, config) => {
    if (chartRef.current) {
      chartRef.current.destroy();
    }
    chartRef.current = new Chart(config.ctx, config.options);
  };

  useEffect(() => {
    if (Object.keys(data.yearly_counts).length > 0) {
      const yearlyCtx = document
        .getElementById("yearlyEventsChart")
        .getContext("2d");
      createChart(yearlyChartRef, {
        ctx: yearlyCtx,
        options: {
          type: "line",
          data: {
            labels: Object.keys(data.yearly_counts),
            datasets: [
              {
                label: "Events Per Year",
                data: Object.values(data.yearly_counts),
                backgroundColor: "rgba(54, 162, 235, 0.2)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1,
              },
            ],
          },
        },
      });

      const countriesCtx = document
        .getElementById("topCountriesChart")
        .getContext("2d");
      createChart(countriesChartRef, {
        ctx: countriesCtx,
        options: {
          type: "bar",
          data: {
            labels: Object.keys(data.top_countries),
            datasets: [
              {
                label: "Top 10 Countries by Attacks",
                data: Object.values(data.top_countries),
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                borderColor: "rgba(255, 99, 132, 1)",
                borderWidth: 1,
              },
            ],
          },
        },
      });

      const attacksCtx = document
        .getElementById("attackTypesChart")
        .getContext("2d");
      createChart(attackTypesChartRef, {
        ctx: attacksCtx,
        options: {
          type: "doughnut",
          responsive: true,
          maintainAspectRatio: true,
          data: {
            labels: Object.keys(data.attack_types),
            datasets: [
              {
                label: "Attack Types",
                data: Object.values(data.attack_types),
                backgroundColor: [
                  "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(255, 206, 86, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(255, 159, 64, 0.2)",
                  "rgba(201, 203, 207, 0.2)",
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(255, 206, 86, 1)",
                  "rgba(75, 192, 192, 1)",
                  "rgba(153, 102, 255, 1)",
                  "rgba(255, 159, 64, 1)",
                  "rgba(201, 203, 207, 1)",
                ],
                borderWidth: 1,
              },
            ],
          },
        },
      });
    }
  }, [data]);

  return (
    <>
      <Sidebar />
      {/* <div className="eda-page"> */}
      <Container fluid>
        <Row>
          <Col className="ms-auto">
            <h2 className="text-center my-4">EDA - All Graphs</h2>
            <div className="charts-grid">
              {/* <div className="chart-container"> */}
              <Card border="info" style={{ width: "50rem" }}>
                {/* <h3 className="text-center">Yearly Events</h3> */}
                <Card.Title>Yearly Events</Card.Title>
                <canvas id="yearlyEventsChart"></canvas>
              </Card>
              {/* </div> */}
              {/* <div className="chart-container"> */}
              <Card border="info" style={{ width: "50rem" }}>
                <Card.Title>Top 10 Countries by Attacks</Card.Title>
                {/* <h3 className="text-center">Top 10 Countries by Attacks</h3> */}
                <canvas id="topCountriesChart"></canvas>
              </Card>
              {/* </div> */}
              {/* <div className="chart-container"> */}
              <Card border="info" style={{ width: "50rem" }}>
                <Card.Title>Attack Types</Card.Title>
                <Card.Text>
                  The pie chart below shows the proportion of each attack type,
                  with the percentages labeled in the legend. The chart visually
                  represents how each type of attack contributes to the total.
                </Card.Text>
                {/* <h3 className="text-center">Attack Types</h3> */}
                <canvas id="attackTypesChart"></canvas>
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

export default EDAPage;
