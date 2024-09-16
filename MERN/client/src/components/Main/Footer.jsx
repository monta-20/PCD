/* eslint-disable jsx-a11y/img-redundant-alt */
import React from "react";
import { Container } from "@mui/material";
import myImage from "../../images/Partener.PNG";
const Footer = () => {
  return (
    
    <Container>
      <img src={myImage} alt="My Image" style={{
        width: "700px", height: "200px",
       position: "absolute",
       bottom: "0",
       left: "45%",
       transform: "translateX(-50%)",
  }} />
    </Container>
  );
};

export default Footer;
