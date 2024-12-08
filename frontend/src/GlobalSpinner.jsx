import React from "react";
import { Spinner, Container } from "react-bootstrap";
import { useLoading } from "./LoadingContext";

const GlobalSpinner = () => {
  const { loading } = useLoading();

  if (!loading) return null;

  return (
    <Container
      className="d-flex justify-content-center align-items-center"
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(255, 255, 255, 0.8)",
        zIndex: 1050,
      }}
    >
      <Spinner animation="border" role="status" variant="primary">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </Container>
  );
};

export default GlobalSpinner;
