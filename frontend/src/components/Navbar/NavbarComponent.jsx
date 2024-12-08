import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import { Link, useLocation } from "react-router-dom";
import "./NavbarComponent.css";

const Sidebar = () => {
  const location = useLocation();
  return (
    <Navbar
      bg="dark"
      variant="dark"
      className="flex-column eda-sidebar"
      fixed="top"
    >
      <Navbar.Brand as={Link} to="/">
        Data Dashboard
      </Navbar.Brand>
      <Nav className="flex-row">
        <Nav.Link as={Link} to="/eda" active={location.pathname === "/eda"}>
          EDA Graphs
        </Nav.Link>
        <Nav.Link
          as={Link}
          to="/trends"
          active={location.pathname === "/trends"}
        >
          Trends Visualisation
        </Nav.Link>
        <Nav.Link
          as={Link}
          to="/hypothesis"
          active={location.pathname === "/hypothesis"}
        >
          Hypothesis
        </Nav.Link>
      </Nav>
    </Navbar>
  );
};

export default Sidebar;
